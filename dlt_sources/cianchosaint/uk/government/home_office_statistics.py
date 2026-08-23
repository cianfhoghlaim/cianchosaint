# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIIP v1 Home Office statistics bulletins.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest, Scenario: UK Government sources).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Source URL: https://www.gov.uk/government/statistics (the UK
# government statistics hub filtered by the Home Office). Falls
# within the cianchosaint OSINT allowlist.

"""cianchosaint.cianchosaint.dlt.british_isles.uk.government.home_office_statistics — HO stats.

Source: `https://www.gov.uk/government/statistics?departments%5B%5D=
home-office` — the UK Home Office statistics bulletins index on
gov.uk. The Home Office is the lead UK government department for
immigration + policing + counter-terrorism + drugs policy; publishes
quarterly + annual statistical bulletins for each.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/uk/government/home_office/`.
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


HOME_OFFICE_STATS_BASE = (
    "https://www.gov.uk/government/statistics"
    "?departments%5B%5D=home-office"
)
HOME_OFFICE_BASE = "https://www.gov.uk/government/organisations/home-office"


def _crawl_home_office_statistics(max_pages: int) -> Iterator[dict[str, Any]]:
    """Crawl the Home Office statistics bulletins + the corporate publications."""
    for url in (HOME_OFFICE_STATS_BASE, HOME_OFFICE_BASE):
        for page in _crawl_source(
            source_name=f"home_office_statistics.{url.split('/')[-1] or 'index'}",
            base_url=url,
            include_paths=["/**"],
            max_pages=max_pages,
            max_depth=3,
        ):
            page["nation"] = "uk"
            page["domain"] = "government"
            page["entity"] = "home_office"
            page["entity_type"] = "statistic"
            yield page


@dlt.source(name="home_office_statistics")
def home_office_statistics_source(max_pages: int = 50):
    """DLT source for Home Office statistics bulletins."""

    @dlt.resource(
        name="statistics",
        write_disposition="merge",
        primary_key=["url"],
    )
    def statistics():
        yield from _crawl_home_office_statistics(max_pages=max_pages)

    return statistics