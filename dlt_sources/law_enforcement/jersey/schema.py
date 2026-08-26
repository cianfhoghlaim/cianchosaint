"""Jersey law-enforcement pydantic schemas (skeleton)."""
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


class JerseyLawEnforcementRow(BaseModel):
    """Canonical Jersey law-enforcement intelligence row."""

    source_id: str
    country_code: Literal["jersey"] = "jersey"
    jurisdiction: Literal["jersey"] = "jersey"
    education_stage: Literal["law_enforcement"] = "law_enforcement"
    sub_vertical: SubVertical
    language: Literal["en", "fr"] = "en"
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


__all__ = ["JerseyLawEnforcementRow", "SubVertical"]