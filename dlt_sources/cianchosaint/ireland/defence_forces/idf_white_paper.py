# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIDP v1 White Paper on Defence (Republic of Ireland).
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest, Scenario: Ireland Defence Forces sources).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Source URL: https://www.defence.ie/defence-and-security/white-paper-
# defence (the White Paper on Defence page). Falls within the
# cianchosaint OSINT allowlist.

"""cianchosaint.cianchosaint.dlt.british_isles.ireland.defence_forces.idf_white_paper — White Paper.

Source: `https://www.defence.ie/defence-and-security/white-paper-defence`
— the White Paper on Defence (2015) page. The White Paper sets the
strategic defence + security posture for the Republic of Ireland;
published by the Department of Defence; covers the next 10 years of
capability investment + overseas deployments.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/ireland/defence_forces/white_paper/`.
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


WHITE_PAPER_BASE = "https://www.defence.ie/defence-and-security/white-paper-defence"
DEFENCE_POLICY_BASE = "https://www.defence.ie/defence-and-security/"


def _crawl_idf_white_paper(max_pages: int) -> Iterator[dict[str, Any]]:
    """Crawl the White Paper on Defence + the broader defence-and-security index."""
    for url in (WHITE_PAPER_BASE, DEFENCE_POLICY_BASE):
        for page in _crawl_source(
            source_name=f"idf_white_paper.{url.split('/')[-1] or 'index'}",
            base_url=url,
            include_paths=["/**"],
            max_pages=max_pages,
            max_depth=3,
        ):
            page["nation"] = "ie"
            page["domain"] = "military"
            page["entity"] = "idf"
            page["entity_type"] = "white_paper"
            yield page


@dlt.source(name="idf_white_paper")
def idf_white_paper_source(max_pages: int = 50):
    """DLT source for the White Paper on Defence."""

    @dlt.resource(
        name="publications",
        write_disposition="merge",
        primary_key=["url"],
    )
    def publications():
        yield from _crawl_idf_white_paper(max_pages=max_pages)

    return publications