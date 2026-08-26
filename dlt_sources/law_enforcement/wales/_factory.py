"""Wales jurisdiction pipeline — law_enforcement vertical.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.

Wales has 4 police forces (Dyfed-Powys + Gwent + North Wales + South
Wales) — devolved policing but the National Crime Agency + the UK
intelligence services are shared. Defence is UK-wide (shared with
England + Scotland + NI). Audit is Wales Audit Office (NOT NAO).
Bilingual Welsh-medium coverage is required for the language pair.
"""
from __future__ import annotations

import logging

from dlt_sources._cross.jurisdiction_pipeline_base import (
    JurisdictionPipelineBase,
)

logger = logging.getLogger(__name__)


LAW_ENFORCEMENT_STAGE: str = "law_enforcement"
WALES_JURISDICTION: str = "wales"


class WalesLawEnforcementPipeline(JurisdictionPipelineBase):
    """Wales jurisdiction pipeline — law_enforcement vertical.

    SKELETON — `build_pipeline_resource()` is a placeholder until
    Phase 4 wires the per-source Wales policing + Wales Audit Office
    resources into the `sources.py` module below.
    """

    STAGE = LAW_ENFORCEMENT_STAGE

    def build_pipeline_resource(self):
        """Yield one row per (jurisdiction, stage, sub-vertical) cohort.

        TODO(2026-09-XX): wire the actual per-source Wales policing +
        intel oversight + Wales Audit Office resources. The Phase 4
        wire-up carves `dlt_sources/cianchosaint/uk/policing/` (the
        4 Welsh forces + data.police.uk) into
        `dlt_sources/law_enforcement/wales/{defence,policing,
        intel_oversight,public_inquiries,emergency_services,wao}/`
        one sub-vertical per source family. Bilingual Welsh-medium
        coverage is required for the public-facing data.
        """
        from .sources import wales_law_enforcement_intelligence_sources

        source = wales_law_enforcement_intelligence_sources()
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
                    f"({resource_name}) for Wales"
                ),
                "source_url": "",
                "display_name_en": f"Wales {resource_name}",
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


wales_law_enforcement_pipeline = WalesLawEnforcementPipeline(
    WALES_JURISDICTION,
)


__all__ = [
    "WalesLawEnforcementPipeline",
    "wales_law_enforcement_pipeline",
    "LAW_ENFORCEMENT_STAGE",
    "WALES_JURISDICTION",
]