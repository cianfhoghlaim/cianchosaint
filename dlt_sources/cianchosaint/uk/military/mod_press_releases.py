# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIDP v1 UK MoD corporate press releases.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest, Scenario: UK Military sources).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Source URL: https://www.gov.uk/government/organisations/
# ministry-of-defence (the UK MoD corporate page on gov.uk). Falls
# within the cianchosaint OSINT allowlist (entry: ig_username=ukmod).

"""cianchosaint.cianchosaint.dlt.british_isles.uk.military.mod_press_releases — UK MoD.

Source: `https://www.gov.uk/government/organisations/ministry-of-defence`
— the UK Ministry of Defence corporate page on gov.uk. Covers MoD
press releases + announcements + statistics + policy papers.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/uk/military/mod/`.
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


MOD_BASE = "https://www.gov.uk/government/organisations/ministry-of-defence"


def _crawl_mod_press_releases(max_pages: int) -> Iterator[dict[str, Any]]:
    """Crawl the UK MoD corporate page + announcements + statistics."""
    for page in _crawl_source(
        source_name="mod_press_releases.announcements",
        base_url=MOD_BASE,
        include_paths=["/**"],
        max_pages=max_pages,
        max_depth=3,
    ):
        page["nation"] = "uk"
        page["domain"] = "military"
        page["entity"] = "uk_mod"
        page["entity_type"] = "press_release"
        yield page


@dlt.source(name="mod_press_releases")
def mod_press_releases_source(max_pages: int = 50):
    """DLT source for UK MoD press releases."""

    @dlt.resource(
        name="press_releases",
        write_disposition="merge",
        primary_key=["url"],
    )
    def press_releases():
        yield from _crawl_mod_press_releases(max_pages=max_pages)

    return press_releases