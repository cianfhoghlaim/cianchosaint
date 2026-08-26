"""Ireland jurisdiction pipeline — law_enforcement vertical.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change +
the parent change `2026-08-24-dlt-sources-to-multi-repo-scaffold-v1` §21.2.

SKELETON — the actual defence + policing + intelligence-oversight
sources for Éire live today in
`dlt_sources/cianchosaint/ireland/{defence_forces,law}/`. Phase 4
(6 → 12 months) carves them into this tree.

## What this skeleton covers (the Éire law-enforcement surface)

- **Defence forces** — Irish Defence Forces (IDF, including the Army +
  Air Corps + Naval Service); the Defence Forces Press Office releases;
  the Annual Report of the Secretary General of Defence; the
  White Paper on Defence (2015) + the Commission on the Defence Forces
  report (2022); the Defence Forces Joint Doctrine publications.
- **Policing** — An Garda Síochána (the national police); the Garda
  Síochána Inspectorate (GSI); the Garda Síochána Ombudsman Commission
  (GSOC); Policing Authority annual reports + inspection reports;
  PULSE data caveats (only published aggregates — never per-incident
  records).
- **Intelligence oversight** — the Garda Inspectorate + the Department
  of Justice + the Policing Authority; the Special Criminal Court
  (court-facing procedural rules → ciandlíthe, NOT here).
- **Public inquiries** — the Commission of Investigation (various
  historical); the Mother & Baby Homes Commission of Investigation;
  the Stardust Tribunal; the Covid-19 Nursing Homes Expert Panel.
- **Emergency services** — HSE emergency planning + the National
  Ambulance Service (NAS) + the Irish Coast Guard + the Defence Forces
  Aid to the Civil Power (ATCP).
- **C&AG reports** — Comptroller and Auditor General reports on the
  Defence Vote + Justice Vote + the Policing Authority Vote.

## Carve rule

Per the user-confirmed split (Q1): **evidence-collection for
law-enforcement purposes** goes to cianchosaint (this repo). Court-facing
procedural rules go to ciandlíthe. The `_factory.py` is a STAGE
sentinel, NOT a pipeline that runs today.

## KCG patterns used
- `JurisdictionPipelineBase` (per `.agents/skills/dlt/SKILL.md`) — the
  shared base class at `dlt_sources/_cross/jurisdiction_pipeline_base.py`.
- dlt 1.30 §6.3 (`.add_limit(1)`) + §6.4 (`retry_schema_update`) +
  §6.5 (`abort_packages`) are inherited from the base.
"""
from __future__ import annotations

import logging

from dlt_sources._cross.jurisdiction_pipeline_base import (
    JurisdictionPipelineBase,
)

logger = logging.getLogger(__name__)


# The canonical Éire law-enforcement stage (per the cianfhoghlaim
# JurisdictionPipelineBase VALID_STAGES — augmented by parent change §21.2).
LAW_ENFORCEMENT_STAGE: str = "law_enforcement"

# The 1 Éire jurisdiction
IRELAND_JURISDICTION: str = "ireland"


class IrelandLawEnforcementPipeline(JurisdictionPipelineBase):
    """Ireland jurisdiction pipeline — law_enforcement vertical.

    SKELETON — `build_pipeline_resource()` is a placeholder until
    Phase 4 wires the per-source Éire defence + policing + intel
    oversight resources into the `sources.py` module below.
    """

    STAGE = LAW_ENFORCEMENT_STAGE

    def build_pipeline_resource(self):
        """Yield one row per (jurisdiction, stage, sub-vertical) cohort.

        TODO(2026-09-XX): wire the actual per-source Éire defence +
        policing + intel oversight resources. The Phase 4 wire-up
        carves `dlt_sources/cianchosaint/ireland/{defence_forces,law}/`
        into `dlt_sources/law_enforcement/ireland/{defence,policing,
        intel_oversight,public_inquiries,emergency_services,cag}/`
        one sub-vertical per source family.
        """
        # Per the cianfhoghlaim JurisdictionPipelineBase.subject_to_row()
        # contract, the yielded dicts MUST carry the canonical
        # natural_key + source_id + jurisdiction + education_stage
        # (= "law_enforcement") fields. The skeleton yields 1 row
        # so the smoke test sees the jurisdiction wired.
        from .sources import ireland_law_enforcement_intelligence_sources

        source = ireland_law_enforcement_intelligence_sources()
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
                    f"({resource_name}) for Éire"
                ),
                "source_url": "",
                "display_name_en": f"Éire {resource_name}",
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


ireland_law_enforcement_pipeline = IrelandLawEnforcementPipeline(
    IRELAND_JURISDICTION,
)


__all__ = [
    "IrelandLawEnforcementPipeline",
    "ireland_law_enforcement_pipeline",
    "LAW_ENFORCEMENT_STAGE",
    "IRELAND_JURISDICTION",
]