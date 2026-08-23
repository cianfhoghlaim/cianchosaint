# CIANCHOSAINT new-build: per-constituency cohort registry for the
# BIPP v1 / BIDP v1 / BIIP v1 milestone gates.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   cohort registry).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# This module enumerates every (jurisdiction, vertical, source,
# cohort_id) tuple for the 26 per-constituency DLT source files
# shipped under dlt_sources/cianchosaint/<jurisdiction>/<vertical>/.
# The cohort registry integrates with the 5-stage pipeline runner at
# dlt_sources/_cross/5_stage_runner.py + the BAML extraction functions
# defined in baml_src/cianchosaint/processing/<vertical>.baml (per the
# follow-up cianchosaint-baml-schemas-v1 change).
#
# Per the cianchosaint-pipeline spec § Requirement: The per-constituency
# DLT source manifest, the cohort grid maps:
#
# - UK policing      → BIPP v1 m2 (5 sources)
# - NI policing      → BIPP v1 m3 (3 sources)
# - Crown Dependencies policing → BIPP v1 m3 (3 sources)
# - UK military      → BIDP v1 m1 (6 sources)
# - Ireland Defence  → BIDP v1 m2 (2 sources)
# - UK intelligence oversight → BIIP v1 m1 (4 sources)
# - UK government    → BIIP v1 m1 (3 sources)

