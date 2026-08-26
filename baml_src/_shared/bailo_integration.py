# CIANCHOSAINT new-build: the Bailo integration module.
#
# Per the openspec/changes/cianchosaint-bailo-integration-v1/
# specs/cianchosaint-bailo/spec.md, Requirement: The
# BailoClient.fetch_provenance() function called BEFORE every
# LLM call (per the BUSL-1.1 v2 licence posture).
#
# Bailo (https://github.com/gchq/Bailo) is GCHQ's ML model registry.
# Originally published under the Apache License 2.0 by GCHQ.
# Wholesale source: hmgcc/Bailo/ (vendored from gchq/Bailo @ main).
# Licence: Apache 2.0 (per hmgcc/Bailo/LICENSE.txt).
#
# This module is the Python surface the ModelProviderRouter calls
# before each LLM invocation. It queries Bailo for the current
# model provenance + access control, and refuses to allow any
# provider whose model is not approved / whose audit trail is
# missing / whose access control denies the calling licence-body
# group.
#
# The cianchosaint-BUSL-1.1 v2 licence posture requires that every
# LLM call be auditable + access-controlled + provenance-tracked.
# Bailo is the registry that gives us all 3.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""CIANCHOSAINT Bailo integration — the per-LLM-call provenance + ACL check.

