"""Ireland per-jurisdiction law-enforcement intelligence sources.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.

SKELETON — the actual defence + policing + intelligence-oversight
sources live today in
`dlt_sources/cianchosaint/ireland/{defence_forces,law}/` and are
carved into this tree by Phase 4 (6 → 12 months).

## The 6 sub-verticals

| Sub-vertical | Today lives at | Phase 4 carve target |
|---|---|---|
| Defence forces | `cianchosaint/ireland/defence_forces/` | `law_enforcement/ireland/defence/` |
| Policing | `cianchosaint/ireland/law/` (subset) | `law_enforcement/ireland/policing/` |
| Intel oversight | `cianchosaint/ireland/law/` (subset) | `law_enforcement/ireland/intel_oversight/` |
| Public inquiries | (new) | `law_enforcement/ireland/public_inquiries/` |
| Emergency services | (new) | `law_enforcement/ireland/emergency_services/` |
| C&AG reports | (new) | `law_enforcement/ireland/cag/` |

## TODO markers

Each sub-vertical below has a `TODO(2026-09-XX):` marker with a
specific follow-up so a future agent knows the exact next step.
"""
from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt


# ─── The 6 sub-verticals ──────────────────────────────────────────────────

IRELAND_LAW_ENFORCEMENT_SUBVERTICALS: tuple[str, ...] = (
    "defence",
    "policing",
    "intel_oversight",
    "public_inquiries",
    "emergency_services",
    "cag",
)


# ─── Per-sub-vertical resource stubs ──────────────────────────────────────
# Each resource is a SKELETON `@dlt.resource` with `write_disposition="merge"`
# + a per-resource `primary_key`. The TODO marker names the exact
# follow-up that wires the real source.


@dlt.resource(
    name="ireland_defence",
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
def ireland_defence(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Irish Defence Forces (IDF + Air Corps + Naval Service) rows.

    TODO(2026-09-XX): wire An Garda Síochána + the Defence Forces
    Press Office releases + the White Paper on Defence (2015) +
    the Commission on the Defence Forces report (2022) once the
    `.ie` data portal scraper is built. The existing source at
    `dlt_sources/cianchosaint/ireland/defence_forces/idf_press_releases.py`
    is the Phase 4 carve target.
    """
    return iter([])  # SKELETON — no rows emitted until Phase 4 wires the real source


@dlt.resource(
    name="ireland_policing",
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
def ireland_policing(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield An Garda Síochána + GSOC + Policing Authority rows.

    TODO(2026-09-XX): wire An Garda Síochána FOI requests + GSOC
    investigation summaries + Policing Authority annual reports
    once the `.ie` data portal scraper is built. PULSE per-incident
    records are OUT OF SCOPE (per osint_allowlist.yaml — only
    published aggregates permitted).
    """
    return iter([])  # SKELETON


@dlt.resource(
    name="ireland_intel_oversight",
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
def ireland_intel_oversight(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Garda Inspectorate + Department of Justice oversight rows.

    TODO(2026-09-XX): wire the Garda Inspectorate published
    inspection reports + the Department of Justice oversight
    committee reports + the Policing Authority reports. The
    Special Criminal Court is OUT OF SCOPE (court-facing procedural
    rules → ciandlíthe).
    """
    return iter([])  # SKELETON


@dlt.resource(
    name="ireland_public_inquiries",
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
def ireland_public_inquiries(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield public-inquiry final reports + interim reports + terms of reference.

    TODO(2026-09-XX): wire the Mother & Baby Homes Commission of
    Investigation + the Stardust Tribunal + the Covid-19 Nursing
    Homes Expert Panel + future tribunals. The Commission of
    Investigation Act 2004 (the procedural rules) → ciandlíthe;
    the inquiry REPORTS are evidence-collection → here.
    """
    return iter([])  # SKELETON


@dlt.resource(
    name="ireland_emergency_services",
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
def ireland_emergency_services(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield HSE + NAS + Coast Guard + Defence Forces ATCP rows.

    TODO(2026-09-XX): wire the HSE emergency planning docs + the
    National Ambulance Service published performance reports +
    the Coast Guard annual reports + the Defence Forces Aid to
    the Civil Power (ATCP) annual reports.
    """
    return iter([])  # SKELETON


@dlt.resource(
    name="ireland_cag",
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
def ireland_cag(language: str = "en") -> Iterator[dict[str, Any]]:
    """Yield Comptroller and Auditor General reports on Éire Votes.

    TODO(2026-09-XX): wire the C&AG annual reports on the Defence
    Vote (Vote 36) + Justice Vote (Vote 24) + Policing Authority
    Vote (Vote 20) + HSE Vote (Vote 40). The C&AG website has a
    paginated publication list — Firecrawl map + paginated scrape.
    """
    return iter([])  # SKELETON


# ─── The per-jurisdiction @dlt.source aggregator ──────────────────────────


@dlt.source(name="ireland_law_enforcement_intelligence")
def ireland_law_enforcement_intelligence_sources(
    language: str = "en",
) -> list[Any]:
    """Éire BI law-enforcement + civil-protection intelligence source.

    Returns the 6 per-sub-vertical `@dlt.resource` stubs that compose
    the canonical Éire law-enforcement intelligence surface:

    1. `ireland_defence` — Irish Defence Forces (IDF + Air Corps + Naval)
    2. `ireland_policing` — An Garda Síochána + GSOC + Policing Authority
    3. `ireland_intel_oversight` — Garda Inspectorate + DoJ oversight
    4. `ireland_public_inquiries` — Tribunals of Investigation
    5. `ireland_emergency_services` — HSE + NAS + Coast Guard + ATCP
    6. `ireland_cag` — C&AG reports on Defence + Justice + Policing Votes

    Per the cianfhoghlaim JurisdictionPipelineBase §6.3 (dlt 1.30
    `.add_limit(1)`): the smoke test runs this source with `.add_limit(1)`
    on each resource so CI finishes in seconds.
    """
    return [
        ireland_defence(language=language),
        ireland_policing(language=language),
        ireland_intel_oversight(language=language),
        ireland_public_inquiries(language=language),
        ireland_emergency_services(language=language),
        ireland_cag(language=language),
    ]


__all__ = [
    "IRELAND_LAW_ENFORCEMENT_SUBVERTICALS",
    "ireland_defence",
    "ireland_policing",
    "ireland_intel_oversight",
    "ireland_public_inquiries",
    "ireland_emergency_services",
    "ireland_cag",
    "ireland_law_enforcement_intelligence_sources",
]