"""Northern Ireland jurisdiction pipeline — law_enforcement vertical.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.

NI has 1 police force (PSNI — Police Service of Northern Ireland)
with devolved oversight via the NI Policing Board + the Department
of Justice (NI). Defence is UK-wide shared. Intelligence oversight
has the NI-specific dimension (NI Policing Board + NI Human Rights
Commission + the Investigatory Powers Commissioner's Office NI
arm). Audit is the NI Audit Office (NIAO).
"""
from __future__ import annotations

import logging

from dlt_sources._cross.jurisdiction_pipeline_base import (
    JurisdictionPipelineBase,
)

logger = logging.getLogger(__name__)


LAW_ENFORCEMENT_STAGE: str = "law_enforcement"
NORTHERN_IRELAND_JURISDICTION: str = "northern_ireland"


class NILawEnforcementPipeline(JurisdictionPipelineBase):
    """Northern Ireland jurisdiction pipeline — law_enforcement vertical.

    SKELETON — `build_pipeline_resource()` is a placeholder until
    Phase 4 wires the per-source NI policing + intel oversight + NIAO
    resources into the `sources.py` module below.
    """

    STAGE = LAW_ENFORCEMENT_STAGE

    def build_pipeline_resource(self):
        """Yield one row per (jurisdiction, stage, sub-vertical) cohort.

        TODO(2026-09-XX): wire the actual per-source NI policing +
        intel oversight + NIAO resources. The Phase 4 wire-up carves
        `dlt_sources/cianchosaint/ni/{policing_board_ni, psni_press_releases,
        justice_ni}.py` + `dlt_sources/cianchosaint/uk/intelligence_oversight/`
        (NI arm) into
        `dlt_sources/law_enforcement/northern_ireland/{defence,policing,
        intel_oversight,public_inquiries,emergency_services,niao}/`
        one sub-vertical per source family.
        """
        from .sources import northern_ireland_law_enforcement_intelligence_sources

        source = northern_ireland_law_enforcement_intelligence_sources()
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
                    f"({resource_name}) for Northern Ireland"
                ),
                "source_url": "",
                "display_name_en": f"NI {resource_name}",
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


northern_ireland_law_enforcement_pipeline = NILawEnforcementPipeline(
    NORTHERN_IRELAND_JURISDICTION,
)


__all__ = [
    "NILawEnforcementPipeline",
    "northern_ireland_law_enforcement_pipeline",
    "LAW_ENFORCEMENT_STAGE",
    "NORTHERN_IRELAND_JURISDICTION",
]