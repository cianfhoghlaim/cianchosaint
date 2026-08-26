# CIANCHOSAINT new-build: the Gaffer integration module.
#
# Per the openspec/changes/cianchosaint-gaffer-integration-v1/
# specs/cianchosaint-gaffer/spec.md, Requirement: The
# GafferClient.get_related_sources() function called by the
# SourcePolicyCard React component.
#
# Gaffer (https://github.com/gchq/Gaffer) is GCHQ's graph database
# framework. Originally published under the Apache License 2.0 by
# GCHQ. Wholesale source: hmgcc/Gaffer/ (vendored from gchq/Gaffer
# @ main — project is archived but the source is preserved).
# Licence: Apache 2.0 (per hmgcc/Gaffer/LICENSE).
#
# This module is the Python surface the ciafagent-* web apps call
# to populate the "Related sources" field in the SourcePolicyCard
# component (per Q32 source_policy_aggregator). It wraps the Gaffer
# REST API ``/rest/v2/graph/operations/execute`` and returns the
# cross-source relationships that match a given source_id + the
# optional relationship_type filter.
#
# The Gaffer graph is built by ``scripts/build_gaffer_graph.py`` from
# the per-source policy aggregator output (Q32 source_policy_aggregator.py)
# + the source catalogue.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""CIANCHOSAINT Gaffer integration — the cross-source relationship client.