"""cianchosaint.cianchosaint.dlt.british_isles._cross.per_constituency_cohort_registry — cohort grid.

Phase 7 of the openspec change. Maintains the per-constituency cohort
grid + the milestone gate mapping for the BIPP v1 / BIDP v1 /
BIIP v1 milestones.

Usage:

    python -m dlt_sources.cianchosaint._cross.per_constituency_cohort_registry

Prints a table of every cohort (jurisdiction × vertical × source ×
cohort_id) with the milestone gate it unblocks.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Cohort:
    """A single (jurisdiction, vertical, source, cohort_id) tuple + milestone gate."""

    jurisdiction: str
    vertical: str
    source: str
    cohort_id: str
    milestone_gate: str
    extraction_function: str
    target_resource: str
    ingest_queue_subdir: str


# ── THE COHORT GRID ────────────────────────────────────────────────────
# 26 cohorts: 5 UK policing + 3 NI policing + 3 Crown Dependencies
# + 6 UK military + 2 Ireland Defence + 4 UK intelligence oversight
# + 3 UK government.
COHORTS: tuple[Cohort, ...] = (
    # === UK POLICING → BIPP v1 m2 ===
    Cohort(
        jurisdiction="uk",
        vertical="policing",
        source="data_police_uk",
        cohort_id="uk.policing.data_police_uk",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractCrimeStatistics",
        target_resource="forces",
        ingest_queue_subdir="uk/policing/data_police_uk/",
    ),
    Cohort(
        jurisdiction="uk",
        vertical="policing",
        source="metropolitan_police_press_releases",
        cohort_id="uk.policing.metropolitan_police_press_releases",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="uk/policing/metropolitan_police/",
    ),
    Cohort(
        jurisdiction="uk",
        vertical="policing",
        source="stop_and_search_uk",
        cohort_id="uk.policing.stop_and_search_uk",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractStopAndSearchRecord",
        target_resource="records",
        ingest_queue_subdir="uk/policing/stop_and_search_uk/",
    ),
    Cohort(
        jurisdiction="uk",
        vertical="policing",
        source="crime_statistics_uk",
        cohort_id="uk.policing.crime_statistics_uk",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractCrimeStatistics",
        target_resource="statistics",
        ingest_queue_subdir="uk/policing/crime_statistics_uk/",
    ),
    Cohort(
        jurisdiction="uk",
        vertical="policing",
        source="police_workforce_uk",
        cohort_id="uk.policing.police_workforce_uk",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractWorkforceStatistic",
        target_resource="workforce",
        ingest_queue_subdir="uk/policing/police_workforce_uk/",
    ),
    # === NI POLICING → BIPP v1 m3 ===
    Cohort(
        jurisdiction="ni",
        vertical="policing",
        source="psni_press_releases",
        cohort_id="ni.policing.psni_press_releases",
        milestone_gate="BIPP v1 m3",
        extraction_function="ExtractPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="ni/policing/psni/",
    ),
    Cohort(
        jurisdiction="ni",
        vertical="policing",
        source="justice_ni",
        cohort_id="ni.policing.justice_ni",
        milestone_gate="BIPP v1 m3",
        extraction_function="ExtractGovernmentPublication",
        target_resource="publications",
        ingest_queue_subdir="ni/policing/justice_ni/",
    ),
    Cohort(
        jurisdiction="ni",
        vertical="policing",
        source="policing_board_ni",
        cohort_id="ni.policing.policing_board_ni",
        milestone_gate="BIPP v1 m3",
        extraction_function="ExtractOversightPublication",
        target_resource="publications",
        ingest_queue_subdir="ni/policing/policing_board/",
    ),
    # === CROWN DEPENDENCIES POLICING → BIPP v1 m3 ===
    Cohort(
        jurisdiction="jsy",
        vertical="policing",
        source="jersey_policing",
        cohort_id="crown_dependencies.policing.jersey_policing",
        milestone_gate="BIPP v1 m3",
        extraction_function="ExtractPressRelease",
        target_resource="news",
        ingest_queue_subdir="crown_dependencies/jersey/",
    ),
    Cohort(
        jurisdiction="ggy",
        vertical="policing",
        source="guernsey_policing",
        cohort_id="crown_dependencies.policing.guernsey_policing",
        milestone_gate="BIPP v1 m3",
        extraction_function="ExtractPressRelease",
        target_resource="news",
        ingest_queue_subdir="crown_dependencies/guernsey/",
    ),
    Cohort(
        jurisdiction="iom",
        vertical="policing",
        source="isle_of_man_policing",
        cohort_id="crown_dependencies.policing.isle_of_man_policing",
        milestone_gate="BIPP v1 m3",
        extraction_function="ExtractPressRelease",
        target_resource="news",
        ingest_queue_subdir="crown_dependencies/isle_of_man/",
    ),
    # === UK MILITARY → BIDP v1 m1 ===
    Cohort(
        jurisdiction="uk",
        vertical="military",
        source="mod_press_releases",
        cohort_id="uk.military.mod_press_releases",
        milestone_gate="BIDP v1 m1",
        extraction_function="ExtractDefencePublication",
        target_resource="press_releases",
        ingest_queue_subdir="uk/military/mod/",
    ),
    Cohort(
        jurisdiction="uk",
        vertical="military",
        source="raf_press_releases",
        cohort_id="uk.military.raf_press_releases",
        milestone_gate="BIDP v1 m1",
        extraction_function="ExtractDefencePublication",
        target_resource="press_releases",
        ingest_queue_subdir="uk/military/raf/",
    ),
    Cohort(
        jurisdiction="uk",
        vertical="military",
        source="royal_navy_press_releases",
        cohort_id="uk.military.royal_navy_press_releases",
        milestone_gate="BIDP v1 m1",
        extraction_function="ExtractDefencePublication",
        target_resource="press_releases",
        ingest_queue_subdir="uk/military/royal_navy/",
    ),
    Cohort(
        jurisdiction="uk",
        vertical="military",
        source="british_army_press_releases",
        cohort_id="uk.military.british_army_press_releases",
        milestone_gate="BIDP v1 m1",
        extraction_function="ExtractDefencePublication",
        target_resource="press_releases",
        ingest_queue_subdir="uk/military/british_army/",
    ),
    Cohort(
        jurisdiction="uk",
        vertical="military",
        source="jsp_doctrine",
        cohort_id="uk.military.jsp_doctrine",
        milestone_gate="BIDP v1 m1",
        extraction_function="ExtractDoctrinePublication",
        target_resource="publications",
        ingest_queue_subdir="uk/military/jsp/",
    ),
    Cohort(
        jurisdiction="uk",
        vertical="military",
        source="jdp_doctrine",
        cohort_id="uk.military.jdp_doctrine",
        milestone_gate="BIDP v1 m1",
        extraction_function="ExtractDoctrinePublication",
        target_resource="publications",
        ingest_queue_subdir="uk/military/jdp/",
    ),
    # === IRELAND DEFENCE FORCES → BIDP v1 m2 ===
    Cohort(
        jurisdiction="ie",
        vertical="military",
        source="idf_press_releases",
        cohort_id="ie.military.idf_press_releases",
        milestone_gate="BIDP v1 m2",
        extraction_function="ExtractDefencePublication",
        target_resource="press_releases",
        ingest_queue_subdir="ireland/defence_forces/idf_news/",
    ),
    Cohort(
        jurisdiction="ie",
        vertical="military",
        source="idf_white_paper",
        cohort_id="ie.military.idf_white_paper",
        milestone_gate="BIDP v1 m2",
        extraction_function="ExtractDefenceWhitePaper",
        target_resource="publications",
        ingest_queue_subdir="ireland/defence_forces/white_paper/",
    ),
    # === UK INTELLIGENCE OVERSIGHT → BIIP v1 m1 ===
    Cohort(
        jurisdiction="uk",
        vertical="intelligence_oversight",
        source="isc_annual_reports",
        cohort_id="uk.intelligence_oversight.isc_annual_reports",
        milestone_gate="BIIP v1 m1",
        extraction_function="ExtractOversightReport",
        target_resource="reports",
        ingest_queue_subdir="uk/intelligence_oversight/isc/",
    ),
    Cohort(
        jurisdiction="uk",
        vertical="intelligence_oversight",
        source="ipco_reports",
        cohort_id="uk.intelligence_oversight.ipco_reports",
        milestone_gate="BIIP v1 m1",
        extraction_function="ExtractOversightReport",
        target_resource="reports",
        ingest_queue_subdir="uk/intelligence_oversight/ipco/",
    ),
    Cohort(
        jurisdiction="uk",
        vertical="intelligence_oversight",
        source="ipt_decisions",
        cohort_id="uk.intelligence_oversight.ipt_decisions",
        milestone_gate="BIIP v1 m1",
        extraction_function="ExtractTribunalDecision",
        target_resource="decisions",
        ingest_queue_subdir="uk/intelligence_oversight/ipt/",
    ),
    Cohort(
        jurisdiction="uk",
        vertical="intelligence_oversight",
        source="investigatory_powers_bill_evidence",
        cohort_id="uk.intelligence_oversight.investigatory_powers_bill_evidence",
        milestone_gate="BIIP v1 m1",
        extraction_function="ExtractBillEvidence",
        target_resource="evidence",
        ingest_queue_subdir="uk/intelligence_oversight/ipb/",
    ),
    # === UK GOVERNMENT → BIIP v1 m1 ===
    Cohort(
        jurisdiction="uk",
        vertical="government",
        source="nca_threat_assessments",
        cohort_id="uk.government.nca_threat_assessments",
        milestone_gate="BIIP v1 m1",
        extraction_function="ExtractThreatAssessment",
        target_resource="assessments",
        ingest_queue_subdir="uk/government/nca/",
    ),
    Cohort(
        jurisdiction="uk",
        vertical="government",
        source="home_office_statistics",
        cohort_id="uk.government.home_office_statistics",
        milestone_gate="BIIP v1 m1",
        extraction_function="ExtractGovernmentStatistic",
        target_resource="statistics",
        ingest_queue_subdir="uk/government/home_office/",
    ),
    Cohort(
        jurisdiction="uk",
        vertical="government",
        source="moj_statistics",
        cohort_id="uk.government.moj_statistics",
        milestone_gate="BIIP v1 m1",
        extraction_function="ExtractGovernmentStatistic",
        target_resource="statistics",
        ingest_queue_subdir="uk/government/moj/",
    ),
)


def get_extraction_function(cohort_id: str) -> str:
    """Return the BAML extraction function name for the given cohort_id.

    Per the spec § Requirement: The per-constituency cohort registry,
    Scenario: Each cohort has a BAML extraction function. The
    extraction function is defined in
    `baml_src/cianchosaint/processing/<vertical>.baml` (per the
    follow-up `cianchosaint-baml-schemas-v1` change).

    Args:
        cohort_id: The cohort identifier (e.g.
            "uk.policing.data_police_uk").

    Returns:
        The BAML extraction function name (e.g. "ExtractCrimeStatistics").

    Raises:
        KeyError: If the cohort_id is not registered.
    """
    for cohort in COHORTS:
        if cohort.cohort_id == cohort_id:
            return cohort.extraction_function
    raise KeyError(f"Unknown cohort_id: {cohort_id!r}")


def get_cohorts_by_milestone(milestone_gate: str) -> tuple[Cohort, ...]:
    """Return every cohort that unblocks the given milestone gate."""
    return tuple(c for c in COHORTS if c.milestone_gate == milestone_gate)


def get_cohorts_by_vertical(vertical: str) -> tuple[Cohort, ...]:
    """Return every cohort for the given vertical (policing/military/...)."""
    return tuple(c for c in COHORTS if c.vertical == vertical)


def get_cohorts_by_jurisdiction(jurisdiction: str) -> tuple[Cohort, ...]:
    """Return every cohort for the given jurisdiction (uk/ni/ie/jsy/...)."""
    return tuple(c for c in COHORTS if c.jurisdiction == jurisdiction)


# ── THE 5-STAGE PIPELINE INTEGRATION ──────────────────────────────────
#
# Each cohort runs through the 5-stage pipeline
# (dlt_sources/_cross/5_stage_runner.py):
#
#   1. Ingestion   — DLT source (this module's referenced file)
#   2. Extraction  — BAML (get_extraction_function returns the name)
#   3. Embedding   — CocoIndex v1 (per the centralised-registry spec)
#   4. ibis logging — the ibis-to-MotherDuck observability layer
#   5. Analytics   — the marimo dashboard layer
#
# The 5-stage runner receives the cohort_id and routes through the
# 4-tier ModelProviderRouter (per the bootstrap-v2 spec, Requirement:
# 4-tier model provider chain). All LLM calls are traced via
# dlt_sources.common.observability.


def _format_table() -> str:
    """Render the cohort grid as an aligned text table."""
    headers = (
        "jurisdiction",
        "vertical",
        "source",
        "cohort_id",
        "milestone_gate",
        "extraction_function",
    )
    widths = [max(len(str(getattr(c, h))), len(h)) for h, c in
              zip(headers, [Cohort(*([None] * 6))] * len(headers))]
    # Recompute widths against the real rows + headers.
    real_widths = [
        max(len(str(getattr(c, h))) for c in COHORTS + [Cohort(*([None] * 6))])
        for h in headers
    ]
    widths = real_widths

    def _row(values: tuple[str, ...]) -> str:
        return "  ".join(
            f"{v:<{w}}" for v, w in zip(values, widths, strict=False)
        )

    sep = "  ".join("-" * w for w in widths)
    lines: list[str] = []
    lines.append(_row(headers))
    lines.append(sep)
    for c in COHORTS:
        lines.append(_row(tuple(str(getattr(c, h)) for h in headers)))
    lines.append(sep)
    lines.append(f"{len(COHORTS)} cohort(s) registered across "
                 f"{len({c.milestone_gate for c in COHORTS})} milestone gate(s)")
    return "\n".join(lines)


def main() -> int:
    """Print the cohort registry table to stdout."""
    print(_format_table())
    return 0


__all__ = [
    "COHORTS",
    "Cohort",
    "get_cohorts_by_jurisdiction",
    "get_cohorts_by_milestone",
    "get_cohorts_by_vertical",
    "get_extraction_function",
    "main",
]


if __name__ == "__main__":
    raise SystemExit(main())