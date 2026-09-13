# CIANCHOSAINT new-build: Oireachtas Register of Members' Interests DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The funders/ DLT
# source tree.
#
# Source: Oireachtas Register of Members' Interests
# URL: https://www.oireachtas.ie/en/members/register-of-interests/
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.funders.register_of_interests_oireachtas — Oireachtas."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.funders._base import (
    FunderPipelineBase,
)

logger = structlog.get_logger(__name__)


OIREACHTAS_REGISTER_INTERESTS_URL = "https://www.oireachtas.ie/en/members/register-of-interests/"


class OireachtasRegisterOfInterestsPipeline(FunderPipelineBase):
    """Oireachtas Register of Members' Interests pipeline."""

    SOURCE_ID = "register_of_interests_oireachtas"
    SOURCE_NAME = "Oireachtas Register of Members' Interests"
    JURISDICTION = "roi_dail"
    SOURCE_BASE = OIREACHTAS_REGISTER_INTERESTS_URL
    SOURCE_TYPE = "register_of_interests"

    def _iter_funder_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Oireachtas Register of Interests cohort row."""
        yield self.funder_to_row()


@dlt.source(name="register_of_interests_oireachtas")
def register_of_interests_oireachtas_source() -> list:
    """DLT source for the Oireachtas Register of Members' Interests."""

    @dlt.resource(
        name="register_of_interests_oireachtas",
        write_disposition="merge",
        primary_key=["source_id", "funder_id"],
    )
    def register() -> Iterator[dict[str, Any]]:
        pipeline = OireachtasRegisterOfInterestsPipeline()
        yield from pipeline._iter_funder_records()

    return [register()]


__all__ = [
    "OIREACHTAS_REGISTER_INTERESTS_URL",
    "OireachtasRegisterOfInterestsPipeline",
    "register_of_interests_oireachtas_source",
]
