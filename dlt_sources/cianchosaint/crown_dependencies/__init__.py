# CIANCHOSAINT new-build: per-constituency DLT source for the
# BIPP v1 Crown Dependencies police forces (Jersey + Guernsey + IoM).
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
# The 3 Crown Dependencies police forces are not part of any UK
# territorial force; they are self-governing Crown Dependencies with
# their own police forces. Source URLs (police.je, guernseypolice.com,
# iompolice.im) are British Isles public-sector OSINT and fall within
# the cianchosaint OSINT allowlist.

"""cianchosaint.cianchosaint.dlt.british_isles.crown_dependencies — Crown Dependencies DLT sources.

Phase 7 of the openspec change. Covers the 3 BIPP v1 m3 cohort grid
entries for the Crown Dependencies:

- `jersey_policing`    — States of Jersey Police.
- `guernsey_policing`  — Bailiwick of Guernsey Police.
- `isle_of_man_policing` — Isle of Man Constabulary.

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/crown_dependencies/`.
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