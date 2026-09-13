# CIANCHOSAINT new-build: adjacent_context_resolver FunctionTool.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-political-graph/spec.md, Requirement: The umbrella
# FunctionTool that returns the 5-axis context (Axis A: politician +
# Axis B: advisors + Axis C: funders + Axis D: historical associations +
# Axis E: wikipedia archives).
#
# Orchestrates:
# - politician_account_resolver (Axis A)
# - 4 DLT source trees (advisors / funders / historical_associations /
#   wikipedia_archives) for Axes B-E
# - PoliticalGraphStore for cross-axis query_dossier() queries
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.tools.adjacent_context_resolver — 5-axis context umbrella FunctionTool.

Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
cianchosaint-political-graph/spec.md, this is the umbrella FunctionTool
that orchestrates the 5-axis politician + adjacent-context pipeline.

The 5 axes are:
- Axis A: the politician themselves (via politician_account_resolver)
- Axis B: advisors (SpAds / PPS / Chief of Staff / researcher / consultant)
- Axis C: funders (Electoral Commission + Companies House + Registers of Interests)
- Axis D: historical associations (Wikidata + court records + officer history)
- Axis E: wikipedia archives (multilingual Wikipedia + Wikidata QID)
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
UTC = timezone.utc
from typing import Any

from google.adk.tools import FunctionTool

logger = logging.getLogger(__name__)


def _try_import_politician_resolver():
    """Lazy import the politician_account_resolver tool."""
    try:
        from agents.cianchosaint.tools.politician_account_resolver import (
            politician_account_resolver,
        )
        return politician_account_resolver
    except ImportError as exc:
        logger.warning("politician_account_resolver_unavailable", error=str(exc))
        return None


def _try_import_graph_store():
    """Lazy import the PoliticalGraphStore."""
    try:
        from agents.cianchosaint.tools.political_graph_store import (
            PoliticalGraphStore,
        )
        return PoliticalGraphStore
    except ImportError as exc:
        logger.warning("political_graph_store_unavailable", error=str(exc))
        return None


async def adjacent_context_resolver(
    politician_id: str | None = None,
    canonical_name: str | None = None,
    party_id: str | None = None,
    jurisdiction: str | None = None,
    *,
    include_advisors: bool = True,
    include_funders: bool = True,
    include_historical_associations: bool = True,
    include_wikipedia_archives: bool = True,
) -> dict[str, Any]:
    """Run the adjacent_context_resolver for one politician.

    This is the umbrella Google ADK FunctionTool that returns the 5-axis
    context for one politician. It orchestrates the 4 adjacent axes
    (advisors + funders + historical associations + wikipedia archives)
    alongside the politician themselves.

    Args:
        politician_id: the canonical politician id (mutually exclusive
            with canonical_name).
        canonical_name: the politician's canonical name (use when you
            don't know the id).
        party_id: the party_id (required when canonical_name is used).
        jurisdiction: the jurisdiction (required when canonical_name is used).
        include_advisors: include Axis B (default True).
        include_funders: include Axis C (default True).
        include_historical_associations: include Axis D (default True).
        include_wikipedia_archives: include Axis E (default True).

    Returns:
        A dict with the 5 axes:
        - axis_a_politician: Politician dict (from politician_account_resolver)
        - axis_b_advisors: list of Advisor dicts (Axis B)
        - axis_c_funders: list of Funder dicts (Axis C)
        - axis_d_historical_associations: list of HistoricalAssociation dicts (Axis D)
        - axis_e_wikipedia_archives: WikipediaArchives dict (Axis E)
        - extracted_at: ISO 8601
        - extraction_source: "adjacent_context_resolver"
        - extraction_confidence: 0.0–1.0 (averaged across axes)
        - osint_ceiling_enforced: True
        - analyst_review_required: True
    """
    if not politician_id and not canonical_name:
        raise ValueError("Either politician_id or canonical_name must be provided")

    logger.info(
        "adjacent_context_resolver_started",
        extra={
            "politician_id": politician_id,
            "canonical_name": canonical_name,
            "include_advisors": include_advisors,
            "include_funders": include_funders,
            "include_historical_associations": include_historical_associations,
            "include_wikipedia_archives": include_wikipedia_archives,
        },
    )

    resolved = {
        "axis_a_politician": None,
        "axis_b_advisors": [],
        "axis_c_funders": [],
        "axis_d_historical_associations": [],
        "axis_e_wikipedia_archives": None,
        "extracted_at": datetime.now(UTC).isoformat(),
        "extraction_source": "adjacent_context_resolver",
        "extraction_confidence": 0.0,
        "osint_ceiling_enforced": True,
        "analyst_review_required": True,
    }

    # ------------------------------------------------------------------------
    # Axis A — the politician themselves (via politician_account_resolver)
    # ------------------------------------------------------------------------
    politician_resolver = _try_import_politician_resolver()
    if politician_resolver is not None:
        try:
            axis_a = await politician_resolver(
                politician_id=politician_id,
                canonical_name=canonical_name,
                party_id=party_id,
                jurisdiction=jurisdiction,
            )
            resolved["axis_a_politician"] = axis_a
        except Exception as exc:
            logger.warning("axis_a_resolution_failed", error=str(exc))

    # ------------------------------------------------------------------------
    # Axes B-E — populated by the 4 DLT source trees. For the initial
    # release, we return the empty list / null — the DLT source trees
    # are wired but not yet executed at FunctionTool call time.
    # ------------------------------------------------------------------------
    if include_advisors:
        # TODO: invoke dlt_sources/cianchosaint/advisors/uk_hoc_spad_register
        # TODO: invoke dlt_sources/cianchosaint/advisors/ni_assembly_spad_register
        # TODO: invoke dlt_sources/cianchosaint/advisors/oireachtas_advisors
        # TODO: invoke dlt_sources/cianchosaint/advisors/holyrood_spad_register
        resolved["axis_b_advisors"] = _stub_advisor_list()

    if include_funders:
        # TODO: invoke the 9 funder DLT sources (filter by jurisdiction)
        resolved["axis_c_funders"] = _stub_funder_list()

    if include_historical_associations:
        # TODO: invoke the 6 historical-association DLT sources
        resolved["axis_d_historical_associations"] = _stub_historical_association_list()

    if include_wikipedia_archives:
        # TODO: invoke the 5 wikipedia_archives DLT sources
        # The WikipediaBridge tool (see wikipedia_bridge.py) is the canonical
        # way to populate Axis E in production.
        resolved["axis_e_wikipedia_archives"] = _stub_wikipedia_archives(canonical_name)

    # ------------------------------------------------------------------------
    # Compute the average extraction confidence across all 5 axes
    # ------------------------------------------------------------------------
    confidences: list[float] = []
    if resolved["axis_a_politician"]:
        confidences.append(resolved["axis_a_politician"].get("extraction_confidence", 0.0))
    if resolved["axis_e_wikipedia_archives"]:
        confidences.append(resolved["axis_e_wikipedia_archives"].get("extraction_confidence", 0.0))

    resolved["extraction_confidence"] = sum(confidences) / len(confidences) if confidences else 0.5

    logger.info(
        "adjacent_context_resolver_completed",
        extra={
            "politician_id": politician_id,
            "canonical_name": canonical_name,
            "axis_a_present": resolved["axis_a_politician"] is not None,
            "axis_b_count": len(resolved["axis_b_advisors"]),
            "axis_c_count": len(resolved["axis_c_funders"]),
            "axis_d_count": len(resolved["axis_d_historical_associations"]),
            "axis_e_present": resolved["axis_e_wikipedia_archives"] is not None,
        },
    )

    return resolved


