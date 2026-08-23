# CIANCHOSAINT new-build: per-political-party DLT source for the
# Green Party / Comhaontas Glas (Ireland).
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.roi.green_party_roi — Greens (Ireland).

Source: ``https://www.greenparty.ie/news/`` — Green Party / Comhaontas
Glas (Ireland) news room. Falls within the cianchosaint OSINT allowlist
(entry: ig_username=greenpartyie).

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/roi/green_party_roi/``.
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


GREEN_ROI_BASE = "https://www.greenparty.ie/news/"
GREEN_ROI_ELECTORAL_COMMISSION_ID = "nil"


class GreenPartyROIPipeline(PoliticalPartyPipelineBase):
    """Green Party / Comhaontas Glas (Ireland) pipeline."""

    PARTY_ID = "green-party-roi"
    PARTY_NAME = "Green Party / Comhaontas Glas (Ireland)"
    JURISDICTION = "roi_dail"
    SOURCE_BASE = GREEN_ROI_BASE
    ELECTORAL_COMMISSION_ID = GREEN_ROI_ELECTORAL_COMMISSION_ID

    def _iter_press_releases(self) -> Iterator[dict[str, Any]]:
        for page in _crawl_source(
            source_name="green_party_roi.news",
            base_url=GREEN_ROI_BASE,
            include_paths=["/**"],
            max_pages=50,
            max_depth=3,
        ):
            page["party_id"] = self.PARTY_ID
            page["party_name"] = self.PARTY_NAME
            page["jurisdiction"] = self.JURISDICTION
            page["electoral_commission_id"] = self.ELECTORAL_COMMISSION_ID
            yield self.party_to_row(page)


@dlt.source(name="green_party_roi")
def green_party_roi_source() -> list:
    """DLT source for the Green Party / Comhaontas Glas (Ireland)."""

    @dlt.resource(
        name="green_party_roi_press_releases",
        write_disposition="merge",
        primary_key=["natural_key"],
    )
    def press_releases() -> Iterator[dict[str, Any]]:
        pipeline = GreenPartyROIPipeline()
        yield from pipeline._iter_press_releases()

    return [press_releases]