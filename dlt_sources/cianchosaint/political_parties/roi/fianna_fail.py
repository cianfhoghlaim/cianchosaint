# CIANCHOSAINT new-build: per-political-party DLT source for Fianna Fáil.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.roi.fianna_fail — Fianna Fáil.

Source: ``https://www.fiannafail.ie/news`` — Fianna Fáil news room.
Falls within the cianchosaint OSINT allowlist (entry:
ig_username=fiannafailparty).

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/roi/fianna_fail/``.
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


FIANNA_FAIL_BASE = "https://www.fiannafail.ie/news"
FIANNA_FAIL_ELECTORAL_COMMISSION_ID = "nil"


class FiannaFailPipeline(PoliticalPartyPipelineBase):
    """Fianna Fáil pipeline."""

    PARTY_ID = "fianna-fail"
    PARTY_NAME = "Fianna Fáil"
    JURISDICTION = "roi_dail"
    SOURCE_BASE = FIANNA_FAIL_BASE
    ELECTORAL_COMMISSION_ID = FIANNA_FAIL_ELECTORAL_COMMISSION_ID

    def _iter_press_releases(self) -> Iterator[dict[str, Any]]:
        for page in _crawl_source(
            source_name="fianna_fail.news",
            base_url=FIANNA_FAIL_BASE,
            include_paths=["/**"],
            max_pages=50,
            max_depth=3,
        ):
            page["party_id"] = self.PARTY_ID
            page["party_name"] = self.PARTY_NAME
            page["jurisdiction"] = self.JURISDICTION
            page["electoral_commission_id"] = self.ELECTORAL_COMMISSION_ID
            yield self.party_to_row(page)


@dlt.source(name="fianna_fail")
def fianna_fail_source() -> list:
    """DLT source for Fianna Fáil."""

    @dlt.resource(
        name="fianna_fail_press_releases",
        write_disposition="merge",
        primary_key=["natural_key"],
    )
    def press_releases() -> Iterator[dict[str, Any]]:
        pipeline = FiannaFailPipeline()
        yield from pipeline._iter_press_releases()

    return [press_releases]