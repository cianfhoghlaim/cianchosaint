# CIANCHOSAINT new-build: Scottish Government Special Adviser register DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The advisors/ DLT
# source tree.
#
# Source: Scottish Government Special Adviser register
# URL: https://www.gov.scot/publications/special-advisers-scotland/
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.advisors.holyrood_spad_register — Holyrood SpAd register."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.advisors._base import (
    AdvisorPipelineBase,
)

logger = structlog.get_logger(__name__)


HOLYROOD_SPAD_REGISTER_URL = "https://www.gov.scot/publications/special-advisers-scotland/"


class HolyroodSpadRegisterPipeline(AdvisorPipelineBase):
    """Scottish Government Special Adviser register pipeline (Holyrood)."""

    SOURCE_ID = "holyrood_spad_register"
    SOURCE_NAME = "Scottish Government Special Adviser Register"
    JURISDICTION = "holyrood"
    SOURCE_BASE = HOLYROOD_SPAD_REGISTER_URL

    def _iter_advisor_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Holyrood SpAd register cohort row."""
        yield self.advisor_to_row()


@dlt.source(name="holyrood_spad_register")
def holyrood_spad_register_source() -> list:
    """DLT source for the Scottish Government Special Adviser register."""

    @dlt.resource(
        name="holyrood_spad_register",
        write_disposition="merge",
        primary_key=["source_id", "advisor_id"],
    )
    def register() -> Iterator[dict[str, Any]]:
        pipeline = HolyroodSpadRegisterPipeline()
        yield from pipeline._iter_advisor_records()

    return [register()]


__all__ = [
    "HOLYROOD_SPAD_REGISTER_URL",
    "HolyroodSpadRegisterPipeline",
    "holyrood_spad_register_source",
]
