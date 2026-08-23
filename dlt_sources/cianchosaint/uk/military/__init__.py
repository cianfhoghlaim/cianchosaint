# CIANCHOSAINT new-build: per-constituency DLT source for the
# British Isles Defence Pipeline (BIDP v1) — United Kingdom.
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
# Source URLs (gov.uk, raf.mod.uk, royalnavy.mod.uk, army.mod.uk) are
# British Isles public-sector OSINT and fall within the cianchosaint
# OSINT allowlist.

"""cianchosaint.cianchosaint.dlt.british_isles.uk.military — UK military DLT sources.

Phase 7 of the openspec change. Covers the 6 BIDP v1 m1 cohort grid
entries for the United Kingdom:

- `mod_press_releases`        — UK MoD corporate (gov.uk).
- `raf_press_releases`        — Royal Air Force (raf.mod.uk).
- `royal_navy_press_releases` — Royal Navy (royalnavy.mod.uk).
- `british_army_press_releases` — British Army (army.mod.uk).
- `jsp_doctrine`              — Joint Service Publications (gov.uk).
- `jdp_doctrine`              — Joint Doctrine Publications (gov.uk).

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/uk/military/`.
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