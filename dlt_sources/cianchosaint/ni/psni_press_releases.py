# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIPP v1 PSNI (Police Service of Northern Ireland) press releases.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest, Scenario: NI Policing sources).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Source URL: https://www.psni.police.uk/news (the PSNI news room).
# Falls within the cianchosaint OSINT allowlist.

"""cianchosaint.cianchosaint.dlt.british_isles.ni.psni_press_releases — PSNI news.

Source: `https://www.psni.police.uk/news` — the Police Service of
Northern Ireland news room. The PSNI is the single territorial force
covering Northern Ireland (~7,000 officers); oversights by the Police
Ombudsman for Northern Ireland + the NI Policing Board.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/ni/policing/psni/`.
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


PSNI_NEWS_BASE = "https://www.psni.police.uk/news"


def _crawl_psni_press_releases(max_pages: int) -> Iterator[dict[str, Any]]:
    """Crawl the PSNI news room."""
    for page in _crawl_source(
        source_name="psni_press_releases.press_releases",
        base_url=PSNI_NEWS_BASE,
        include_paths=["/**"],
        max_pages=max_pages,
        max_depth=3,
    ):
        page["nation"] = "ni"
        page["domain"] = "policing"
        page["entity"] = "psni"
        page["entity_type"] = "press_release"
        yield page


@dlt.source(name="psni_press_releases")
def psni_press_releases_source(max_pages: int = 50):
    """DLT source for the PSNI press releases."""

    @dlt.resource(
        name="press_releases",
        write_disposition="merge",
        primary_key=["url"],
    )
    def press_releases():
        yield from _crawl_psni_press_releases(max_pages=max_pages)

    return press_releases