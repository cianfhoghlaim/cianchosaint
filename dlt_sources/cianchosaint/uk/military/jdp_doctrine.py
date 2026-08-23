# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIDP v1 JDP (Joint Doctrine Publications) library.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest, Scenario: UK Military sources).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Source URL: https://www.gov.uk/government/collections/jdp- (the JDP
# doctrine collection on gov.uk). Falls within the cianchosaint OSINT
# allowlist.

"""cianchosaint.cianchosaint.dlt.british_isles.uk.military.jdp_doctrine — JDP doctrine.

Source: `https://www.gov.uk/government/collections/jdp-` — the Joint
Doctrine Publications collection on gov.uk. JDPs are the publicly-
released doctrine documents that describe how the UK armed forces
operate together in joint / combined environments; cover maritime +
land + air + cyber + special ops + the 5 NATO joint functions.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/uk/military/jdp/`.
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


JDP_BASE = "https://www.gov.uk/government/collections/jdp-"


def _crawl_jdp_doctrine(max_pages: int) -> Iterator[dict[str, Any]]:
    """Crawl the JDP doctrine collection."""
    for page in _crawl_source(
        source_name="jdp_doctrine.publications",
        base_url=JDP_BASE,
        include_paths=["/**"],
        max_pages=max_pages,
        max_depth=3,
    ):
        page["nation"] = "uk"
        page["domain"] = "military"
        page["entity"] = "jdp"
        page["entity_type"] = "doctrine_publication"
        yield page


@dlt.source(name="jdp_doctrine")
def jdp_doctrine_source(max_pages: int = 50):
    """DLT source for JDP doctrine publications."""

    @dlt.resource(
        name="publications",
        write_disposition="merge",
        primary_key=["url"],
    )
    def publications():
        yield from _crawl_jdp_doctrine(max_pages=max_pages)

    return publications