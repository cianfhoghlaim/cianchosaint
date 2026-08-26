// CIANCHOSAINT new-build: BAML extraction schema for the GCHQ stroom
// log extraction (per the openspec/changes/cianchosaint-hmgcc-gchq-
// tooling-v1/specs/cianchosaint-hmgcc-gchq-tooling/spec.md, stroom
// track).
//
// Per the openspec/changes/cianchosaint-baml-schemas-v1/spec.md,
// Requirement: The 7 per-vertical BAML extraction schemas.
//
// Provides 1 extraction function:
// - ExtractStroomLog (raw GCHQ stroom event → typed StroomLog with
//   event_type, source_id, timestamp, structured_data).
//
// All functions route through the 4-tier client chain
// (Primary → Fallback → Emergency → LastResort) declared in
// baml_src/clients.baml per the cianchosaint-bootstrap-v2 spec.
//
// Wholesale source: hmgcc/stroom/ (Apache 2.0). The
// `event_type` enum mirrors the bounded subset the cianchosaint
// pipeline routes through stroom (see
// `StroomLogPipeline.EVENT_TYPES` in
// dlt_sources/cianchosaint/uk/stroom/log_extraction.py).
//
// Licence: BUSL-1.1 (per LICENSE.md)
//
// The conservative-posture fields
// (`osint_ceiling_enforced: bool`, `licence_posture: string`,
// `analyst_review_required: bool`) are REQUIRED on every
// `StroomLog` record (per the cianchosaint-baml-schemas spec,
// Requirement: Conservative-posture guard on every extraction).

class StroomLog {
  event_id string
  event_type enum<PAGE_CHANGE, LLM_OBSERVABILITY_TRACE, BROWSER_NAVIGATION, HTTP_REQUEST, AUTH_ATTEMPT, AGENT_TOOL_CALL>
  source_id enum<craw4ai, langfuse, changedetection, unsloth_studio, litellm, cianchosaint_agent>
  timestamp string
  pipeline_id string
  structured_data string
  osint_ceiling_enforced bool
  licence_posture string
  analyst_review_required bool
}

function ExtractStroomLog(input: string) -> StroomLog {
  client Primary
  prompt #"
    {{ _.role("user") }}
    You are a GCHQ stroom event analyst working for the cianchosaint
    intelligence pipeline.

    Extract the structured fields from the following stroom event
    (post-XSL-transform). The raw log was routed through stroom's
    XSL pipeline + the structured event is what lands in the
    `stroom_structured_events` DLT resource.

    The `structured_data` field is a JSON string — capture the
    canonical post-transform fields (e.g. for PAGE_CHANGE: the url,
    previous_hash, current_hash, diff_summary).

    The `pipeline_id` is the cianchosaint XSL pipeline that ran on
    the raw log (e.g. "cianchosaint.craw4ai.page_change").

    {{ input }}
  "#
}
