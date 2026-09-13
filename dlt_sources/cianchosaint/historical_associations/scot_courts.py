# CIANCHOSAINT new-build: Scottish Courts and Tribunals DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The historical_associations/
# DLT source tree.
#
# Source: Scottish Courts and Tribunals (scotcourts.gov.uk)
# URL: https://www.scotcourts.gov.uk/
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.historical_associations.scot_courts — Scottish Courts."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.historical_associations._base import (
    HistoricalAssociationPipelineBase,
)

logger = structlog.get_logger(__name__)


SCOT_COURTS_URL = "https://www.scotcourts.gov.uk/"


class ScotCourtsPipeline(HistoricalAssociationPipelineBase):
    """Scottish Courts and Tribunals pipeline."""

    SOURCE_ID = "scot_courts"
    SOURCE_NAME = "Scottish Courts and Tribunals (scotcourts.gov.uk)"
    SOURCE_BASE = SCOT_COURTS_URL

    def _iter_historical_association_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Scottish Courts cohort row."""
        yield self.historical_association_to_row()


@dlt.source(name="scot_courts")
def scot_courts_source() -> list:
    """DLT source for the Scottish Courts and Tribunals Service."""

    @dlt.resource(
        name="scot_courts",
        write_disposition="merge",
        primary_key=["source_id", "association_id"],
    )
    def courts() -> Iterator[dict[str, Any]]:
        pipeline = ScotCourtsPipeline()
        yield from pipeline._iter_historical_association_records()

    return [courts()]


__all__ = [
    "SCOT_COURTS_URL",
    "ScotCourtsPipeline",
    "scot_courts_source",
]
