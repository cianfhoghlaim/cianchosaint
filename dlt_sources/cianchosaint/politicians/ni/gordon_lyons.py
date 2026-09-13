# CIANCHOSAINT new-build: per-politician DLT source for Gordon Lyons MLA (DUP / East Antrim / NI Assembly).
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The 7 case-study
# politician DLT source modules.
#
# Canonical sources:
# - https://mydup.com/people/gordon-lyons (DUP profile)
# - https://www.niassembly.gov.uk/your-mlas/gordon-lyons (NI Assembly)
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.politicians.ni.gordon_lyons — Gordon Lyons.

Canonical sources:
- DUP profile:         https://mydup.com/people/gordon-lyons
- NI Assembly:         https://www.niassembly.gov.uk/your-mlas/gordon-lyons

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/ni_assembly/gordon_lyons/`.
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


DUP_LYONS_PROFILE = "https://mydup.com/people/gordon-lyons"
NI_ASSEMBLY_LYONS_URL = "https://www.niassembly.gov.uk/your-mlas/gordon-lyons"


class GordonLyonsPipeline(PoliticianPipelineBase):
    """Gordon Lyons — DUP MLA for East Antrim (NI Assembly)."""

    POLITICIAN_ID = "gordon_lyons"
    CANONICAL_NAME = "Gordon Lyons"
    HONORIFIC = "MLA"
    PARTY_ID = "dup"
    PARTY_NAME = "Democratic Unionist Party"
    JURISDICTION = "ni_assembly"
    CONSTITUENCY = "East Antrim"
    SOURCE_BASE = DUP_LYONS_PROFILE

    def _iter_politician_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Gordon Lyons Politician cohort row."""
        yield self.politician_to_row()


@dlt.source(name="gordon_lyons")
def gordon_lyons_source() -> list:
    """DLT source for Gordon Lyons MLA (DUP / East Antrim / NI Assembly)."""

    @dlt.resource(
        name="gordon_lyons_politician",
        write_disposition="merge",
        primary_key=["politician_id"],
    )
    def politician() -> Iterator[dict[str, Any]]:
        pipeline = GordonLyonsPipeline()
        yield from pipeline._iter_politician_records()

    return [politician()]


__all__ = [
    "DUP_LYONS_PROFILE",
    "GordonLyonsPipeline",
    "NI_ASSEMBLY_LYONS_URL",
    "gordon_lyons_source",
]
