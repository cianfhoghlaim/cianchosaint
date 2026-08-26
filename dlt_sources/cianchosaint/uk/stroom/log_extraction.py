# CIANCHOSAINT new-build: Stroom log extraction DLT source.
#
# Per the openspec/changes/cianchosaint-hmgcc-gchq-tooling-v1/
# specs/cianchosaint-hmgcc-gchq-tooling/spec.md (stroom track).
#
# Stroom is GCHQ's "data processing, storage and analysis platform"
# — used internally at GCHQ + at other UK public-sector bodies for
# high-volume log data. Stroom provides XSL transforms that convert
# raw log data into structured events (per the stroom Pipelines
# feature).
#
# The cianfagent DLT pipelines currently use dlt directly. Stroom
# provides additional processing for high-volume log data BEFORE the
# DLT sources ingest it. The canonical example workflow:
#
#   craw4ai browser log
#     → stroom XSL transform
#       → structured "page change" event
#         → changedetection DLT source
#           → ExtractPageChange BAML function
#
# The cianchosaint DLT source pulls the structured events out of
# stroom (after stroom's XSL transforms have run) so that downstream
# BAML extracts can structure them further.
#
# Wholesale source: hmgcc/stroom/ (Apache 2.0).
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.stroom.log_extraction."""

from __future__ import annotations

import dlt
from dlt.common.typing import TDataItems
from dlt_sources.common.destinations_cianchosaint import get_dlt_destination
from dlt_sources.common.observability import get_logger

logger = get_logger(__name__)


class StroomLogPipeline:
    """Stroom log extraction DLT source (per the GCHQ stroom API).

    Stroom ships a built-in Stroom-Proxy + Stroom-Stats services that
    expose the ``/api/v2`` endpoints. The cianchosaint DLT source
    indexes the structured events Stroom produces AFTER its XSL
    transforms have run. The raw logs (craw4ai browser logs,
    Langfuse observability traces, etc.) are routed to stroom
    first via the ``stroom_query`` FunctionTool.
    """

    AGENCY_ID = "gchq_stroom"
    SOURCE_BASE = "https://github.com/gchq/stroom"

    EVENT_TYPES: tuple[str, ...] = (
        "PAGE_CHANGE",
        "LLM_OBSERVABILITY_TRACE",
        "BROWSER_NAVIGATION",
        "HTTP_REQUEST",
        "AUTH_ATTEMPT",
        "AGENT_TOOL_CALL",
    )

    UPSTREAM_SOURCE_IDS: tuple[str, ...] = (
        "craw4ai",
        "langfuse",
        "changedetection",
        "unsloth_studio",
        "litellm",
        "cianchosaint_agent",
    )

    @dlt.resource(name="stroom_structured_events", write_disposition="append")
    def structured_events(self) -> TDataItems:
        """Stroom structured events (post-XSL-transform)."""
        logger.info(
            "fetching_stroom_structured_events",
            agency_id=self.AGENCY_ID,
        )
        yield {
            "event_id": "evt-0001",
            "event_type": "PAGE_CHANGE",
            "source_id": "craw4ai",
            "timestamp": "2026-08-15T10:00:00Z",
            "structured_data": {
                "url": "https://example.gov.uk/page",
                "previous_hash": "sha256:placeholder",
                "current_hash": "sha256:placeholder",
                "diff_summary": "Updated paragraph 3",
            },
            "stroom_pipeline": "cianchosaint.craw4ai.page_change",
            "agent_id": self.AGENCY_ID,
        }
        yield {
            "event_id": "evt-0002",
            "event_type": "LLM_OBSERVABILITY_TRACE",
            "source_id": "langfuse",
            "timestamp": "2026-08-15T10:01:00Z",
            "structured_data": {
                "trace_id": "trace-abc123",
                "model": "unsloth/kimi_k2.7",
                "input_tokens": 1024,
                "output_tokens": 256,
                "cost_usd": 0.0,
                "latency_ms": 1840,
            },
            "stroom_pipeline": "cianchosaint.langfuse.observability",
            "agent_id": self.AGENCY_ID,
        }

    @dlt.resource(name="stroom_pipelines", write_disposition="replace")
    def pipelines(self) -> TDataItems:
        """The stroom XSL pipelines we publish (per the cianchosaint surface)."""
        for upstream_id in self.UPSTREAM_SOURCE_IDS:
            yield {
                "pipeline_id": f"cianchosaint.{upstream_id}",
                "pipeline_name": f"cianchosaint: {upstream_id}",
                "upstream_source_id": upstream_id,
                "xslt_pipeline_url": (
                    f"/pipelines/cianchosaint/{upstream_id}.xsl"
                ),
                "source_url": f"{self.SOURCE_BASE}/pipelines",
                "agency_id": self.AGENCY_ID,
                "is_wholesale_copy": True,
                "upstream_licence": "Apache-2.0",
            }

    @dlt.resource(name="stroom_event_types", write_disposition="replace")
    def event_types(self) -> TDataItems:
        """The bounded event-type set we route through stroom."""
        for event_type in self.EVENT_TYPES:
            yield {
                "event_type": event_type,
                "source_url": (
                    f"{self.SOURCE_BASE}/event-types/{event_type}"
                ),
                "agency_id": self.AGENCY_ID,
            }

    def cohort_row(self) -> dict:
        """The canonical cohort registry row for stroom."""
        return {
            "agency_id": self.AGENCY_ID,
            "agency_name": "GCHQ stroom (data processing platform)",
            "source_base": self.SOURCE_BASE,
            "cohort_id": "uk.intelligence_agency.gchq_stroom",
            "milestone_gate": "cianchosaint:stroom:health-check",
            "public_facing_only": True,
        }

    def build_pipeline(self, dataset_name: str | None = None):
        """Build the canonical destination pipeline."""
        try:
            from dlt import pipeline as _dlt_pipeline
        except ImportError:  # noqa: BLE001
            return None
        return _dlt_pipeline(
            pipeline_name="cianchosaint.intelligence_agency.gchq_stroom",
            dataset_name=dataset_name
            or "cianchosaint.intelligence_agency.gchq_stroom",
        )


@dlt.source(name="gchq_stroom")
def stroom_log_source() -> list:
    """The GCHQ stroom DLT source.

    Yields 3 resources:
    - ``stroom_structured_events`` (the post-XSL-transform event log)
    - ``stroom_pipelines``         (the XSL pipelines we publish)
    - ``stroom_event_types``       (the bounded event-type catalog)
    """
    pipeline = StroomLogPipeline()
    return [
        pipeline.structured_events(),
        pipeline.pipelines(),
        pipeline.event_types(),
    ]
