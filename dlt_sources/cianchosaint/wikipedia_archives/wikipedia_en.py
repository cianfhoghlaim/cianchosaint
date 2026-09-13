# CIANCHOSAINT new-build: English Wikipedia politician archive DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The wikipedia_archives/
# DLT source tree.
#
# Source: English Wikipedia Category:British_politicians (and sub-categories)
# URL: https://en.wikipedia.org/wiki/Category:British_politicians
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.wikipedia_archives.wikipedia_en — English Wikipedia."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.wikipedia_archives._base import (
    WikipediaArchivesPipelineBase,
)

logger = structlog.get_logger(__name__)


WIKIPEDIA_EN_URL = "https://en.wikipedia.org/wiki/Category:British_politicians"


class WikipediaEnPipeline(WikipediaArchivesPipelineBase):
    """English Wikipedia politician archive pipeline."""

    SOURCE_ID = "wikipedia_en"
    SOURCE_NAME = "English Wikipedia Politician Archive"
    SOURCE_BASE = WIKIPEDIA_EN_URL
    LANGUAGE_CODE = "en"

    def _iter_wikipedia_archive_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical English Wikipedia cohort row."""
        yield self.wikipedia_archives_to_row()


@dlt.source(name="wikipedia_en")
def wikipedia_en_source() -> list:
    """DLT source for the English Wikipedia politician archive."""

    @dlt.resource(
        name="wikipedia_en",
        write_disposition="merge",
        primary_key=["source_id", "wikipedia_archives_id"],
    )
    def wikipedia() -> Iterator[dict[str, Any]]:
        pipeline = WikipediaEnPipeline()
        yield from pipeline._iter_wikipedia_archive_records()

    return [wikipedia()]


__all__ = [
    "WIKIPEDIA_EN_URL",
    "WikipediaEnPipeline",
    "wikipedia_en_source",
]
