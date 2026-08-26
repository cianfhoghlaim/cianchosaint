"""England jurisdiction pipeline — law_enforcement vertical.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change +
the parent change `2026-08-24-dlt-sources-to-multi-repo-scaffold-v1` §21.2.

SKELETON — the actual defence + policing + intelligence-oversight
sources for England live today in
`dlt_sources/cianchosaint/uk/{policing,military,intelligence_oversight,
intelligence_agencies,government}/`. Phase 4 carves them into this
tree.

## What this skeleton covers (the England law-enforcement surface)

- **Defence forces** — UK MoD + RAF + RN + Army (UK-wide; the England
  slice is the bulk of the data); MoD + service press releases; the
  Annual Report and Accounts of the MoD; the Defence Equipment and
  Support (DE&S) major projects reports; the JSP + JDP doctrine.
- **Policing** — the 43 Home Office police forces (England & Wales
  combined at the force level); the Metropolitan Police + City of
  London Police + BTP; the Home Office Police Workforce England &
  Wales statistics; the Home Office Crime Outcomes statistics; the
  data.police.uk open data API.
- **Intelligence oversight** — the Investigatory Powers Commissioner's
  Office (IPCO); the Investigatory Powers Tribunal (IPT) decisions;
  the Biometrics Commissioner; the Intelligence Services Commissioner.
- **Public inquiries** — the UK COVID-19 Inquiry; the Grenfell Tower
  Inquiry; the Iraq Inquiry (Chilcot); the Undercover Policing Inquiry.
- **Emergency services** — the London Ambulance Service + the
  National Police Air Service + the Maritime & Coastguard Agency.
- **NAO reports** — the National Audit Office reports on the MoD +
  Home Office + MoJ.
"""
from __future__ import annotations

import logging

from dlt_sources._cross.jurisdiction_pipeline_base import (
    JurisdictionPipelineBase,
)

logger = logging.getLogger(__name__)


LAW_ENFORCEMENT_STAGE: str = "law_enforcement"
ENGLAND_JURISDICTION: str = "england"


class EnglandLawEnforcementPipeline(JurisdictionPipelineBase):
    """England jurisdiction pipeline — law_enforcement vertical.

    SKELETON — `build_pipeline_resource()` is a placeholder until
    Phase 4 wires the per-source England defence + policing + intel
    oversight resources into the `sources.py` module below.
    """

    STAGE = LAW_ENFORCEMENT_STAGE

    def build_pipeline_resource(self):
        """Yield one row per (jurisdiction, stage, sub-vertical) cohort.

        TODO(2026-09-XX): wire the actual per-source England defence +
        policing + intel oversight resources. The Phase 4 wire-up
        carves `dlt_sources/cianchosaint/uk/{policing,military,
        intelligence_oversight,intelligence_agencies,government}/`
        into `dlt_sources/law_enforcement/england/{defence,policing,
        intel_oversight,public_inquiries,emergency_services,nao}/`
        one sub-vertical per source family.
        """
        from .sources import england_law_enforcement_intelligence_sources

        source = england_law_enforcement_intelligence_sources()
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
                    f"({resource_name}) for England"
                ),
                "source_url": "",
                "display_name_en": f"England {resource_name}",
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


england_law_enforcement_pipeline = EnglandLawEnforcementPipeline(
    ENGLAND_JURISDICTION,
)


__all__ = [
    "EnglandLawEnforcementPipeline",
    "england_law_enforcement_pipeline",
    "LAW_ENFORCEMENT_STAGE",
    "ENGLAND_JURISDICTION",
]