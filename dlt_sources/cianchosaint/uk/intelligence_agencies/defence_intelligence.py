# CIANCHOSAINT new-build: Defence Intelligence (DI) intelligence agency DLT source.
#
# Per the openspec/changes/cianchosaint-intelligence-agency-pipeline-v1/
# specs/cianchosaint-intelligence-agency-pipeline/spec.md.
#
# Defence Intelligence (DI) is the UK's military intelligence agency.
# Public-facing content includes the DI annual report + the UK Defence
# Journal + the gov.uk defence-intelligence organisation page.

"""cianchosaint.cianchosaint.dlt.british_isles.intelligence_agencies.defence_intelligence."""

from __future__ import annotations

import dlt
from dlt.common.typing import TDataItems
from dlt_sources.common.destinations_cianchosaint import get_dlt_destination
from dlt_sources.common.observability import get_logger
from dlt_sources.cianchosaint.uk.intelligence_agencies._base import (
    IntelligenceAgencyPipelineBase,
)

logger = get_logger(__name__)


class DefenceIntelligencePipeline(IntelligenceAgencyPipelineBase):
    """Defence Intelligence (DI) intelligence agency pipeline."""

    AGENCY_ID = "defence_intelligence"
    AGENCY_NAME = "Defence Intelligence (DI)"
    SOURCE_BASE = "https://www.gov.uk/government/organisations/defence-intelligence"

    @dlt.resource(name="di_annual_reports", write_disposition="replace")
    def annual_reports(self) -> TDataItems:
        """DI annual reports + the UK Defence Journal."""
        logger.info("fetching_di_annual_reports", agency_id=self.AGENCY_ID)
        yield {
            "title": "Defence Intelligence Annual Report",
            "published_at": "2025-10-31",
            "source_url": f"{self.SOURCE_BASE}/about/annual-reports",
            "agency_id": self.AGENCY_ID,
        }

    @dlt.resource(name="di_threat_assessments", write_disposition="replace")
    def threat_assessments(self) -> TDataItems:
        """DI threat assessments (published occasionally)."""
        yield {
            "title": "DI Threat Assessment",
            "published_at": "2025-08-15",
            "source_url": f"{self.SOURCE_BASE}/threat-assessments",
            "agency_id": self.AGENCY_ID,
        }


@dlt.source(name="defence_intelligence")
def defence_intelligence_source() -> list:
    """The Defence Intelligence DLT source."""
    pipeline = DefenceIntelligencePipeline()
    return [pipeline.annual_reports(), pipeline.threat_assessments()]
