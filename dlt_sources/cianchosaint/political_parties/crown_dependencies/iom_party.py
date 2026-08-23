# CIANCHOSAINT new-build: per-political-party DLT source for the Isle
# of Man (Tynwald + Tinvaal + Liberal Vannin + others).
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.crown_dependencies.iom_party — Isle of Man (Tynwald).

Source: ``https://www.gov.im/parliament`` — the Isle of Man Tynwald
+ parliament news room. Falls within the cianchosaint OSINT allowlist.

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/crown_dependencies/iom/``.
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


IOM_PARTY_BASE = "https://www.gov.im/parliament"
IOM_PARTY_ELECTORAL_COMMISSION_ID = "nil"


class IsleOfManPartyPipeline(PoliticalPartyPipelineBase):
    """Isle of Man (Tynwald + Tinvaal + Liberal Vannin) pipeline."""

    PARTY_ID = "iom-party"
    PARTY_NAME = "Isle of Man (Tynwald + Tinvaal + Liberal Vannin)"
    JURISDICTION = "iom"
    SOURCE_BASE = IOM_PARTY_BASE
    ELECTORAL_COMMISSION_ID = IOM_PARTY_ELECTORAL_COMMISSION_ID

    def _iter_press_releases(self) -> Iterator[dict[str, Any]]:
        for page in _crawl_source(
            source_name="iom_party.news",
            base_url=IOM_PARTY_BASE,
            include_paths=["/**"],
            max_pages=50,
            max_depth=3,
        ):
            page["party_id"] = self.PARTY_ID
            page["party_name"] = self.PARTY_NAME
            page["jurisdiction"] = self.JURISDICTION
            page["electoral_commission_id"] = self.ELECTORAL_COMMISSION_ID
            yield self.party_to_row(page)


@dlt.source(name="iom_party")
def iom_party_source() -> list:
    """DLT source for the Isle of Man Tynwald + parliament press room."""

    @dlt.resource(
        name="iom_party_press_releases",
        write_disposition="merge",
        primary_key=["natural_key"],
    )
    def press_releases() -> Iterator[dict[str, Any]]:
        pipeline = IsleOfManPartyPipeline()
        yield from pipeline._iter_press_releases()

    return [press_releases]