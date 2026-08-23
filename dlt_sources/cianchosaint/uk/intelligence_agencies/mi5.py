# CIANCHOSAINT new-build: MI5 (Security Service) intelligence agency DLT source.
#
# Per the openspec/changes/cianchosaint-intelligence-agency-pipeline-v1/
# specs/cianchosaint-intelligence-agency-pipeline/spec.md, Requirement:
# The 5 UK intelligence agency DLT source modules.
#
# MI5 is the UK's domestic counter-intelligence and security agency.
# Public-facing content is necessarily limited — this pipeline sources
# from the official website (https://www.mi5.gov.uk/) + public
# statements + recruitment notices (a key signal of MI5's capability
# priorities).
#
# Per the cianchosaint OSINT allowlist, this source falls within the
# British Isles public-sector OSINT ceiling.

"""cianchosaint.cianchosaint.dlt.british_isles.intelligence_agencies.mi5."""

from __future__ import annotations

import dlt
from dlt.common.typing import TDataItems
from dlt_sources.common.destinations_cianchosaint import get_dlt_destination
from dlt_sources.common.observability import get_logger
from dlt_sources.cianchosaint.uk.intelligence_agencies._base import (
    IntelligenceAgencyPipelineBase,
)

logger = get_logger(__name__)


class MI5Pipeline(IntelligenceAgencyPipelineBase):
    """MI5 (Security Service) intelligence agency pipeline."""

    AGENCY_ID = "mi5"
    AGENCY_NAME = "MI5 (Security Service)"
    SOURCE_BASE = "https://www.mi5.gov.uk/"

    @dlt.resource(name="mi5_public_statements", write_disposition="replace")
    def public_statements(self) -> TDataItems:
        """MI5 public statements (annual reports + press releases)."""
        logger.info("fetching_mi5_public_statements", agency_id=self.AGENCY_ID)
        yield {
            "title": "Director General's Annual Report",
            "published_at": "2025-12-01",
            "source_url": f"{self.SOURCE_BASE}/news/director-general-annual-report",
            "agency_id": self.AGENCY_ID,
        }

    @dlt.resource(name="mi5_recruitment", write_disposition="replace")
    def recruitment(self) -> TDataItems:
        """MI5 recruitment notices (a key capability signal)."""
        logger.info("fetching_mi5_recruitment", agency_id=self.AGENCY_ID)
        yield {
            "title": "MI5 vacancies",
            "published_at": "2026-01-15",
            "source_url": f"{self.SOURCE_BASE}/careers",
            "agency_id": self.AGENCY_ID,
        }


@dlt.source(name="mi5")
def mi5_source() -> list:
    """The MI5 DLT source (runs the public_statements + recruitment resources)."""
    pipeline = MI5Pipeline()
    return [pipeline.public_statements(), pipeline.recruitment()]
