# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIDP v1 Royal Navy press releases.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest, Scenario: UK Military sources).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Source URL: https://www.royalnavy.mod.uk/news (the Royal Navy news
# room). Falls within the cianchosaint OSINT allowlist.

"""cianchosaint.cianchosaint.dlt.british_isles.uk.military.royal_navy_press_releases — RN.

Source: `https://www.royalnavy.mod.uk/news` — the Royal Navy news
room. The RN is the maritime branch of the UK armed forces (~32k
personnel); operates 60+ commissioned vessels + the Royal Marines.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/uk/military/royal_navy/`.
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


ROYAL_NAVY_NEWS_BASE = "https://www.royalnavy.mod.uk/news"


def _crawl_royal_navy_press_releases(max_pages: int) -> Iterator[dict[str, Any]]:
    """Crawl the Royal Navy news room."""
    for page in _crawl_source(
        source_name="royal_navy_press_releases.press_releases",
        base_url=ROYAL_NAVY_NEWS_BASE,
        include_paths=["/**"],
        max_pages=max_pages,
        max_depth=3,
    ):
        page["nation"] = "uk"
        page["domain"] = "military"
        page["entity"] = "royal_navy"
        page["entity_type"] = "press_release"
        yield page


@dlt.source(name="royal_navy_press_releases")
def royal_navy_press_releases_source(max_pages: int = 50):
    """DLT source for Royal Navy press releases."""

    @dlt.resource(
        name="press_releases",
        write_disposition="merge",
        primary_key=["url"],
    )
    def press_releases():
        yield from _crawl_royal_navy_press_releases(max_pages=max_pages)

    return press_releases