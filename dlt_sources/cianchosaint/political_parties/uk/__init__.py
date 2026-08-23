# CIANCHOSAINT new-build: per-political-party DLT source module for UK HoC.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.uk — UK HoC DLT sources.

Phase 4 of the openspec change. Covers the 7 active political parties
of the United Kingdom House of Commons:

- ``conservative_party_uk``   — Conservative and Unionist Party (UK)
- ``labour_party_uk``         — Labour Party (UK)
- ``liberal_democrats_uk``    — Liberal Democrats
- ``reform_uk``               — Reform UK (⭐ the canonical pilot case study)
- ``green_party_ew``          — Green Party of England and Wales
- ``plaid_cymru``             — Plaid Cymru (UK HoC scope)
- ``snp``                     — Scottish National Party (UK HoC scope)

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/uk_hoc/<party>/``.
"""
from __future__ import annotations

import dlt

import dlt_sources
from dlt_sources.common.site_crawler import crawl_site

from dlt_sources.cianchosaint.political_parties import _crawl_source

__all__ = [
    "_crawl_source",
]