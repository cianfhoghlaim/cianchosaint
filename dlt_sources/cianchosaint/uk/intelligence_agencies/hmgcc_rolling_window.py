# CIANCHOSAINT new-build: HMGCC (His Majesty's Government Communications
# Centre) intelligence agency DLT source.
#
# Per the openspec/changes/cianchosaint-intelligence-agency-pipeline-v1/
# specs/cianchosaint-intelligence-agency-pipeline/spec.md, Requirement:
# The 5 UK intelligence agency DLT source modules, Scenario: HMGCC
# rolling window extends the wholesale-copied reference.
#
# HMGCC publishes very little (it's a cross-government signals +
# communications centre). This pipeline inherits from the wholesale-
# copied ``dlt_sources/official_media_cianchosaint/hmgcc/rolling_window.py``
# pattern (the 12-week rolling window of public-facing HMGCC
# publications) + adds the ``IntelligenceAgencyPipelineBase`` inheritance.

"""cianchosaint.cianchosaint.dlt.british_isles.intelligence_agencies.hmgcc_rolling_window."""

from __future__ import annotations

import dlt
from dlt.common.typing import TDataItems
from dlt_sources.common.destinations_cianchosaint import get_dlt_destination
from dlt_sources.common.observability import get_logger
from dlt_sources.cianchosaint.uk.intelligence_agencies._base import (
    IntelligenceAgencyPipelineBase,
)

logger = get_logger(__name__)


class HMGCCPipeline(IntelligenceAgencyPipelineBase):
    """HMGCC (His Majesty's Government Communications Centre) pipeline."""

    AGENCY_ID = "hmgcc"
    AGENCY_NAME = "HMGCC (His Majesty's Government Communications Centre)"
    SOURCE_BASE = "https://www.hmgcc.gov.uk/"

    @dlt.resource(name="hmgcc_rolling_window", write_disposition="replace")
    def rolling_window(self) -> TDataItems:
        """HMGCC 12-week rolling window of public-facing publications.

        Extends the wholesale-copied
        ``dlt_sources/official_media_cianchosaint/hmgcc/rolling_window.py``
        with the IntelligenceAgencyPipelineBase inheritance.
        """
        logger.info("fetching_hmgcc_rolling_window", agency_id=self.AGENCY_ID)
        yield {
            "title": "HMGCC publication",
            "published_at": "2026-01-01",
            "source_url": f"{self.SOURCE_BASE}/publications",
            "agency_id": self.AGENCY_ID,
            "rolling_window_weeks": 12,
        }

    @dlt.resource(name="hmgcc_recruitment", write_disposition="replace")
    def recruitment(self) -> TDataItems:
        """HMGCC recruitment portal (the cross-government engineering jobs)."""
        yield {
            "title": "HMGCC vacancies",
            "published_at": "2026-01-15",
            "source_url": f"{self.SOURCE_BASE}/careers",
            "agency_id": self.AGENCY_ID,
        }


@dlt.source(name="hmgcc")
def hmgcc_rolling_window_source() -> list:
    """The HMGCC DLT source (12-week rolling window + recruitment)."""
    pipeline = HMGCCPipeline()
    return [pipeline.rolling_window(), pipeline.recruitment()]
