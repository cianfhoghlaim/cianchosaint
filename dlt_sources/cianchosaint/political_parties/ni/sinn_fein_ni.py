# CIANCHOSAINT new-build: per-political-party DLT source for Sinn Féin
# (Northern Ireland branch).
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.ni.sinn_fein_ni — Sinn Féin (NI).

Source: ``https://www.sinnfein.ie/ni/news`` — Sinn Féin (NI branch)
news room. Note: Sinn Féin also has a separate ROI branch source at
``dlt_sources/cianchosaint/political_parties/roi/sinn_fein_roi.py``.

Falls within the cianchosaint OSINT allowlist (entry:
ig_username=sinnfeinbelfast).

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/ni_assembly/sinn_fein/``.
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


SINN_FEIN_NI_BASE = "https://www.sinnfein.ie/ni/news"
SINN_FEIN_NI_ELECTORAL_COMMISSION_ID = "PP-10126"


class SinnFeinNIPipeline(PoliticalPartyPipelineBase):
    """Sinn Féin (Northern Ireland branch) pipeline."""

    PARTY_ID = "sinn-fein-ni"
    PARTY_NAME = "Sinn Féin (Northern Ireland branch)"
    JURISDICTION = "ni_assembly"
    SOURCE_BASE = SINN_FEIN_NI_BASE
    ELECTORAL_COMMISSION_ID = SINN_FEIN_NI_ELECTORAL_COMMISSION_ID

    def _iter_press_releases(self) -> Iterator[dict[str, Any]]:
        for page in _crawl_source(
            source_name="sinn_fein_ni.news",
            base_url=SINN_FEIN_NI_BASE,
            include_paths=["/**"],
            max_pages=50,
            max_depth=3,
        ):
            page["party_id"] = self.PARTY_ID
            page["party_name"] = self.PARTY_NAME
            page["jurisdiction"] = self.JURISDICTION
            page["electoral_commission_id"] = self.ELECTORAL_COMMISSION_ID
            yield self.party_to_row(page)


@dlt.source(name="sinn_fein_ni")
def sinn_fein_ni_source() -> list:
    """DLT source for Sinn Féin (NI branch)."""

    @dlt.resource(
        name="sinn_fein_ni_press_releases",
        write_disposition="merge",
        primary_key=["natural_key"],
    )
    def press_releases() -> Iterator[dict[str, Any]]:
        pipeline = SinnFeinNIPipeline()
        yield from pipeline._iter_press_releases()

    return [press_releases]