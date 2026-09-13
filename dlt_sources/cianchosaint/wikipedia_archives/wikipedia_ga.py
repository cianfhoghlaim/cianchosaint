# CIANCHOSAINT new-build: Irish-language Wikipedia politician archive DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The wikipedia_archives/
# DLT source tree.
#
# Source: Irish-language (Gaeilge) Wikipedia Category:Polaitiúcháí_na_hÉireann
# URL: https://ga.wikipedia.org/wiki/Catagóir:Polaitiúcháí_na_hÉireann
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.wikipedia_archives.wikipedia_ga — Irish-language Wikipedia."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.wikipedia_archives._base import (
    WikipediaArchivesPipelineBase,
)

logger = structlog.get_logger(__name__)


WIKIPEDIA_GA_URL = "https://ga.wikipedia.org/wiki/Catag%C3%B3ir:Polaiti%C3%BAch%C3%AD_na_h%C3%89ireann"


class WikipediaGaPipeline(WikipediaArchivesPipelineBase):
    """Irish-language Wikipedia politician archive pipeline."""

    SOURCE_ID = "wikipedia_ga"
    SOURCE_NAME = "Irish-language (Gaeilge) Wikipedia Politician Archive"
    SOURCE_BASE = WIKIPEDIA_GA_URL
    LANGUAGE_CODE = "ga"

    def _iter_wikipedia_archive_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Irish-language Wikipedia cohort row."""
        yield self.wikipedia_archives_to_row()


@dlt.source(name="wikipedia_ga")
def wikipedia_ga_source() -> list:
    """DLT source for the Irish-language Wikipedia politician archive."""

    @dlt.resource(
        name="wikipedia_ga",
        write_disposition="merge",
        primary_key=["source_id", "wikipedia_archives_id"],
    )
    def wikipedia() -> Iterator[dict[str, Any]]:
        pipeline = WikipediaGaPipeline()
        yield from pipeline._iter_wikipedia_archive_records()

    return [wikipedia()]


__all__ = [
    "WIKIPEDIA_GA_URL",
    "WikipediaGaPipeline",
    "wikipedia_ga_source",
]
