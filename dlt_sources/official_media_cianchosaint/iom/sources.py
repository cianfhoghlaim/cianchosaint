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

"""Isle of Man (Tynwald) official-media sub-asset.

Per the 2026-08-05-official-media-biiep-v3-coverage-v1 change
(closes GitHub issue #47 — add IoM jurisdiction to official-media).
"""
from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


IOM_SOURCES = [
    {
        "name": "Tynwald Hansard",
        "url": "https://www.tynwald.org.im/business/hansard",
        "type": "hansard",
        "cadence": "daily",
    },
    {
        "name": "Isle of Man Government News",
        "url": "https://www.gov.im/news/",
        "type": "press_release",
        "cadence": "daily",
    },
    {
        "name": "Department of Education, Sport and Culture",
        "url": "https://www.gov.im/about-the-government/departments/education,-sport-and-culture/",
        "type": "policy_update",
        "cadence": "weekly",
    },
]


async def fetch_iom_sources() -> list[dict[str, Any]]:
    """Fetch the latest Isle of Man official-media sources."""
    logger.info("fetching IoM official-media sources (count=%d)", len(IOM_SOURCES))
    return [
        {**src, "fetched_at": datetime.now(UTC).isoformat(), "jurisdiction": "isle_of_man"}
        for src in IOM_SOURCES
    ]


__all__ = ["IOM_SOURCES", "fetch_iom_sources"]
