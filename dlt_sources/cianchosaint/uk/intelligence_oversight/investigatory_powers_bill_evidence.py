# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIIP v1 Investigatory Powers Bill evidence submissions.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest, Scenario: Intelligence Oversight sources).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Source URL: https://bills.parliament.uk/bills/2687 (the
# Investigatory Powers Bill page on bills.parliament.uk). Falls
# within the cianchosaint OSINT allowlist.

"""cianchosaint.cianchosaint.dlt.british_isles.uk.intelligence_oversight.investigatory_powers_bill_evidence — IPB.

Source: `https://bills.parliament.uk/bills/2687` — the Investigatory
Powers Bill page on bills.parliament.uk. The IP Bill became the
Investigatory Powers Act 2016; the parliamentary record includes
written evidence submissions from civil society + industry + agencies.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/uk/intelligence_oversight/ipb/`.
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


IPB_BASE = "https://bills.parliament.uk/bills/2687"


def _crawl_investigatory_powers_bill_evidence(max_pages: int) -> Iterator[dict[str, Any]]:
    """Crawl the Investigatory Powers Bill evidence submissions."""
    for page in _crawl_source(
        source_name="investigatory_powers_bill_evidence.evidence",
        base_url=IPB_BASE,
        include_paths=["/**"],
        max_pages=max_pages,
        max_depth=3,
    ):
        page["nation"] = "uk"
        page["domain"] = "intelligence_oversight"
        page["entity"] = "ipb"
        page["entity_type"] = "evidence_submission"
        yield page


@dlt.source(name="investigatory_powers_bill_evidence")
def investigatory_powers_bill_evidence_source(max_pages: int = 50):
    """DLT source for Investigatory Powers Bill evidence submissions."""

    @dlt.resource(
        name="evidence",
        write_disposition="merge",
        primary_key=["url"],
    )
    def evidence():
        yield from _crawl_investigatory_powers_bill_evidence(max_pages=max_pages)

    return evidence