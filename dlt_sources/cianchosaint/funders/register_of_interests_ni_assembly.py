# CIANCHOSAINT new-build: NI Assembly Register of Members' Interests DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The funders/ DLT
# source tree.
#
# Source: NI Assembly Register of Members' Interests
# URL: https://www.niassembly.gov.uk/your-mlas/register-of-interests/
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.funders.register_of_interests_ni_assembly — NI Assembly."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.funders._base import (
    FunderPipelineBase,
)

logger = structlog.get_logger(__name__)


NI_ASSEMBLY_REGISTER_INTERESTS_URL = "https://www.niassembly.gov.uk/your-mlas/register-of-interests/"


class NIAssemblyRegisterOfInterestsPipeline(FunderPipelineBase):
    """NI Assembly Register of Members' Interests pipeline."""

    SOURCE_ID = "register_of_interests_ni_assembly"
    SOURCE_NAME = "NI Assembly Register of Members' Interests"
    JURISDICTION = "ni_assembly"
    SOURCE_BASE = NI_ASSEMBLY_REGISTER_INTERESTS_URL
    SOURCE_TYPE = "register_of_interests"

    def _iter_funder_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical NI Assembly Register of Interests cohort row."""
        yield self.funder_to_row()


@dlt.source(name="register_of_interests_ni_assembly")
def register_of_interests_ni_assembly_source() -> list:
    """DLT source for the NI Assembly Register of Members' Interests."""

    @dlt.resource(
        name="register_of_interests_ni_assembly",
        write_disposition="merge",
        primary_key=["source_id", "funder_id"],
    )
    def register() -> Iterator[dict[str, Any]]:
        pipeline = NIAssemblyRegisterOfInterestsPipeline()
        yield from pipeline._iter_funder_records()

    return [register()]


__all__ = [
    "NI_ASSEMBLY_REGISTER_INTERESTS_URL",
    "NIAssemblyRegisterOfInterestsPipeline",
    "register_of_interests_ni_assembly_source",
]