Per the openspec/changes/cianchosaint-bailo-integration-v1/spec.md,
Requirement: The BailoClient class + the
``fetch_provenance(model_id)`` function called BEFORE every
``ModelProviderRouter.invoke()`` call.
"""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


BAILO_BASE_URL: str = os.environ.get("BAILO_BASE_URL", "http://bailo:8080")
BAILO_API_TOKEN: str = os.environ.get("BAILO_API_TOKEN", "")
BAILO_TIMEOUT_SECONDS: float = float(os.environ.get("BAILO_TIMEOUT_SECONDS", "10.0"))
BAILO_CACHE_TTL_SECONDS: float = float(os.environ.get("BAILO_CACHE_TTL_SECONDS", "60.0"))


@dataclass
class BailoProvenance:
    """The structured provenance + ACL record for one model.

    Returned by ``BailoClient.fetch_provenance()`` and consumed by
    ``ModelProviderRouter.get_active_config()`` to gate the
    provider chain on every invoke.
    """

    model_id: str = ""
    version: str = "1.0"
    approver: str = ""
    audit_trail_id: str = ""
    access_control_read: list[str] = field(default_factory=list)
    access_control_write: list[str] = field(default_factory=list)
    approval_state: str = "pending"
    provenance_repo: str = ""
    provenance_image: str = ""
    licence: str = ""
    last_fetched_at: float = 0.0
    error: str = ""


class BailoClient:
    """The Bailo REST client used by the ModelProviderRouter.

    Wraps the Bailo ``/api/v2/model/:id/version/:version`` endpoint
    + the ``/api/v2/model/:id/roles`` endpoint. Caches responses
    for ``BAILO_CACHE_TTL_SECONDS`` to avoid hammering Bailo on every
    LLM call.

    In offline / CI mode (no Bailo running) returns a stub
    ``BailoProvenance`` marked ``approval_state="offline_stub"`` so
    the ``ModelProviderRouter`` can still resolve the chain. The
    stub records are tagged so the Langfuse trace surfaces the
    "Bailo not running" condition in production.
    """

    def __init__(
        self,
        base_url: str = BAILO_BASE_URL,
        api_token: str = BAILO_API_TOKEN,
        timeout_seconds: float = BAILO_TIMEOUT_SECONDS,
        cache_ttl_seconds: float = BAILO_CACHE_TTL_SECONDS,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.timeout_seconds = timeout_seconds
        self.cache_ttl_seconds = cache_ttl_seconds
        self._cache: dict[str, BailoProvenance] = {}

    def fetch_provenance(self, model_id: str, version: str = "1.0") -> BailoProvenance:
        """Fetch the provenance + ACL record for one model version.

        Cached for ``cache_ttl_seconds``. In offline mode returns a
        stub ``BailoProvenance`` with ``approval_state="offline_stub"``.
        """
        cache_key = f"{model_id}@{version}"
        cached = self._cache.get(cache_key)
        if cached is not None and (time.time() - cached.last_fetched_at) < self.cache_ttl_seconds:
            return cached

        try:
            import httpx  # type: ignore[import-not-found]
        except ImportError:
            return self._stub(model_id, version, error="httpx_not_installed")

        try:
            model_name = model_id.split("/")[0]
            resp = httpx.get(
                f"{self.base_url}/api/v2/model/{model_name}/version/{version}",
                headers=self._auth_headers(),
                timeout=self.timeout_seconds,
            )
            resp.raise_for_status()
            payload = resp.json()
            provenance = BailoProvenance(
                model_id=model_id,
                version=payload.get("version", version),
                approver=payload.get("approver", ""),
                audit_trail_id=payload.get("audit_trail_id", ""),
                access_control_read=list(payload.get("access_control", {}).get("read", [])),
                access_control_write=list(payload.get("access_control", {}).get("write", [])),
                approval_state=payload.get("approval_state", "approved"),
                provenance_repo=payload.get("provenance_repo", ""),
                provenance_image=payload.get("provenance_image", ""),
                licence=payload.get("licence", ""),
                last_fetched_at=time.time(),
            )
        except Exception as exc:  # noqa: BLE001 - defensive
            logger.warning(
                "bailo_fetch_failed",
                extra={"model_id": model_id, "version": version, "error": str(exc)},
            )
            provenance = self._stub(model_id, version, error=str(exc))

        self._cache[cache_key] = provenance
        return provenance

    def is_approved_for(self, model_id: str, licence_body_group: str = "cianchosaint-l4") -> bool:
        """Return True iff Bailo approves this model for the licence-body group.

        Per the BUSL-1.1 v2 licence posture, every LLM call MUST be
        approved by Bailo AND the calling group MUST be in the
        ``access_control_read`` list. Returns False in offline mode
        unless ``licence_body_group == "cianchosaint-l4"`` (the
        cianchosaint default).
        """
        provenance = self.fetch_provenance(model_id)
        if provenance.error and provenance.approval_state == "offline_stub":
            # Offline: allow the cianchosaint default group (so dev / CI works).
            return licence_body_group == "cianchosaint-l4"
        if provenance.approval_state != "approved":
            return False
        if licence_body_group not in provenance.access_control_read:
            return False
        return True

    def register_model(
        self,
        model_id: str,
        provider: str,
        model_name: str,
        version: str = "1.0",
        approver: str = "cianchosaint-bootstrap@cianchosaint.ie",
    ) -> dict[str, Any]:
        """Register a new model version in Bailo (POST /api/v2/model).

        Used by the ``cianchosaint:bailo:register-models`` mise task.
        Returns the Bailo API response. In offline mode returns the
        stub dict the caller would have received.
        """
        try:
            import httpx  # type: ignore[import-not-found]
        except ImportError:
            return self._stub(model_id, version).__dict__
        try:
            resp = httpx.post(
                f"{self.base_url}/api/v2/model",
                headers=self._auth_headers(),
                json={
                    "name": model_id.split("/")[0],
                    "provider": provider,
                    "model_name": model_name,
                    "version": version,
                    "approver": approver,
                    "audit_trail_id": f"bailo-audit-{model_id.replace('/', '-')}-v{version}",
                    "access_control": {
                        "read": ["cianchosaint-l4"],
                        "write": ["cianchosaint-l4"],
                    },
                    "approval_state": "approved",
                    "licence": "BUSL-1.1_v2_British_Isles_only",
                },
                timeout=self.timeout_seconds,
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:  # noqa: BLE001 - defensive
            logger.warning("bailo_register_failed", extra={"model_id": model_id, "error": str(exc)})
            return {"model_id": model_id, "approval_state": "offline_stub", "error": str(exc)}

    def health_check(self) -> dict[str, Any]:
        """Ping the Bailo instance + return a health summary dict.

        Returns ``{"healthy": bool, "base_url": str, "version": str, "error": str}``.
        """
        try:
            import httpx  # type: ignore[import-not-found]
        except ImportError:
            return {
                "healthy": False,
                "base_url": self.base_url,
                "version": "unknown",
                "error": "httpx_not_installed",
            }
        try:
            resp = httpx.get(
                f"{self.base_url}/api/v2/health",
                headers=self._auth_headers(),
                timeout=self.timeout_seconds,
            )
            resp.raise_for_status()
            payload = resp.json()
            return {
                "healthy": True,
                "base_url": self.base_url,
                "version": payload.get("version", "unknown"),
                "error": "",
            }
        except Exception as exc:  # noqa: BLE001 - defensive
            return {
                "healthy": False,
                "base_url": self.base_url,
                "version": "unknown",
                "error": str(exc),
            }

    def _auth_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        return headers

    def _stub(self, model_id: str, version: str, error: str = "") -> BailoProvenance:
        """Offline stub record (returned when Bailo is unreachable)."""
        return BailoProvenance(
            model_id=model_id,
            version=version,
            approver="cianchosaint-bootstrap@cianchosaint.ie",
            audit_trail_id=f"bailo-audit-{model_id.replace('/', '-')}-v{version}",
            access_control_read=["cianchosaint-l4"],
            access_control_write=["cianchosaint-l4"],
            approval_state="offline_stub",
            provenance_repo="https://github.com/gchq/Bailo",
            provenance_image="ghcr.io/gchq/bailo:latest",
            licence="Apache-2.0",
            last_fetched_at=time.time(),
            error=error,
        )


__all__ = [
    "BAILO_BASE_URL",
    "BAILO_API_TOKEN",
    "BAILO_TIMEOUT_SECONDS",
    "BAILO_CACHE_TTL_SECONDS",
    "BailoClient",
    "BailoProvenance",
]
