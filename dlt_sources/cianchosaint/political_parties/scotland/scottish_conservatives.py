# CIANCHOSAINT new-build: per-political-party DLT source for the
# Scottish Conservatives.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.scotland.scottish_conservatives — Scottish Conservatives.

Source: ``https://www.scottishconservatives.com/news`` — Scottish
Conservatives news room. Falls within the cianchosaint OSINT allowlist.

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/holyrood/conservative/``.
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


SCOTTISH_CONSERVATIVES_BASE = "https://www.scottishconservatives.com/news"
SCOTTISH_CONSERVATIVES_ELECTORAL_COMMISSION_ID = "PP-10133"


class ScottishConservativesPipeline(PoliticalPartyPipelineBase):
    """Scottish Conservatives pipeline."""

    PARTY_ID = "scottish-conservatives"
    PARTY_NAME = "Scottish Conservatives"
    JURISDICTION = "holyrood"
    SOURCE_BASE = SCOTTISH_CONSERVATIVES_BASE
    ELECTORAL_COMMISSION_ID = SCOTTISH_CONSERVATIVES_ELECTORAL_COMMISSION_ID

    def _iter_press_releases(self) -> Iterator[dict[str, Any]]:
        for page in _crawl_source(
            source_name="scottish_conservatives.news",
            base_url=SCOTTISH_CONSERVATIVES_BASE,
            include_paths=["/**"],
            max_pages=50,
            max_depth=3,
        ):
            page["party_id"] = self.PARTY_ID
            page["party_name"] = self.PARTY_NAME
            page["jurisdiction"] = self.JURISDICTION
            page["electoral_commission_id"] = self.ELECTORAL_COMMISSION_ID
            yield self.party_to_row(page)


@dlt.source(name="scottish_conservatives")
def scottish_conservatives_source() -> list:
    """DLT source for the Scottish Conservatives."""

    @dlt.resource(
        name="scottish_conservatives_press_releases",
        write_disposition="merge",
        primary_key=["natural_key"],
    )
    def press_releases() -> Iterator[dict[str, Any]]:
        pipeline = ScottishConservativesPipeline()
        yield from pipeline._iter_press_releases()

    return [press_releases]