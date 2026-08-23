# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIPP v1 NI Policing Board oversight publications.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest, Scenario: NI Policing sources).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Source URL: https://www.nipolicingboard.org.uk/publications (the NI
# Policing Board oversight publications library). Falls within the
# cianchosaint OSINT allowlist.

"""cianchosaint.cianchosaint.dlt.british_isles.ni.policing_board_ni — NI Policing Board.

Source: `https://www.nipolicingboard.org.uk/publications` — the
Northern Ireland Policing Board oversight publication library. The
NI Policing Board is the statutory oversight body for the PSNI;
publishes annual reports + thematic reviews + Code of Ethics guidance.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/ni/policing/policing_board/`.
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


POLICING_BOARD_BASE = "https://www.nipolicingboard.org.uk/publications"


def _crawl_policing_board_ni(max_pages: int) -> Iterator[dict[str, Any]]:
    """Crawl the NI Policing Board oversight publications."""
    for page in _crawl_source(
        source_name="policing_board_ni.publications",
        base_url=POLICING_BOARD_BASE,
        include_paths=["/**"],
        max_pages=max_pages,
        max_depth=3,
    ):
        page["nation"] = "ni"
        page["domain"] = "policing"
        page["entity"] = "policing_board_ni"
        page["entity_type"] = "publication"
        yield page


@dlt.source(name="policing_board_ni")
def policing_board_ni_source(max_pages: int = 50):
    """DLT source for the NI Policing Board publications."""

    @dlt.resource(
        name="publications",
        write_disposition="merge",
        primary_key=["url"],
    )
    def publications():
        yield from _crawl_policing_board_ni(max_pages=max_pages)

    return publications