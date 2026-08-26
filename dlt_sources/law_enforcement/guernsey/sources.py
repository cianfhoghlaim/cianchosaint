"""Guernsey per-jurisdiction law-enforcement intelligence sources."""
from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt


GUERNSEY_LAW_ENFORCEMENT_SUBVERTICALS: tuple[str, ...] = (
    "defence",
    "policing",
    "intel_oversight",
    "public_inquiries",
    "emergency_services",
    "cag",
)


@dlt.resource(name="guernsey_defence", write_disposition="merge", primary_key=["url", "language"])
def guernsey_defence(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield UK MoD Guernsey-related defence rows.

    TODO(2026-09-XX): wire UK MoD Guernsey-related defence engagement
    reports. Guernsey has no standing UK military base; defence is
    provided by the UK via treaty. Includes the Royal Court of
    Guernsey's defence-related civil contingencies cooperation.
    """
    return iter([])


@dlt.resource(name="guernsey_policing", write_disposition="merge", primary_key=["url", "language"])
def guernsey_policing(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Guernsey Police + BGLE + Customs + Immigration rows.

    TODO(2026-09-XX): wire the Guernsey Police published reports +
    the Bailiwick of Guernsey Law Enforcement (BGLE) annual reports
    + the Customs and Immigration Service. The existing source at
    `dlt_sources/cianchosaint/crown_dependencies/guernsey_policing.py`
    is the Phase 4 carve target.
    """
    return iter([])


@dlt.resource(name="guernsey_intel_oversight", write_disposition="merge", primary_key=["url", "language"])
def guernsey_intel_oversight(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Guernsey IPA + Data Protection rows.

    TODO(2026-09-XX): wire the Guernsey IPA Annual Reports + the
    Office of the Data Protection Authority (ODPA) for the
    Bailiwick of Guernsey.
    """
    return iter([])


@dlt.resource(name="guernsey_public_inquiries", write_disposition="merge", primary_key=["url", "language"])
def guernsey_public_inquiries(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Guernsey public-inquiry final reports.

    TODO(2026-09-XX): wire the Guernsey Inquiry into Child Sexual
    Abuse + future Bailiwick inquiries.
    """
    return iter([])


@dlt.resource(name="guernsey_emergency_services", write_disposition="merge", primary_key=["url", "language"])
def guernsey_emergency_services(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Guernsey Ambulance + Fire + Coastguard rows.

    TODO(2026-09-XX): wire the Guernsey Ambulance & Rescue Service
    + the Guernsey Fire & Rescue + the Channel Islands Coastguard
    (a Jersey/Guernsey joint body).
    """
    return iter([])


@dlt.resource(name="guernsey_cag", write_disposition="merge", primary_key=["url", "language"])
def guernsey_cag(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield C&AG of the Bailiwick of Guernsey reports.

    TODO(2026-09-XX): wire the C&AG of the Bailiwick of Guernsey
    Annual Reports + performance audit reports on the
    Justice Department (Guernsey).
    """
    return iter([])


@dlt.source(name="guernsey_law_enforcement_intelligence")
def guernsey_law_enforcement_intelligence_sources(
    language: str = "en",
) -> list[Any]:
    """Guernsey BI law-enforcement + civil-protection intelligence source."""
    return [
        guernsey_defence(language=language),
        guernsey_policing(language=language),
        guernsey_intel_oversight(language=language),
        guernsey_public_inquiries(language=language),
        guernsey_emergency_services(language=language),
        guernsey_cag(language=language),
    ]


__all__ = [
    "GUERNSEY_LAW_ENFORCEMENT_SUBVERTICALS",
    "guernsey_defence",
    "guernsey_policing",
    "guernsey_intel_oversight",
    "guernsey_public_inquiries",
    "guernsey_emergency_services",
    "guernsey_cag",
    "guernsey_law_enforcement_intelligence_sources",
]