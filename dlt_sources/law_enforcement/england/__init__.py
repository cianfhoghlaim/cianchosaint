"""dlt_sources/law_enforcement/england — BI law-enforcement England surface.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.

SKELETON — the actual sources live in
`dlt_sources/cianchosaint/uk/{policing,military,government,intelligence_oversight,intelligence_agencies}/`
until Phase 4 (6 → 12 months) carves them here.
"""
from __future__ import annotations

from ._factory import EnglandLawEnforcementPipeline, england_law_enforcement_pipeline

__all__ = [
    "EnglandLawEnforcementPipeline",
    "england_law_enforcement_pipeline",
]