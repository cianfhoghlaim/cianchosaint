"""Jersey per-jurisdiction law-enforcement intelligence sources."""
from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt


JERSEY_LAW_ENFORCEMENT_SUBVERTICALS: tuple[str, ...] = (
    "defence",
    "policing",
    "intel_oversight",
    "public_inquiries",
    "emergency_services",
    "cag",
)


@dlt.resource(name="jersey_defence", write_disposition="merge", primary_key=["url", "language"])
def jersey_defence(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield UK MoD Jersey-related defence rows (British Forces Gibraltar + Jersey).

    TODO(2026-09-XX): wire UK MoD Jersey-related defence engagement
    reports. Jersey has no standing UK military base; defence is
    provided by the UK via treaty.
    """
    return iter([])


@dlt.resource(name="jersey_policing", write_disposition="merge", primary_key=["url", "language"])
def jersey_policing(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield States of Jersey Police + Customs + Immigration rows.

    TODO(2026-09-XX): wire the States of Jersey Police annual
    reports + the Customs and Immigration Service annual reports
    + the JFSC (Jersey Financial Services Commission) AML oversight.
    The existing source at
    `dlt_sources/cianchosaint/crown_dependencies/jersey_policing.py`
    is the Phase 4 carve target.
    """
    return iter([])


@dlt.resource(name="jersey_intel_oversight", write_disposition="merge", primary_key=["url", "language"])
def jersey_intel_oversight(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Jersey Investigatory Powers Authority + Data Protection rows.

    TODO(2026-09-XX): wire the Jersey IPA Annual Reports + the
    Jersey Office of the Information Commissioner (JOIC).
    """
    return iter([])


@dlt.resource(name="jersey_public_inquiries", write_disposition="merge", primary_key=["url", "language"])
def jersey_public_inquiries(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Jersey States of Jersey public-inquiry final reports.

    TODO(2026-09-XX): wire the Jersey Care Inquiry + the Jersey
    Child Protection Inquiry (historical). Future inquiries will
    be added as they're announced.
    """
    return iter([])


@dlt.resource(name="jersey_emergency_services", write_disposition="merge", primary_key=["url", "language"])
def jersey_emergency_services(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Jersey Ambulance + Fire + Coastguard + Honorary Police rows.

    TODO(2026-09-XX): wire the Jersey Ambulance Service annual
    reports + the Jersey Fire & Rescue Service + the Jersey
    Coastguard + the Honorary Police (the parish-level
    policing-by-the-community tradition).
    """
    return iter([])


@dlt.resource(name="jersey_cag", write_disposition="merge", primary_key=["url", "language"])
def jersey_cag(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Jersey Comptroller and Auditor General reports.

    TODO(2026-09-XX): wire the Jersey C&AG Annual Report + the
    Jersey Audit Office performance audit reports on Justice
    Department + Home Affairs Department.
    """
    return iter([])


@dlt.source(name="jersey_law_enforcement_intelligence")
def jersey_law_enforcement_intelligence_sources(
    language: str = "en",
) -> list[Any]:
    """Jersey BI law-enforcement + civil-protection intelligence source."""
    return [
        jersey_defence(language=language),
        jersey_policing(language=language),
        jersey_intel_oversight(language=language),
        jersey_public_inquiries(language=language),
        jersey_emergency_services(language=language),
        jersey_cag(language=language),
    ]


__all__ = [
    "JERSEY_LAW_ENFORCEMENT_SUBVERTICALS",
    "jersey_defence",
    "jersey_policing",
    "jersey_intel_oversight",
    "jersey_public_inquiries",
    "jersey_emergency_services",
    "jersey_cag",
    "jersey_law_enforcement_intelligence_sources",
]