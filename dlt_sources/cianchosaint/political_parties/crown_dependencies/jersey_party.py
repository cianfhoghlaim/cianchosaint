# CIANCHOSAINT new-build: per-political-party DLT source for Jersey
# (States Assembly + Reform Jersey).
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.crown_dependencies.jersey_party — Jersey (States Assembly).

Source: ``https://www.gov.je/Government/Pages/States.aspx`` — the
States of Jersey government news room. Falls within the cianchosaint
OSINT allowlist.

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/crown_dependencies/jsy/``.
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


JERSEY_PARTY_BASE = "https://www.gov.je/Government/Pages/States.aspx"
JERSEY_PARTY_ELECTORAL_COMMISSION_ID = "nil"


class JerseyPartyPipeline(PoliticalPartyPipelineBase):
    """Jersey (States Assembly + Reform Jersey) pipeline."""

    PARTY_ID = "jersey-party"
    PARTY_NAME = "Jersey (States Assembly + Reform Jersey)"
    JURISDICTION = "jsy"
    SOURCE_BASE = JERSEY_PARTY_BASE
    ELECTORAL_COMMISSION_ID = JERSEY_PARTY_ELECTORAL_COMMISSION_ID

    def _iter_press_releases(self) -> Iterator[dict[str, Any]]:
        for page in _crawl_source(
            source_name="jersey_party.news",
            base_url=JERSEY_PARTY_BASE,
            include_paths=["/**"],
            max_pages=50,
            max_depth=3,
        ):
            page["party_id"] = self.PARTY_ID
            page["party_name"] = self.PARTY_NAME
            page["jurisdiction"] = self.JURISDICTION
            page["electoral_commission_id"] = self.ELECTORAL_COMMISSION_ID
            yield self.party_to_row(page)


@dlt.source(name="jersey_party")
def jersey_party_source() -> list:
    """DLT source for the States of Jersey government press room."""

    @dlt.resource(
        name="jersey_party_press_releases",
        write_disposition="merge",
        primary_key=["natural_key"],
    )
    def press_releases() -> Iterator[dict[str, Any]]:
        pipeline = JerseyPartyPipeline()
        yield from pipeline._iter_press_releases()

    return [press_releases]