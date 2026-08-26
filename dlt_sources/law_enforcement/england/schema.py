"""England law-enforcement pydantic schemas (skeleton).

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.
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
    "nao",
]


class EnglandLawEnforcementRow(BaseModel):
    """Canonical England law-enforcement intelligence row."""

    source_id: str
    country_code: Literal["england"] = "england"
    jurisdiction: Literal["england"] = "england"
    education_stage: Literal["law_enforcement"] = "law_enforcement"
    sub_vertical: SubVertical
    language: Literal["en", "cy"] = "en"
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


__all__ = ["EnglandLawEnforcementRow", "SubVertical"]