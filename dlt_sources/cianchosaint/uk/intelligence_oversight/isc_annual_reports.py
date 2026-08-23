# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIIP v1 Intelligence and Security Committee (ISC) annual reports.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest, Scenario: Intelligence Oversight sources).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Source URL: https://isc.independent.gov.uk/annual-reports (the ISC
# annual reports index). Falls within the cianchosaint OSINT allowlist.

"""cianchosaint.cianchosaint.dlt.british_isles.uk.intelligence_oversight.isc_annual_reports — ISC reports.

Source: `https://isc.independent.gov.uk/annual-reports` — the
Intelligence and Security Committee annual report index. The ISC is
the parliamentary committee that oversees the UK intelligence agencies
(MI5 / MI6 / GCHQ); publishes annual reports + inquiries into major
operational or legislative events.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/uk/intelligence_oversight/isc/`.
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


ISC_BASE = "https://isc.independent.gov.uk/annual-reports"
ISC_UK_GOV_BASE = "https://www.gov.uk/government/organisations/isc"


def _crawl_isc_annual_reports(max_pages: int) -> Iterator[dict[str, Any]]:
    """Crawl the ISC annual reports index + the gov.uk ISC corporate page."""
    for url in (ISC_BASE, ISC_UK_GOV_BASE):
        for page in _crawl_source(
            source_name=f"isc_annual_reports.{url.split('/')[-1] or 'index'}",
            base_url=url,
            include_paths=["/**"],
            max_pages=max_pages,
            max_depth=3,
        ):
            page["nation"] = "uk"
            page["domain"] = "intelligence_oversight"
            page["entity"] = "isc"
            page["entity_type"] = "annual_report"
            yield page


@dlt.source(name="isc_annual_reports")
def isc_annual_reports_source(max_pages: int = 50):
    """DLT source for ISC annual reports."""

    @dlt.resource(
        name="reports",
        write_disposition="merge",
        primary_key=["url"],
    )
    def reports():
        yield from _crawl_isc_annual_reports(max_pages=max_pages)

    return reports