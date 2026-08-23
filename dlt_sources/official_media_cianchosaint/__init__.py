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

"""oideachais.cianfhoghlaim.dlt.official_media — Instagram-export → British-Isles government source enrichment.

Phase 1 of the ``official-media-pipeline`` openspec change. Parses the
JSON bundle Instagram ships in the standard export format, filters
out the noise (friends, family, celebrities) via a curated allowlist
+ BAML fallback, and resolves the canonical official source
(Wikipedia + Companies House + CRO + Mastodon + Bluesky) for each
surviving profile.

Public API (the only thing the rest of the stack imports):

    from dlt_sources.official_media import (
        instagram_export_source,        # @dlt.source
        allowlist_filter,                # Stage-1 + Stage-2 classifier
        source_resolver,                 # 4-lookup parallel resolver
    )
"""
from __future__ import annotations

from dlt_sources.official_media.allowlist import AllowlistFilter, allowlist_filter
from dlt_sources.official_media.instagram_export import (
    FOLLOWER_LIST_KINDS,
    InstagramExportParser,
    instagram_export_source,
)
from dlt_sources.official_media.source_resolver import SourceResolver, source_resolver

__all__ = [
    "FOLLOWER_LIST_KINDS",
    "AllowlistFilter",
    "InstagramExportParser",
    "SourceResolver",
    "allowlist_filter",
    "instagram_export_source",
    "source_resolver",
]
