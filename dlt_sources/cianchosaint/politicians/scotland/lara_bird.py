# CIANCHOSAINT new-build: per-politician DLT source for Lara Bird MSP (SNP / East Lothian / Holyrood).
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The 7 case-study
# politician DLT source modules.
#
# Canonical sources:
# - https://www.snp.org/people/lara-bird (SNP profile)
# - https://www.parliament.scot/msps/electors/17683 (Scottish Parliament)
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.politicians.scotland.lara_bird — Lara Bird.

Canonical sources:
- SNP profile:          https://www.snp.org/people/lara-bird
- Scottish Parliament:  https://www.parliament.scot/msps/electors/17683

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/holyrood/lara_bird/`.
"""
from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.politicians._base import (
    PoliticianPipelineBase,
)

logger = structlog.get_logger(__name__)


SNP_BIRD_PROFILE = "https://www.snp.org/people/lara-bird"
HOLYROOD_BIRD_URL = "https://www.parliament.scot/msps/electors/17683"


class LaraBirdPipeline(PoliticianPipelineBase):
    """Lara Bird — SNP MSP for East Lothian (Holyrood)."""

    POLITICIAN_ID = "lara_bird"
    CANONICAL_NAME = "Lara Bird"
    HONORIFIC = "MSP"
    PARTY_ID = "snp"
    PARTY_NAME = "Scottish National Party"
    JURISDICTION = "holyrood"
    CONSTITUENCY = "East Lothian"
    SOURCE_BASE = SNP_BIRD_PROFILE

    def _iter_politician_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Lara Bird Politician cohort row."""
        yield self.politician_to_row()


@dlt.source(name="lara_bird")
def lara_bird_source() -> list:
    """DLT source for Lara Bird MSP (SNP / East Lothian / Holyrood)."""

    @dlt.resource(
        name="lara_bird_politician",
        write_disposition="merge",
        primary_key=["politician_id"],
    )
    def politician() -> Iterator[dict[str, Any]]:
        pipeline = LaraBirdPipeline()
        yield from pipeline._iter_politician_records()

    return [politician()]


__all__ = [
    "HOLYROOD_BIRD_URL",
    "LaraBirdPipeline",
    "SNP_BIRD_PROFILE",
    "lara_bird_source",
]
