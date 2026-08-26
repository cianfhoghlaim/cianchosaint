"""Guernsey jurisdiction pipeline — law_enforcement vertical.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.

Guernsey is a Crown Dependency (Bailiwick of Guernsey includes
Alderney + Sark + Herm). Defence via UK MoD by treaty. Local
policing is the Guernsey Police + Customs + Immigration + the
Bailiwick of Guernsey Law Enforcement (BGLE). Intel oversight
is the Guernsey IPA + Data Protection. Audit is the C&AG of
the Bailiwick of Guernsey.
"""
from __future__ import annotations

import logging

from dlt_sources._cross.jurisdiction_pipeline_base import (
    JurisdictionPipelineBase,
)

logger = logging.getLogger(__name__)


LAW_ENFORCEMENT_STAGE: str = "law_enforcement"
GUERNSEY_JURISDICTION: str = "guernsey"


class GuernseyLawEnforcementPipeline(JurisdictionPipelineBase):
    """Guernsey jurisdiction pipeline — law_enforcement vertical."""

    STAGE = LAW_ENFORCEMENT_STAGE

    def build_pipeline_resource(self):
        """Yield one row per (jurisdiction, stage, sub-vertical) cohort.

        TODO(2026-09-XX): wire the actual per-source Guernsey policing +
        intel oversight + BGLE resources. The Phase 4 wire-up carves
        `dlt_sources/cianchosaint/crown_dependencies/guernsey_policing.py`
        into `dlt_sources/law_enforcement/guernsey/{defence,policing,
        intel_oversight,public_inquiries,emergency_services,cag}/`
        one sub-vertical per source family.
        """
        from .sources import guernsey_law_enforcement_intelligence_sources

        source = guernsey_law_enforcement_intelligence_sources()
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
                    f"({resource_name}) for Guernsey"
                ),
                "source_url": "",
                "display_name_en": f"Guernsey {resource_name}",
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


guernsey_law_enforcement_pipeline = GuernseyLawEnforcementPipeline(
    GUERNSEY_JURISDICTION,
)


__all__ = [
    "GuernseyLawEnforcementPipeline",
    "guernsey_law_enforcement_pipeline",
    "LAW_ENFORCEMENT_STAGE",
    "GUERNSEY_JURISDICTION",
]