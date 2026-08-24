# CIANCHOSAINT — BIPP v2 cohort registry.
#
# Per the openspec/changes/cianchosaint-bipp-v2-political-party-v2-v1/
# specs/cianchosaint-bipp-v2/spec.md.
#
# Enumerates all 7 BIPP v2 cohorts × 6-8 British Isles sub-nations
# = ~50 cohorts. Each cohort has its canonical `cohort_id`,
# `jurisdiction`, `source_url`, `source_pdfs` (the leabharlann
# Gemini Deep Research PDFs), and `milestone_gate`.
#
# License: BUSL-1.1 (per LICENSE.md).

"""cianchosaint.cianchosaint.dlt.british_isles.bipp_v2._registry — cohort registry.

The canonical BIPP v2 cohort registry. Enumerates all 7 thematic
cohorts × 6-8 British Isles sub-nations = ~50 cohorts.

Mirrors the cianchosaint `dlt_sources/cianchosaint/political_parties/_registry.py`
+ the `dlt_sources/cianchosaint/uk/intelligence_agencies/_base.py`.

Each registry entry has:
- `cohort_id`         — the canonical id (one of the 7 cohorts)
- `cohort_name`       — the human-readable display name
- `jurisdiction`      — the British Isles sub-nation
- `source_url`        — the OSINT-allowlisted official source URL
- `source_pdfs`       — the leabharlann PDFs (read-only context)
- `milestone_gate`    — the BIPP v2 milestone gate (m1 / m2 / m3 / ga)

Run:
    python3 -m dlt_sources.cianchosaint.bipp_v2._registry
"""

from __future__ import annotations

import os
from typing import Any, TypedDict


class CohortEntry(TypedDict):
    cohort_id: str
    cohort_name: str
    jurisdiction: str
    source_url: str
    source_pdfs: list[str]
    milestone_gate: str


