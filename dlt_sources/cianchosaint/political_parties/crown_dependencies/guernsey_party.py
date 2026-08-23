# CIANCHOSAINT new-build: per-political-party DLT source for Guernsey
# (States of Guernsey + parish-level independents).
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.crown_dependencies.guernsey_party — Guernsey (States).

Source: ``https://www.gov.gg/StatesofGuernsey`` — the States of
Guernsey government news room. Falls within the cianchosaint OSINT
allowlist.

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/crown_dependencies/ggy/``.
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


GUERNSEY_PARTY_BASE = "https://www.gov.gg/StatesofGuernsey"
GUERNSEY_PARTY_ELECTORAL_COMMISSION_ID = "nil"


class GuernseyPartyPipeline(PoliticalPartyPipelineBase):
    """Guernsey (States of Guernsey) pipeline."""

    PARTY_ID = "guernsey-party"
    PARTY_NAME = "Guernsey (States of Guernsey)"
    JURISDICTION = "ggy"
    SOURCE_BASE = GUERNSEY_PARTY_BASE
    ELECTORAL_COMMISSION_ID = GUERNSEY_PARTY_ELECTORAL_COMMISSION_ID

    def _iter_press_releases(self) -> Iterator[dict[str, Any]]:
        for page in _crawl_source(
            source_name="guernsey_party.news",
            base_url=GUERNSEY_PARTY_BASE,
            include_paths=["/**"],
            max_pages=50,
            max_depth=3,
        ):
            page["party_id"] = self.PARTY_ID
            page["party_name"] = self.PARTY_NAME
            page["jurisdiction"] = self.JURISDICTION
            page["electoral_commission_id"] = self.ELECTORAL_COMMISSION_ID
            yield self.party_to_row(page)


@dlt.source(name="guernsey_party")
def guernsey_party_source() -> list:
    """DLT source for the States of Guernsey government press room."""

    @dlt.resource(
        name="guernsey_party_press_releases",
        write_disposition="merge",
        primary_key=["natural_key"],
    )
    def press_releases() -> Iterator[dict[str, Any]]:
        pipeline = GuernseyPartyPipeline()
        yield from pipeline._iter_press_releases()

    return [press_releases]