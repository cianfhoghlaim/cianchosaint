# CIANCHOSAINT new-build: per-political-party DLT source for Reform UK.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: Reform UK is the canonical pilot source).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# This is the canonical Reform UK source — used by the
# reform-uk-pilot-workflow (per Q12 = B + the locked plan). It is the
# FIRST party source authored in this change and serves as the PATTERN
# for the other 23.
#
# Sources data from:
# - Reform UK official website: https://www.reformparty.uk/news
# - Reform UK Companies House filings: bulk data via data.police.uk-style
#   bulk endpoints (to be wired in a follow-up)
# - Reform UK Electoral Commission returns: bulk data via the Electoral
#   Commission Register of Political Parties API
#
# Per the cianchosaint OSINT allowlist (see
# dlt_sources/official_media_cianchosaint/fixtures/allowlist_parties.yaml
# + dlt_sources/cianchosaint/common/osint_allowlist.yaml), this source
# falls within the British Isles public-sector OSINT ceiling.

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.uk.reform_uk — Reform UK.

Canonical sources (per Q12 = B — Reform UK pilot case study):
- https://www.reformparty.uk/news (press releases)
- Companies House bulk data (donor analysis; follow-up change)
- Electoral Commission returns (voting records; follow-up change)

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/uk_hoc/reform_uk/``.
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


REFORM_UK_BASE = "https://www.reformparty.uk/news"
REFORM_UK_ELECTORAL_COMMISSION_ID = "PP-12345"  # Reform UK's Electoral Commission ID (verify)


class ReformUKPipeline(PoliticalPartyPipelineBase):
    """Reform UK party pipeline.

    Canonical sources:
    - https://www.reformparty.uk/news (press releases)
    - Companies House bulk data (donor analysis)
    - Electoral Commission returns (voting records)
    """

    PARTY_ID = "reform-uk"
    PARTY_NAME = "Reform UK"
    JURISDICTION = "uk_hoc"
    SOURCE_BASE = REFORM_UK_BASE
    ELECTORAL_COMMISSION_ID = REFORM_UK_ELECTORAL_COMMISSION_ID

    def _iter_press_releases(self) -> Iterator[dict[str, Any]]:
        """Yield Reform UK press releases from reformparty.uk/news.

        Returns the canonical cohort row per record (see
        ``PoliticalPartyPipelineBase.party_to_row``).
        """
        for page in _crawl_source(
            source_name="reform_uk.news",
            base_url=REFORM_UK_BASE,
            include_paths=["/**"],
            max_pages=50,
            max_depth=3,
        ):
            page["party_id"] = self.PARTY_ID
            page["party_name"] = self.PARTY_NAME
            page["jurisdiction"] = self.JURISDICTION
            page["electoral_commission_id"] = self.ELECTORAL_COMMISSION_ID
            yield self.party_to_row(page)


@dlt.source(name="reform_uk")
def reform_uk_source() -> list:
    """DLT source for Reform UK press releases (the canonical pilot case study)."""

    @dlt.resource(
        name="reform_uk_press_releases",
        write_disposition="merge",
        primary_key=["natural_key"],
    )
    def press_releases() -> Iterator[dict[str, Any]]:
        pipeline = ReformUKPipeline()
        yield from pipeline._iter_press_releases()

    return [press_releases]