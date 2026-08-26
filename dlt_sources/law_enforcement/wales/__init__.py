"""dlt_sources/law_enforcement/wales — BI law-enforcement Wales surface.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.
"""
from __future__ import annotations

from ._factory import WalesLawEnforcementPipeline, wales_law_enforcement_pipeline

__all__ = [
    "WalesLawEnforcementPipeline",
    "wales_law_enforcement_pipeline",
]