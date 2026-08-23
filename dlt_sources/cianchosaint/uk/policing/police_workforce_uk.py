# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIPP v1 UK police workforce statistics.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest, Scenario: UK Policing sources).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Source URL: https://data.police.uk/api/staff (the open data portal's
# workforce endpoint). Falls within the cianchosaint OSINT allowlist.

"""cianchosaint.cianchosaint.dlt.british_isles.uk.policing.police_workforce_uk — UK workforce.

Source: `https://data.police.uk/api/staff` — the open data portal's
force-level workforce endpoint. Each row is one (force, role, count)
tuple for a given quarter; covers police officers + PCSOs + staff.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/uk/policing/police_workforce_uk/`.
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


WORKFORCE_API = "https://data.police.uk/api/staff"
WORKFORCE_DOCS = "https://data.police.uk/docs/method/staff/"


def _crawl_police_workforce_uk(max_pages: int) -> Iterator[dict[str, Any]]:
    """Crawl the workforce API docs (live data via API, not crawl_site)."""
    for page in _crawl_source(
        source_name="police_workforce_uk.docs",
        base_url=WORKFORCE_DOCS,
        include_paths=["/**"],
        max_pages=max_pages // 2,
        max_depth=2,
    ):
        page["nation"] = "uk"
        page["domain"] = "policing"
        page["entity"] = "workforce"
        page["entity_type"] = "stat_doc"
        yield page


@dlt.source(name="police_workforce_uk")
def police_workforce_uk_source(max_pages: int = 50):
    """DLT source for UK police workforce statistics (data.police.uk)."""

    @dlt.resource(
        name="workforce",
        write_disposition="merge",
        primary_key=["url"],
    )
    def workforce():
        yield from _crawl_police_workforce_uk(max_pages=max_pages)

    return workforce