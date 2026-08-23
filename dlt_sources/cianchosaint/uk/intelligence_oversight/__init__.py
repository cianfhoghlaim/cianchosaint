# CIANCHOSAINT new-build: per-constituency DLT source for the
# British Isles Intelligence Oversight Pipeline (BIIP v1) — United Kingdom.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-
#   constituency-dlt-sources/spec.md, Requirement: The per-constituency
#   DLT source manifest).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Per the cianchosaint-repo-bootstrap-v2 change (Phase 3.1), every
# per-constituency DLT source module lives at
# dlt_sources/cianchosaint/<jurisdiction>/<vertical>/<source>.py.
# Source URLs (isc.independent.gov.uk, ipco.org.uk, investigatory-
# powerstribunal.org.uk, bills.parliament.uk) are British Isles
# public-sector OSINT and fall within the cianchosaint OSINT allowlist.

"""cianchosaint.cianchosaint.dlt.british_isles.uk.intelligence_oversight — UK oversight DLT sources.

Phase 7 of the openspec change. Covers the 4 BIIP v1 m1 cohort grid
entries for the United Kingdom:

- `isc_annual_reports`               — Intelligence and Security Committee.
- `ipco_reports`                     — Investigatory Powers Commissioner's Office.
- `ipt_decisions`                    — Investigatory Powers Tribunal.
- `investigatory_powers_bill_evidence` — Parliament bills evidence submissions.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/uk/intelligence_oversight/`.
"""
from __future__ import annotations

import dlt

import dlt_sources
from dlt_sources.common.site_crawler import crawl_site


def _crawl_source(*args, **kwargs):
    # The legacy _crawl_source took (source_name, base_url, ...) — source_name
    # was used only for logging in the legacy helper. The new crawl_site
    # primitive has no source_name, so we drop it if present.
    if args and isinstance(args[0], str) and args[0] == kwargs.get("source_name"):
        args = args[1:]
    kwargs.pop("source_name", None)
    for page in crawl_site(*args, **kwargs):
        yield page.to_dict()