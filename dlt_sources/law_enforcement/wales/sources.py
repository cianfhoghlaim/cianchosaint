"""Wales per-jurisdiction law-enforcement intelligence sources.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.

Wales has 4 police forces (Dyfed-Powys + Gwent + North Wales + South
Wales) — devolved policing. Defence is UK-wide shared. Audit is Wales
Audit Office (NOT NAO). Bilingual Welsh-medium (cy) coverage required
for the public-facing data.
"""
from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt


WALES_LAW_ENFORCEMENT_SUBVERTICALS: tuple[str, ...] = (
    "defence",
    "policing",
    "intel_oversight",
    "public_inquiries",
    "emergency_services",
    "wao",
)


@dlt.resource(name="wales_defence", write_disposition="merge", primary_key=["url", "language"])
def wales_defence(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield UK MoD Wales-specific defence rows (Sennybridge + Castlemartin + Brecon).

    TODO(2026-09-XX): wire the UK MoD Wales defence estate reports
    + Sennybridge Training Area + Castlemartin Range + Brecon
    Mountain Rescue (military-trained) + the Welsh Government's
    Defence Engagement annual report (cy).
    """
    return iter([])


@dlt.resource(name="wales_policing", write_disposition="merge", primary_key=["url", "language"])
def wales_policing(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield the 4 Welsh police forces + HMICFRS rows.

    TODO(2026-09-XX): wire the 4 Welsh forces (Dyfed-Powys + Gwent
    + North Wales + South Wales) published FOI responses +
    HMICFRS Wales inspection reports + bilingual (cy) data.police.uk
    street-level crime per month.
    """
    return iter([])


@dlt.resource(name="wales_intel_oversight", write_disposition="merge", primary_key=["url", "language"])
def wales_intel_oversight(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield IPCO Wales + Welsh Information Commissioner rows.

    TODO(2026-09-XX): wire the IPCO Annual Report Wales section +
    the Welsh Information Commissioner's published oversight
    decisions on Welsh intelligence bodies.
    """
    return iter([])


@dlt.resource(name="wales_public_inquiries", write_disposition="merge", primary_key=["url", "language"])
def wales_public_inquiries(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Wales devolved public-inquiry final reports.

    TODO(2026-09-XX): wire the Welsh Infected Blood Inquiry (the
    Wales-specific arm of the UK inquiry) + future Welsh
    inquiries. Bilingual Welsh-medium publication is the canonical
    requirement.
    """
    return iter([])


@dlt.resource(name="wales_emergency_services", write_disposition="merge", primary_key=["url", "language"])
def wales_emergency_services(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Welsh Ambulance Services + Mid + West Wales + South Wales FRS rows.

    TODO(2026-09-XX): wire the Welsh Ambulance Services NHS Trust
    published performance reports + the 3 Welsh Fire & Rescue
    Services (Mid + West Wales + South Wales + North Wales).
    """
    return iter([])


@dlt.resource(name="wales_wao", write_disposition="merge", primary_key=["url", "language"])
def wales_wao(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Wales Audit Office reports on police + fire + ambulance + justice.

    TODO(2026-09-XX): wire Wales Audit Office reports on the 4
    Welsh police forces + Welsh Fire + Welsh Ambulance. WAO uses
    a paginated publication list — Firecrawl map + paginated scrape.
    """
    return iter([])


@dlt.source(name="wales_law_enforcement_intelligence")
def wales_law_enforcement_intelligence_sources(
    language: str = "en",
) -> list[Any]:
    """Wales BI law-enforcement + civil-protection intelligence source."""
    return [
        wales_defence(language=language),
        wales_policing(language=language),
        wales_intel_oversight(language=language),
        wales_public_inquiries(language=language),
        wales_emergency_services(language=language),
        wales_wao(language=language),
    ]


__all__ = [
    "WALES_LAW_ENFORCEMENT_SUBVERTICALS",
    "wales_defence",
    "wales_policing",
    "wales_intel_oversight",
    "wales_public_inquiries",
    "wales_emergency_services",
    "wales_wao",
    "wales_law_enforcement_intelligence_sources",
]