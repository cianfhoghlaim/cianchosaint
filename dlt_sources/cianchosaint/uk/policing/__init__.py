# CIANCHOSAINT new-build: per-constituency DLT source for the
# British Isles Policing Pipeline (BIPP v1).
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
# dlt_sources/cianchosaint/<jurisdiction>/<vertical>/<source>.py
# and uses the wholesale-copied common helpers:
#   - dlt_sources.common.site_crawler (the crawl_site primitive)
#   - dlt_sources.common.endpoint_recovery (3-strategy recovery ladder)
#   - dlt_sources.common.observability (structlog + MLflow + Langfuse)
#   - dlt_sources.common.destinations_cianchosaint (md:cianchosaint
#     DuckLake destination factory)
#
# Source URLs (data.police.uk, www.met.police.uk) are British Isles
# public-sector OSINT and fall within the cianchosaint OSINT allowlist
# (per the cianchosaint-pipeline spec, Requirement: OSINT source URL
# allowlist). Every URL referenced here is enumerated in
# dlt_sources/cianchosaint/common/osint_allowlist.yaml and is on a
# British Isles domain (.police.uk / .mod.uk / .gov.uk etc.).

"""cianchosaint.cianchosaint.dlt.british_isles.uk.policing — UK policing DLT sources.

Phase 7 of the openspec change. Covers the 5 BIPP v1 m2 cohort grid
entries for the United Kingdom:

- `data_police_uk` — 43 territorial forces + the British Transport
  Police + the Metropolitan Police Service, all aggregated by the
  data.police.uk open data portal (home office / ONS publication).
- `metropolitan_police_press_releases` — MET news room.
- `stop_and_search_uk` — stop & search records from data.police.uk.
- `crime_statistics_uk` — force-level crime statistics.
- `police_workforce_uk` — force-level workforce statistics.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/uk/policing/`.
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