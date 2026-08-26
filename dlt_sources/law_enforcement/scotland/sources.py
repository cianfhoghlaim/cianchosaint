"""Scotland per-jurisdiction law-enforcement intelligence sources.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.

Scotland has 6 sub-verticals (parity with England/Éire):
defence (UK-wide shared) + policing (Police Scotland devolved) +
intel oversight (shared IPCO) + public inquiries (devolved) +
emergency services (Scottish Ambulance Service + SFRS) +
audit reports (Audit Scotland, NOT NAO).
"""
from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt


SCOTLAND_LAW_ENFORCEMENT_SUBVERTICALS: tuple[str, ...] = (
    "defence",
    "policing",
    "intel_oversight",
    "public_inquiries",
    "emergency_services",
    "audit",
)


@dlt.resource(name="scotland_defence", write_disposition="merge", primary_key=["url", "language"])
def scotland_defence(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield UK MoD Scotland-specific defence rows (HMNB Clyde + Leuchars + Faslane).

    TODO(2026-09-XX): wire the UK MoD Scotland defence estate reports
    + HMNB Clyde (Faslane) published outputs + Leuchars Army Station
    + the Scottish Government's Defence Engagement annual report.
    Defence sources are UK-wide and SHARED with the England skeleton.
    """
    return iter([])


@dlt.resource(name="scotland_policing", write_disposition="merge", primary_key=["url", "language"])
def scotland_policing(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Police Scotland + Scottish Police Authority (SPA) rows.

    TODO(2026-09-XX): wire Police Scotland published FOI responses +
    SPA annual reports + HMICS (Her Majesty's Inspectorate of
    Constabulary in Scotland) inspection reports + the Police
    (Scotland) Act 2017 secondary legislation (which is the
    procedural rules → ciandlíthe).
    """
    return iter([])


@dlt.resource(name="scotland_intel_oversight", write_disposition="merge", primary_key=["url", "language"])
def scotland_intel_oversight(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield IPCO Scotland + Scottish Information Commissioner rows.

    TODO(2026-09-XX): wire the IPCO Annual Report Scotland section +
    the Scottish Information Commissioner's published oversight
    decisions on Scottish intelligence bodies (e.g. Police Scotland
    intelligence function).
    """
    return iter([])


@dlt.resource(name="scotland_public_inquiries", write_disposition="merge", primary_key=["url", "language"])
def scotland_public_inquiries(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Scottish devolved public-inquiry final reports.

    TODO(2026-09-XX): wire the Scottish COVID-19 Inquiry + the
    Edinburgh Tram Inquiry + future devolved inquiries. The
    Inquiries (Scotland) Rules 2007 (the procedural rules) →
    ciandlíthe; the inquiry REPORTS → here.
    """
    return iter([])


@dlt.resource(name="scotland_emergency_services", write_disposition="merge", primary_key=["url", "language"])
def scotland_emergency_services(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Scottish Ambulance Service + SFRS + MCA + mountain rescue rows.

    TODO(2026-09-XX): wire the Scottish Ambulance Service annual
    reports + the Scottish Fire and Rescue Service annual reports +
    the Maritime & Coastguard Agency (shared with England).
    """
    return iter([])


@dlt.resource(name="scotland_audit", write_disposition="merge", primary_key=["url", "language"])
def scotland_audit(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Audit Scotland reports on justice + police + fire + ambulance.

    TODO(2026-09-XX): wire Audit Scotland reports on Police
    Scotland + Scottish Fire + Scottish Ambulance + the Scottish
    Courts and Tribunals Service. Audit Scotland uses a paginated
    publication list — Firecrawl map + paginated scrape.
    """
    return iter([])


@dlt.source(name="scotland_law_enforcement_intelligence")
def scotland_law_enforcement_intelligence_sources(
    language: str = "en",
) -> list[Any]:
    """Scotland BI law-enforcement + civil-protection intelligence source."""
    return [
        scotland_defence(language=language),
        scotland_policing(language=language),
        scotland_intel_oversight(language=language),
        scotland_public_inquiries(language=language),
        scotland_emergency_services(language=language),
        scotland_audit(language=language),
    ]


__all__ = [
    "SCOTLAND_LAW_ENFORCEMENT_SUBVERTICALS",
    "scotland_defence",
    "scotland_policing",
    "scotland_intel_oversight",
    "scotland_public_inquiries",
    "scotland_emergency_services",
    "scotland_audit",
    "scotland_law_enforcement_intelligence_sources",
]