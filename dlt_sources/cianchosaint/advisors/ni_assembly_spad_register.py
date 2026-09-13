# CIANCHOSAINT new-build: NI Assembly Special Adviser register DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The advisors/ DLT
# source tree.
#
# Source: NI Executive Office Special Adviser register
# URL: https://www.northernireland.gov.uk/topics/your-executive/northern-ireland-executive-office
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.advisors.ni_assembly_spad_register — NI Assembly SpAd register."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.advisors._base import (
    AdvisorPipelineBase,
)

logger = structlog.get_logger(__name__)


NI_SPAD_REGISTER_URL = "https://www.northernireland.gov.uk/topics/your-executive/northern-ireland-executive-office"


class NIAssemblySpadRegisterPipeline(AdvisorPipelineBase):
    """NI Assembly Executive Office Special Adviser register pipeline."""

    SOURCE_ID = "ni_assembly_spad_register"
    SOURCE_NAME = "NI Executive Office Special Adviser Register"
    JURISDICTION = "ni_assembly"
    SOURCE_BASE = NI_SPAD_REGISTER_URL

    def _iter_advisor_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical NI Assembly SpAd register cohort row."""
        yield self.advisor_to_row()


@dlt.source(name="ni_assembly_spad_register")
def ni_assembly_spad_register_source() -> list:
    """DLT source for the NI Assembly Executive Office Special Adviser register."""

    @dlt.resource(
        name="ni_assembly_spad_register",
        write_disposition="merge",
        primary_key=["source_id", "advisor_id"],
    )
    def register() -> Iterator[dict[str, Any]]:
        pipeline = NIAssemblySpadRegisterPipeline()
        yield from pipeline._iter_advisor_records()

    return [register()]


__all__ = [
    "NI_SPAD_REGISTER_URL",
    "NIAssemblySpadRegisterPipeline",
    "ni_assembly_spad_register_source",
]
