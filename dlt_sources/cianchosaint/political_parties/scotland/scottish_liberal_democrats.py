# CIANCHOSAINT new-build: per-political-party DLT source for the
# Scottish Liberal Democrats.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.scotland.scottish_liberal_democrats — Scottish Lib Dems.

Source: ``https://www.scotlibdems.org.uk/news`` — Scottish Liberal
Democrats news room. Falls within the cianchosaint OSINT allowlist.

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/holyrood/libdems/``.
"""
from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

import dlt_sources

from dlt_sources.cianchosaint.political_parties._base import (
    PoliticalPartyPipelineBase,
)
from dlt_sources.cianchosaint.political_parties import _crawl_source

logger = structlog.get_logger(__name__)


SCOTTISH_LIBDEMS_BASE = "https://www.scotlibdems.org.uk/news"
SCOTTISH_LIBDEMS_ELECTORAL_COMMISSION_ID = "PP-10134"


class ScottishLiberalDemocratsPipeline(PoliticalPartyPipelineBase):
    """Scottish Liberal Democrats pipeline."""

    PARTY_ID = "scottish-liberal-democrats"
    PARTY_NAME = "Scottish Liberal Democrats"
    JURISDICTION = "holyrood"
    SOURCE_BASE = SCOTTISH_LIBDEMS_BASE
    ELECTORAL_COMMISSION_ID = SCOTTISH_LIBDEMS_ELECTORAL_COMMISSION_ID

    def _iter_press_releases(self) -> Iterator[dict[str, Any]]:
        for page in _crawl_source(
            source_name="scottish_liberal_democrats.news",
            base_url=SCOTTISH_LIBDEMS_BASE,
            include_paths=["/**"],
            max_pages=50,
            max_depth=3,
        ):
            page["party_id"] = self.PARTY_ID
            page["party_name"] = self.PARTY_NAME
            page["jurisdiction"] = self.JURISDICTION
            page["electoral_commission_id"] = self.ELECTORAL_COMMISSION_ID
            yield self.party_to_row(page)


@dlt.source(name="scottish_liberal_democrats")
def scottish_liberal_democrats_source() -> list:
    """DLT source for the Scottish Liberal Democrats."""

    @dlt.resource(
        name="scottish_liberal_democrats_press_releases",
        write_disposition="merge",
        primary_key=["natural_key"],
    )
    def press_releases() -> Iterator[dict[str, Any]]:
        pipeline = ScottishLiberalDemocratsPipeline()
        yield from pipeline._iter_press_releases()

    return [press_releases]