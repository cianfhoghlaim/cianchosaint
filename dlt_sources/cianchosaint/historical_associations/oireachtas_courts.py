# CIANCHOSAINT new-build: Oireachtas Courts Service DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The historical_associations/
# DLT source tree.
#
# Source: Courts Service Ireland (courts.ie)
# URL: https://www.courts.ie/
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.historical_associations.oireachtas_courts — Oireachtas courts."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.historical_associations._base import (
    HistoricalAssociationPipelineBase,
)

logger = structlog.get_logger(__name__)


OIREACHTAS_COURTS_URL = "https://www.courts.ie/"


class OireachtasCourtsPipeline(HistoricalAssociationPipelineBase):
    """Oireachtas Courts Service (ROI) pipeline."""

    SOURCE_ID = "oireachtas_courts"
    SOURCE_NAME = "Courts Service Ireland (courts.ie)"
    SOURCE_BASE = OIREACHTAS_COURTS_URL

    def _iter_historical_association_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Oireachtas Courts cohort row."""
        yield self.historical_association_to_row()


@dlt.source(name="oireachtas_courts")
def oireachtas_courts_source() -> list:
    """DLT source for the Courts Service Ireland."""

    @dlt.resource(
        name="oireachtas_courts",
        write_disposition="merge",
        primary_key=["source_id", "association_id"],
    )
    def courts() -> Iterator[dict[str, Any]]:
        pipeline = OireachtasCourtsPipeline()
        yield from pipeline._iter_historical_association_records()

    return [courts()]


__all__ = [
    "OIREACHTAS_COURTS_URL",
    "OireachtasCourtsPipeline",
    "oireachtas_courts_source",
]
