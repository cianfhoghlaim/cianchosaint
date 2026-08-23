# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIPP v1 NI Department of Justice.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest, Scenario: NI Policing sources).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Source URL: https://www.justice-ni.gov.uk/news (the NI Department
# of Justice news room). Falls within the cianchosaint OSINT allowlist
# (entry: ig_username=justiceni_gov).

"""cianchosaint.cianchosaint.dlt.british_isles.ni.justice_ni — NI Department of Justice.

Source: `https://www.justice-ni.gov.uk/news` — the Northern Ireland
Department of Justice news room. The DoJ NI oversees the PSNI + the
NI Prison Service + the Youth Justice Agency + the Legal Services
Agency + the Compensation Agency.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/ni/policing/justice_ni/`.
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


JUSTICE_NI_BASE = "https://www.justice-ni.gov.uk/news"
JUSTICE_NI_PUBLICATIONS = "https://www.justice-ni.gov.uk/publications"


def _crawl_justice_ni(max_pages: int) -> Iterator[dict[str, Any]]:
    """Crawl the NI DoJ news + publications."""
    for url in (JUSTICE_NI_BASE, JUSTICE_NI_PUBLICATIONS):
        for page in _crawl_source(
            source_name=f"justice_ni.{url.split('/')[-1]}",
            base_url=url,
            include_paths=["/**"],
            max_pages=max_pages,
            max_depth=3,
        ):
            page["nation"] = "ni"
            page["domain"] = "policing"
            page["entity"] = "justice_ni"
            page["entity_type"] = "publication"
            yield page


@dlt.source(name="justice_ni")
def justice_ni_source(max_pages: int = 50):
    """DLT source for the NI Department of Justice."""

    @dlt.resource(
        name="publications",
        write_disposition="merge",
        primary_key=["url"],
    )
    def publications():
        yield from _crawl_justice_ni(max_pages=max_pages)

    return publications