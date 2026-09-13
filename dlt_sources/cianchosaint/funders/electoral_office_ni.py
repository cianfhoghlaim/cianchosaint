# CIANCHOSAINT new-build: NI Electoral Office DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The funders/ DLT
# source tree.
#
# Source: NI Electoral Office (under the Northern Ireland Act 1998)
# URL: https://www.eoni.org.uk/
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.funders.electoral_office_ni — NI Electoral Office."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.funders._base import (
    FunderPipelineBase,
)

logger = structlog.get_logger(__name__)


NI_ELECTORAL_OFFICE_URL = "https://www.eoni.org.uk/"


class NIElectoralOfficePipeline(FunderPipelineBase):
    """NI Electoral Office pipeline (NI Assembly jurisdiction)."""

    SOURCE_ID = "electoral_office_ni"
    SOURCE_NAME = "NI Electoral Office (under the Northern Ireland Act 1998)"
    JURISDICTION = "ni_assembly"
    SOURCE_BASE = NI_ELECTORAL_OFFICE_URL
    SOURCE_TYPE = "electoral_commission"

    def _iter_funder_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical NI Electoral Office cohort row."""
        yield self.funder_to_row()


@dlt.source(name="electoral_office_ni")
def electoral_office_ni_source() -> list:
    """DLT source for the NI Electoral Office."""

    @dlt.resource(
        name="electoral_office_ni",
        write_disposition="merge",
        primary_key=["source_id", "funder_id"],
    )
    def register() -> Iterator[dict[str, Any]]:
        pipeline = NIElectoralOfficePipeline()
        yield from pipeline._iter_funder_records()

    return [register()]


__all__ = [
    "NIElectoralOfficePipeline",
    "NI_ELECTORAL_OFFICE_URL",
    "electoral_office_ni_source",
]
