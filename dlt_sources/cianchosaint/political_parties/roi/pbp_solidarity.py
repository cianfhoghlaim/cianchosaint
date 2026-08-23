# CIANCHOSAINT new-build: per-political-party DLT source for People
# Before Profit–Solidarity (all-island).
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.roi.pbp_solidarity — PBP–Solidarity.

Source: ``https://www.pbp.ie/news/`` — People Before Profit–Solidarity
(all-island) news room. Falls within the cianchosaint OSINT allowlist
(entry: ig_username=pbp_solidarity).

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/roi/pbp_solidarity/``.
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


PBP_SOLIDARITY_BASE = "https://www.pbp.ie/news/"
PBP_SOLIDARITY_ELECTORAL_COMMISSION_ID = "nil"


class PBPSolidarityPipeline(PoliticalPartyPipelineBase):
    """People Before Profit–Solidarity (all-island) pipeline."""

    PARTY_ID = "pbp-solidarity"
    PARTY_NAME = "People Before Profit–Solidarity (all-island)"
    JURISDICTION = "roi_dail"
    SOURCE_BASE = PBP_SOLIDARITY_BASE
    ELECTORAL_COMMISSION_ID = PBP_SOLIDARITY_ELECTORAL_COMMISSION_ID

    def _iter_press_releases(self) -> Iterator[dict[str, Any]]:
        for page in _crawl_source(
            source_name="pbp_solidarity.news",
            base_url=PBP_SOLIDARITY_BASE,
            include_paths=["/**"],
            max_pages=50,
            max_depth=3,
        ):
            page["party_id"] = self.PARTY_ID
            page["party_name"] = self.PARTY_NAME
            page["jurisdiction"] = self.JURISDICTION
            page["electoral_commission_id"] = self.ELECTORAL_COMMISSION_ID
            yield self.party_to_row(page)


@dlt.source(name="pbp_solidarity")
def pbp_solidarity_source() -> list:
    """DLT source for People Before Profit–Solidarity (all-island)."""

    @dlt.resource(
        name="pbp_solidarity_press_releases",
        write_disposition="merge",
        primary_key=["natural_key"],
    )
    def press_releases() -> Iterator[dict[str, Any]]:
        pipeline = PBPSolidarityPipeline()
        yield from pipeline._iter_press_releases()

    return [press_releases]