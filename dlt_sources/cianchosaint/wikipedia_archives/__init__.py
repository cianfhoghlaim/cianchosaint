# CIANCHOSAINT new-build: multilingual Wikipedia + Wikidata DLT source tree.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The wikipedia_archives/
# DLT source tree (Axis E of the 5-axis politician + adjacent-context pipeline).
#
# Provides 5 Wikipedia surfaces:
# - wikipedia_en (English Wikipedia)
# - wikipedia_ga (Irish-language Wikipedia)
# - wikipedia_cy (Welsh-language Wikipedia)
# - wikipedia_gd (Scottish Gaelic Wikipedia)
# - wikidata    (Wikidata Query Service)
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.wikipedia_archives — base + registry + 5 surfaces."""

from ._base import (
    VALID_LANGUAGE_CODES,
    WikipediaArchivesCohort,
    WikipediaArchivesPipelineBase,
)
from ._registry import (
    WIKIPEDIA_ARCHIVES_REGISTRY,
    add_wikipedia_archive,
    get_wikipedia_archive,
    list_wikipedia_archives,
)

__all__ = [
    "VALID_LANGUAGE_CODES",
    "WIKIPEDIA_ARCHIVES_REGISTRY",
    "WikipediaArchivesCohort",
    "WikipediaArchivesPipelineBase",
    "add_wikipedia_archive",
    "get_wikipedia_archive",
    "list_wikipedia_archives",
]
