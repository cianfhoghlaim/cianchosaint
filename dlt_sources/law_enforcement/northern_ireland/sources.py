"""NI per-jurisdiction law-enforcement intelligence sources.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.
"""
from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt


NORTHERN_IRELAND_LAW_ENFORCEMENT_SUBVERTICALS: tuple[str, ...] = (
    "defence",
    "policing",
    "intel_oversight",
    "public_inquiries",
    "emergency_services",
    "niao",
)


@dlt.resource(name="northern_ireland_defence", write_disposition="merge", primary_key=["url", "language"])
def northern_ireland_defence(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield UK MoD NI-specific defence rows (Aldergrove + Ballykinler + Lisburn).

    TODO(2026-09-XX): wire the UK MoD NI defence estate reports +
    Aldergrove (now renamed Aldergrove Flying Station) +
    Ballykinler Training Area + Lisburn (former army base).
    Defence is UK-wide shared but the NI-specific estate is local.
    """
    return iter([])


@dlt.resource(name="northern_ireland_policing", write_disposition="merge", primary_key=["url", "language"])
def northern_ireland_policing(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield PSNI + NI Policing Board + DOJ(NI) rows.

    TODO(2026-09-XX): wire the PSNI published FOI responses +
    NI Policing Board annual reports + DOJ(NI) oversight reports.
    The existing sources at
    `dlt_sources/cianchosaint/ni/{psni_press_releases,
    policing_board_ni, justice_ni}.py` are the Phase 4 carve targets.
    """
    return iter([])


@dlt.resource(name="northern_ireland_intel_oversight", write_disposition="merge", primary_key=["url", "language"])
def northern_ireland_intel_oversight(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield IPCO NI + NI Policing Board + NIHRC + MI5 oversight rows.

    TODO(2026-09-XX): wire the IPCO Annual Report NI section +
    the NI Policing Board's published oversight reports + the
    Northern Ireland Human Rights Commission's annual reports +
    the MI5 transparency reports (NI arm).
    """
    return iter([])


@dlt.resource(name="northern_ireland_public_inquiries", write_disposition="merge", primary_key=["url", "language"])
def northern_ireland_public_inquiries(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield NI-specific public-inquiry final reports.

    TODO(2026-09-XX): wire the UK COVID-19 Inquiry NI Module +
    the Historical Institutional Abuse Inquiry (HIA) + the
    Muckamore Abbey Hospital Inquiry + the Patrick Finucane
    case-related inquiries. The Inquiries Act 2005 → ciandlíthe;
    the inquiry REPORTS → here.
    """
    return iter([])


@dlt.resource(name="northern_ireland_emergency_services", write_disposition="merge", primary_key=["url", "language"])
def northern_ireland_emergency_services(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield NIAS + NIFRS + NI Community Safety + MCA rows.

    TODO(2026-09-XX): wire the Northern Ireland Ambulance Service
    published performance reports + the Northern Ireland Fire &
    Rescue Service annual reports + the NI Community Safety
    partnerships.
    """
    return iter([])


@dlt.resource(name="northern_ireland_niao", write_disposition="merge", primary_key=["url", "language"])
def northern_ireland_niao(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield NI Audit Office reports on PSNI + NIFRS + NIAS + DOJ(NI).

    TODO(2026-09-XX): wire the NIAO reports on the PSNI + NIFRS
    + NIAS + DOJ(NI). The NIAO has a paginated publication list.
    """
    return iter([])


@dlt.source(name="northern_ireland_law_enforcement_intelligence")
def northern_ireland_law_enforcement_intelligence_sources(
    language: str = "en",
) -> list[Any]:
    """Northern Ireland BI law-enforcement + civil-protection intelligence source."""
    return [
        northern_ireland_defence(language=language),
        northern_ireland_policing(language=language),
        northern_ireland_intel_oversight(language=language),
        northern_ireland_public_inquiries(language=language),
        northern_ireland_emergency_services(language=language),
        northern_ireland_niao(language=language),
    ]


__all__ = [
    "NORTHERN_IRELAND_LAW_ENFORCEMENT_SUBVERTICALS",
    "northern_ireland_defence",
    "northern_ireland_policing",
    "northern_ireland_intel_oversight",
    "northern_ireland_public_inquiries",
    "northern_ireland_emergency_services",
    "northern_ireland_niao",
    "northern_ireland_law_enforcement_intelligence_sources",
]