def _stub_advisor_list() -> list[dict[str, Any]]:
    """Return a stub list of advisors for the initial release.

    The real implementation invokes the 4 advisor DLT sources
    (UK HoC SpAd register + NI Assembly SpAd register + Oireachtas
    advisors + Holyrood SpAd register) and filters by the politician's
    jurisdiction.
    """
    return [
        {
            "source_id": "uk_hoc_spad_register",
            "source_name": "UK Cabinet Office Special Adviser Register",
            "note": "Initial release returns the source description only; per-advisor records are populated by the DLT pipeline at scrape time.",
            "osint_ceiling_enforced": True,
            "analyst_review_required": True,
        },
    ]


def _stub_funder_list() -> list[dict[str, Any]]:
    """Return a stub list of funder sources for the initial release.

    The real implementation invokes the 9 funder DLT sources (filter by
    the politician's jurisdiction + party_id).
    """
    return [
        {
            "source_id": "electoral_commission_uk",
            "source_name": "UK Electoral Commission Register of Political Parties",
            "note": "Initial release returns the source description only; per-funder records are populated by the DLT pipeline at scrape time.",
            "osint_ceiling_enforced": True,
            "analyst_review_required": True,
        },
    ]


def _stub_historical_association_list() -> list[dict[str, Any]]:
    """Return a stub list of historical-association sources."""
    return [
        {
            "source_id": "wikidata_politician",
            "source_name": "Wikidata Query Service for Politician QIDs",
            "note": "Initial release returns the source description only; per-association records are populated by the DLT pipeline at scrape time.",
            "osint_ceiling_enforced": True,
            "analyst_review_required": True,
        },
    ]


def _stub_wikipedia_archives(canonical_name: str | None) -> dict[str, Any]:
    """Return a stub WikipediaArchives record for the initial release.

    The real implementation invokes the wikipedia_bridge.py FunctionTool
    to look up the Wikidata QID + the multilingual Wikipedia article titles.
    """
    return {
        "wikipedia_archives_id": f"wikipedia_archives:{canonical_name or 'unknown'}",
        "subject_canonical_name": canonical_name or "",
        "wikidata_qid": None,  # populated by wikipedia_bridge
        "wikipedia_title_en": None,
        "wikipedia_title_ga": None,
        "wikipedia_title_cy": None,
        "wikipedia_title_gd": None,
        "wikidata_statements": [],
        "wikipedia_categories": [],
        "note": "Initial release returns null; populated by wikipedia_bridge.py + the 5 wikipedia_archives DLT sources at scrape time.",
        "osint_ceiling_enforced": True,
        "analyst_review_required": True,
        "extraction_confidence": 0.0,
    }


adjacent_context_resolver_tool = FunctionTool(func=adjacent_context_resolver)


__all__ = [
    "adjacent_context_resolver",
    "adjacent_context_resolver_tool",
]
