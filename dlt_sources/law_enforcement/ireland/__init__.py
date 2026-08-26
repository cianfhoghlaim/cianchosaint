"""dlt_sources/law_enforcement/ireland — BI law-enforcement Éire surface.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.

SKELETON — the actual sources live in
`dlt_sources/cianchosaint/ireland/{defence_forces,law}/` until Phase 4
(6 → 12 months) carves them here.
"""
from __future__ import annotations

from ._factory import IrelandLawEnforcementPipeline, ireland_law_enforcement_pipeline

__all__ = [
    "IrelandLawEnforcementPipeline",
    "ireland_law_enforcement_pipeline",
]