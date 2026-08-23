# CIANCHOSAINT new-build: per-political-party DLT source module for the
# Crown Dependencies (Jersey + Guernsey + Isle of Man).
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.crown_dependencies — Crown Dependencies DLT sources.

Phase 4 of the openspec change. Covers the 3 Crown Dependencies
parliaments (Jersey, Guernsey, Isle of Man). Note: the Crown
Dependencies do not field UK-style political parties — they elect
parish-level independents + a handful of small parties (Reform Jersey,
Tinvaal, Liberal Vannin, etc.). The pipelines here ingest the
official government + party press rooms for each Crown Dependency.

- ``jersey_party``   — Jersey (States Assembly)
- ``guernsey_party`` — Guernsey (States of Guernsey)
- ``iom_party``      — Isle of Man (Tynwald + Tinvaal + Liberal Vannin)

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/crown_dependencies/<cd>/``.
"""
from __future__ import annotations

import dlt

import dlt_sources
from dlt_sources.common.site_crawler import crawl_site

from dlt_sources.cianchosaint.political_parties import _crawl_source

__all__ = ["_crawl_source"]