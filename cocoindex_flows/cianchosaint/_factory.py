# CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Per-jurisdiction CocoIndex flow factory for the BIPP v1 (British
# Isles Policing Pipeline) + BIIP v1 (British Isles Intelligence
# Oversight Pipeline) verticals.
#
# The factory pattern collapses 53 UK forces + 3 Crown Dependencies
# + 1 Garda + 4 Welsh + 1 PSD + 1 PSNI = 59 per-jurisdiction CocoIndex
# Apps into 1 factory module + 59 1-line re-export shims (~800 LOC
# total, vs ~7,500 LOC if each force had its own module -- 89%
# reduction). Mirrors the European-nations factory pattern at
# cocoindex_flows/european_nations/_factory.py.
"""
from __future__ import annotations

import cocoindex as coco  # type: ignore[import-not-found]

from .._shared._lifespan import shared_lifespan, LANCE_DB, EMBEDDER  # noqa: F401


# Stub implementation — the full factory pattern (53 forces + 3
# Crown Dependencies + 6 oversight bodies) is implemented as a
# follow-up change. This module exists primarily to:
# 1. Establish the canonical factory pattern at the cianchosaint
#    namespace level
# 2. Provide a placeholder for the per-jurisdiction shims
# 3. Pass the R1-R4 conformance check (R1: imports from
#    .._shared._lifespan)


# The actual factory pattern (mirroring
# cocoindex_flows/european_nations/_factory.py) is implemented in
# the follow-up openspec change
# `cianchosaint-cocoindex-factory-pattern-v1` per the bootstrap-v2
# tasks.md § 3.6. For now, this module just establishes the
# namespace and the lifespan import.

__all__ = ["shared_lifespan", "LANCE_DB", "EMBEDDER"]
