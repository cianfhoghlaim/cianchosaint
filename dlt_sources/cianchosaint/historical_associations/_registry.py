# CIANCHOSAINT — HistoricalAssociation cohort registry (6 surfaces).
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The historical_associations/
# cohort registry.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.historical_associations._registry — cohort registry."""

from __future__ import annotations

import logging

from ._base import HistoricalAssociationCohort

logger = logging.getLogger(__name__)


_HISTORICAL_ASSOCIATIONS: dict[str, HistoricalAssociationCohort] = {
    # === Wikidata Query Service for politician QIDs ===
    "wikidata_politician": HistoricalAssociationCohort(
        source_id="wikidata_politician",
        source_name="Wikidata Query Service for Politician QIDs",
        source_url="https://query.wikidata.org/",
        extraction_confidence=0.95,
    ),
    # === NI Courts Service ===
    "ni_courts_service": HistoricalAssociationCohort(
        source_id="ni_courts_service",
        source_name="NI Courts Service (courtserve.net)",
        source_url="https://www.courtserve.net/",
        extraction_confidence=0.80,
    ),
    # === Oireachtas Courts (ROI) ===
    "oireachtas_courts": HistoricalAssociationCohort(
        source_id="oireachtas_courts",
        source_name="Courts Service Ireland (courts.ie)",
        source_url="https://www.courts.ie/",
        extraction_confidence=0.80,
    ),
    # === Scottish Courts ===
    "scot_courts": HistoricalAssociationCohort(
        source_id="scot_courts",
        source_name="Scottish Courts and Tribunals (scotcourts.gov.uk)",
        source_url="https://www.scotcourts.gov.uk/",
        extraction_confidence=0.80,
    ),
    # === UK Companies House Officer History ===
    "companies_house_officer_history": HistoricalAssociationCohort(
        source_id="companies_house_officer_history",
        source_name="UK Companies House Officer History",
        source_url="https://find-and-update.company-information.service.gov.uk/",
        extraction_confidence=0.85,
    ),
    # === UK Insolvency Service ===
    "insolvency_service": HistoricalAssociationCohort(
        source_id="insolvency_service",
        source_name="UK Insolvency Service Determinations",
        source_url="https://www.gov.uk/government/organisations/insolvency-service",
        extraction_confidence=0.80,
    ),
}


def HISTORICAL_ASSOCIATION_REGISTRY() -> list[HistoricalAssociationCohort]:
    """Return the list of all registered historical-association sources."""
    return list(_HISTORICAL_ASSOCIATIONS.values())


def list_historical_associations() -> list[HistoricalAssociationCohort]:
    """Return the list of all registered historical-association sources."""
    return HISTORICAL_ASSOCIATION_REGISTRY()


def get_historical_association(source_id: str) -> HistoricalAssociationCohort | None:
    """Return the historical-association source with the given id, or None."""
    return _HISTORICAL_ASSOCIATIONS.get(source_id)


def add_historical_association(
    cohort: HistoricalAssociationCohort,
    *,
    overwrite: bool = False,
) -> bool:
    """Add a historical-association source to the registry."""
    if cohort.source_id in _HISTORICAL_ASSOCIATIONS and not overwrite:
        logger.info(
            "historical_association_already_in_registry",
            extra={"source_id": cohort.source_id, "skipped": True},
        )
        return False

    _HISTORICAL_ASSOCIATIONS[cohort.source_id] = cohort
    logger.info(
        "historical_association_added_to_registry",
        extra={"source_id": cohort.source_id, "overwrite": overwrite},
    )
    return True


__all__ = [
    "HISTORICAL_ASSOCIATION_REGISTRY",
    "add_historical_association",
    "get_historical_association",
    "list_historical_associations",
]


if __name__ == "__main__":
    print(f"Historical association registry: {len(list_historical_associations())} surfaces")
    for h in sorted(list_historical_associations(), key=lambda x: x.source_id):
        print(f"  {h.source_id}: {h.source_name}")
        print(f"    url: {h.source_url}")
