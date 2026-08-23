# CIANCHOSAINT new-build: per-political-party DLT source for the
# Conservative and Unionist Party (UK).
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.uk.conservative_party_uk — UK Conservatives.

Source: ``https://www.conservatives.com/our-plan`` — the Conservative
and Unionist Party (UK) policy + press releases library. Falls within
the cianchosaint OSINT allowlist (entry: ig_username=ukconservative).

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/uk_hoc/conservative/``.
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


CONSERVATIVE_UK_BASE = "https://www.conservatives.com/our-plan"
CONSERVATIVE_UK_ELECTORAL_COMMISSION_ID = "PP-10125"


class ConservativeUKPipeline(PoliticalPartyPipelineBase):
    """Conservative and Unionist Party (UK) pipeline."""

    PARTY_ID = "conservative-uk"
    PARTY_NAME = "Conservative and Unionist Party (UK)"
    JURISDICTION = "uk_hoc"
    SOURCE_BASE = CONSERVATIVE_UK_BASE
    ELECTORAL_COMMISSION_ID = CONSERVATIVE_UK_ELECTORAL_COMMISSION_ID

    def _iter_press_releases(self) -> Iterator[dict[str, Any]]:
        for page in _crawl_source(
            source_name="conservative_uk.our_plan",
            base_url=CONSERVATIVE_UK_BASE,
            include_paths=["/**"],
            max_pages=50,
            max_depth=3,
        ):
            page["party_id"] = self.PARTY_ID
            page["party_name"] = self.PARTY_NAME
            page["jurisdiction"] = self.JURISDICTION
            page["electoral_commission_id"] = self.ELECTORAL_COMMISSION_ID
            yield self.party_to_row(page)


@dlt.source(name="conservative_uk")
def conservative_uk_source() -> list:
    """DLT source for the Conservative and Unionist Party (UK)."""

    @dlt.resource(
        name="conservative_uk_press_releases",
        write_disposition="merge",
        primary_key=["natural_key"],
    )
    def press_releases() -> Iterator[dict[str, Any]]:
        pipeline = ConservativeUKPipeline()
        yield from pipeline._iter_press_releases()

    return [press_releases]