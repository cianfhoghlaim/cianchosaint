# CIANCHOSAINT new-build: per-political-party DLT source for the
# Scottish National Party (Holyrood scope).
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.scotland.snp_scottish — SNP (Holyrood).

Source: ``https://www.snp.org/holyrood`` — Scottish National Party
(Holyrood scope) news room. Note: SNP also has a separate UK HoC scope
source at ``dlt_sources/cianchosaint/political_parties/uk/snp.py``.

Falls within the cianchosaint OSINT allowlist (entry:
ig_username=snp).

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/holyrood/snp/``.
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


SNP_SCOTTISH_BASE = "https://www.snp.org/holyrood"
SNP_SCOTTISH_ELECTORAL_COMMISSION_ID = "PP-10122"


class SNPScottishPipeline(PoliticalPartyPipelineBase):
    """SNP (Holyrood scope) pipeline."""

    PARTY_ID = "snp-scottish"
    PARTY_NAME = "Scottish National Party (Holyrood scope)"
    JURISDICTION = "holyrood"
    SOURCE_BASE = SNP_SCOTTISH_BASE
    ELECTORAL_COMMISSION_ID = SNP_SCOTTISH_ELECTORAL_COMMISSION_ID

    def _iter_press_releases(self) -> Iterator[dict[str, Any]]:
        for page in _crawl_source(
            source_name="snp_scottish.news",
            base_url=SNP_SCOTTISH_BASE,
            include_paths=["/**"],
            max_pages=50,
            max_depth=3,
        ):
            page["party_id"] = self.PARTY_ID
            page["party_name"] = self.PARTY_NAME
            page["jurisdiction"] = self.JURISDICTION
            page["electoral_commission_id"] = self.ELECTORAL_COMMISSION_ID
            yield self.party_to_row(page)


@dlt.source(name="snp_scottish")
def snp_scottish_source() -> list:
    """DLT source for the SNP (Holyrood scope)."""

    @dlt.resource(
        name="snp_scottish_press_releases",
        write_disposition="merge",
        primary_key=["natural_key"],
    )
    def press_releases() -> Iterator[dict[str, Any]]:
        pipeline = SNPScottishPipeline()
        yield from pipeline._iter_press_releases()

    return [press_releases]