Per the openspec/changes/cianchosaint-gaffer-integration-v1/spec.md,
Requirement: The GafferClient class + the
``get_related_sources(source_id, ...)`` function.
"""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


GAFFER_BASE_URL: str = os.environ.get("GAFFER_BASE_URL", "http://gaffer:8080")
GAFFER_TIMEOUT_SECONDS: float = float(os.environ.get("GAFFER_TIMEOUT_SECONDS", "30.0"))
GAFFER_CACHE_TTL_SECONDS: float = float(os.environ.get("GAFFER_CACHE_TTL_SECONDS", "300.0"))


GAFFER_RELATIONSHIP_TYPES: tuple[str, ...] = (
    "source_cites_source",
    "source_financed_by",
    "source_oversees_source",
    "source_is_branch_of_source",
    "source_is_in_jurisdiction_of",
)


@dataclass
class GafferRelationship:
    """One edge in the cross-source relationship graph."""

    source_1_id: str = ""
    source_2_id: str = ""
    relationship_type: str = ""
    confidence: float = 0.0
    provenance: str = ""
    last_fetched_at: float = 0.0


@dataclass
class GafferRelatedSources:
    """The structured "Related sources" payload for one source_id."""

    source_id: str = ""
    related: list[GafferRelationship] = field(default_factory=list)
    by_type: dict[str, list[GafferRelationship]] = field(default_factory=dict)
    last_fetched_at: float = 0.0
    error: str = ""


class GafferClient:
    """The Gaffer REST client used by the ciafagent-* web apps.

    Wraps the Gaffer v2 ``/rest/v2/graph/operations/execute``
    endpoint. Caches results for ``GAFFER_CACHE_TTL_SECONDS`` to
    avoid hammering Gaffer on every web-app render.

    In offline / CI mode (no Gaffer running) returns an empty
    ``GafferRelatedSources`` so the SourcePolicyCard degrades
    gracefully (the "Related sources" field is just hidden).
    """

    def __init__(
        self,
        base_url: str = GAFFER_BASE_URL,
        timeout_seconds: float = GAFFER_TIMEOUT_SECONDS,
        cache_ttl_seconds: float = GAFFER_CACHE_TTL_SECONDS,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.cache_ttl_seconds = cache_ttl_seconds
        self._cache: dict[str, GafferRelatedSources] = {}

    def get_related_sources(
        self,
        source_id: str,
        relationship_type: str | None = None,
    ) -> GafferRelatedSources:
        """Return all edges where ``source_1_id == source_id`` (or the reverse).

        Optionally filtered by ``relationship_type`` (one of the 5
        canonical values in ``GAFFER_RELATIONSHIP_TYPES``).

        Cached for ``cache_ttl_seconds``.
        """
        cache_key = f"{source_id}@{relationship_type or 'ALL'}"
        cached = self._cache.get(cache_key)
        if cached is not None and (time.time() - cached.last_fetched_at) < self.cache_ttl_seconds:
            return cached

        if relationship_type and relationship_type not in GAFFER_RELATIONSHIP_TYPES:
            return GafferRelatedSources(
                source_id=source_id,
                error=f"unknown_relationship_type:{relationship_type}",
                last_fetched_at=time.time(),
            )

        try:
            import httpx  # type: ignore[import-not-found]
        except ImportError:
            return GafferRelatedSources(
                source_id=source_id, error="httpx_not_installed", last_fetched_at=time.time(),
            )

        try:
            operation: dict[str, Any] = {
                "class": "uk.gov.gchq.gaffer.operation.impl.get.GetElements",
                "input": [
                    {
                        "class": "uk.gov.gchq.gaffer.data.element.Entity",
                        "vertex": source_id,
                    }
                ],
                "view": {
                    "edges": {
                        "BasicEdge": {"groupBy": []}
                    }
                },
            }
            resp = httpx.post(
                f"{self.base_url}/rest/v2/graph/operations/execute",
                json=operation,
                headers={"Content-Type": "application/json"},
                timeout=self.timeout_seconds,
            )
            resp.raise_for_status()
            payload = resp.json()
            edges = payload.get("edges", []) or payload.get("entities", [])

            related: list[GafferRelationship] = []
            for edge in edges:
                src = edge.get("source", "")
                dst = edge.get("destination", "")
                rel_type = edge.get("class", "unknown").split(".")[-1]
                if rel_type not in GAFFER_RELATIONSHIP_TYPES:
                    continue
                if relationship_type and rel_type != relationship_type:
                    continue
                props = edge.get("properties", {}) or {}
                try:
                    conf = float(props.get("confidence", "0.5"))
                except (TypeError, ValueError):
                    conf = 0.5
                # Match either direction.
                if src == source_id or dst == source_id:
                    if src == source_id:
                        s1, s2 = src, dst
                    else:
                        s1, s2 = dst, src
                    related.append(
                        GafferRelationship(
                            source_1_id=s1,
                            source_2_id=s2,
                            relationship_type=rel_type,
                            confidence=conf,
                            provenance=str(props.get("provenance", "")),
                            last_fetched_at=time.time(),
                        )
                    )
            by_type: dict[str, list[GafferRelationship]] = {rt: [] for rt in GAFFER_RELATIONSHIP_TYPES}
            for rel in related:
                by_type[rel.relationship_type].append(rel)
            result = GafferRelatedSources(
                source_id=source_id,
                related=related,
                by_type=by_type,
                last_fetched_at=time.time(),
            )
        except Exception as exc:  # noqa: BLE001 - defensive
            logger.warning(
                "gaffer_get_related_failed",
                extra={"source_id": source_id, "error": str(exc)},
            )
            result = GafferRelatedSources(
                source_id=source_id, error=str(exc), last_fetched_at=time.time(),
            )

        self._cache[cache_key] = result
        return result

    def add_relationship(
        self,
        source_1_id: str,
        source_2_id: str,
        relationship_type: str,
        confidence: float = 0.5,
        provenance: str = "",
    ) -> dict[str, Any]:
        """Add an edge to the Gaffer graph.

        Used by ``scripts/build_gaffer_graph.py`` to populate the
        graph. In offline mode returns the stub dict the caller
        would have received.
        """
        if relationship_type not in GAFFER_RELATIONSHIP_TYPES:
            return {"error": f"unknown_relationship_type:{relationship_type}"}
        try:
            import httpx  # type: ignore[import-not-found]
        except ImportError:
            return {"error": "httpx_not_installed", "source_1_id": source_1_id, "source_2_id": source_2_id}
        try:
            operation = {
                "class": "uk.gov.gchq.gaffer.operation.impl.add.AddElements",
                "input": [
                    {
                        "class": "uk.gov.gchq.gaffer.data.element.Edge",
                        "group": "BasicEdge",
                        "source": source_1_id,
                        "destination": source_2_id,
                        "directed": True,
                        "properties": {
                            "confidence": str(confidence),
                            "provenance": provenance,
                            "relationship_type": relationship_type,
                        },
                    }
                ],
            }
            resp = httpx.post(
                f"{self.base_url}/rest/v2/graph/operations/execute",
                json=operation,
                headers={"Content-Type": "application/json"},
                timeout=self.timeout_seconds,
            )
            resp.raise_for_status()
            return resp.json() or {"added": True}
        except Exception as exc:  # noqa: BLE001 - defensive
            logger.warning(
                "gaffer_add_relationship_failed",
                extra={
                    "source_1_id": source_1_id,
                    "source_2_id": source_2_id,
                    "error": str(exc),
                },
            )
            return {"error": str(exc), "source_1_id": source_1_id, "source_2_id": source_2_id}

    def health_check(self) -> dict[str, Any]:
        """Ping the Gaffer instance + return a health summary dict."""
        try:
            import httpx  # type: ignore[import-not-found]
        except ImportError:
            return {"healthy": False, "base_url": self.base_url, "version": "unknown", "error": "httpx_not_installed"}
        try:
            resp = httpx.get(
                f"{self.base_url}/rest/v2/status",
                timeout=self.timeout_seconds,
            )
            resp.raise_for_status()
            return {
                "healthy": True,
                "base_url": self.base_url,
                "version": "unknown",
                "error": "",
            }
        except Exception as exc:  # noqa: BLE001 - defensive
            return {
                "healthy": False,
                "base_url": self.base_url,
                "version": "unknown",
                "error": str(exc),
            }


__all__ = [
    "GAFFER_BASE_URL",
    "GAFFER_TIMEOUT_SECONDS",
    "GAFFER_CACHE_TTL_SECONDS",
    "GAFFER_RELATIONSHIP_TYPES",
    "GafferClient",
    "GafferRelationship",
    "GafferRelatedSources",
]
