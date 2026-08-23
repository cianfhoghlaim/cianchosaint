# CIANCHOSAINT new-build: per-political-party DLT source module for the
# Welsh Senedd.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.wales — Welsh Senedd DLT sources.

Phase 4 of the openspec change. Covers the 4 active political parties
of the Welsh Senedd Cymru (the devolved Welsh parliament):

- ``plaid_cymru_senedd``        — Plaid Cymru (Senedd scope)
- ``labour_wales``              — Welsh Labour
- ``conservative_wales``        — Welsh Conservatives
- ``liberal_democrats_wales``   — Welsh Liberal Democrats

Plaid Cymru also appears as a UK-HoC source at
``dlt_sources/cianchosaint/political_parties/uk/plaid_cymru.py`` —
different scope, same party.

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/senedd/<party>/``.
"""
from __future__ import annotations

import dlt

import dlt_sources
from dlt_sources.common.site_crawler import crawl_site

from dlt_sources.cianchosaint.political_parties import _crawl_source

__all__ = ["_crawl_source"]