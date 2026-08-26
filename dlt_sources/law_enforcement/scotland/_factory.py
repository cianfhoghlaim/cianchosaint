"""Scotland jurisdiction pipeline — law_enforcement vertical.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.

Scotland shares UK-wide defence (UK MoD + RAF + RN + Army) with
England + Wales + NI; policing is devolved to Police Scotland (single
force since 2013); intelligence oversight is shared (IPCO for Scotland
+ Scottish Information Commissioner's oversight of intelligence
services). Audit reports come from Audit Scotland (not NAO).
"""
from __future__ import annotations

import logging

from dlt_sources._cross.jurisdiction_pipeline_base import (
    JurisdictionPipelineBase,
)

logger = logging.getLogger(__name__)


LAW_ENFORCEMENT_STAGE: str = "law_enforcement"
SCOTLAND_JURISDICTION: str = "scotland"


class ScotlandLawEnforcementPipeline(JurisdictionPipelineBase):
    """Scotland jurisdiction pipeline — law_enforcement vertical.

    SKELETON — `build_pipeline_resource()` is a placeholder until
    Phase 4 wires the per-source Scotland policing + intel oversight
    + audit-scotland resources into the `sources.py` module below.
    """

    STAGE = LAW_ENFORCEMENT_STAGE

    def build_pipeline_resource(self):
        """Yield one row per (jurisdiction, stage, sub-vertical) cohort.

        TODO(2026-09-XX): wire the actual per-source Scotland policing +
        intel oversight + audit-scotland resources. The Phase 4 wire-up
        carves `dlt_sources/cianchosaint/uk/{policing,government,
        intelligence_oversight}/` (Scotland-relevant slice) into
        `dlt_sources/law_enforcement/scotland/{defence,policing,
        intel_oversight,public_inquiries,emergency_services,audit}/`
        one sub-vertical per source family. Defence sources are
        UK-wide and SHARED with England; the per-jurisdiction row
        counter reflects Scotland-only attribution.
        """
        from .sources import scotland_law_enforcement_intelligence_sources

        source = scotland_law_enforcement_intelligence_sources()
        for resource_name in source.selected_resources:
            yield {
                "source_id": (
                    f"british_isles.{self.jurisdiction}.law_enforcement."
                    f"{resource_name}"
                ),
                "country_code": self.jurisdiction,
                "jurisdiction": self.jurisdiction,
                "education_stage": self.STAGE,
                "subject": resource_name,
                "qualification_level": "n_a",
                "language": "en",
                "baml_function": "law_enforcement_intelligence_row",
                "concept": (
                    f"BI law-enforcement intelligence source "
                    f"({resource_name}) for Scotland"
                ),
                "source_url": "",
                "display_name_en": f"Scotland {resource_name}",
                "display_name_local": "",
                "last_verified": "2026-08-25",
                "namespace": (
                    f"cianchosaint.law_enforcement.{self.jurisdiction}."
                    f"{resource_name}"
                ),
                "natural_key": (
                    f"{self.jurisdiction}|{self.STAGE}|{resource_name}|"
                    f"none|n_a|en"
                ),
                "content_sha256": "",
            }


scotland_law_enforcement_pipeline = ScotlandLawEnforcementPipeline(
    SCOTLAND_JURISDICTION,
)


__all__ = [
    "ScotlandLawEnforcementPipeline",
    "scotland_law_enforcement_pipeline",
    "LAW_ENFORCEMENT_STAGE",
    "SCOTLAND_JURISDICTION",
]