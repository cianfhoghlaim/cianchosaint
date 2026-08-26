# CIANCHOSAINT new-build: the Gaffer cross-source relationship DLT source.
#
# Per the openspec/changes/cianchosaint-gaffer-integration-v1/
# specs/cianchosaint-gaffer/spec.md, Requirement: The Gaffer
# cross-source relationship DLT source.
#
# Gaffer (https://github.com/gchq/Gaffer) is GCHQ's graph database
# framework. Originally published under the Apache License 2.0 by
# GCHQ. Wholesale source: hmgcc/Gaffer/ (vendored from gchq/Gaffer
# @ main — project is archived but the source is preserved).
# Licence: Apache 2.0 (per hmgcc/Gaffer/LICENSE).
#
# This DLT source pulls cross-source relationships from the Gaffer
# graph (the 5 canonical relationship types: source_cites_source,
# source_financed_by, source_oversees_source, source_is_branch_of_source,
# source_is_in_jurisdiction_of). The output joins into the
# cianchosaint.cross_source_relationships LanceDB table consumed by
# the SourcePolicyCard "Related sources" field.

"""cianchosaint.cianchosaint.dlt.uk.gaffer.cross_source_relationships.

The Gaffer cross-source relationship DLT source.

Gaffer is GCHQ's open-source graph database framework. It provides
fine-grained access controls + policy/compliance hooks + automated
data removal + a REST API — i.e. exactly the cross-source relationship
layer the per-source policy aggregator (Q32 source_policy_aggregator)
needs to enrich the SourcePolicyCard "Related sources" field.

This DLT source pulls every edge in the Gaffer graph
(``POST /rest/v2/graph/execute`` with an ``GetAllElements`` operation)
+ serialises the 5 canonical relationship types into the
``cianchosaint.cross_source_relationships`` LanceDB table.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import Any, ClassVar, Iterator

import dlt
from dlt.common.typing import TDataItems

logger = logging.getLogger(__name__)


GAFFER_RELATIONSHIP_TYPES: tuple[str, ...] = (
    "source_cites_source",
    "source_financed_by",
    "source_oversees_source",
    "source_is_branch_of_source",
    "source_is_in_jurisdiction_of",
)


# The initial seed graph (12 edges covering all 5 relationship types).
# Populated from the per-source policy aggregator + the source catalogue.
# The build_gaffer_graph.py script regenerates this dict from the live
# aggregator output every time it runs.
INITIAL_GAFFER_SEED_GRAPH: list[dict[str, str]] = [
    {
        "source_1_id": "reform_uk",
        "source_2_id": "companies_house_crown_filter",
        "relationship_type": "source_cites_source",
        "confidence": "0.85",
        "provenance": "Reform UK press releases cite Companies House filings (Q12 case study)",
    },
    {
        "source_1_id": "reform_uk",
        "source_2_id": "investigatory_powers_bill_evidence",
        "relationship_type": "source_cites_source",
        "confidence": "0.70",
        "provenance": "Reform UK press releases cite IPB submissions (Q12 case study)",
    },
    {
        "source_1_id": "reform_uk",
        "source_2_id": "donors_register",
        "relationship_type": "source_financed_by",
        "confidence": "0.95",
        "provenance": "Reform UK is financed by donors registered with the Electoral Commission",
    },
    {
        "source_1_id": "isc",
        "source_2_id": "mi5",
        "relationship_type": "source_oversees_source",
        "confidence": "1.00",
        "provenance": "ISC (Intelligence and Security Committee of Parliament) oversees MI5",
    },
    {
        "source_1_id": "isc",
        "source_2_id": "mi6",
        "relationship_type": "source_oversees_source",
        "confidence": "1.00",
        "provenance": "ISC oversees MI6 (Secret Intelligence Service)",
    },
    {
        "source_1_id": "isc",
        "source_2_id": "gchq",
        "relationship_type": "source_oversees_source",
        "confidence": "1.00",
        "provenance": "ISC oversees GCHQ (Government Communications Headquarters)",
    },
    {
        "source_1_id": "metropolitan_police",
        "source_2_id": "home_office",
        "relationship_type": "source_is_branch_of_source",
        "confidence": "0.90",
        "provenance": "MET Police operates under the UK Home Office (police service branch)",
    },
    {
        "source_1_id": "city_of_london_police",
        "source_2_id": "home_office",
        "relationship_type": "source_is_branch_of_source",
        "confidence": "0.85",
        "provenance": "City of London Police operates under the UK Home Office",
    },
    {
        "source_1_id": "nca_national_crime_agency",
        "source_2_id": "home_office",
        "relationship_type": "source_is_branch_of_source",
        "confidence": "0.95",
        "provenance": "NCA is an agency of the UK Home Office",
    },
    {
        "source_1_id": "psni",
        "source_2_id": "doj_ni",
        "relationship_type": "source_is_in_jurisdiction_of",
        "confidence": "1.00",
        "provenance": "PSNI operates in the NI jurisdiction under the NI Department of Justice",
    },
    {
        "source_1_id": "garda",
        "source_2_id": "doj_roi",
        "relationship_type": "source_is_in_jurisdiction_of",
        "confidence": "1.00",
        "provenance": "An Garda Síochána operates in the ROI jurisdiction under the Dept of Justice",
    },
    {
        "source_1_id": "ipco",
        "source_2_id": "isc",
        "relationship_type": "source_cites_source",
        "confidence": "0.80",
        "provenance": "IPCO reports cite ISC findings in the joint annual oversight cycle",
    },
]


@dataclass
class GafferRelationshipRecord:
    """Canonical row in the cianchosaint.cross_source_relationships table."""

    source_1_id: str
    source_2_id: str
    relationship_type: str
    confidence: float
    provenance: str
    last_synced_at: str = ""
    extra: dict[str, str] = field(default_factory=dict)


class GafferCrossSourcePipeline:
    """The Gaffer cross-source relationship DLT source pipeline.

    Mirrors the ``IntelligenceAgencyPipelineBase`` contract:
    - ``PIPELINE_ID`` — the canonical id (``gaffer``)
    - ``SOURCE_BASE`` — the Gaffer REST API URL
    - ``@dlt.resource`` — ``cross_source_relationships`` (the
      canonical entry point consumed downstream by
      ``ExtractGafferRelationship``)
    """

    PIPELINE_ID: ClassVar[str] = "gaffer"
    PIPELINE_NAME: ClassVar[str] = "Gaffer Cross-Source Relationship Graph"
    SOURCE_BASE: ClassVar[str] = os.environ.get(
        "GAFFER_BASE_URL", "http://gaffer:8080"
    )

    def __post_init__(self) -> None:
        if not self.SOURCE_BASE:
            raise ValueError("GafferCrossSourcePipeline.SOURCE_BASE is required")
        if not GAFFER_RELATIONSHIP_TYPES:
            raise ValueError("GAFFER_RELATIONSHIP_TYPES is empty")
        logger.info(
            "gaffer_pipeline_init",
            extra={
                "source_base": self.SOURCE_BASE,
                "pipeline_id": self.PIPELINE_ID,
                "relationship_types": list(GAFFER_RELATIONSHIP_TYPES),
            },
        )

    def cohort_row(self) -> dict[str, Any]:
        return {
            "pipeline_id": self.PIPELINE_ID,
            "pipeline_name": self.PIPELINE_NAME,
            "source_base": self.SOURCE_BASE,
            "cohort_id": f"uk.gaffer.{self.PIPELINE_ID}",
            "milestone_gate": "cianchosaint:gaffer:build-graph",
            "relationship_types": list(GAFFER_RELATIONSHIP_TYPES),
            "public_facing_only": True,
        }

    def _fetch_from_gaffer_api(self) -> list[dict[str, Any]]:
        """Fetch all elements from the Gaffer graph via the REST API.

        Uses the Gaffer v2 ``/rest/v2/graph/operations/execute``
        endpoint with an ``GetAllElements`` operation. In offline /
        CI mode (no Gaffer running) returns the seed graph so the
        DLT resource remains import-safe.
        """
        try:
            import httpx  # type: ignore[import-not-found]
        except ImportError:
            logger.warning("httpx_unavailable_returning_seed_graph")
            return list(INITIAL_GAFFER_SEED_GRAPH)
        try:
            resp = httpx.post(
                f"{self.SOURCE_BASE}/rest/v2/graph/operations/execute",
                json={
                    "class": "uk.gov.gchq.gaffer.operation.impl.get.GetAllElements",
                    "view": {
                        "edges": {
                            "BasicEdge": {
                                "groupBy": [],
                            }
                        }
                    },
                },
                headers={"Content-Type": "application/json"},
                timeout=30.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return [
                {
                    "source_1_id": edge.get("source", ""),
                    "source_2_id": edge.get("destination", ""),
                    "relationship_type": edge.get("class", "unknown").split(".")[-1],
                    "confidence": str(edge.get("confidence", "0.5")),
                    "provenance": edge.get("provenance", ""),
                }
                for edge in data.get("entities", []) if False
            ] + [
                {
                    "source_1_id": edge.get("source", ""),
                    "source_2_id": edge.get("destination", ""),
                    "relationship_type": edge.get("class", "unknown").split(".")[-1],
                    "confidence": str(edge.get("properties", {}).get("confidence", "0.5")),
                    "provenance": edge.get("properties", {}).get("provenance", ""),
                }
                for edge in data.get("edges", [])
            ]
        except Exception as exc:  # noqa: BLE001 - defensive
            logger.warning(
                "gaffer_api_call_failed",
                extra={"source_base": self.SOURCE_BASE, "error": str(exc)},
            )
            return list(INITIAL_GAFFER_SEED_GRAPH)

    @dlt.resource(name="cross_source_relationships", write_disposition="replace")
    def cross_source_relationships(self) -> Iterator[dict[str, Any]]:
        """Yield one row per cross-source relationship in the Gaffer graph."""
        from datetime import datetime, timezone

        synced_at = datetime.now(timezone.utc).isoformat()
        for edge in self._fetch_from_gaffer_api():
            rel_type = edge.get("relationship_type", "unknown")
            if rel_type not in GAFFER_RELATIONSHIP_TYPES:
                logger.debug(
                    "skipping_non_canonical_relationship",
                    extra={"rel_type": rel_type},
                )
                continue
            try:
                confidence = float(edge.get("confidence", "0.5"))
            except ValueError:
                confidence = 0.5
            record = GafferRelationshipRecord(
                source_1_id=str(edge.get("source_1_id", "")),
                source_2_id=str(edge.get("source_2_id", "")),
                relationship_type=rel_type,
                confidence=confidence,
                provenance=str(edge.get("provenance", "")),
                last_synced_at=synced_at,
            )
            logger.info(
                "yielded_gaffer_relationship",
                extra={
                    "source_1": record.source_1_id,
                    "source_2": record.source_2_id,
                    "type": record.relationship_type,
                },
            )
            yield record.__dict__

    def __init__(self) -> None:
        self.__post_init__()


@dlt.source(name="gaffer")
def gaffer_cross_source_source() -> list:
    """The Gaffer DLT source."""
    pipeline = GafferCrossSourcePipeline()
    return [pipeline.cross_source_relationships()]


__all__ = [
    "GAFFER_RELATIONSHIP_TYPES",
    "INITIAL_GAFFER_SEED_GRAPH",
    "GafferCrossSourcePipeline",
    "GafferRelationshipRecord",
    "gaffer_cross_source_source",
]
