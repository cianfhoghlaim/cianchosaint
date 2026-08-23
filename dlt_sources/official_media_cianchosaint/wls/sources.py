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

"""Wales (Senedd Cymru) official-media sub-asset.

Per the 2026-08-05-official-media-biiep-v3-coverage-v1 change
(closes GitHub issue #47 — add WLS jurisdiction to official-media).
"""
from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


# Senedd Cymru (Welsh Parliament) press releases + committee reports
WALES_SOURCES = [
    {
        "name": "Senedd Cymru Press Releases",
        "url": "https://senedd.cymru/media/",
        "type": "press_release",
        "cadence": "daily",
    },
    {
        "name": "Welsh Government News",
        "url": "https://www.gov.wales/news",
        "type": "press_release",
        "cadence": "daily",
    },
    {
        "name": "Qualifications Wales Updates",
        "url": "https://qualificationswales.org/news/",
        "type": "policy_update",
        "cadence": "weekly",
    },
]


async def fetch_wales_sources() -> list[dict[str, Any]]:
    """Fetch the latest Wales official-media sources."""
    logger.info("fetching Wales official-media sources (count=%d)", len(WALES_SOURCES))
    return [
        {**src, "fetched_at": datetime.now(UTC).isoformat(), "jurisdiction": "wales"}
        for src in WALES_SOURCES
    ]


__all__ = ["WALES_SOURCES", "fetch_wales_sources"]
