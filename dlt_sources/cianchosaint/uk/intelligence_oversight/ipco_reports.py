# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIIP v1 Investigatory Powers Commissioner's Office (IPCO) reports.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest, Scenario: Intelligence Oversight sources).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Source URL: https://www.ipco.org.uk/reports (the IPCO report index).
# Falls within the cianchosaint OSINT allowlist.

"""cianchosaint.cianchosaint.dlt.british_isles.uk.intelligence_oversight.ipco_reports — IPCO.

Source: `https://www.ipco.org.uk/reports` — the Investigatory Powers
Commissioner's Office report index. The IPCO is the independent
judicial oversight body for the use of investigatory powers by UK
public authorities; publishes annual reports + thematic reviews.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/uk/intelligence_oversight/ipco/`.
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


IPCO_BASE = "https://www.ipco.org.uk/reports"


def _crawl_ipco_reports(max_pages: int) -> Iterator[dict[str, Any]]:
    """Crawl the IPCO reports index."""
    for page in _crawl_source(
        source_name="ipco_reports.reports",
        base_url=IPCO_BASE,
        include_paths=["/**"],
        max_pages=max_pages,
        max_depth=3,
    ):
        page["nation"] = "uk"
        page["domain"] = "intelligence_oversight"
        page["entity"] = "ipco"
        page["entity_type"] = "report"
        yield page


@dlt.source(name="ipco_reports")
def ipco_reports_source(max_pages: int = 50):
    """DLT source for IPCO reports."""

    @dlt.resource(
        name="reports",
        write_disposition="merge",
        primary_key=["url"],
    )
    def reports():
        yield from _crawl_ipco_reports(max_pages=max_pages)

    return reports