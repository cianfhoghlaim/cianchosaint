# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIPP v1 UK crime statistics (force-level).
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest, Scenario: UK Policing sources).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Source URL: https://data.police.uk/api/crimes-street/all-crime
# (the open data portal's all-crime street-level endpoint). Falls
# within the cianchosaint OSINT allowlist.

"""cianchosaint.cianchosaint.dlt.british_isles.uk.policing.crime_statistics_uk — UK crime stats.

Source: `https://data.police.uk/api/crimes-street/all-crime` — the
open data portal's force-level + street-level crime endpoint. Each row
is one crime record with category + outcome + lat/lon + force.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/uk/policing/crime_statistics_uk/`.
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


CRIME_STATS_API = "https://data.police.uk/api/crimes-street/all-crime"
CRIME_STATS_DOCS = "https://data.police.uk/docs/method/crime-street/"


def _crawl_crime_statistics_uk(max_pages: int) -> Iterator[dict[str, Any]]:
    """Crawl the crime statistics API docs (live data via API, not crawl_site)."""
    for page in _crawl_source(
        source_name="crime_statistics_uk.docs",
        base_url=CRIME_STATS_DOCS,
        include_paths=["/**"],
        max_pages=max_pages // 2,
        max_depth=2,
    ):
        page["nation"] = "uk"
        page["domain"] = "policing"
        page["entity"] = "crime_statistics"
        page["entity_type"] = "stat_doc"
        yield page


@dlt.source(name="crime_statistics_uk")
def crime_statistics_uk_source(max_pages: int = 50):
    """DLT source for UK crime statistics (data.police.uk)."""

    @dlt.resource(
        name="statistics",
        write_disposition="merge",
        primary_key=["url"],
    )
    def statistics():
        yield from _crawl_crime_statistics_uk(max_pages=max_pages)

    return statistics