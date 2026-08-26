"""dlt_sources/law_enforcement/northern_ireland — BI law-enforcement NI surface.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.
"""
from __future__ import annotations

from ._factory import NILawEnforcementPipeline, northern_ireland_law_enforcement_pipeline

__all__ = [
    "NILawEnforcementPipeline",
    "northern_ireland_law_enforcement_pipeline",
]