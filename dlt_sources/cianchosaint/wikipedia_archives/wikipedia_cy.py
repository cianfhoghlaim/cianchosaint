# CIANCHOSAINT new-build: Welsh-language Wikipedia politician archive DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The wikipedia_archives/
# DLT source tree.
#
# Source: Welsh-language (Cymraeg) Wikipedia Category:Gwleidyddion
# URL: https://cy.wikipedia.org/wiki/Categori:Gwleidyddion_yr_20fed_ganrif
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.wikipedia_archives.wikipedia_cy — Welsh-language Wikipedia."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.wikipedia_archives._base import (
    WikipediaArchivesPipelineBase,
)

logger = structlog.get_logger(__name__)


WIKIPEDIA_CY_URL = "https://cy.wikipedia.org/wiki/Categori:Gwleidyddion_yr_20fed_ganrif"


class WikipediaCyPipeline(WikipediaArchivesPipelineBase):
    """Welsh-language Wikipedia politician archive pipeline."""

    SOURCE_ID = "wikipedia_cy"
    SOURCE_NAME = "Welsh-language (Cymraeg) Wikipedia Politician Archive"
    SOURCE_BASE = WIKIPEDIA_CY_URL
    LANGUAGE_CODE = "cy"

    def _iter_wikipedia_archive_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Welsh-language Wikipedia cohort row."""
        yield self.wikipedia_archives_to_row()


@dlt.source(name="wikipedia_cy")
def wikipedia_cy_source() -> list:
    """DLT source for the Welsh-language Wikipedia politician archive."""

    @dlt.resource(
        name="wikipedia_cy",
        write_disposition="merge",
        primary_key=["source_id", "wikipedia_archives_id"],
    )
    def wikipedia() -> Iterator[dict[str, Any]]:
        pipeline = WikipediaCyPipeline()
        yield from pipeline._iter_wikipedia_archive_records()

    return [wikipedia()]


__all__ = [
    "WIKIPEDIA_CY_URL",
    "WikipediaCyPipeline",
    "wikipedia_cy_source",
]
