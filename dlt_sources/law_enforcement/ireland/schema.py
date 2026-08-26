"""Ireland law-enforcement pydantic schemas (skeleton).

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.

SKELETON — the schemas below mirror the `cianfhoghlaim
education.<subject>` row shape (`subject_to_row()` from
`JurisdictionPipelineBase`). They are placeholders until Phase 4
wires the actual per-sub-vertical sources.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field


SubVertical = Literal[
    "defence",
    "policing",
    "intel_oversight",
    "public_inquiries",
    "emergency_services",
    "cag",
]


class IrelandLawEnforcementRow(BaseModel):
    """Canonical Éire law-enforcement intelligence row.

    Mirrors the `subject_to_row()` output contract from
    `dlt_sources/_cross/jurisdiction_pipeline_base.py`.
    """

    source_id: str
    country_code: Literal["ireland"] = "ireland"
    jurisdiction: Literal["ireland"] = "ireland"
    education_stage: Literal["law_enforcement"] = "law_enforcement"
    sub_vertical: SubVertical
    language: Literal["en", "ga"] = "en"
    url: str
    title: str
    institution: str
    document_type: str
    region: str = "british_isles"
    official_status: str = "published"
    extracted_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
    )
    source: str
    source_file: str = ""


__all__ = [
    "IrelandLawEnforcementRow",
    "SubVertical",
]