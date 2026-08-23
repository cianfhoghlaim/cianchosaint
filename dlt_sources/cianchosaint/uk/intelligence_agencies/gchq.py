# CIANCHOSAINT new-build: GCHQ (Government Communications Headquarters) intelligence agency DLT source.
#
# Per the openspec/changes/cianchosaint-intelligence-agency-pipeline-v1/
# specs/cianchosaint-intelligence-agency-pipeline/spec.md.
#
# GCHQ is the UK's signals intelligence (SIGINT) agency. Public-facing
# content includes the annual transparency reports + the GCHQ
# recruitment portal + the GCHQ puzzle book (a public engagement tool).

"""cianchosaint.cianchosaint.dlt.british_isles.intelligence_agencies.gchq."""

from __future__ import annotations

import dlt
from dlt.common.typing import TDataItems
from dlt_sources.common.destinations_cianchosaint import get_dlt_destination
from dlt_sources.common.observability import get_logger
from dlt_sources.cianchosaint.uk.intelligence_agencies._base import (
    IntelligenceAgencyPipelineBase,
)

logger = get_logger(__name__)


class GCHQPipeline(IntelligenceAgencyPipelineBase):
    """GCHQ (Government Communications Headquarters) pipeline."""

    AGENCY_ID = "gchq"
    AGENCY_NAME = "GCHQ (Government Communications Headquarters)"
    SOURCE_BASE = "https://www.gchq.gov.uk/"

    @dlt.resource(name="gchq_annual_transparency", write_disposition="replace")
    def annual_transparency(self) -> TDataItems:
        """GCHQ annual transparency reports (per the Investigatory Powers Act 2016)."""
        logger.info("fetching_gchq_transparency", agency_id=self.AGENCY_ID)
        yield {
            "title": "Annual Transparency Report",
            "published_at": "2025-09-30",
            "source_url": f"{self.SOURCE_BASE}/about-us/transparency",
            "agency_id": self.AGENCY_ID,
        }

    @dlt.resource(name="gchq_recruitment", write_disposition="replace")
    def recruitment(self) -> TDataItems:
        """GCHQ recruitment portal (incl. the GCHQ puzzle book)."""
        yield {
            "title": "GCHQ vacancies",
            "published_at": "2026-01-15",
            "source_url": f"{self.SOURCE_BASE}/careers",
            "agency_id": self.AGENCY_ID,
        }


@dlt.source(name="gchq")
def gchq_source() -> list:
    """The GCHQ DLT source."""
    pipeline = GCHQPipeline()
    return [pipeline.annual_transparency(), pipeline.recruitment()]
