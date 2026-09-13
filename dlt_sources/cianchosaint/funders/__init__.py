# CIANCHOSAINT new-build: per-jurisdiction Funder (Electoral Commission +
#                                  Companies House + Registers of Interests) DLT
# source tree.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The funders/ DLT
# source tree (Axis C of the 5-axis politician + adjacent-context pipeline).
#
# Provides 9 funder surfaces:
# - electoral_commission_uk            (UK Electoral Commission register of political parties)
# - electoral_commission_ie            (Irish Electoral Commission register)
# - electoral_office_ni                (NI Electoral Office)
# - companies_house_psc                (UK Companies House Persons of Significant Control)
# - register_of_interests_uk_hoc       (UK HoC Register of Members' Financial Interests)
# - register_of_interests_ni_assembly  (NI Assembly Register of Interests)
# - register_of_interests_oireachtas   (Oireachtas Register of Members' Interests)
# - register_of_interests_holyrood     (Scottish Parliament Register of Interests)
# - register_of_interests_senedd       (Senedd / Welsh Parliament Register of Interests)
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.funders — base + registry + 9 funder surfaces."""

from ._base import (
    Donation,
    FunderCohort,
    FunderPipelineBase,
    VALID_DONOR_TYPES,
    VALID_JURISDICTIONS,
)
from ._registry import (
    FUNDER_REGISTRY,
    add_funder,
    get_funder,
    list_funders,
    list_funders_by_jurisdiction,
    list_funders_by_source_type,
)

__all__ = [
    "Donation",
    "FUNDER_REGISTRY",
    "FunderCohort",
    "FunderPipelineBase",
    "VALID_DONOR_TYPES",
    "VALID_JURISDICTIONS",
    "add_funder",
    "get_funder",
    "list_funders",
    "list_funders_by_jurisdiction",
    "list_funders_by_source_type",
]
