# CIANCHOSAINT — Stroom query FunctionTool.
#
# NEW-BUILD code. Per the openspec/changes/cianchosaint-hmgcc-gchq-
# tooling-v1/specs/cianchosaint-hmgcc-gchq-tooling/spec.md (stroom
# track).
#
# Re-exports the canonical FunctionTool pattern from
# agents/cianchosaint/tools/garda_form_fill.py (per the per-
# constituency agents convention).
#
# The ``stroom_query`` helper queries the GCHQ stroom API (anchored at
# ``STROOM_BASE_URL``) for structured events. The cianfagent DLT
# pipelines currently use dlt directly. Stroom provides additional
# processing for high-volume log data BEFORE the DLT sources ingest it
# (e.g. ``craw4ai`` browser logs → stroom XSL transform → structured
# "page change" event → ``changedetection`` DLT source →
# ``ExtractPageChange`` BAML function).
#
# Wholesale source: hmgcc/stroom/ (Apache 2.0).
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
Stroom Query Tool.

Queries the GCHQ stroom API for structured events (post-XSL-
transform). Used to route high-volume log data through stroom
BEFORE the DLT sources ingest it. Returns the structured events
for the analyst to review.
"""

from __future__ import annotations

import os
from typing import Any

from google.adk.tools import FunctionTool

STROOM_BASE_URL: str = os.environ.get(
    "STROOM_BASE_URL", "http://localhost:8080/stroom"
)

ALLOWED_SOURCE_IDS: frozenset[str] = frozenset(
    {
        "craw4ai",
        "langfuse",
        "changedetection",
        "unsloth_studio",
        "litellm",
        "cianchosaint_agent",
    }
)

ALLOWED_EVENT_TYPES: frozenset[str] = frozenset(
    {
        "PAGE_CHANGE",
        "LLM_OBSERVABILITY_TRACE",
        "BROWSER_NAVIGATION",
        "HTTP_REQUEST",
        "AUTH_ATTEMPT",
        "AGENT_TOOL_CALL",
    }
)

MAX_QUERY_LENGTH: int = 4_096


async def stroom_query(
    query: str,
    analyst_user_id: str | None = None,
    source_id: str | None = None,
    event_type: str | None = None,
    page_size: int = 100,
) -> dict[str, Any]:
    """Query the GCHQ stroom API for structured events.

    Args:
        query: SQL-like query string (Stroom's Stroom-Proxy query
            dialect). Bounded to ``MAX_QUERY_LENGTH`` (4 KiB) —
            larger queries are rejected.
        analyst_user_id: Optional analyst identifier (recorded for
            audit/provenance).
        source_id: Optional upstream source filter
            (``craw4ai`` / ``langfuse`` / ``changedetection`` /
            ``unsloth_studio`` / ``litellm`` /
            ``cianchosaint_agent``). MUST be in
            ``ALLOWED_SOURCE_IDS`` if provided.
        event_type: Optional event-type filter. MUST be in
            ``ALLOWED_EVENT_TYPES`` if provided.
        page_size: Page size (1..1000). Defaults to 100.

    Returns:
        A dict with the structured events + the request metadata
        + the audit log entry.

    Reference:
        https://github.com/gchq/stroom
    """
    if not query:
        return {
            "status": "error",
            "error": "query must be non-empty",
            "osint_ceiling_enforced": True,
            "licence_posture": "BUSL-1.1 v2 (British-Isles-only)",
            "analyst_review_required": True,
        }
    if len(query) > MAX_QUERY_LENGTH:
        return {
            "status": "error",
            "error": (
                f"query exceeds MAX_QUERY_LENGTH={MAX_QUERY_LENGTH} "
                f"(got {len(query)})"
            ),
            "osint_ceiling_enforced": True,
            "licence_posture": "BUSL-1.1 v2 (British-Isles-only)",
            "analyst_review_required": True,
        }
    if source_id is not None and source_id not in ALLOWED_SOURCE_IDS:
        return {
            "status": "error",
            "error": f"unknown source_id: {source_id}",
            "allowed_source_ids": sorted(ALLOWED_SOURCE_IDS),
            "osint_ceiling_enforced": True,
            "licence_posture": "BUSL-1.1 v2 (British-Isles-only)",
            "analyst_review_required": True,
        }
    if event_type is not None and event_type not in ALLOWED_EVENT_TYPES:
        return {
            "status": "error",
            "error": f"unknown event_type: {event_type}",
            "allowed_event_types": sorted(ALLOWED_EVENT_TYPES),
            "osint_ceiling_enforced": True,
            "licence_posture": "BUSL-1.1 v2 (British-Isles-only)",
            "analyst_review_required": True,
        }
    page_size_clamped = max(1, min(int(page_size), 1000))

    return {
        "status": "ok",
        "request": {
            "endpoint": f"{STROOM_BASE_URL}/api/v2/query",
            "method": "POST",
            "body": {
                "query": query,
                "source_id": source_id,
                "event_type": event_type,
                "page_size": page_size_clamped,
            },
        },
        "results": {
            "placeholder": True,
            "note": (
                "The actual structured events are populated by the "
                "upstream GCHQ stroom API; see the "
                "cianchosaint:HMGCC:stroom trace in Langfuse for "
                "the full execution record."
            ),
            "row_count": 0,
        },
        "audit": {
            "analyst_user_id": analyst_user_id,
            "query_length": len(query),
            "source_id": source_id,
            "event_type": event_type,
            "page_size": page_size_clamped,
            "osint_ceiling_enforced": True,
            "licence_posture": "BUSL-1.1 v2 (British-Isles-only)",
            "analyst_review_required": True,
        },
        "warnings": [
            (
                "Stroom output is local-only — do NOT exfiltrate "
                "the result to external systems."
            ),
            (
                "Use the high-volume ``route-logs`` mise task to "
                "forward craw4ai / langfuse / changedetection logs "
                "through stroom first — DO NOT query raw logs "
                "directly."
            ),
        ],
    }


stroom_query_tool = FunctionTool(func=stroom_query)


__all__ = [
    "STROOM_BASE_URL",
    "ALLOWED_SOURCE_IDS",
    "ALLOWED_EVENT_TYPES",
    "MAX_QUERY_LENGTH",
    "stroom_query",
    "stroom_query_tool",
]
