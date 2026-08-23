# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIPP v1 Isle of Man Constabulary.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest, Scenario: Crown Dependencies sources).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Source URL: https://www.iompolice.im/news (the IoM Constabulary
# news room). Falls within the cianchosaint OSINT allowlist (entry:
# ig_username=iom_constabulary_official).

"""cianchosaint.cianchosaint.dlt.british_isles.crown_dependencies.isle_of_man_policing — IoM Constabulary.

Source: `https://www.iompolice.im/news` — the Isle of Man Constabulary
news room. The IoM Constabulary is the territorial police force for
the Isle of Man (~240 officers); oversees the island + the EEZ around
the Isle of Man.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/crown_dependencies/isle_of_man/`.
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


IOM_NEWS_BASE = "https://www.iompolice.im/news"


def _crawl_isle_of_man_policing(max_pages: int) -> Iterator[dict[str, Any]]:
    """Crawl the IoM Constabulary news room."""
    for page in _crawl_source(
        source_name="isle_of_man_policing.news",
        base_url=IOM_NEWS_BASE,
        include_paths=["/**"],
        max_pages=max_pages,
        max_depth=3,
    ):
        page["nation"] = "iom"
        page["domain"] = "policing"
        page["entity"] = "iom_constabulary"
        page["entity_type"] = "press_release"
        yield page


@dlt.source(name="isle_of_man_policing")
def isle_of_man_policing_source(max_pages: int = 50):
    """DLT source for the Isle of Man Constabulary."""

    @dlt.resource(
        name="news",
        write_disposition="merge",
        primary_key=["url"],
    )
    def news():
        yield from _crawl_isle_of_man_policing(max_pages=max_pages)

    return news