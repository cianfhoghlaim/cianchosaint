# CIANCHOSAINT — Politician cohort registry.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The politicians/
# cohort registry.
#
# Enumerates the 7 manual case-study politicians (per the user's verbatim
# request on 2026-09-06) plus the runtime `add_politician()` extension point
# so the bulk-harvested names from `harvest_politicians_from_leabharlann.py`
# can be appended at runtime.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.politicians._registry — cohort registry.

The canonical Politician cohort registry. Enumerates the 7 manual case
studies (Farage, Polanski, O'Dowd, Lyons, Givan, Robinson, Bird) +
exposes `add_politician()` so the bulk-harvested names from the
`harvest_politicians_from_leabharlann.py` script can be appended at runtime.

Cohort totals
-------------
- UK HoC:       2 case studies (Farage, Polanski) + Robinson (2024–)
- NI Assembly:  4 case studies (O'Dowd, Lyons, Givan, [Robinson pre-2024])
- Holyrood:     1 case study (Bird)
- ROI Dáil:     0 case studies (the user did not name any ROI TDs)
- Total manual: 7 (per the user's verbatim request)

The bulk-harvested politicians (per
`scripts/harvest_politicians_from_leabharlann.py`) are appended at runtime
via `add_politician()`.
"""

from __future__ import annotations

import logging
from typing import Any

from ._base import PoliticianCohort, VALID_JURISDICTIONS, VALID_PARTY_IDS

logger = logging.getLogger(__name__)


# ── THE COHORT GRID ──────────────────────────────────────────────────────
# 7 manual case-study politicians per the user's verbatim 2026-09-06 request.
_POLITICIANS: dict[str, PoliticianCohort] = {
    # === UK HoC × Reform UK ===
    "nigel_farage": PoliticianCohort(
        politician_id="nigel_farage",
        canonical_name="Nigel Farage",
        honorific="MP",
        party_id="reform-uk",
        party_name="Reform UK",
        jurisdiction="uk_hoc",
        constituency="Clacton",
        source_url="https://www.reformparty.uk/people/nigel-farage",
        electoral_commission_id=None,  # Reform UK MPs register individually
        theyworkforyou_id="nigel_farage/clacton",
        parliament_member_id="4677",
        official_website="https://www.nigelfarage.com",
        source_urls=[
            "https://www.reformparty.uk/people/nigel-farage",
            "https://www.nigelfarage.com",
        ],
        milestone_gate="cianchosaint:politician:bulk-resolve",
    ),
    # === UK HoC × Green Party of England and Wales (co-leader) ===
    "zack_polanski": PoliticianCohort(
        politician_id="zack_polanski",
        canonical_name="Zack Polanski",
        honorific="",
        party_id="green-party-ew",
        party_name="Green Party of England and Wales",
        jurisdiction="uk_hoc",
        constituency="",  # Co-leader; not currently a constituency MP
        source_url="https://greenparty.org.uk/people/zack-polanski",
        electoral_commission_id=None,
        theyworkforyou_id=None,
        parliament_member_id=None,
        official_website=None,  # Green co-leaders typically don't have personal sites
        source_urls=[
            "https://greenparty.org.uk/people/zack-polanski",
        ],
        milestone_gate="cianchosaint:politician:bulk-resolve",
    ),
    # === NI Assembly × Sinn Féin ===
    "john_o_dowd": PoliticianCohort(
        politician_id="john_o_dowd",
        canonical_name="John O'Dowd",
        honorific="MLA",
        party_id="sinn-fein",
        party_name="Sinn Féin",
        jurisdiction="ni_assembly",
        constituency="Upper Bann",
        source_url="https://www.sinnfein.ie/people/john-o-dowd",
        mla_id="",  # populate from NI Assembly API
        source_urls=[
            "https://www.sinnfein.ie/people/john-o-dowd",
            "https://www.niassembly.gov.uk/your-mlas/john-o-dowd",
        ],
        milestone_gate="cianchosaint:politician:bulk-resolve",
    ),
    # === NI Assembly × DUP ===
    "gordon_lyons": PoliticianCohort(
        politician_id="gordon_lyons",
        canonical_name="Gordon Lyons",
        honorific="MLA",
        party_id="dup",
        party_name="Democratic Unionist Party",
        jurisdiction="ni_assembly",
        constituency="East Antrim",
        source_url="https://mydup.com/people/gordon-lyons",
        mla_id="",
        source_urls=[
            "https://mydup.com/people/gordon-lyons",
            "https://www.niassembly.gov.uk/your-mlas/gordon-lyons",
        ],
        milestone_gate="cianchosaint:politician:bulk-resolve",
    ),
    # === NI Assembly × DUP ===
    "paul_givan": PoliticianCohort(
        politician_id="paul_givan",
        canonical_name="Paul Givan",
        honorific="MLA",
        party_id="dup",
        party_name="Democratic Unionist Party",
        jurisdiction="ni_assembly",
        constituency="Lagan Valley",
        source_url="https://mydup.com/people/paul-givan",
        mla_id="",
        source_urls=[
            "https://mydup.com/people/paul-givan",
            "https://www.niassembly.gov.uk/your-mlas/paul-givan",
        ],
        milestone_gate="cianchosaint:politician:bulk-resolve",
    ),
    # === UK HoC × DUP (Robinson was MP for Belfast East 2015–2024; 2024 general
    #     election he moved to North Down but lost; the user references him as
    #     "gavin robinson dup" — the canonical record keeps him in the DUP
    #     cohort and notes the constituency change) ===
    "gavin_robinson": PoliticianCohort(
        politician_id="gavin_robinson",
        canonical_name="Gavin Robinson",
        honorific="MP",
        party_id="dup",
        party_name="Democratic Unionist Party",
        jurisdiction="uk_hoc",
        constituency="Belfast East",  # 2015–2024
        source_url="https://mydup.com/people/gavin-robinson",
        theyworkforyou_id="gavin_robinson/belfast-east",
        parliament_member_id="4582",
        source_urls=[
            "https://mydup.com/people/gavin-robinson",
            "https://www.parliament.uk/biographies/commons/mr-gavin-robinson/4582",
        ],
        milestone_gate="cianchosaint:politician:bulk-resolve",
    ),
    # === Holyrood × SNP ===
    "lara_bird": PoliticianCohort(
        politician_id="lara_bird",
        canonical_name="Lara Bird",
        honorific="MSP",
        party_id="snp",
        party_name="Scottish National Party",
        jurisdiction="holyrood",
        constituency="East Lothian",
        source_url="https://www.snp.org/people/lara-bird",
        msp_id="",  # populate from Scottish Parliament API
        source_urls=[
            "https://www.snp.org/people/lara-bird",
            "https://www.parliament.scot/msps/electors/17683",
        ],
        milestone_gate="cianchosaint:politician:bulk-resolve",
    ),
}


def POLITICIAN_REGISTRY() -> list[PoliticianCohort]:
    """Return the list of all registered politicians (snapshot at call time)."""
    return list(_POLITICIANS.values())


def list_politicians() -> list[PoliticianCohort]:
    """Return the list of all registered politicians (snapshot at call time)."""
    return POLITICIAN_REGISTRY()


def list_politicians_by_party(party_id: str) -> list[PoliticianCohort]:
    """Return all politicians in the given party."""
    return [p for p in _POLITICIANS.values() if p.party_id == party_id]


def list_politicians_by_jurisdiction(jurisdiction: str) -> list[PoliticianCohort]:
    """Return all politicians in the given jurisdiction."""
    if jurisdiction not in VALID_JURISDICTIONS:
        raise ValueError(f"jurisdiction {jurisdiction!r} is not in VALID_JURISDICTIONS")
    return [p for p in _POLITICIANS.values() if p.jurisdiction == jurisdiction]


def get_politician(politician_id: str) -> PoliticianCohort | None:
    """Return the politician with the given id, or None if not found."""
    return _POLITICIANS.get(politician_id)


def add_politician(
    cohort: PoliticianCohort,
    *,
    overwrite: bool = False,
) -> bool:
    """Add a politician to the registry.

    Args:
        cohort: the PoliticianCohort to add.
        overwrite: if True, replace an existing entry with the same politician_id.

    Returns:
        True if the politician was added (or overwritten); False if it was
        skipped because the id already exists and overwrite is False.
    """
    if cohort.party_id not in VALID_PARTY_IDS:
        raise ValueError(
            f"politician {cohort.politician_id!r}: party_id {cohort.party_id!r} is not in VALID_PARTY_IDS"
        )
    if cohort.jurisdiction not in VALID_JURISDICTIONS:
        raise ValueError(
            f"politician {cohort.politician_id!r}: jurisdiction {cohort.jurisdiction!r} is not in VALID_JURISDICTIONS"
        )

    if cohort.politician_id in _POLITICIANS and not overwrite:
        logger.info(
            "politician_already_in_registry",
            extra={"politician_id": cohort.politician_id, "skipped": True},
        )
        return False

    _POLITICIANS[cohort.politician_id] = cohort
    logger.info(
        "politician_added_to_registry",
        extra={
            "politician_id": cohort.politician_id,
            "party_id": cohort.party_id,
            "jurisdiction": cohort.jurisdiction,
            "overwrite": overwrite,
        },
    )
    return True


__all__ = [
    "POLITICIAN_REGISTRY",
    "add_politician",
    "get_politician",
    "list_politicians",
    "list_politicians_by_jurisdiction",
    "list_politicians_by_party",
]


if __name__ == "__main__":
    # Allow: python3 -m dlt_sources.cianchosaint.politicians._registry
    print(f"Politician registry: {len(list_politicians())} case-study politicians")
    for party in sorted({p.party_id for p in list_politicians()}):
        rows = list_politicians_by_party(party)
        print(f"  {party}: {len(rows)} politicians")
        for r in rows:
            print(f"    - {r.canonical_name} ({r.honorific}) [{r.jurisdiction}/{r.constituency}]")
