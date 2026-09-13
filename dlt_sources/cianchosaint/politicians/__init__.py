# CIANCHOSAINT new-build: per-politician DLT source tree.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The 5 new DLT
# source trees (politicians/ + advisors/ + funders/ + historical_associations/
# + wikipedia_archives/).
#
# This tree is the **Axis A** of the 5-axis politician + adjacent-context
# pipeline. It provides the per-politician DLT source modules that harvest
# the canonical Politician schema (canonical_name, party_id, jurisdiction,
# constituency, official_website, social_handles[], public_metrics[]).
#
# The 7 case-study politicians (per the user's verbatim request on 2026-09-06):
# - Nigel Farage        (reform-uk / uk_hoc / Clacton)
# - Zack Polanski       (green-party-ew / uk_hoc / [co-leader])
# - John O'Dowd MLA     (sinn-fein / ni_assembly / Upper Bann)
# - Gordon Lyons MLA    (dup / ni_assembly / East Antrim)
# - Paul Givan MLA      (dup / ni_assembly / Lagan Valley)
# - Gavin Robinson MP   (dup / uk_hoc / North Down [until 2024])
# - Lara Bird MSP       (snp / holyrood / East Lothian)
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.politicians — base + registry + 7 case studies.

Exports:
    PoliticianPipelineBase     — the canonical contract for per-politician DLT sources
    POLITICIAN_REGISTRY        — the cohort registry (7 manual case studies + N harvested)
    PoliticianCohort           — the (politician_id, party_id, jurisdiction, source_url) tuple
"""

from ._base import (
    DEFAULT_LEABHARLANN_ROOT,
    PoliticianCohort,
    PoliticianPipelineBase,
    VALID_JURISDICTIONS,
    VALID_PARTY_IDS,
)
from ._registry import (
    POLITICIAN_REGISTRY,
    add_politician,
    get_politician,
    list_politicians,
    list_politicians_by_jurisdiction,
    list_politicians_by_party,
)

__all__ = [
    "DEFAULT_LEABHARLANN_ROOT",
    "POLITICIAN_REGISTRY",
    "PoliticianCohort",
    "PoliticianPipelineBase",
    "VALID_JURISDICTIONS",
    "VALID_PARTY_IDS",
    "add_politician",
    "get_politician",
    "list_politicians",
    "list_politicians_by_jurisdiction",
    "list_politicians_by_party",
]
