# CIANCHOSAINT new-build: per-politician DLT source for Gavin Robinson MP (DUP / Belfast East / UK HoC).
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The 7 case-study
# politician DLT source modules.
#
# Canonical sources:
# - https://mydup.com/people/gavin-robinson (DUP profile)
# - https://www.parliament.uk/biographies/commons/mr-gavin-robinson/4582 (UK Parliament)
# - https://www.theyworkforyou.com/mp/gavin_robinson/belfast-east (TWFY)
#
# NOTE: Robinson was MP for Belfast East 2015–2024. He contested North
# Down in 2024 and lost. The user's request lists him as "gavin robinson
# dup" — the canonical record keeps him in the DUP cohort under UK HoC
# and notes the constituency change.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.politicians.ni.gavin_robinson — Gavin Robinson.

Canonical sources:
- DUP profile:    https://mydup.com/people/gavin-robinson
- UK Parliament:  https://www.parliament.uk/biographies/commons/mr-gavin-robinson/4582
- TWFY:           https://www.theyworkforyou.com/mp/gavin_robinson/belfast-east

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/uk_hoc/gavin_robinson/`.
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


DUP_ROBINSON_PROFILE = "https://mydup.com/people/gavin-robinson"
ROBINSON_PARLIAMENT_URL = "https://www.parliament.uk/biographies/commons/mr-gavin-robinson/4582"
ROBINSON_TWFY_URL = "https://www.theyworkforyou.com/mp/gavin_robinson/belfast-east"


class GavinRobinsonPipeline(PoliticianPipelineBase):
    """Gavin Robinson — DUP MP for Belfast East (UK HoC, 2015–2024)."""

    POLITICIAN_ID = "gavin_robinson"
    CANONICAL_NAME = "Gavin Robinson"
    HONORIFIC = "MP"
    PARTY_ID = "dup"
    PARTY_NAME = "Democratic Unionist Party"
    JURISDICTION = "uk_hoc"
    CONSTITUENCY = "Belfast East"
    SOURCE_BASE = DUP_ROBINSON_PROFILE

    def _iter_politician_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Gavin Robinson Politician cohort row."""
        yield self.politician_to_row()


@dlt.source(name="gavin_robinson")
def gavin_robinson_source() -> list:
    """DLT source for Gavin Robinson MP (DUP / Belfast East / UK HoC)."""

    @dlt.resource(
        name="gavin_robinson_politician",
        write_disposition="merge",
        primary_key=["politician_id"],
    )
    def politician() -> Iterator[dict[str, Any]]:
        pipeline = GavinRobinsonPipeline()
        yield from pipeline._iter_politician_records()

    return [politician()]


__all__ = [
    "DUP_ROBINSON_PROFILE",
    "GavinRobinsonPipeline",
    "ROBINSON_PARLIAMENT_URL",
    "ROBINSON_TWFY_URL",
    "gavin_robinson_source",
]
