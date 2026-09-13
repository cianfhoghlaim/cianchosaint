# CIANCHOSAINT new-build: UK Insolvency Service DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The historical_associations/
# DLT source tree.
#
# Source: UK Insolvency Service determinations
# URL: https://www.gov.uk/government/organisations/insolvency-service
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.historical_associations.insolvency_service — UK Insolvency Service."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.historical_associations._base import (
    HistoricalAssociationPipelineBase,
)

logger = structlog.get_logger(__name__)


INSOLVENCY_SERVICE_URL = "https://www.gov.uk/government/organisations/insolvency-service"


class InsolvencyServicePipeline(HistoricalAssociationPipelineBase):
    """UK Insolvency Service pipeline."""

    SOURCE_ID = "insolvency_service"
    SOURCE_NAME = "UK Insolvency Service Determinations"
    SOURCE_BASE = INSOLVENCY_SERVICE_URL

    def _iter_historical_association_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Insolvency Service cohort row."""
        yield self.historical_association_to_row()


@dlt.source(name="insolvency_service")
def insolvency_service_source() -> list:
    """DLT source for the UK Insolvency Service."""

    @dlt.resource(
        name="insolvency_service",
        write_disposition="merge",
        primary_key=["source_id", "association_id"],
    )
    def insolvency() -> Iterator[dict[str, Any]]:
        pipeline = InsolvencyServicePipeline()
        yield from pipeline._iter_historical_association_records()

    return [insolvency()]


__all__ = [
    "INSOLVENCY_SERVICE_URL",
    "InsolvencyServicePipeline",
    "insolvency_service_source",
]
