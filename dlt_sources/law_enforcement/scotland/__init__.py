"""dlt_sources/law_enforcement/scotland — BI law-enforcement Scotland surface.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.
"""
from __future__ import annotations

from ._factory import ScotlandLawEnforcementPipeline, scotland_law_enforcement_pipeline

__all__ = [
    "ScotlandLawEnforcementPipeline",
    "scotland_law_enforcement_pipeline",
]