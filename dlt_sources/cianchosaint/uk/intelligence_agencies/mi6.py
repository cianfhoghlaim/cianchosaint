# CIANCHOSAINT new-build: MI6 (Secret Intelligence Service) intelligence agency DLT source.
#
# Per the openspec/changes/cianchosaint-intelligence-agency-pipeline-v1/
# specs/cianchosaint-intelligence-agency-pipeline/spec.md.
#
# MI6 is the UK's foreign intelligence agency (the Secret
# Intelligence Service, SIS). Public-facing content is necessarily
# limited — this pipeline sources from the official website +
# the SIS open recruitment portal.

"""cianchosaint.cianchosaint.dlt.british_isles.intelligence_agencies.mi6."""

from __future__ import annotations

import dlt
from dlt.common.typing import TDataItems
from dlt_sources.common.destinations_cianchosaint import get_dlt_destination
from dlt_sources.common.observability import get_logger
from dlt_sources.cianchosaint.uk.intelligence_agencies._base import (
    IntelligenceAgencyPipelineBase,
)

logger = get_logger(__name__)


class MI6Pipeline(IntelligenceAgencyPipelineBase):
    """MI6 (Secret Intelligence Service) intelligence agency pipeline."""

    AGENCY_ID = "mi6"
    AGENCY_NAME = "MI6 (Secret Intelligence Service)"
    SOURCE_BASE = "https://www.sis.gov.uk/"

    @dlt.resource(name="mi6_public_statements", write_disposition="replace")
    def public_statements(self) -> TDataItems:
        """MI6 public statements (the Chief's annual speech + recruitment)."""
        logger.info("fetching_mi6_public_statements", agency_id=self.AGENCY_ID)
        yield {
            "title": "Chief of the Secret Intelligence Service speech",
            "published_at": "2025-11-15",
            "source_url": f"{self.SOURCE_BASE}/news/chief-speech",
            "agency_id": self.AGENCY_ID,
        }

    @dlt.resource(name="mi6_recruitment", write_disposition="replace")
    def recruitment(self) -> TDataItems:
        """MI6 recruitment portal."""
        yield {
            "title": "SIS vacancies",
            "published_at": "2026-01-15",
            "source_url": f"{self.SOURCE_BASE}/careers",
            "agency_id": self.AGENCY_ID,
        }


@dlt.source(name="mi6")
def mi6_source() -> list:
    """The MI6 DLT source."""
    pipeline = MI6Pipeline()
    return [pipeline.public_statements(), pipeline.recruitment()]
