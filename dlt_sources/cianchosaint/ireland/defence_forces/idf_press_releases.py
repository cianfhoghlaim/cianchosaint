# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIDP v1 Irish Defence Forces (IDF) press releases.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest, Scenario: Ireland Defence Forces sources).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Source URL: https://www.defence.ie/news-and-events/news (the IDF
# news room). Falls within the cianchosaint OSINT allowlist.

"""cianchosaint.cianchosaint.dlt.british_isles.ireland.defence_forces.idf_press_releases — IDF news.

Source: `https://www.defence.ie/news-and-events/news` — the Irish
Defence Forces press release index. The IDF consists of the Army +
the Air Corps + the Naval Service; ~7,500 active personnel + ~1,500
reservists; based primarily in the Curragh + Custume + the Casement
Aerodrome + Haulbowline + the Defence Forces Training Centre.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/ireland/defence_forces/idf_news/`.
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


IDF_NEWS_BASE = "https://www.defence.ie/news-and-events/news"


def _crawl_idf_press_releases(max_pages: int) -> Iterator[dict[str, Any]]:
    """Crawl the IDF news room."""
    for page in _crawl_source(
        source_name="idf_press_releases.press_releases",
        base_url=IDF_NEWS_BASE,
        include_paths=["/**"],
        max_pages=max_pages,
        max_depth=3,
    ):
        page["nation"] = "ie"
        page["domain"] = "military"
        page["entity"] = "idf"
        page["entity_type"] = "press_release"
        yield page


@dlt.source(name="idf_press_releases")
def idf_press_releases_source(max_pages: int = 50):
    """DLT source for Irish Defence Forces press releases."""

    @dlt.resource(
        name="press_releases",
        write_disposition="merge",
        primary_key=["url"],
    )
    def press_releases():
        yield from _crawl_idf_press_releases(max_pages=max_pages)

    return press_releases