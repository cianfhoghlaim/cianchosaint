# CIANCHOSAINT new-build: Senedd / Welsh Parliament Register of Members' Interests DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The funders/ DLT
# source tree.
#
# Source: Senedd / Welsh Parliament Register of Members' Interests
# URL: https://senedd.wales/members/register-of-interests/
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.funders.register_of_interests_senedd — Senedd."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.funders._base import (
    FunderPipelineBase,
)

logger = structlog.get_logger(__name__)


SENEDD_REGISTER_INTERESTS_URL = "https://senedd.wales/members/register-of-interests/"


class SeneddRegisterOfInterestsPipeline(FunderPipelineBase):
    """Senedd / Welsh Parliament Register of Members' Interests pipeline."""

    SOURCE_ID = "register_of_interests_senedd"
    SOURCE_NAME = "Senedd / Welsh Parliament Register of Members' Interests"
    JURISDICTION = "senedd"
    SOURCE_BASE = SENEDD_REGISTER_INTERESTS_URL
    SOURCE_TYPE = "register_of_interests"

    def _iter_funder_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Senedd Register of Interests cohort row."""
        yield self.funder_to_row()


@dlt.source(name="register_of_interests_senedd")
def register_of_interests_senedd_source() -> list:
    """DLT source for the Senedd / Welsh Parliament Register of Members' Interests."""

    @dlt.resource(
        name="register_of_interests_senedd",
        write_disposition="merge",
        primary_key=["source_id", "funder_id"],
    )
    def register() -> Iterator[dict[str, Any]]:
        pipeline = SeneddRegisterOfInterestsPipeline()
        yield from pipeline._iter_funder_records()

    return [register()]


__all__ = [
    "SENEDD_REGISTER_INTERESTS_URL",
    "SeneddRegisterOfInterestsPipeline",
    "register_of_interests_senedd_source",
]
