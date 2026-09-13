# CIANCHOSAINT new-build: per-jurisdiction HistoricalAssociation DLT source tree.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The historical_associations/
# DLT source tree (Axis D of the 5-axis politician + adjacent-context pipeline).
#
# Provides 6 historical-association surfaces:
# - wikidata_politician              (Wikidata Query Service for politician QIDs)
# - ni_courts_service                (NI Courts Service: courtserve.net)
# - oireachtas_courts                (ROI Courts Service: courts.ie)
# - scot_courts                      (Scottish Courts: scotcourts.gov.uk)
# - companies_house_officer_history  (UK Companies House officer history)
# - insolvency_service               (UK Insolvency Service determinations)
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.historical_associations — base + registry + 6 surfaces."""

from ._base import (
    HistoricalAssociationCohort,
    HistoricalAssociationPipelineBase,
    VALID_ASSOCIATION_TYPES,
)
from ._registry import (
    HISTORICAL_ASSOCIATION_REGISTRY,
    add_historical_association,
    get_historical_association,
    list_historical_associations,
)

__all__ = [
    "HistoricalAssociationCohort",
    "HistoricalAssociationPipelineBase",
    "HISTORICAL_ASSOCIATION_REGISTRY",
    "VALID_ASSOCIATION_TYPES",
    "add_historical_association",
    "get_historical_association",
    "list_historical_associations",
]
