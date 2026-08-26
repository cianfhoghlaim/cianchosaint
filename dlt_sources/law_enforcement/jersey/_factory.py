"""Jersey jurisdiction pipeline — law_enforcement vertical.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.

Jersey is a Crown Dependency (NOT part of the UK). Defence is
provided via the UK MoD by treaty; the States of Jersey Police
+ Customs + Immigration are local; the Jersey Investigatory
Powers Authority is the local oversight body; the Comptroller and
Auditor General (C&AG) is local.
"""
from __future__ import annotations

import logging

from dlt_sources._cross.jurisdiction_pipeline_base import (
    JurisdictionPipelineBase,
)

logger = logging.getLogger(__name__)


LAW_ENFORCEMENT_STAGE: str = "law_enforcement"
JERSEY_JURISDICTION: str = "jersey"


class JerseyLawEnforcementPipeline(JurisdictionPipelineBase):
    """Jersey jurisdiction pipeline — law_enforcement vertical."""

    STAGE = LAW_ENFORCEMENT_STAGE

    def build_pipeline_resource(self):
        """Yield one row per (jurisdiction, stage, sub-vertical) cohort.

        TODO(2026-09-XX): wire the actual per-source Jersey policing +
        intel oversight + C&AG resources. The Phase 4 wire-up carves
        `dlt_sources/cianchosaint/crown_dependencies/jersey_policing.py`
        into `dlt_sources/law_enforcement/jersey/{defence,policing,
        intel_oversight,public_inquiries,emergency_services,cag}/`
        one sub-vertical per source family. Defence is UK MoD by
        treaty (not local). Jersey-specific surveillance and
        investigatory powers are governed by the Regulation of
        Investigatory Powers (Jersey) Law 2005 (procedural → ciandlíthe).
        """
        from .sources import jersey_law_enforcement_intelligence_sources

        source = jersey_law_enforcement_intelligence_sources()
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
                    f"({resource_name}) for Jersey"
                ),
                "source_url": "",
                "display_name_en": f"Jersey {resource_name}",
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


jersey_law_enforcement_pipeline = JerseyLawEnforcementPipeline(
    JERSEY_JURISDICTION,
)


__all__ = [
    "JerseyLawEnforcementPipeline",
    "jersey_law_enforcement_pipeline",
    "LAW_ENFORCEMENT_STAGE",
    "JERSEY_JURISDICTION",
]