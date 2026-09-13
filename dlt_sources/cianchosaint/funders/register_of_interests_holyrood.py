# CIANCHOSAINT new-build: Scottish Parliament Register of Members' Interests DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The funders/ DLT
# source tree.
#
# Source: Scottish Parliament Register of Members' Interests
# URL: https://www.parliament.scot/msps/register-of-interests
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.funders.register_of_interests_holyrood — Holyrood."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.funders._base import (
    FunderPipelineBase,
)

logger = structlog.get_logger(__name__)


HOLYROOD_REGISTER_INTERESTS_URL = "https://www.parliament.scot/msps/register-of-interests"


class HolyroodRegisterOfInterestsPipeline(FunderPipelineBase):
    """Scottish Parliament Register of Members' Interests pipeline."""

    SOURCE_ID = "register_of_interests_holyrood"
    SOURCE_NAME = "Scottish Parliament Register of Members' Interests"
    JURISDICTION = "holyrood"
    SOURCE_BASE = HOLYROOD_REGISTER_INTERESTS_URL
    SOURCE_TYPE = "register_of_interests"

    def _iter_funder_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Holyrood Register of Interests cohort row."""
        yield self.funder_to_row()


@dlt.source(name="register_of_interests_holyrood")
def register_of_interests_holyrood_source() -> list:
    """DLT source for the Scottish Parliament Register of Members' Interests."""

    @dlt.resource(
        name="register_of_interests_holyrood",
        write_disposition="merge",
        primary_key=["source_id", "funder_id"],
    )
    def register() -> Iterator[dict[str, Any]]:
        pipeline = HolyroodRegisterOfInterestsPipeline()
        yield from pipeline._iter_funder_records()

    return [register()]


__all__ = [
    "HOLYROOD_REGISTER_INTERESTS_URL",
    "HolyroodRegisterOfInterestsPipeline",
    "register_of_interests_holyrood_source",
]
