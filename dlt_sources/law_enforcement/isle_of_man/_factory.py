"""Isle of Man jurisdiction pipeline — law_enforcement vertical.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.

The Isle of Man is a Crown Dependency (a self-governing British
Crown Dependency, NOT part of the UK). Defence via UK MoD by
treaty. Local policing is the Isle of Man Constabulary + Customs
& Excise. Intel oversight is the Data Protection Registrar +
the Isle of Man equivalent. Audit is the Tynwald's General
Audit Committee.
"""
from __future__ import annotations

import logging

from dlt_sources._cross.jurisdiction_pipeline_base import (
    JurisdictionPipelineBase,
)

logger = logging.getLogger(__name__)


LAW_ENFORCEMENT_STAGE: str = "law_enforcement"
ISLE_OF_MAN_JURISDICTION: str = "isle_of_man"


class IsleOfManLawEnforcementPipeline(JurisdictionPipelineBase):
    """Isle of Man jurisdiction pipeline — law_enforcement vertical."""

    STAGE = LAW_ENFORCEMENT_STAGE

    def build_pipeline_resource(self):
        """Yield one row per (jurisdiction, stage, sub-vertical) cohort.

        TODO(2026-09-XX): wire the actual per-source IoM policing +
        intel oversight + Tynwald resources. The Phase 4 wire-up carves
        `dlt_sources/cianchosaint/crown_dependencies/isle_of_man_policing.py`
        into `dlt_sources/law_enforcement/isle_of_man/{defence,policing,
        intel_oversight,public_inquiries,emergency_services,audit}/`
        one sub-vertical per source family.
        """
        from .sources import isle_of_man_law_enforcement_intelligence_sources

        source = isle_of_man_law_enforcement_intelligence_sources()
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
                    f"({resource_name}) for Isle of Man"
                ),
                "source_url": "",
                "display_name_en": f"Isle of Man {resource_name}",
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


isle_of_man_law_enforcement_pipeline = IsleOfManLawEnforcementPipeline(
    ISLE_OF_MAN_JURISDICTION,
)


__all__ = [
    "IsleOfManLawEnforcementPipeline",
    "isle_of_man_law_enforcement_pipeline",
    "LAW_ENFORCEMENT_STAGE",
    "ISLE_OF_MAN_JURISDICTION",
]