# CIANCHOSAINT new-build: UK HoC Special Adviser register DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The advisors/ DLT
# source tree.
#
# Source: UK Cabinet Office Special Adviser register
# URL: https://www.gov.uk/government/publications/special-adviser-data
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.advisors.uk_hoc_spad_register — UK HoC SpAd register."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.advisors._base import (
    AdvisorPipelineBase,
)

logger = structlog.get_logger(__name__)


UK_SPAD_REGISTER_URL = "https://www.gov.uk/government/publications/special-adviser-data"


class UKHoCSpadRegisterPipeline(AdvisorPipelineBase):
    """UK HoC Cabinet Office Special Adviser register pipeline."""

    SOURCE_ID = "uk_hoc_spad_register"
    SOURCE_NAME = "UK Cabinet Office Special Adviser Register"
    JURISDICTION = "uk_hoc"
    SOURCE_BASE = UK_SPAD_REGISTER_URL

    def _iter_advisor_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical UK HoC SpAd register cohort row."""
        yield self.advisor_to_row()


@dlt.source(name="uk_hoc_spad_register")
def uk_hoc_spad_register_source() -> list:
    """DLT source for the UK HoC Cabinet Office Special Adviser register."""

    @dlt.resource(
        name="uk_hoc_spad_register",
        write_disposition="merge",
        primary_key=["source_id", "advisor_id"],
    )
    def register() -> Iterator[dict[str, Any]]:
        pipeline = UKHoCSpadRegisterPipeline()
        yield from pipeline._iter_advisor_records()

    return [register()]


__all__ = [
    "UK_SPAD_REGISTER_URL",
    "UKHoCSpadRegisterPipeline",
    "uk_hoc_spad_register_source",
]
