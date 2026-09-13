# CIANCHOSAINT new-build: UK Electoral Commission register DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The funders/ DLT
# source tree.
#
# Source: UK Electoral Commission register of political parties + donations
# URL: https://www.electoralcommission.org.uk/
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.funders.electoral_commission_uk — UK Electoral Commission."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.funders._base import (
    FunderPipelineBase,
)

logger = structlog.get_logger(__name__)


UK_ELECTORAL_COMMISSION_URL = "https://www.electoralcommission.org.uk/"


class UKElectoralCommissionPipeline(FunderPipelineBase):
    """UK Electoral Commission register pipeline."""

    SOURCE_ID = "electoral_commission_uk"
    SOURCE_NAME = "UK Electoral Commission Register of Political Parties"
    JURISDICTION = "uk_hoc"
    SOURCE_BASE = UK_ELECTORAL_COMMISSION_URL
    SOURCE_TYPE = "electoral_commission"

    def _iter_funder_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical UK Electoral Commission cohort row."""
        yield self.funder_to_row()


@dlt.source(name="electoral_commission_uk")
def electoral_commission_uk_source() -> list:
    """DLT source for the UK Electoral Commission register."""

    @dlt.resource(
        name="electoral_commission_uk",
        write_disposition="merge",
        primary_key=["source_id", "funder_id"],
    )
    def register() -> Iterator[dict[str, Any]]:
        pipeline = UKElectoralCommissionPipeline()
        yield from pipeline._iter_funder_records()

    return [register()]


__all__ = [
    "UKElectoralCommissionPipeline",
    "UK_ELECTORAL_COMMISSION_URL",
    "electoral_commission_uk_source",
]
