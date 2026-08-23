# CIANCHOSAINT new-build: per-political-party DLT source module for ROI.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules, Scenario: All 24 parties ship from this change).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties.roi — ROI Dáil + Seanad DLT sources.

Phase 4 of the openspec change. Covers the 12 active political parties
of the Republic of Ireland (Dáil Éireann + Seanad Éireann):

- ``fianna_fail``             — Fianna Fáil
- ``fine_gael``               — Fine Gael
- ``sinn_fein_roi``           — Sinn Féin (ROI branch)
- ``labour_roi``              — Irish Labour Party
- ``social_democrats``        — Social Democrats (Ireland)
- ``pbp_solidarity``          — People Before Profit–Solidarity
- ``green_party_roi``         — Green Party / Comhaontas Glas (Ireland)
- ``aontu``                   — Aontú
- ``independent_ireland``     — Independent Ireland
- ``irish_freedom_party``     — Irish Freedom Party
- ``national_party_roi``      — National Party (Ireland)
- ``rise_roi``                — Rise (ROI)

ROI parties fall under the Electoral Reform Act 2022 register; the
``electoral_commission_id`` is the future register id (currently
``nil`` pending the register's public launch).

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/roi/<party>/``.
"""
from __future__ import annotations

import dlt

import dlt_sources
from dlt_sources.common.site_crawler import crawl_site

from dlt_sources.cianchosaint.political_parties import _crawl_source

__all__ = ["_crawl_source"]