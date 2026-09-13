# CIANCHOSAINT new-build: Scottish Gaelic Wikipedia politician archive DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The wikipedia_archives/
# DLT source tree.
#
# Source: Scottish Gaelic (Gàidhlig) Wikipedia
# URL: https://gd.wikipedia.org/wiki/Roinn-se%C3%B2rsa:Poileataichean
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.wikipedia_archives.wikipedia_gd — Scottish Gaelic Wikipedia."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.wikipedia_archives._base import (
    WikipediaArchivesPipelineBase,
)

logger = structlog.get_logger(__name__)


WIKIPEDIA_GD_URL = "https://gd.wikipedia.org/wiki/Roinn-se%C3%B2rsa:Poileataichean"


class WikipediaGdPipeline(WikipediaArchivesPipelineBase):
    """Scottish Gaelic Wikipedia politician archive pipeline."""

    SOURCE_ID = "wikipedia_gd"
    SOURCE_NAME = "Scottish Gaelic (Gàidhlig) Wikipedia Politician Archive"
    SOURCE_BASE = WIKIPEDIA_GD_URL
    LANGUAGE_CODE = "gd"

    def _iter_wikipedia_archive_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Scottish Gaelic Wikipedia cohort row."""
        yield self.wikipedia_archives_to_row()


@dlt.source(name="wikipedia_gd")
def wikipedia_gd_source() -> list:
    """DLT source for the Scottish Gaelic Wikipedia politician archive."""

    @dlt.resource(
        name="wikipedia_gd",
        write_disposition="merge",
        primary_key=["source_id", "wikipedia_archives_id"],
    )
    def wikipedia() -> Iterator[dict[str, Any]]:
        pipeline = WikipediaGdPipeline()
        yield from pipeline._iter_wikipedia_archive_records()

    return [wikipedia()]


__all__ = [
    "WIKIPEDIA_GD_URL",
    "WikipediaGdPipeline",
    "wikipedia_gd_source",
]
