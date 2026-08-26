"""Isle of Man per-jurisdiction law-enforcement intelligence sources."""
from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt


ISLE_OF_MAN_LAW_ENFORCEMENT_SUBVERTICALS: tuple[str, ...] = (
    "defence",
    "policing",
    "intel_oversight",
    "public_inquiries",
    "emergency_services",
    "audit",
)


@dlt.resource(name="isle_of_man_defence", write_disposition="merge", primary_key=["url", "language"])
def isle_of_man_defence(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield UK MoD IoM-related defence rows (RAF base + radar station).

    TODO(2026-09-XX): wire UK MoD Isle of Man defence engagement
    reports. The RAF Valley (in Wales) is the closest training
    area; the IoM has a Civil Defence Corps under the Home Office.
    """
    return iter([])


@dlt.resource(name="isle_of_man_policing", write_disposition="merge", primary_key=["url", "language"])
def isle_of_man_policing(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Isle of Man Constabulary + Customs + Immigration rows.

    TODO(2026-09-XX): wire the IoM Constabulary annual reports +
    the Customs & Excise Division + the Financial Services
    Authority AML oversight. The existing source at
    `dlt_sources/cianchosaint/crown_dependencies/isle_of_man_policing.py`
    is the Phase 4 carve target.
    """
    return iter([])


@dlt.resource(name="isle_of_man_intel_oversight", write_disposition="merge", primary_key=["url", "language"])
def isle_of_man_intel_oversight(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield IoM Data Protection Registrar + Information Commissioner rows.

    TODO(2026-09-XX): wire the Isle of Man Data Protection
    Registrar Annual Reports + the Information Commissioner's
    published oversight decisions.
    """
    return iter([])


@dlt.resource(name="isle_of_man_public_inquiries", write_disposition="merge", primary_key=["url", "language"])
def isle_of_man_public_inquiries(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield IoM Tynwald-level public-inquiry final reports.

    TODO(2026-09-XX): wire any historical Tynwald Inquiry reports
    + future devolved inquiries. The Tynwald is the IoM parliament.
    """
    return iter([])


@dlt.resource(name="isle_of_man_emergency_services", write_disposition="merge", primary_key=["url", "language"])
def isle_of_man_emergency_services(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield IoM Ambulance + Fire + Coastguard + Civil Defence rows.

    TODO(2026-09-XX): wire the Isle of Man Ambulance Service +
    the Isle of Man Fire & Rescue Service + the Isle of Man
    Coastguard + the IoM Civil Defence Corps.
    """
    return iter([])


@dlt.resource(name="isle_of_man_audit", write_disposition="merge", primary_key=["url", "language"])
def isle_of_man_audit(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Tynwald General Audit Committee + IoM Audit Office reports.

    TODO(2026-09-XX): wire the Tynwald General Audit Committee
    Annual Reports + the Audit Office's performance audit reports
    on the Department of Home Affairs + the Isle of Man Police.
    """
    return iter([])


@dlt.source(name="isle_of_man_law_enforcement_intelligence")
def isle_of_man_law_enforcement_intelligence_sources(
    language: str = "en",
) -> list[Any]:
    """Isle of Man BI law-enforcement + civil-protection intelligence source."""
    return [
        isle_of_man_defence(language=language),
        isle_of_man_policing(language=language),
        isle_of_man_intel_oversight(language=language),
        isle_of_man_public_inquiries(language=language),
        isle_of_man_emergency_services(language=language),
        isle_of_man_audit(language=language),
    ]


__all__ = [
    "ISLE_OF_MAN_LAW_ENFORCEMENT_SUBVERTICALS",
    "isle_of_man_defence",
    "isle_of_man_policing",
    "isle_of_man_intel_oversight",
    "isle_of_man_public_inquiries",
    "isle_of_man_emergency_services",
    "isle_of_man_audit",
    "isle_of_man_law_enforcement_intelligence_sources",
]