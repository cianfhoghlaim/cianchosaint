# CIANCHOSAINT new-build: UK Companies House officer history DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The historical_associations/
# DLT source tree.
#
# Source: UK Companies House (officer history + PSC history)
# URL: https://find-and-update.company-information.service.gov.uk/
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.historical_associations.companies_house_officer_history — CH officer history."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.historical_associations._base import (
    HistoricalAssociationPipelineBase,
)

logger = structlog.get_logger(__name__)


COMPANIES_HOUSE_URL = "https://find-and-update.company-information.service.gov.uk/"


class CompaniesHouseOfficerHistoryPipeline(HistoricalAssociationPipelineBase):
    """UK Companies House officer history pipeline."""

    SOURCE_ID = "companies_house_officer_history"
    SOURCE_NAME = "UK Companies House Officer History"
    SOURCE_BASE = COMPANIES_HOUSE_URL

    def _iter_historical_association_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Companies House officer history cohort row."""
        yield self.historical_association_to_row()


@dlt.source(name="companies_house_officer_history")
def companies_house_officer_history_source() -> list:
    """DLT source for the UK Companies House officer history."""

    @dlt.resource(
        name="companies_house_officer_history",
        write_disposition="merge",
        primary_key=["source_id", "association_id"],
    )
    def officer_history() -> Iterator[dict[str, Any]]:
        pipeline = CompaniesHouseOfficerHistoryPipeline()
        yield from pipeline._iter_historical_association_records()

    return [officer_history()]


__all__ = [
    "COMPANIES_HOUSE_URL",
    "CompaniesHouseOfficerHistoryPipeline",
    "companies_house_officer_history_source",
]
