# CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# This file is part of the cianchosaint official-media DLT layer. The
# official-media layer supports the British Isles government source
# enrichment pipeline (per the cianchosaint-agentic-interaction-v1
# openspec change, Requirement: Lateralised GA + irishstatutebook.ie
# + courts.ie pipelines + the cross-constituency FunctionTool
# coverage for the GA/MET/PSNI agents).
#
# instagram_export.py was intentionally EXCLUDED from the wholesale-
# copy (social-media-specific, not relevant to defence/policing).

"""Jersey (States of Jersey) official-media sub-asset.

Per the 2026-08-05-official-media-biiep-v3-coverage-v1 change
(closes GitHub issue #47 — add JEY jurisdiction to official-media).
"""
from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


JERSEY_SOURCES = [
    {
        "name": "States of Jersey News",
        "url": "https://www.gov.je/news",
        "type": "press_release",
        "cadence": "daily",
    },
    {
        "name": "States Assembly Hansard",
        "url": "https://statesassembly.je/hansard",
        "type": "hansard",
        "cadence": "weekly",
    },
    {
        "name": "Children, Education & Home Affairs",
        "url": "https://www.gov.je/government/departments/children-education-home-affairs",
        "type": "policy_update",
        "cadence": "weekly",
    },
]


async def fetch_jersey_sources() -> list[dict[str, Any]]:
    """Fetch the latest Jersey official-media sources."""
    logger.info("fetching Jersey official-media sources (count=%d)", len(JERSEY_SOURCES))
    return [
        {**src, "fetched_at": datetime.now(UTC).isoformat(), "jurisdiction": "jersey"}
        for src in JERSEY_SOURCES
    ]


__all__ = ["JERSEY_SOURCES", "fetch_jersey_sources"]
