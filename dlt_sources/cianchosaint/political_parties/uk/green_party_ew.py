# CIANCHOSAINT new-build: per-political-party DLT source for the
# Green Party of England and Wales.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.uk.green_party_ew — Greens (E&W).

Source: ``https://greenparty.org.uk/news`` — the Green Party of England
and Wales news room. Falls within the cianchosaint OSINT allowlist
(entry: ig_username=thegreenparty).

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/uk_hoc/green_party_ew/``.
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


GREEN_EW_BASE = "https://greenparty.org.uk/news"
GREEN_EW_ELECTORAL_COMMISSION_ID = "PP-10123"


class GreenPartyEWPipeline(PoliticalPartyPipelineBase):
    """Green Party of England and Wales pipeline."""

    PARTY_ID = "green-party-ew"
    PARTY_NAME = "Green Party of England and Wales"
    JURISDICTION = "uk_hoc"
    SOURCE_BASE = GREEN_EW_BASE
    ELECTORAL_COMMISSION_ID = GREEN_EW_ELECTORAL_COMMISSION_ID

    def _iter_press_releases(self) -> Iterator[dict[str, Any]]:
        for page in _crawl_source(
            source_name="green_party_ew.news",
            base_url=GREEN_EW_BASE,
            include_paths=["/**"],
            max_pages=50,
            max_depth=3,
        ):
            page["party_id"] = self.PARTY_ID
            page["party_name"] = self.PARTY_NAME
            page["jurisdiction"] = self.JURISDICTION
            page["electoral_commission_id"] = self.ELECTORAL_COMMISSION_ID
            yield self.party_to_row(page)


@dlt.source(name="green_party_ew")
def green_party_ew_source() -> list:
    """DLT source for the Green Party of England and Wales."""

    @dlt.resource(
        name="green_party_ew_press_releases",
        write_disposition="merge",
        primary_key=["natural_key"],
    )
    def press_releases() -> Iterator[dict[str, Any]]:
        pipeline = GreenPartyEWPipeline()
        yield from pipeline._iter_press_releases()

    return [press_releases]