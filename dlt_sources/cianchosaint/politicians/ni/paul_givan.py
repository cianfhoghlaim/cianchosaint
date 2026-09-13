# CIANCHOSAINT new-build: per-politician DLT source for Paul Givan MLA (DUP / Lagan Valley / NI Assembly).
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The 7 case-study
# politician DLT source modules.
#
# Canonical sources:
# - https://mydup.com/people/paul-givan (DUP profile)
# - https://www.niassembly.gov.uk/your-mlas/paul-givan (NI Assembly)
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.politicians.ni.paul_givan — Paul Givan.

Canonical sources:
- DUP profile:         https://mydup.com/people/paul-givan
- NI Assembly:         https://www.niassembly.gov.uk/your-mlas/paul-givan

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/ni_assembly/paul_givan/`.
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


DUP_GIVAN_PROFILE = "https://mydup.com/people/paul-givan"
NI_ASSEMBLY_GIVAN_URL = "https://www.niassembly.gov.uk/your-mlas/paul-givan"


class PaulGivanPipeline(PoliticianPipelineBase):
    """Paul Givan — DUP MLA for Lagan Valley (NI Assembly)."""

    POLITICIAN_ID = "paul_givan"
    CANONICAL_NAME = "Paul Givan"
    HONORIFIC = "MLA"
    PARTY_ID = "dup"
    PARTY_NAME = "Democratic Unionist Party"
    JURISDICTION = "ni_assembly"
    CONSTITUENCY = "Lagan Valley"
    SOURCE_BASE = DUP_GIVAN_PROFILE

    def _iter_politician_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Paul Givan Politician cohort row."""
        yield self.politician_to_row()


@dlt.source(name="paul_givan")
def paul_givan_source() -> list:
    """DLT source for Paul Givan MLA (DUP / Lagan Valley / NI Assembly)."""

    @dlt.resource(
        name="paul_givan_politician",
        write_disposition="merge",
        primary_key=["politician_id"],
    )
    def politician() -> Iterator[dict[str, Any]]:
        pipeline = PaulGivanPipeline()
        yield from pipeline._iter_politician_records()

    return [politician()]


__all__ = [
    "DUP_GIVAN_PROFILE",
    "NI_ASSEMBLY_GIVAN_URL",
    "PaulGivanPipeline",
    "paul_givan_source",
]
