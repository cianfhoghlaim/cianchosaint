# CIANCHOSAINT new-build: UK Companies House Persons of Significant Control DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The funders/ DLT
# source tree.
#
# Source: UK Companies House Persons of Significant Control register
# URL: https://find-and-update.company-information.service.gov.uk/
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.funders.companies_house_psc — UK Companies House PSC."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.funders._base import (
    FunderPipelineBase,
)

logger = structlog.get_logger(__name__)


COMPANIES_HOUSE_PSC_URL = "https://find-and-update.company-information.service.gov.uk/"


class CompaniesHousePSCPipeline(FunderPipelineBase):
    """UK Companies House Persons of Significant Control pipeline."""

    SOURCE_ID = "companies_house_psc"
    SOURCE_NAME = "UK Companies House Persons of Significant Control"
    JURISDICTION = "uk_hoc"
    SOURCE_BASE = COMPANIES_HOUSE_PSC_URL
    SOURCE_TYPE = "companies_house"

    def _iter_funder_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Companies House PSC cohort row."""
        yield self.funder_to_row()


@dlt.source(name="companies_house_psc")
def companies_house_psc_source() -> list:
    """DLT source for the UK Companies House Persons of Significant Control register."""

    @dlt.resource(
        name="companies_house_psc",
        write_disposition="merge",
        primary_key=["source_id", "funder_id"],
    )
    def psc() -> Iterator[dict[str, Any]]:
        pipeline = CompaniesHousePSCPipeline()
        yield from pipeline._iter_funder_records()

    return [psc()]


__all__ = [
    "COMPANIES_HOUSE_PSC_URL",
    "CompaniesHousePSCPipeline",
    "companies_house_psc_source",
]
