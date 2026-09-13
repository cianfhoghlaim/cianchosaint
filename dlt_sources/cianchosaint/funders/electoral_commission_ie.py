# CIANCHOSAINT new-build: Irish Electoral Commission register DLT source.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The funders/ DLT
# source tree.
#
# Source: Irish Electoral Commission register (under the Electoral Reform Act 2022)
# URL: https://www.electoralcommission.ie/
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.funders.electoral_commission_ie — Irish Electoral Commission."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.funders._base import (
    FunderPipelineBase,
)

logger = structlog.get_logger(__name__)


IE_ELECTORAL_COMMISSION_URL = "https://www.electoralcommission.ie/"


class IEElectoralCommissionPipeline(FunderPipelineBase):
    """Irish Electoral Commission register pipeline."""

    SOURCE_ID = "electoral_commission_ie"
    SOURCE_NAME = "Irish Electoral Commission Register (Electoral Reform Act 2022)"
    JURISDICTION = "roi_dail"
    SOURCE_BASE = IE_ELECTORAL_COMMISSION_URL
    SOURCE_TYPE = "electoral_commission"

    def _iter_funder_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Irish Electoral Commission cohort row."""
        yield self.funder_to_row()


@dlt.source(name="electoral_commission_ie")
def electoral_commission_ie_source() -> list:
    """DLT source for the Irish Electoral Commission register."""

    @dlt.resource(
        name="electoral_commission_ie",
        write_disposition="merge",
        primary_key=["source_id", "funder_id"],
    )
    def register() -> Iterator[dict[str, Any]]:
        pipeline = IEElectoralCommissionPipeline()
        yield from pipeline._iter_funder_records()

    return [register()]


__all__ = [
    "IEElectoralCommissionPipeline",
    "IE_ELECTORAL_COMMISSION_URL",
    "electoral_commission_ie_source",
]
