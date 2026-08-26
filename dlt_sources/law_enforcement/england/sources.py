"""England per-jurisdiction law-enforcement intelligence sources.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.

SKELETON — the actual defence + policing + intelligence-oversight
sources live today in
`dlt_sources/cianchosaint/uk/{policing,military,intelligence_oversight,
intelligence_agencies,government}/` and are carved into this tree by
Phase 4 (6 → 12 months).
"""
from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt


ENGLAND_LAW_ENFORCEMENT_SUBVERTICALS: tuple[str, ...] = (
    "defence",
    "policing",
    "intel_oversight",
    "public_inquiries",
    "emergency_services",
    "nao",
)


@dlt.resource(
    name="england_defence",
    write_disposition="merge",
    primary_key=["url", "language"],
    columns={
        "jurisdiction": {"data_type": "text"},
        "sub_vertical": {"data_type": "text"},
        "language": {"data_type": "text"},
        "url": {"data_type": "text"},
        "title": {"data_type": "text"},
        "institution": {"data_type": "text"},
        "document_type": {"data_type": "text"},
        "region": {"data_type": "text"},
        "official_status": {"data_type": "text"},
        "extracted_at": {"data_type": "timestamp"},
        "source": {"data_type": "text"},
        "source_file": {"data_type": "text"},
    },
)
def england_defence(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield UK MoD + RAF + RN + Army rows.

    TODO(2026-09-XX): wire the UK MoD Annual Reports + the JSP/JDP
    doctrine publications + the RAF/RN/Army press releases + the
    DE&S major projects reports. The existing sources at
    `dlt_sources/cianchosaint/uk/military/{mod,raf_press_releases,
    royal_navy_press_releases, british_army_press_releases,
    jsp_doctrine, jdp_doctrine}.py` are the Phase 4 carve targets.
    """
    return iter([])


@dlt.resource(
    name="england_policing",
    write_disposition="merge",
    primary_key=["url", "language"],
    columns={
        "jurisdiction": {"data_type": "text"},
        "sub_vertical": {"data_type": "text"},
        "language": {"data_type": "text"},
        "url": {"data_type": "text"},
        "title": {"data_type": "text"},
        "institution": {"data_type": "text"},
        "document_type": {"data_type": "text"},
        "region": {"data_type": "text"},
        "official_status": {"data_type": "text"},
        "extracted_at": {"data_type": "timestamp"},
        "source": {"data_type": "text"},
        "source_file": {"data_type": "text"},
    },
)
def england_policing(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield the 43 Home Office police forces + Met + City of London + BTP rows.

    TODO(2026-09-XX): wire the data.police.uk open data API (crimes
    + outcomes + street-level crime per month) + the Home Office
    Police Workforce England & Wales statistics + the Home Office
    Crime Outcomes statistics. The existing sources at
    `dlt_sources/cianchosaint/uk/policing/{data_police_uk,
    crime_statistics_uk, metropolitan_police_press_releases,
    police_workforce_uk, stop_and_search_uk}.py` are the Phase 4
    carve targets.
    """
    return iter([])


@dlt.resource(
    name="england_intel_oversight",
    write_disposition="merge",
    primary_key=["url", "language"],
    columns={
        "jurisdiction": {"data_type": "text"},
        "sub_vertical": {"data_type": "text"},
        "language": {"data_type": "text"},
        "url": {"data_type": "text"},
        "title": {"data_type": "text"},
        "institution": {"data_type": "text"},
        "document_type": {"data_type": "text"},
        "region": {"data_type": "text"},
        "official_status": {"data_type": "text"},
        "extracted_at": {"data_type": "timestamp"},
        "source": {"data_type": "text"},
        "source_file": {"data_type": "text"},
    },
)
def england_intel_oversight(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield IPCO + IPT + Biometrics Commissioner + ISC rows.

    TODO(2026-09-XX): wire the IPCO Annual Reports + the IPT
    published decisions + the Biometrics Commissioner annual
    reports + the ISC Annual Reports. The existing sources at
    `dlt_sources/cianchosaint/uk/intelligence_oversight/{ipco_reports,
    ipt_decisions, isc_annual_reports}.py` are the Phase 4 carve
    targets.
    """
    return iter([])


@dlt.resource(
    name="england_public_inquiries",
    write_disposition="merge",
    primary_key=["url", "language"],
    columns={
        "jurisdiction": {"data_type": "text"},
        "sub_vertical": {"data_type": "text"},
        "language": {"data_type": "text"},
        "url": {"data_type": "text"},
        "title": {"data_type": "text"},
        "institution": {"data_type": "text"},
        "document_type": {"data_type": "text"},
        "region": {"data_type": "text"},
        "official_status": {"data_type": "text"},
        "extracted_at": {"data_type": "timestamp"},
        "source": {"data_type": "text"},
        "source_file": {"data_type": "text"},
    },
)
def england_public_inquiries(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield UK COVID-19 Inquiry + Grenfell + Iraq Inquiry + Undercover Policing Inquiry rows.

    TODO(2026-09-XX): wire the UK COVID-19 Inquiry modules + the
    Grenfell Tower Inquiry final report + the Iraq Inquiry (Chilcot)
    + the Undercover Policing Inquiry + future UK inquiries. The
    Inquiries Act 2005 (the procedural rules) → ciandlíthe; the
    inquiry REPORTS are evidence-collection → here.
    """
    return iter([])


@dlt.resource(
    name="england_emergency_services",
    write_disposition="merge",
    primary_key=["url", "language"],
    columns={
        "jurisdiction": {"data_type": "text"},
        "sub_vertical": {"data_type": "text"},
        "language": {"data_type": "text"},
        "url": {"data_type": "text"},
        "title": {"data_type": "text"},
        "institution": {"data_type": "text"},
        "document_type": {"data_type": "text"},
        "region": {"data_type": "text"},
        "official_status": {"data_type": "text"},
        "extracted_at": {"data_type": "timestamp"},
        "source": {"data_type": "text"},
        "source_file": {"data_type": "text"},
    },
)
def england_emergency_services(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield London Ambulance + NPAS + MCA + FRS rows.

    TODO(2026-09-XX): wire the LAS published performance reports +
    the National Police Air Service + the Maritime & Coastguard
    Agency + the National Fire Chiefs Council + the Local
    Resilience Forums (LRFs).
    """
    return iter([])


@dlt.resource(
    name="england_nao",
    write_disposition="merge",
    primary_key=["url", "language"],
    columns={
        "jurisdiction": {"data_type": "text"},
        "sub_vertical": {"data_type": "text"},
        "language": {"data_type": "text"},
        "url": {"data_type": "text"},
        "title": {"data_type": "text"},
        "institution": {"data_type": "text"},
        "document_type": {"data_type": "text"},
        "region": {"data_type": "text"},
        "official_status": {"data_type": "text"},
        "extracted_at": {"data_type": "timestamp"},
        "source": {"data_type": "text"},
        "source_file": {"data_type": "text"},
    },
)
def england_nao(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield NAO reports on MoD + Home Office + MoJ.

    TODO(2026-09-XX): wire the NAO website reports on the MoD (e.g.
    "Carrier Strike: HMS Queen Elizabeth Class Aircraft Carriers"
    2024) + the Home Office + MoJ. The NAO has a paginated
    publication list — Firecrawl map + paginated scrape.
    """
    return iter([])


@dlt.source(name="england_law_enforcement_intelligence")
def england_law_enforcement_intelligence_sources(
    language: str = "en",
) -> list[Any]:
    """England BI law-enforcement + civil-protection intelligence source."""
    return [
        england_defence(language=language),
        england_policing(language=language),
        england_intel_oversight(language=language),
        england_public_inquiries(language=language),
        england_emergency_services(language=language),
        england_nao(language=language),
    ]


__all__ = [
    "ENGLAND_LAW_ENFORCEMENT_SUBVERTICALS",
    "england_defence",
    "england_policing",
    "england_intel_oversight",
    "england_public_inquiries",
    "england_emergency_services",
    "england_nao",
    "england_law_enforcement_intelligence_sources",
]