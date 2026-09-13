# CIANCHOSAINT — Advisor cohort registry.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The advisors/
# cohort registry.
#
# Enumerates the 4 jurisdictional SpAd registers:
# - uk_hoc_spad_register        — UK Cabinet Office Special Adviser register
# - ni_assembly_spad_register   — NI Executive Office Special Adviser register
# - oireachtas_advisors         — Oireachtas Committee on Finance advisors
# - holyrood_spad_register      — Scottish Government Special Adviser register
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.advisors._registry — cohort registry."""

from __future__ import annotations

import logging

from ._base import AdvisorCohort, VALID_JURISDICTIONS

logger = logging.getLogger(__name__)


_ADVISORS: dict[str, AdvisorCohort] = {
    # === UK HoC — Cabinet Office Special Adviser Register ===
    "uk_hoc_spad_register": AdvisorCohort(
        source_id="uk_hoc_spad_register",
        source_name="UK Cabinet Office Special Adviser Register",
        jurisdiction="uk_hoc",
        source_url="https://www.gov.uk/government/publications/special-adviser-data",
        source_urls=[
            "https://www.gov.uk/government/publications/special-adviser-data",
        ],
    ),
    # === NI Assembly — NI Executive Office Special Adviser Register ===
    "ni_assembly_spad_register": AdvisorCohort(
        source_id="ni_assembly_spad_register",
        source_name="NI Executive Office Special Adviser Register",
        jurisdiction="ni_assembly",
        source_url="https://www.northernireland.gov.uk/topics/your-executive/northern-ireland-executive-office",
        source_urls=[
            "https://www.northernireland.gov.uk/topics/your-executive/northern-ireland-executive-office",
        ],
    ),
    # === ROI Oireachtas — Committee on Finance advisors ===
    "oireachtas_advisors": AdvisorCohort(
        source_id="oireachtas_advisors",
        source_name="Oireachtas Committee on Finance Advisors",
        jurisdiction="roi_dail",
        source_url="https://www.oireachtas.ie/en/committees/finance/",
        source_urls=[
            "https://www.oireachtas.ie/en/committees/finance/",
        ],
    ),
    # === Holyrood — Scottish Government Special Adviser Register ===
    "holyrood_spad_register": AdvisorCohort(
        source_id="holyrood_spad_register",
        source_name="Scottish Government Special Adviser Register",
        jurisdiction="holyrood",
        source_url="https://www.gov.scot/publications/special-advisers-scotland/",
        source_urls=[
            "https://www.gov.scot/publications/special-advisers-scotland/",
        ],
    ),
}


def ADVISOR_REGISTRY() -> list[AdvisorCohort]:
    """Return the list of all registered advisor sources."""
    return list(_ADVISORS.values())


def list_advisors() -> list[AdvisorCohort]:
    """Return the list of all registered advisor sources."""
    return ADVISOR_REGISTRY()


def list_advisors_by_jurisdiction(jurisdiction: str) -> list[AdvisorCohort]:
    """Return all advisor sources for the given jurisdiction."""
    if jurisdiction not in VALID_JURISDICTIONS:
        raise ValueError(f"jurisdiction {jurisdiction!r} is not in VALID_JURISDICTIONS")
    return [a for a in _ADVISORS.values() if a.jurisdiction == jurisdiction]


def get_advisor(source_id: str) -> AdvisorCohort | None:
    """Return the advisor source with the given id, or None if not found."""
    return _ADVISORS.get(source_id)


def add_advisor(
    cohort: AdvisorCohort,
    *,
    overwrite: bool = False,
) -> bool:
    """Add an advisor source to the registry."""
    if cohort.jurisdiction not in VALID_JURISDICTIONS:
        raise ValueError(
            f"advisor {cohort.source_id!r}: jurisdiction {cohort.jurisdiction!r} is not in VALID_JURISDICTIONS"
        )

    if cohort.source_id in _ADVISORS and not overwrite:
        logger.info("advisor_already_in_registry", extra={"source_id": cohort.source_id, "skipped": True})
        return False

    _ADVISORS[cohort.source_id] = cohort
    logger.info(
        "advisor_added_to_registry",
        extra={"source_id": cohort.source_id, "jurisdiction": cohort.jurisdiction, "overwrite": overwrite},
    )
    return True


__all__ = [
    "ADVISOR_REGISTRY",
    "add_advisor",
    "get_advisor",
    "list_advisors",
    "list_advisors_by_jurisdiction",
]


if __name__ == "__main__":
    print(f"Advisor registry: {len(list_advisors())} jurisdictional sources")
    for a in sorted(list_advisors(), key=lambda x: x.source_id):
        print(f"  {a.source_id}: {a.source_name} ({a.jurisdiction})")
        print(f"    url: {a.source_url}")
