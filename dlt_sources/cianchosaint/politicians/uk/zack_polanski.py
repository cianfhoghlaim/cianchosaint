# CIANCHOSAINT new-build: per-politician DLT source for Zack Polanski (Green Party of England and Wales / co-leader).
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The 7 case-study
# politician DLT source modules.
#
# Canonical sources:
# - https://greenparty.org.uk/people/zack-polanski (Green Party co-leader profile)
#
# NOTE: Zack Polanski (formerly Adrian Ramsay's co-leader) was elected
# co-leader of the Green Party of England and Wales in 2025. As a party
# co-leader (not a constituency MP), they do not currently have a
# constituency or parliament profile.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.politicians.uk.zack_polanski — Zack Polanski.

Canonical sources:
- Green Party profile: https://greenparty.org.uk/people/zack-polanski

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/uk_hoc/zack_polanski/`.
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


GREEN_PARTY_POLANSKI_PROFILE = "https://greenparty.org.uk/people/zack-polanski"


class ZackPolanskiPipeline(PoliticianPipelineBase):
    """Zack Polanski — Green Party of England and Wales co-leader."""

    POLITICIAN_ID = "zack_polanski"
    CANONICAL_NAME = "Zack Polanski"
    HONORIFIC = ""  # Co-leader; not currently an MP / MLA / MSP / TD
    PARTY_ID = "green-party-ew"
    PARTY_NAME = "Green Party of England and Wales"
    JURISDICTION = "uk_hoc"
    CONSTITUENCY = ""  # Co-leader; not currently a constituency MP
    SOURCE_BASE = GREEN_PARTY_POLANSKI_PROFILE

    def _iter_politician_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Zack Polanski Politician cohort row."""
        yield self.politician_to_row()


@dlt.source(name="zack_polanski")
def zack_polanski_source() -> list:
    """DLT source for Zack Polanski (Green Party of England and Wales co-leader)."""

    @dlt.resource(
        name="zack_polanski_politician",
        write_disposition="merge",
        primary_key=["politician_id"],
    )
    def politician() -> Iterator[dict[str, Any]]:
        pipeline = ZackPolanskiPipeline()
        yield from pipeline._iter_politician_records()

    return [politician()]


__all__ = [
    "GREEN_PARTY_POLANSKI_PROFILE",
    "ZackPolanskiPipeline",
    "zack_polanski_source",
]
