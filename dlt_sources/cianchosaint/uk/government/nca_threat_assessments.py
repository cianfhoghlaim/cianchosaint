# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIIP v1 National Crime Agency (NCA) threat assessments.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest, Scenario: UK Government sources).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Source URL: https://www.nationalcrimeagency.gov.uk/what-we-do/
# crime-threats (the NCA crime-threats page). Falls within the
# cianchosaint OSINT allowlist.

"""cianchosaint.cianchosaint.dlt.british_isles.uk.government.nca_threat_assessments — NCA.

Source: `https://www.nationalcrimeagency.gov.uk/what-we-do/crime-threats`
— the National Crime Agency crime-threats page. The NCA is the UK
lead agency against serious + organised crime; publishes the annual
National Strategic Assessment of Serious and Organised Crime + per-
threat-type assessments (cyber, drugs, firearms, modern slavery, etc.).

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/uk/government/nca/`.
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


NCA_THREATS_BASE = "https://www.nationalcrimeagency.gov.uk/what-we-do/crime-threats"


def _crawl_nca_threat_assessments(max_pages: int) -> Iterator[dict[str, Any]]:
    """Crawl the NCA crime-threats index."""
    for page in _crawl_source(
        source_name="nca_threat_assessments.assessments",
        base_url=NCA_THREATS_BASE,
        include_paths=["/**"],
        max_pages=max_pages,
        max_depth=3,
    ):
        page["nation"] = "uk"
        page["domain"] = "government"
        page["entity"] = "nca"
        page["entity_type"] = "threat_assessment"
        yield page


@dlt.source(name="nca_threat_assessments")
def nca_threat_assessments_source(max_pages: int = 50):
    """DLT source for NCA threat assessments."""

    @dlt.resource(
        name="assessments",
        write_disposition="merge",
        primary_key=["url"],
    )
    def assessments():
        yield from _crawl_nca_threat_assessments(max_pages=max_pages)

    return assessments