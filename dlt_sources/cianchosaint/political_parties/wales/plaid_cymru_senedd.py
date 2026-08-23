# CIANCHOSAINT new-build: per-political-party DLT source for Plaid
# Cymru (Senedd scope).
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.wales.plaid_cymru_senedd — Plaid Cymru (Senedd).

Source: ``https://www.partyof.wales/senedd`` — Plaid Cymru (Senedd
scope) news room. Note: Plaid Cymru also has a separate UK HoC scope
source at
``dlt_sources/cianchosaint/political_parties/uk/plaid_cymru.py``.

Falls within the cianchosaint OSINT allowlist (entry:
ig_username=plaid_cymru).

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/senedd/plaid_cymru/``.
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


PLAID_CYMRU_SENEDD_BASE = "https://www.partyof.wales/senedd"
PLAID_CYMRU_SENEDD_ELECTORAL_COMMISSION_ID = "PP-10115"


class PlaidCymruSeneddPipeline(PoliticalPartyPipelineBase):
    """Plaid Cymru (Senedd scope) pipeline."""

    PARTY_ID = "plaid-cymru-senedd"
    PARTY_NAME = "Plaid Cymru — Party of Wales (Senedd scope)"
    JURISDICTION = "senedd"
    SOURCE_BASE = PLAID_CYMRU_SENEDD_BASE
    ELECTORAL_COMMISSION_ID = PLAID_CYMRU_SENEDD_ELECTORAL_COMMISSION_ID

    def _iter_press_releases(self) -> Iterator[dict[str, Any]]:
        for page in _crawl_source(
            source_name="plaid_cymru_senedd.news",
            base_url=PLAID_CYMRU_SENEDD_BASE,
            include_paths=["/**"],
            max_pages=50,
            max_depth=3,
        ):
            page["party_id"] = self.PARTY_ID
            page["party_name"] = self.PARTY_NAME
            page["jurisdiction"] = self.JURISDICTION
            page["electoral_commission_id"] = self.ELECTORAL_COMMISSION_ID
            yield self.party_to_row(page)


@dlt.source(name="plaid_cymru_senedd")
def plaid_cymru_senedd_source() -> list:
    """DLT source for Plaid Cymru (Senedd scope)."""

    @dlt.resource(
        name="plaid_cymru_senedd_press_releases",
        write_disposition="merge",
        primary_key=["natural_key"],
    )
    def press_releases() -> Iterator[dict[str, Any]]:
        pipeline = PlaidCymruSeneddPipeline()
        yield from pipeline._iter_press_releases()

    return [press_releases]