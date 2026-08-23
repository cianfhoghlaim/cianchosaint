# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIDP v1 British Army press releases.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest, Scenario: UK Military sources).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Source URL: https://www.army.mod.uk/news (the British Army news
# room). Falls within the cianchosaint OSINT allowlist.

"""cianchosaint.cianchosaint.dlt.british_isles.uk.military.british_army_press_releases — Army.

Source: `https://www.army.mod.uk/news` — the British Army news room.
The British Army is the land warfare branch of the UK armed forces
(~75k regular personnel + ~30k reservists); operates from 100+
bases across the UK + overseas.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/uk/military/british_army/`.
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


ARMY_NEWS_BASE = "https://www.army.mod.uk/news"


def _crawl_british_army_press_releases(max_pages: int) -> Iterator[dict[str, Any]]:
    """Crawl the British Army news room."""
    for page in _crawl_source(
        source_name="british_army_press_releases.press_releases",
        base_url=ARMY_NEWS_BASE,
        include_paths=["/**"],
        max_pages=max_pages,
        max_depth=3,
    ):
        page["nation"] = "uk"
        page["domain"] = "military"
        page["entity"] = "british_army"
        page["entity_type"] = "press_release"
        yield page


@dlt.source(name="british_army_press_releases")
def british_army_press_releases_source(max_pages: int = 50):
    """DLT source for British Army press releases."""

    @dlt.resource(
        name="press_releases",
        write_disposition="merge",
        primary_key=["url"],
    )
    def press_releases():
        yield from _crawl_british_army_press_releases(max_pages=max_pages)

    return press_releases