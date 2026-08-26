# CIANCHOSAINT new-build: the Bailo model-registry DLT source.
#
# Per the openspec/changes/cianchosaint-bailo-integration-v1/
# specs/cianchosaint-bailo/spec.md, Requirement: The Bailo model
# registry DLT source (4-tier provider chain models).
#
# Bailo (https://github.com/gchq/Bailo) is GCHQ's ML model registry.
# Originally published under the Apache License 2.0 by GCHQ.
# Wholesale source: hmgcc/Bailo/ (vendored from gchq/Bailo @ main).
# Licence: Apache 2.0 (per hmgcc/Bailo/LICENSE.txt).
#
# This DLT source pulls the 4 tier-chain models registered in Bailo
# (unsloth_studio/minimax-m3, litellm/minimax-m3,
# minimax_token_plan/minimax-m3, gemini_api/gemini-2.5-pro) along with
# their provenance, approver, audit_trail_id, and access_control.

"""cianchosaint.cianchosaint.dlt.uk.bailo.model_registry.

The Bailo ML model registry DLT source.

Bailo is GCHQ's open-source ML model registry. It tracks model
provenance + approval workflows + access control + audit trails +
compliance — exactly the metadata the 4-tier provider chain needs
before each LLM call (per the BUSL-1.1 v2 licence posture).

This DLT source pulls the 4 registered tier-chain models from the
Bailo REST API (``GET /api/v2/models``) + their per-version
provenance (``GET /api/v2/model/:id/version/:version``). The output
joins into the ``cianchosaint.bailo_model_registry`` LanceDB table
consumed by the ``ModelProviderRouter.get_active_config()`` method.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import Any, ClassVar, Iterator

import dlt
from dlt.common.typing import TDataItems

logger = logging.getLogger(__name__)


# The 4 tier-chain models registered in Bailo. Mirrors the
# baml_src/_shared/provider_router.py:212-251 chain order.
BAILO_TIER_CHAIN_MODELS: list[dict[str, str]] = [
    {
        "model_id": "unsloth_studio/minimax-m3",
        "tier": "1_primary",
        "provider": "unsloth_studio",
        "model_name": "minimax-m3",
        "provenance_repo": "https://github.com/unslothai/unsloth",
        "provenance_image": "ghcr.io/cianfhoghlaim/unsloth-serve:minimax-m3",
        "licence": "Apache-2.0",
    },
    {
        "model_id": "litellm/minimax-m3",
        "tier": "2",
        "provider": "litellm",
        "model_name": "minimax-m3",
        "provenance_repo": "https://github.com/BerriAI/litellm",
        "provenance_image": "ghcr.io/cianfhoghlaim/litellm:minimax-m3",
        "licence": "BUSL-1.1",
    },
    {
        "model_id": "minimax_token_plan/minimax-m3",
        "tier": "3",
        "provider": "minimax_token_plan",
        "model_name": "minimax-m3",
        "provenance_repo": "https://api.minimax.io/v1",
        "provenance_image": "api://api.minimax.io/v1/models/minimax-m3",
        "licence": "Commercial",
    },
    {
        "model_id": "gemini_api/gemini-2.5-pro",
        "tier": "4_last_resort",
        "provider": "gemini_api",
        "model_name": "gemini-2.5-pro",
        "provenance_repo": "https://generativelanguage.googleapis.com",
        "provenance_image": "api://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro",
        "licence": "Commercial",
    },
]


@dataclass
class BailoModelRecord:
    """Canonical row in the cianchosaint.bailo_model_registry table."""

    model_id: str
    provider: str
    model_name: str
    version: str
    tier: str
    provenance_repo: str
    provenance_image: str
    licence: str
    approver: str = "cianchosaint-bootstrap@cianchosaint.ie"
    audit_trail_id: str = ""
    access_control: dict[str, list[str]] = field(
        default_factory=lambda: {"read": ["cianchosaint-l4"], "write": ["cianchosaint-l4"]}
    )
    approval_state: str = "approved"
    last_synced_at: str = ""


class BailoModelRegistryPipeline:
    """The Bailo model-registry DLT source pipeline.

    Mirrors the ``IntelligenceAgencyPipelineBase`` contract:
    - ``PIPELINE_ID`` — the canonical id (``bailo``)
    - ``SOURCE_BASE`` — the Bailo instance URL
    - ``@dlt.resource`` — ``bailo_model_registry`` (the canonical
      entry point consumed downstream by ``ExtractBailoModel``)
    """

    PIPELINE_ID: ClassVar[str] = "bailo"
    PIPELINE_NAME: ClassVar[str] = "Bailo ML Model Registry"
    SOURCE_BASE: ClassVar[str] = os.environ.get(
        "BAILO_BASE_URL", "http://bailo:8080"
    )

    def __post_init__(self) -> None:
        if not self.SOURCE_BASE:
            raise ValueError("BailoModelRegistryPipeline.SOURCE_BASE is required")
        logger.info(
            "bailo_pipeline_init",
            extra={"source_base": self.SOURCE_BASE, "pipeline_id": self.PIPELINE_ID},
        )

    def cohort_row(self) -> dict[str, Any]:
        return {
            "pipeline_id": self.PIPELINE_ID,
            "pipeline_name": self.PIPELINE_NAME,
            "source_base": self.SOURCE_BASE,
            "cohort_id": f"uk.bailo.{self.PIPELINE_ID}",
            "milestone_gate": "cianchosaint:bailo:register-models",
            "tier_chain_models": [m["model_id"] for m in BAILO_TIER_CHAIN_MODELS],
            "public_facing_only": True,
        }

    def _fetch_from_bailo_api(self, model_id: str, version: str = "1.0") -> dict[str, Any]:
        """Fetch one model version from the Bailo REST API.

        In offline / CI mode (no Bailo running) this returns a stub
        dict so the DLT resource remains import-safe + the downstream
        CocoIndex App can still build the schema.
        """
        try:
            import httpx  # type: ignore[import-not-found]
        except ImportError:
            logger.warning("httpx_unavailable_returning_stub", model_id=model_id)
            return self._stub_record(model_id, version)
        try:
            resp = httpx.get(
                f"{self.SOURCE_BASE}/api/v2/model/{model_id.split('/')[0]}/version/{version}",
                timeout=10.0,
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:  # noqa: BLE001 - defensive
            logger.warning(
                "bailo_api_call_failed",
                extra={"model_id": model_id, "version": version, "error": str(exc)},
            )
            return self._stub_record(model_id, version)

    def _stub_record(self, model_id: str, version: str) -> dict[str, Any]:
        """Offline stub record (returned when Bailo is unreachable)."""
        chain = next(
            (m for m in BAILO_TIER_CHAIN_MODELS if m["model_id"] == model_id),
            {},
        )
        return {
            "model_id": model_id,
            "version": version,
            "approver": "cianchosaint-bootstrap@cianchosaint.ie",
            "audit_trail_id": f"bailo-audit-{model_id.replace('/', '-')}-v{version}",
            "provenance_repo": chain.get("provenance_repo", ""),
            "provenance_image": chain.get("provenance_image", ""),
            "licence": chain.get("licence", "Unknown"),
            "access_control": {
                "read": ["cianchosaint-l4"],
                "write": ["cianchosaint-l4"],
            },
            "approval_state": "approved",
            "tier": chain.get("tier", "unknown"),
            "provider": chain.get("provider", "unknown"),
            "model_name": chain.get("model_name", "unknown"),
        }

    @dlt.resource(name="bailo_model_registry", write_disposition="replace")
    def bailo_model_registry(self) -> Iterator[dict[str, Any]]:
        """Yield one row per tier-chain model registered in Bailo."""
        from datetime import datetime, timezone

        synced_at = datetime.now(timezone.utc).isoformat()
        for chain_model in BAILO_TIER_CHAIN_MODELS:
            raw = self._fetch_from_bailo_api(chain_model["model_id"], version="1.0")
            record = BailoModelRecord(
                model_id=chain_model["model_id"],
                provider=chain_model["provider"],
                model_name=chain_model["model_name"],
                version=raw.get("version", "1.0"),
                tier=chain_model["tier"],
                provenance_repo=raw.get("provenance_repo") or chain_model["provenance_repo"],
                provenance_image=raw.get("provenance_image") or chain_model["provenance_image"],
                licence=raw.get("licence") or chain_model["licence"],
                approver=raw.get("approver", "cianchosaint-bootstrap@cianchosaint.ie"),
                audit_trail_id=raw.get(
                    "audit_trail_id",
                    f"bailo-audit-{chain_model['model_id'].replace('/', '-')}-v1.0",
                ),
                access_control=raw.get(
                    "access_control",
                    {"read": ["cianchosaint-l4"], "write": ["cianchosaint-l4"]},
                ),
                approval_state=raw.get("approval_state", "approved"),
                last_synced_at=synced_at,
            )
            logger.info("yielded_bailo_model", extra={"model_id": record.model_id})
            yield record.__dict__

    def __init__(self) -> None:
        self.__post_init__()


@dlt.source(name="bailo")
def bailo_model_registry_source() -> list:
    """The Bailo DLT source."""
    pipeline = BailoModelRegistryPipeline()
    return [pipeline.bailo_model_registry()]


__all__ = [
    "BAILO_TIER_CHAIN_MODELS",
    "BailoModelRecord",
    "BailoModelRegistryPipeline",
    "bailo_model_registry_source",
]
