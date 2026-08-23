# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIIP v1 Investigatory Powers Tribunal (IPT) decisions.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest, Scenario: Intelligence Oversight sources).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Source URL: https://www.investigatorypowerstribunal.org.uk/decisions
# (the IPT published-decisions index). Falls within the cianchosaint
# OSINT allowlist.

"""cianchosaint.cianchosaint.dlt.british_isles.uk.intelligence_oversight.ipt_decisions — IPT.

Source: `https://www.investigatorypowerstribunal.org.uk/decisions` —
the Investigatory Powers Tribunal published-decisions index. The IPT
is the standalone tribunal that hears complaints against the UK
intelligence agencies + the police + other public authorities for
misuse of investigatory powers; publishes selected decisions.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/uk/intelligence_oversight/ipt/`.
"""
from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt

import structlog

import dlt_sources

from dlt_sources.common.site_crawler import crawl_site

logger = structlog.get_logger(__name__)


def _crawl_source(*args, **kwargs):
    # The legacy _crawl_source took (source_name, base_url, ...) — source_name
    # was used only for logging in the legacy helper. The new crawl_site
    # primitive has no source_name, so we drop it if present.
    if args and isinstance(args[0], str) and args[0] == kwargs.get("source_name"):
        args = args[1:]
    kwargs.pop("source_name", None)
    for page in crawl_site(*args, **kwargs):
        yield page.to_dict()


IPT_BASE = "https://www.investigatorypowerstribunal.org.uk/decisions"


def _crawl_ipt_decisions(max_pages: int) -> Iterator[dict[str, Any]]:
    """Crawl the IPT published decisions index."""
    for page in _crawl_source(
        source_name="ipt_decisions.decisions",
        base_url=IPT_BASE,
        include_paths=["/**"],
        max_pages=max_pages,
        max_depth=3,
    ):
        page["nation"] = "uk"
        page["domain"] = "intelligence_oversight"
        page["entity"] = "ipt"
        page["entity_type"] = "decision"
        yield page


@dlt.source(name="ipt_decisions")
def ipt_decisions_source(max_pages: int = 50):
    """DLT source for IPT decisions."""

    @dlt.resource(
        name="decisions",
        write_disposition="merge",
        primary_key=["url"],
    )
    def decisions():
        yield from _crawl_ipt_decisions(max_pages=max_pages)

    return decisions