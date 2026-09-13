# CIANCHOSAINT new-build: NI Courts Service DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The historical_associations/
# DLT source tree.
#
# Source: NI Courts Service (courtserve.net)
# URL: https://www.courtserve.net/
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.historical_associations.ni_courts_service — NI Courts Service."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.historical_associations._base import (
    HistoricalAssociationPipelineBase,
)

logger = structlog.get_logger(__name__)


NI_COURTS_SERVICE_URL = "https://www.courtserve.net/"


class NICourtsServicePipeline(HistoricalAssociationPipelineBase):
    """NI Courts Service pipeline."""

    SOURCE_ID = "ni_courts_service"
    SOURCE_NAME = "NI Courts Service (courtserve.net)"
    SOURCE_BASE = NI_COURTS_SERVICE_URL

    def _iter_historical_association_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical NI Courts Service cohort row."""
        yield self.historical_association_to_row()


@dlt.source(name="ni_courts_service")
def ni_courts_service_source() -> list:
    """DLT source for the NI Courts Service."""

    @dlt.resource(
        name="ni_courts_service",
        write_disposition="merge",
        primary_key=["source_id", "association_id"],
    )
    def courts() -> Iterator[dict[str, Any]]:
        pipeline = NICourtsServicePipeline()
        yield from pipeline._iter_historical_association_records()

    return [courts()]


__all__ = [
    "NICourtsServicePipeline",
    "NI_COURTS_SERVICE_URL",
    "ni_courts_service_source",
]
