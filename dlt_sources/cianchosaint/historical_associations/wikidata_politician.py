# CIANCHOSAINT new-build: Wikidata politician QID DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The historical_associations/
# DLT source tree.
#
# Source: Wikidata Query Service (SPARQL endpoint for politician QIDs)
# URL: https://query.wikidata.org/
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.historical_associations.wikidata_politician — Wikidata politician QIDs."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.historical_associations._base import (
    HistoricalAssociationPipelineBase,
)

logger = structlog.get_logger(__name__)


WIKIDATA_QUERY_URL = "https://query.wikidata.org/"


class WikidataPoliticianPipeline(HistoricalAssociationPipelineBase):
    """Wikidata politician QID pipeline."""

    SOURCE_ID = "wikidata_politician"
    SOURCE_NAME = "Wikidata Query Service for Politician QIDs"
    SOURCE_BASE = WIKIDATA_QUERY_URL

    def _iter_historical_association_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Wikidata politician cohort row."""
        yield self.historical_association_to_row()


@dlt.source(name="wikidata_politician")
def wikidata_politician_source() -> list:
    """DLT source for the Wikidata politician QID Query Service."""

    @dlt.resource(
        name="wikidata_politician",
        write_disposition="merge",
        primary_key=["source_id", "association_id"],
    )
    def wikidata() -> Iterator[dict[str, Any]]:
        pipeline = WikidataPoliticianPipeline()
        yield from pipeline._iter_historical_association_records()

    return [wikidata()]


__all__ = [
    "WIKIDATA_QUERY_URL",
    "WikidataPoliticianPipeline",
    "wikidata_politician_source",
]
