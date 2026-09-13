# CIANCHOSAINT new-build: per-politician DLT source for John O'Dowd MLA (Sinn Féin / Upper Bann / NI Assembly).
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The 7 case-study
# politician DLT source modules.
#
# Canonical sources:
# - https://www.sinnfein.ie/people/john-o-dowd (Sinn Féin profile)
# - https://www.niassembly.gov.uk/your-mlas/john-o-dowd (NI Assembly)
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.politicians.ni.john_o_dowd — John O'Dowd.

Canonical sources:
- Sinn Féin profile:  https://www.sinnfein.ie/people/john-o-dowd
- NI Assembly:        https://www.niassembly.gov.uk/your-mlas/john-o-dowd

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/ni_assembly/john_o_dowd/`.
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


SINN_FEIN_ODOWD_PROFILE = "https://www.sinnfein.ie/people/john-o-dowd"
NI_ASSEMBLY_ODOWD_URL = "https://www.niassembly.gov.uk/your-mlas/john-o-dowd"


class JohnODowdPipeline(PoliticianPipelineBase):
    """John O'Dowd — Sinn Féin MLA for Upper Bann (NI Assembly)."""

    POLITICIAN_ID = "john_o_dowd"
    CANONICAL_NAME = "John O'Dowd"
    HONORIFIC = "MLA"
    PARTY_ID = "sinn-fein"
    PARTY_NAME = "Sinn Féin"
    JURISDICTION = "ni_assembly"
    CONSTITUENCY = "Upper Bann"
    SOURCE_BASE = SINN_FEIN_ODOWD_PROFILE

    def _iter_politician_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical John O'Dowd Politician cohort row."""
        yield self.politician_to_row()


@dlt.source(name="john_o_dowd")
def john_o_dowd_source() -> list:
    """DLT source for John O'Dowd MLA (Sinn Féin / Upper Bann / NI Assembly)."""

    @dlt.resource(
        name="john_o_dowd_politician",
        write_disposition="merge",
        primary_key=["politician_id"],
    )
    def politician() -> Iterator[dict[str, Any]]:
        pipeline = JohnODowdPipeline()
        yield from pipeline._iter_politician_records()

    return [politician()]


__all__ = [
    "JohnODowdPipeline",
    "NI_ASSEMBLY_ODOWD_URL",
    "SINN_FEIN_ODOWD_PROFILE",
    "john_o_dowd_source",
]
