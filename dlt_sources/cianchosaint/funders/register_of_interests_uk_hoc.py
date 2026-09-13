# CIANCHOSAINT new-build: UK HoC Register of Members' Financial Interests DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The funders/ DLT
# source tree.
#
# Source: UK House of Commons Register of Members' Financial Interests
# URL: https://commonsvotes.digiminster.com/Divisions/Register
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.funders.register_of_interests_uk_hoc — UK HoC."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.funders._base import (
    FunderPipelineBase,
)

logger = structlog.get_logger(__name__)


UK_HOC_REGISTER_INTERESTS_URL = "https://commonsvotes.digiminster.com/Divisions/Register"


class UKHoCRegisterOfInterestsPipeline(FunderPipelineBase):
    """UK HoC Register of Members' Financial Interests pipeline."""

    SOURCE_ID = "register_of_interests_uk_hoc"
    SOURCE_NAME = "UK House of Commons Register of Members' Financial Interests"
    JURISDICTION = "uk_hoc"
    SOURCE_BASE = UK_HOC_REGISTER_INTERESTS_URL
    SOURCE_TYPE = "register_of_interests"

    def _iter_funder_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical UK HoC Register of Interests cohort row."""
        yield self.funder_to_row()


@dlt.source(name="register_of_interests_uk_hoc")
def register_of_interests_uk_hoc_source() -> list:
    """DLT source for the UK HoC Register of Members' Financial Interests."""

    @dlt.resource(
        name="register_of_interests_uk_hoc",
        write_disposition="merge",
        primary_key=["source_id", "funder_id"],
    )
    def register() -> Iterator[dict[str, Any]]:
        pipeline = UKHoCRegisterOfInterestsPipeline()
        yield from pipeline._iter_funder_records()

    return [register()]


__all__ = [
    "UKHoCRegisterOfInterestsPipeline",
    "UK_HOC_REGISTER_INTERESTS_URL",
    "register_of_interests_uk_hoc_source",
]
