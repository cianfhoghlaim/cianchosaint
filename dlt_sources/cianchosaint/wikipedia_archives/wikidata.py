# CIANCHOSAINT new-build: Wikidata politician QID register DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The wikipedia_archives/
# DLT source tree.
#
# Source: Wikidata WikiProject Politics
# URL: https://www.wikidata.org/wiki/Wikidata:WikiProject_Politics
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.wikipedia_archives.wikidata — Wikidata politician QIDs."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.wikipedia_archives._base import (
    WikipediaArchivesPipelineBase,
)

logger = structlog.get_logger(__name__)


WIKIDATA_WIKIPROJECT_POLITICS_URL = "https://www.wikidata.org/wiki/Wikidata:WikiProject_Politics"


class WikidataPoliticianQidPipeline(WikipediaArchivesPipelineBase):
    """Wikidata WikiProject Politics pipeline."""

    SOURCE_ID = "wikidata"
    SOURCE_NAME = "Wikidata Politician QID Register"
    SOURCE_BASE = WIKIDATA_WIKIPROJECT_POLITICS_URL
    LANGUAGE_CODE = "en"

    def _iter_wikipedia_archive_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Wikidata politician cohort row."""
        yield self.wikipedia_archives_to_row()


@dlt.source(name="wikidata")
def wikidata_source() -> list:
    """DLT source for the Wikidata WikiProject Politics politician QID register."""

    @dlt.resource(
        name="wikidata",
        write_disposition="merge",
        primary_key=["source_id", "wikipedia_archives_id"],
    )
    def wikidata() -> Iterator[dict[str, Any]]:
        pipeline = WikidataPoliticianQidPipeline()
        yield from pipeline._iter_wikipedia_archive_records()

    return [wikidata()]


__all__ = [
    "WIKIDATA_WIKIPROJECT_POLITICS_URL",
    "WikidataPoliticianQidPipeline",
    "wikidata_source",
]