# The canonical 7 BIPP v2 cohorts × 6-8 British Isles sub-nations = ~50 cohorts.
# Per openspec/specs/cianchosaint-bipp-v2/spec.md §Purpose.
COHORT_REGISTRY: list[CohortEntry] = [
    # ----------------------------------------------------------------------
    # Cohort 1: Reform UK accountability (UK HoC)
    # ----------------------------------------------------------------------
    {
        "cohort_id": "reform_uk_accountability",
        "cohort_name": "Reform UK Accountability",
        "jurisdiction": "uk",
        "source_url": "https://www.reformparty.uk/news",
        "source_pdfs": [
            "leabharlann/gemini_deep_research/politics/reform_richard_tice_debt_fraud.pdf",
            "leabharlann/gemini_deep_research/politics/reform_corruption.pdf",
            "leabharlann/gemini_deep_research/politics/clacton_farage_reform_refusal.pdf",
            "leabharlann/gemini_deep_research/politics/farage_20reform_20uk_20crypto_20oversight.pdf",
            "leabharlann/gemini_deep_research/politics/farage_s_failed_political_history_research_plan.pdf",
        ],
        "milestone_gate": "cianchosaint:bipp:v2:m2",
    },
    # ----------------------------------------------------------------------
    # Cohort 2: Reform UK devolved branches (NI + Scotland)
    # ----------------------------------------------------------------------
    {
        "cohort_id": "reform_uk_devolved_branches",
        "cohort_name": "Reform UK Devolved Branches",
        "jurisdiction": "uk",
        "source_url": "https://www.reformparty.uk/news",
        "source_pdfs": [
            "leabharlann/gemini_deep_research/politics/farage_clacton_opposition_research_blueprint.md",
            "leabharlann/gemini_deep_research/politics/sturgeon_political_history_research_plan.pdf",
        ],
        "milestone_gate": "cianchosaint:bipp:v2:m2",
    },
    {
        "cohort_id": "reform_uk_devolved_branches",
        "cohort_name": "Reform UK Devolved Branches (NI)",
        "jurisdiction": "ni",
        "source_url": "https://www.reformparty.uk/news",
        "source_pdfs": [
            "leabharlann/gemini_deep_research/politics/farage_clacton_opposition_research_blueprint.md",
        ],
        "milestone_gate": "cianchosaint:bipp:v2:m2",
    },
    {
        "cohort_id": "reform_uk_devolved_branches",
        "cohort_name": "Reform UK Devolved Branches (Scotland)",
        "jurisdiction": "scotland",
        "source_url": "https://www.reformparty.uk/news",
        "source_pdfs": [
            "leabharlann/gemini_deep_research/politics/sturgeon_political_history_research_plan.pdf",
        ],
        "milestone_gate": "cianchosaint:bipp:v2:m2",
    },
    # ----------------------------------------------------------------------
    # Cohort 3: Northern Ireland political accountability
    # ----------------------------------------------------------------------
    {
        "cohort_id": "ni_political_accountability",
        "cohort_name": "Northern Ireland Political Accountability",
        "jurisdiction": "ni",
        "source_url": "https://www.nidirect.gov.uk/",
        "source_pdfs": [
            "leabharlann/gemini_deep_research/politics/sinn_f_in_data_funding_and_foreign_influence.pdf",
            "leabharlann/gemini_deep_research/politics/sinn_f_in_history_and_funding_inquiry.pdf",
            "leabharlann/gemini_deep_research/politics/burnham_streeting_compromised_assets.pdf",
            "leabharlann/gemini_deep_research/politics/arlene_foster_research_plan_generation.pdf",
        ],
        "milestone_gate": "cianchosaint:bipp:v2:m1",
    },
    # ----------------------------------------------------------------------
    # Cohort 4: Scottish political accountability
    # ----------------------------------------------------------------------
    {
        "cohort_id": "scottish_political_accountability",
        "cohort_name": "Scottish Political Accountability",
        "jurisdiction": "scotland",
        "source_url": "https://www.scotcourts.gov.uk/",
        "source_pdfs": [
            "leabharlann/gemini_deep_research/politics/sturgeon_political_history_research_plan.pdf",
            "leabharlann/gemini_deep_research/politics/russell_group_whistleblower_protocol_inquiry.pdf",
            "leabharlann/gemini_deep_research/politics/whistleblower_investigates_scottish_officials.pdf",
        ],
        "milestone_gate": "cianchosaint:bipp:v2:m2",
    },
    # ----------------------------------------------------------------------
    # Cohort 5: Welsh + London political accountability
    # ----------------------------------------------------------------------
    {
        "cohort_id": "welsh_london_political_accountability",
        "cohort_name": "Welsh + London Political Accountability",
        "jurisdiction": "wales",
        "source_url": "https://www.senedd.wales/",
        "source_pdfs": [
            "leabharlann/gemini_deep_research/politics/london_boroughs_funding_and_cleanliness_investigation.pdf",
            "leabharlann/gemini_deep_research/politics/veolia_outsourcing_and_neglect_investigation.pdf",
            "leabharlann/gemini_deep_research/politics/kneecap_band_business_and_youth_concerns.pdf",
            "leabharlann/gemini_deep_research/politics/kneecap_deep_dive_investigation.pdf",
            "leabharlann/gemini_deep_research/politics/royal_family_kneecap_and_irish_cities.pdf",
        ],
        "milestone_gate": "cianchosaint:bipp:v2:m2",
    },
    # ----------------------------------------------------------------------
    # Cohort 6: ROI political accountability
    # ----------------------------------------------------------------------
    {
        "cohort_id": "roi_political_accountability",
        "cohort_name": "Republic of Ireland Political Accountability",
        "jurisdiction": "ireland",
        "source_url": "https://www.gov.ie/",
        "source_pdfs": [
            "leabharlann/gemini_deep_research/politics/farrell_sinn_f_in_and_united_ireland_rhetoric.pdf",
            "leabharlann/gemini_deep_research/politics/fine_gael_coalition_strategy_analysis.pdf",
            "leabharlann/gemini_deep_research/politics/irish_political_strategy_and_performance_analysis.pdf",
            "leabharlann/gemini_deep_research/politics/varadkar_controversies_and_political_future.pdf",
            "leabharlann/gemini_deep_research/politics/galway_by_election_media_analysis.pdf",
            "leabharlann/gemini_deep_research/politics/galway_west_election_candidate_analysis.pdf",
        ],
        "milestone_gate": "cianchosaint:bipp:v2:m1",
    },
    # ----------------------------------------------------------------------
    # Cohort 7: Cross-cutting intelligence / cybersecurity
    # ----------------------------------------------------------------------
    {
        "cohort_id": "cross_cutting_intelligence_cybersecurity",
        "cohort_name": "Cross-cutting Intelligence / Cybersecurity",
        "jurisdiction": "uk",
        "source_url": "https://www.gov.uk/government/organisations",
        "source_pdfs": [
            "leabharlann/gemini_deep_research/politics/intelligence_disinformation_and_geopolitics.pdf",
            "leabharlann/gemini_deep_research/politics/intelligence_agency_software_job_cycles.pdf",
            "leabharlann/gemini_deep_research/politics/propaganda_language_and_intelligence_agencies.pdf",
            "leabharlann/gemini_deep_research/politics/russia_us_cyber_influence_comparison.pdf",
            "leabharlann/gemini_deep_research/politics/cybersecurity_strategy_for_british_isles.pdf",
            "leabharlann/gemini_deep_research/politics/british_isles_cyber_defense_strategy.pdf",
            "leabharlann/gemini_deep_research/politics/crypto_group_investigation_and_takedown.pdf",
            "leabharlann/gemini_deep_research/politics/investigating_radicalization_and_venues.pdf",
            "leabharlann/gemini_deep_research/politics/radicalization_manipulation_and_prevention_strategies.pdf",
            "leabharlann/gemini_deep_research/politics/uk_intelligence_jobs_belfast_vs_london.pdf",
            "leabharlann/gemini_deep_research/politics/uk_security_job_eligibility_research.pdf",
        ],
        "milestone_gate": "cianchosaint:bipp:v2:m3",
    },
]


def list_cohorts() -> list[dict[str, Any]]:
    """Return all cohort registry entries."""
    return [dict(c) for c in COHORT_REGISTRY]


def list_cohorts_by_milestone(milestone: str) -> list[dict[str, Any]]:
    """Return cohorts that match the given milestone gate."""
    return [c for c in COHORT_REGISTRY if c["milestone_gate"] == milestone]


def list_cohorts_by_jurisdiction(jurisdiction: str) -> list[dict[str, Any]]:
    """Return cohorts that match the given jurisdiction."""
    return [c for c in COHORT_REGISTRY if c["jurisdiction"] == jurisdiction]


def get_cohort(cohort_id: str, jurisdiction: str) -> dict[str, Any] | None:
    """Return the canonical cohort entry for (cohort_id, jurisdiction)."""
    for c in COHORT_REGISTRY:
        if c["cohort_id"] == cohort_id and c["jurisdiction"] == jurisdiction:
            return dict(c)
    return None


__all__ = [
    "COHORT_REGISTRY",
    "CohortEntry",
    "list_cohorts",
    "list_cohorts_by_milestone",
    "list_cohorts_by_jurisdiction",
    "get_cohort",
]


if __name__ == "__main__":
    import json

    print(json.dumps(list_cohorts(), indent=2))