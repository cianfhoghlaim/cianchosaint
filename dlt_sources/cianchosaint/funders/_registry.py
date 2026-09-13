# CIANCHOSAINT — Funder cohort registry (9 funder surfaces).
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The funders/ cohort
# registry.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.funders._registry — cohort registry (9 surfaces)."""

from __future__ import annotations

import logging

from ._base import FunderCohort, VALID_JURISDICTIONS

logger = logging.getLogger(__name__)


_FUNDERS: dict[str, FunderCohort] = {
    # === UK Electoral Commission ===
    "electoral_commission_uk": FunderCohort(
        source_id="electoral_commission_uk",
        source_name="UK Electoral Commission Register of Political Parties",
        jurisdiction="uk_hoc",
        source_url="https://www.electoralcommission.org.uk/",
        source_type="electoral_commission",
    ),
    # === Irish Electoral Commission ===
    "electoral_commission_ie": FunderCohort(
        source_id="electoral_commission_ie",
        source_name="Irish Electoral Commission Register (Electoral Reform Act 2022)",
        jurisdiction="roi_dail",
        source_url="https://www.electoralcommission.ie/",
        source_type="electoral_commission",
    ),
    # === NI Electoral Office ===
    "electoral_office_ni": FunderCohort(
        source_id="electoral_office_ni",
        source_name="NI Electoral Office (under the Northern Ireland Act 1998)",
        jurisdiction="ni_assembly",
        source_url="https://www.eoni.org.uk/",
        source_type="electoral_commission",
    ),
    # === UK Companies House Persons of Significant Control ===
    "companies_house_psc": FunderCohort(
        source_id="companies_house_psc",
        source_name="UK Companies House Persons of Significant Control",
        jurisdiction="uk_hoc",
        source_url="https://find-and-update.company-information.service.gov.uk/",
        source_type="companies_house",
    ),
    # === UK HoC Register of Members' Financial Interests ===
    "register_of_interests_uk_hoc": FunderCohort(
        source_id="register_of_interests_uk_hoc",
        source_name="UK House of Commons Register of Members' Financial Interests",
        jurisdiction="uk_hoc",
        source_url="https://commonsvotes.digiminster.com/Divisions/Register",
        source_type="register_of_interests",
    ),
    # === NI Assembly Register of Interests ===
    "register_of_interests_ni_assembly": FunderCohort(
        source_id="register_of_interests_ni_assembly",
        source_name="NI Assembly Register of Members' Interests",
        jurisdiction="ni_assembly",
        source_url="https://www.niassembly.gov.uk/your-mlas/register-of-interests/",
        source_type="register_of_interests",
    ),
    # === Oireachtas Register of Members' Interests ===
    "register_of_interests_oireachtas": FunderCohort(
        source_id="register_of_interests_oireachtas",
        source_name="Oireachtas Register of Members' Interests",
        jurisdiction="roi_dail",
        source_url="https://www.oireachtas.ie/en/members/register-of-interests/",
        source_type="register_of_interests",
    ),
    # === Holyrood Register of Interests ===
    "register_of_interests_holyrood": FunderCohort(
        source_id="register_of_interests_holyrood",
        source_name="Scottish Parliament Register of Members' Interests",
        jurisdiction="holyrood",
        source_url="https://www.parliament.scot/msps/register-of-interests",
        source_type="register_of_interests",
    ),
    # === Senedd Register of Interests ===
    "register_of_interests_senedd": FunderCohort(
        source_id="register_of_interests_senedd",
        source_name="Senedd / Welsh Parliament Register of Members' Interests",
        jurisdiction="senedd",
        source_url="https://senedd.wales/members/register-of-interests/",
        source_type="register_of_interests",
    ),
}


def FUNDER_REGISTRY() -> list[FunderCohort]:
    """Return the list of all registered funder sources."""
    return list(_FUNDERS.values())


def list_funders() -> list[FunderCohort]:
    """Return the list of all registered funder sources."""
    return FUNDER_REGISTRY()


def list_funders_by_jurisdiction(jurisdiction: str) -> list[FunderCohort]:
    """Return all funder sources for the given jurisdiction."""
    if jurisdiction not in VALID_JURISDICTIONS:
        raise ValueError(f"jurisdiction {jurisdiction!r} is not in VALID_JURISDICTIONS")
    return [f for f in _FUNDERS.values() if f.jurisdiction == jurisdiction]


def list_funders_by_source_type(source_type: str) -> list[FunderCohort]:
    """Return all funder sources of the given type."""
    return [f for f in _FUNDERS.values() if f.source_type == source_type]


def get_funder(source_id: str) -> FunderCohort | None:
    """Return the funder source with the given id, or None if not found."""
    return _FUNDERS.get(source_id)


def add_funder(
    cohort: FunderCohort,
    *,
    overwrite: bool = False,
) -> bool:
    """Add a funder source to the registry."""
    if cohort.jurisdiction not in VALID_JURISDICTIONS:
        raise ValueError(
            f"funder {cohort.source_id!r}: jurisdiction {cohort.jurisdiction!r} is not in VALID_JURISDICTIONS"
        )

    if cohort.source_id in _FUNDERS and not overwrite:
        logger.info("funder_already_in_registry", extra={"source_id": cohort.source_id, "skipped": True})
        return False

    _FUNDERS[cohort.source_id] = cohort
    logger.info(
        "funder_added_to_registry",
        extra={"source_id": cohort.source_id, "jurisdiction": cohort.jurisdiction, "overwrite": overwrite},
    )
    return True


__all__ = [
    "FUNDER_REGISTRY",
    "add_funder",
    "get_funder",
    "list_funders",
    "list_funders_by_jurisdiction",
    "list_funders_by_source_type",
]


if __name__ == "__main__":
    print(f"Funder registry: {len(list_funders())} surfaces")
    by_type: dict[str, int] = {}
    for f in sorted(list_funders(), key=lambda x: x.source_id):
        by_type[f.source_type] = by_type.get(f.source_type, 0) + 1
        print(f"  {f.source_id} [{f.source_type}/{f.jurisdiction}]")
    print(f"By source type: {by_type}")
