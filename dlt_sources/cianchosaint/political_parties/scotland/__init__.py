# CIANCHOSAINT new-build: per-political-party DLT source module for the
# Scottish Holyrood.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.scotland — Scottish Holyrood DLT sources.

Phase 4 of the openspec change. Covers the 5 active political parties
of the Scottish Parliament (Holyrood):

- ``snp_scottish``              — Scottish National Party (Holyrood scope)
- ``scottish_labour``           — Scottish Labour
- ``scottish_conservatives``    — Scottish Conservatives
- ``scottish_liberal_democrats`` — Scottish Liberal Democrats
- ``scottish_greens``           — Scottish Greens

SNP also appears as a UK-HoC source at
``dlt_sources/cianchosaint/political_parties/uk/snp.py`` — different
scope, same party.

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/holyrood/<party>/``.
"""
from __future__ import annotations

import dlt

import dlt_sources
from dlt_sources.common.site_crawler import crawl_site

from dlt_sources.cianchosaint.political_parties import _crawl_source

__all__ = ["_crawl_source"]