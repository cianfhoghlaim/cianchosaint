# CIANCHOSAINT new-build: per-political-party DLT source for the
# Democratic Unionist Party (DUP).
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.ni.dup — Democratic Unionist Party.

Source: ``https://mydup.com/news`` — Democratic Unionist Party news
room. Falls within the cianchosaint OSINT allowlist (entry:
ig_username=dupofficial).

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/ni_assembly/dup/``.
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


DUP_BASE = "https://mydup.com/news"
DUP_ELECTORAL_COMMISSION_ID = "PP-10113"


class DUPPipeline(PoliticalPartyPipelineBase):
    """Democratic Unionist Party pipeline."""

    PARTY_ID = "dup"
    PARTY_NAME = "Democratic Unionist Party"
    JURISDICTION = "ni_assembly"
    SOURCE_BASE = DUP_BASE
    ELECTORAL_COMMISSION_ID = DUP_ELECTORAL_COMMISSION_ID

    def _iter_press_releases(self) -> Iterator[dict[str, Any]]:
        for page in _crawl_source(
            source_name="dup.news",
            base_url=DUP_BASE,
            include_paths=["/**"],
            max_pages=50,
            max_depth=3,
        ):
            page["party_id"] = self.PARTY_ID
            page["party_name"] = self.PARTY_NAME
            page["jurisdiction"] = self.JURISDICTION
            page["electoral_commission_id"] = self.ELECTORAL_COMMISSION_ID
            yield self.party_to_row(page)


@dlt.source(name="dup")
def dup_source() -> list:
    """DLT source for the Democratic Unionist Party."""

    @dlt.resource(
        name="dup_press_releases",
        write_disposition="merge",
        primary_key=["natural_key"],
    )
    def press_releases() -> Iterator[dict[str, Any]]:
        pipeline = DUPPipeline()
        yield from pipeline._iter_press_releases()

    return [press_releases]