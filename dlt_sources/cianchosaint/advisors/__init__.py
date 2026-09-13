# CIANCHOSAINT new-build: per-jurisdiction Advisor / SpAd DLT source tree.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The advisors/ DLT
# source tree (Axis B of the 5-axis politician + adjacent-context pipeline).
#
# Provides 4 jurisdictional SpAd registers:
# - UK HoC:        UK Cabinet Office Special Adviser register
# - NI Assembly:   NI Executive Office Special Adviser register
# - ROI Oireachtas: Oireachtas Committee on Finance advisors
# - Holyrood:      Scottish Government Special Adviser register
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.advisors — base + registry + 4 jurisdictional SpAd sources."""

from ._base import (
    AdvisorCohort,
    AdvisorPipelineBase,
    VALID_JURISDICTIONS,
)
from ._registry import (
    ADVISOR_REGISTRY,
    add_advisor,
    get_advisor,
    list_advisors,
    list_advisors_by_jurisdiction,
)

__all__ = [
    "ADVISOR_REGISTRY",
    "AdvisorCohort",
    "AdvisorPipelineBase",
    "VALID_JURISDICTIONS",
    "add_advisor",
    "get_advisor",
    "list_advisors",
    "list_advisors_by_jurisdiction",
]
