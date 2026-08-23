# CIANCHOSAINT new-build: per-political-party DLT source for the
# Ulster Unionist Party (UUP).
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.ni.uup — Ulster Unionist Party.

Source: ``https://uup.org/news/`` — Ulster Unionist Party news room.
Falls within the cianchosaint OSINT allowlist (entry:
ig_username=uuponline).

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/ni_assembly/uup/``.
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


UUP_BASE = "https://uup.org/news/"
UUP_ELECTORAL_COMMISSION_ID = "PP-10121"


class UUPPipeline(PoliticalPartyPipelineBase):
    """Ulster Unionist Party pipeline."""

    PARTY_ID = "uup"
    PARTY_NAME = "Ulster Unionist Party"
    JURISDICTION = "ni_assembly"
    SOURCE_BASE = UUP_BASE
    ELECTORAL_COMMISSION_ID = UUP_ELECTORAL_COMMISSION_ID

    def _iter_press_releases(self) -> Iterator[dict[str, Any]]:
        for page in _crawl_source(
            source_name="uup.news",
            base_url=UUP_BASE,
            include_paths=["/**"],
            max_pages=50,
            max_depth=3,
        ):
            page["party_id"] = self.PARTY_ID
            page["party_name"] = self.PARTY_NAME
            page["jurisdiction"] = self.JURISDICTION
            page["electoral_commission_id"] = self.ELECTORAL_COMMISSION_ID
            yield self.party_to_row(page)


@dlt.source(name="uup")
def uup_source() -> list:
    """DLT source for the Ulster Unionist Party."""

    @dlt.resource(
        name="uup_press_releases",
        write_disposition="merge",
        primary_key=["natural_key"],
    )
    def press_releases() -> Iterator[dict[str, Any]]:
        pipeline = UUPPipeline()
        yield from pipeline._iter_press_releases()

    return [press_releases]