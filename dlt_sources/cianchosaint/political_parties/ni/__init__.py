# CIANCHOSAINT new-build: per-political-party DLT source module for the
# Northern Ireland Assembly.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.ni — NI Assembly DLT sources.

Phase 4 of the openspec change. Covers the 7 active political parties
of the Northern Ireland Assembly:

- ``dup``        — Democratic Unionist Party
- ``sinn_fein_ni`` — Sinn Féin (NI branch)
- ``alliance_ni`` — Alliance Party of Northern Ireland
- ``uup``        — Ulster Unionist Party
- ``sdlp``       — Social Democratic and Labour Party
- ``tuv_ni``     — Traditional Unionist Voice
- ``pbp_ni``     — People Before Profit (Northern Ireland)

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/ni_assembly/<party>/``.

This module is separate from the cianchosaint/ni/__init__.py module
that hosts PSNI / NI Policing Board / NI Department of Justice sources
(those are policing / law-enforcement verticals — not political parties).
"""
from __future__ import annotations

import dlt

import dlt_sources
from dlt_sources.common.site_crawler import crawl_site

from dlt_sources.cianchosaint.political_parties import _crawl_source

__all__ = ["_crawl_source"]