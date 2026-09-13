# CIANCHOSAINT new-build: Oireachtas (ROI) Committee advisors DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The advisors/ DLT
# source tree.
#
# Source: Oireachtas Committee on Finance advisors (the canonical committee
# that publishes the list of advisor engagements with TDs).
# URL: https://www.oireachtas.ie/en/committees/finance/
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.advisors.oireachtas_advisors — ROI Oireachtas advisors."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.advisors._base import (
    AdvisorPipelineBase,
)

logger = structlog.get_logger(__name__)


OIREACHTAS_FINANCE_URL = "https://www.oireachtas.ie/en/committees/finance/"


class OireachtasAdvisorsPipeline(AdvisorPipelineBase):
    """Oireachtas Committee on Finance advisors pipeline (ROI)."""

    SOURCE_ID = "oireachtas_advisors"
    SOURCE_NAME = "Oireachtas Committee on Finance Advisors"
    JURISDICTION = "roi_dail"
    SOURCE_BASE = OIREACHTAS_FINANCE_URL

    def _iter_advisor_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Oireachtas advisors cohort row."""
        yield self.advisor_to_row()


@dlt.source(name="oireachtas_advisors")
def oireachtas_advisors_source() -> list:
    """DLT source for the Oireachtas Committee on Finance advisors."""

    @dlt.resource(
        name="oireachtas_advisors",
        write_disposition="merge",
        primary_key=["source_id", "advisor_id"],
    )
    def advisors() -> Iterator[dict[str, Any]]:
        pipeline = OireachtasAdvisorsPipeline()
        yield from pipeline._iter_advisor_records()

    return [advisors()]


__all__ = [
    "OIREACHTAS_FINANCE_URL",
    "OireachtasAdvisorsPipeline",
    "oireachtas_advisors_source",
]
