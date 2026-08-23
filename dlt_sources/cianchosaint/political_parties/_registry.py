# CIANCHOSAINT new-build: per-political-party cohort registry.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The PoliticalPartyPipelineBase
#   class + the per-jurisdiction cohort registry, Scenario: The cohort
#   registry enumerates all 24 parties).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties._registry — cohort grid.

Phase 4 of the openspec change. Maintains the per-party cohort grid +
the milestone gate mapping for the BIPP v1 / BIDP v1 / BIIP v1 +
political-party vertical.

Usage::

    python -m dlt_sources.cianchosaint.political_parties._registry

Prints a table of every cohort (party_id × jurisdiction × source_url ×
cohort_id) with the milestone gate it unblocks + the active/dormant
flag (per the Electoral Commission register).

Cohort totals
-------------

- UK HoC              : 7 parties (reform-uk is the canonical pilot)
- ROI Dáil + Seanad   : 12 parties
- NI Assembly         : 7 parties
- Wales Senedd        : 4 parties (plaid-cymru has a separate UK-HoC source)
- Scotland Holyrood   : 5 parties (snp has a separate UK-HoC source)
- Crown Dependencies  : 3 parties (jsy / ggy / iom)

Total: 38 DLT source files / 24 unique parties (some parties appear
under multiple jurisdictions — they share party_id but ship different
scope files where the source URL diverges, e.g. ``snp.py`` UK-HoC vs
``snp_scottish.py`` Holyrood).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PartyCohort:
    """A single (party_id, jurisdiction, source_url, cohort_id) tuple + milestone gate."""

    party_id: str
    party_name: str
    jurisdiction: str
    source_url: str
    electoral_commission_id: str
    cohort_id: str
    milestone_gate: str
    extraction_function: str
    target_resource: str
    ingest_queue_subdir: str
    active: bool = True  # False for parties removed from the Electoral Commission register


# ── THE COHORT GRID ────────────────────────────────────────────────────
# 38 cohort rows: 7 UK-HoC + 12 ROI + 7 NI + 4 Wales + 5 Scotland +
# 3 Crown Dependencies. The 38 row count > 24 unique parties because
# some parties appear in multiple jurisdictions (Plaid Cymru in UK HoC
# + Senedd, SNP in UK HoC + Holyrood, Sinn Féin in ROI + NI).
COHORTS: tuple[PartyCohort, ...] = (
    # === UK HoC → BIPP v1 m1 ===
    PartyCohort(
        party_id="conservative-uk",
        party_name="Conservative and Unionist Party (UK)",
        jurisdiction="uk_hoc",
        source_url="https://www.conservatives.com/contact",
        electoral_commission_id="PP-10125",
        cohort_id="uk_hoc.conservative_uk",
        milestone_gate="BIPP v1 m1",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="uk_hoc/conservative/",
    ),
    PartyCohort(
        party_id="labour-uk",
        party_name="Labour Party (UK)",
        jurisdiction="uk_hoc",
        source_url="https://labour.org.uk/contact/",
        electoral_commission_id="PP-10116",
        cohort_id="uk_hoc.labour_uk",
        milestone_gate="BIPP v1 m1",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="uk_hoc/labour/",
    ),
    PartyCohort(
        party_id="liberal-democrats-uk",
        party_name="Liberal Democrats",
        jurisdiction="uk_hoc",
        source_url="https://www.libdems.org.uk/contact",
        electoral_commission_id="PP-10117",
        cohort_id="uk_hoc.liberal_democrats_uk",
        milestone_gate="BIPP v1 m1",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="uk_hoc/libdems/",
    ),
    PartyCohort(
        party_id="reform-uk",
        party_name="Reform UK",
        jurisdiction="uk_hoc",
        source_url="https://www.reformparty.uk/contact",
        electoral_commission_id="PP-12345",
        cohort_id="uk_hoc.reform_uk",
        milestone_gate="BIPP v1 m1 (canonical pilot)",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="uk_hoc/reform_uk/",
    ),
    PartyCohort(
        party_id="green-party-ew",
        party_name="Green Party of England and Wales",
        jurisdiction="uk_hoc",
        source_url="https://greenparty.org.uk/contact/",
        electoral_commission_id="PP-10123",
        cohort_id="uk_hoc.green_party_ew",
        milestone_gate="BIPP v1 m1",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="uk_hoc/green_party_ew/",
    ),
    PartyCohort(
        party_id="plaid-cymru",
        party_name="Plaid Cymru — Party of Wales (UK HoC scope)",
        jurisdiction="uk_hoc",
        source_url="https://www.partyof.wales/contact/",
        electoral_commission_id="PP-10115",
        cohort_id="uk_hoc.plaid_cymru",
        milestone_gate="BIPP v1 m1",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="uk_hoc/plaid_cymru/",
    ),
    PartyCohort(
        party_id="snp",
        party_name="Scottish National Party (UK HoC scope)",
        jurisdiction="uk_hoc",
        source_url="https://www.snp.org/contact/",
        electoral_commission_id="PP-10122",
        cohort_id="uk_hoc.snp",
        milestone_gate="BIPP v1 m1",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="uk_hoc/snp/",
    ),
    # === ROI Dáil + Seanad → BIPP v1 m2 ===
    PartyCohort(
        party_id="fianna-fail",
        party_name="Fianna Fáil",
        jurisdiction="roi_dail",
        source_url="https://www.fiannafail.ie/contact",
        electoral_commission_id="nil",
        cohort_id="roi.fianna_fail",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="roi/fianna_fail/",
    ),
    PartyCohort(
        party_id="fine-gael",
        party_name="Fine Gael",
        jurisdiction="roi_dail",
        source_url="https://www.finegael.ie/our-party/contact/",
        electoral_commission_id="nil",
        cohort_id="roi.fine_gael",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="roi/fine_gael/",
    ),
    PartyCohort(
        party_id="sinn-fein-roi",
        party_name="Sinn Féin (Republic of Ireland branch)",
        jurisdiction="roi_dail",
        source_url="https://www.sinnfein.ie/contact",
        electoral_commission_id="nil",
        cohort_id="roi.sinn_fein_roi",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="roi/sinn_fein/",
    ),
    PartyCohort(
        party_id="labour-roi",
        party_name="Irish Labour Party",
        jurisdiction="roi_dail",
        source_url="https://www.labour.ie/contact/",
        electoral_commission_id="nil",
        cohort_id="roi.labour_roi",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="roi/labour/",
    ),
    PartyCohort(
        party_id="social-democrats",
        party_name="Social Democrats (Ireland)",
        jurisdiction="roi_dail",
        source_url="https://www.socialdemocrats.ie/contact/",
        electoral_commission_id="nil",
        cohort_id="roi.social_democrats",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="roi/social_democrats/",
    ),
    PartyCohort(
        party_id="pbp-solidarity",
        party_name="People Before Profit–Solidarity (all-island)",
        jurisdiction="roi_dail",
        source_url="https://www.pbp.ie/contact/",
        electoral_commission_id="nil",
        cohort_id="roi.pbp_solidarity",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="roi/pbp_solidarity/",
    ),
    PartyCohort(
        party_id="green-party-roi",
        party_name="Green Party / Comhaontas Glas (Ireland)",
        jurisdiction="roi_dail",
        source_url="https://www.greenparty.ie/contact/",
        electoral_commission_id="nil",
        cohort_id="roi.green_party_roi",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="roi/green_party_roi/",
    ),
    PartyCohort(
        party_id="aontu",
        party_name="Aontú (all-island)",
        jurisdiction="roi_dail",
        source_url="https://aontu.ie/contact/",
        electoral_commission_id="nil",
        cohort_id="roi.aontu",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="roi/aontu/",
    ),
    PartyCohort(
        party_id="independent-ireland",
        party_name="Independent Ireland",
        jurisdiction="roi_dail",
        source_url="https://www.independentireland.ie/contact",
        electoral_commission_id="nil",
        cohort_id="roi.independent_ireland",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="roi/independent_ireland/",
    ),
    PartyCohort(
        party_id="irish-freedom-party",
        party_name="Irish Freedom Party",
        jurisdiction="roi_dail",
        source_url="https://www.irishfreedomparty.ie/contact",
        electoral_commission_id="nil",
        cohort_id="roi.irish_freedom_party",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="roi/irish_freedom_party/",
    ),
    PartyCohort(
        party_id="national-party-roi",
        party_name="National Party (Ireland)",
        jurisdiction="roi_dail",
        source_url="https://www.nationalparty.ie/contact",
        electoral_commission_id="nil",
        cohort_id="roi.national_party_roi",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="roi/national_party/",
    ),
    PartyCohort(
        party_id="rise-roi",
        party_name="Rise (Republic of Ireland)",
        jurisdiction="roi_dail",
        source_url="https://www.riseparty.ie/contact",
        electoral_commission_id="nil",
        cohort_id="roi.rise_roi",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="roi/rise/",
    ),
    # === NI Assembly → BIPP v1 m2 ===
    PartyCohort(
        party_id="dup",
        party_name="Democratic Unionist Party",
        jurisdiction="ni_assembly",
        source_url="https://mydup.com/contact",
        electoral_commission_id="PP-10113",
        cohort_id="ni_assembly.dup",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="ni_assembly/dup/",
    ),
    PartyCohort(
        party_id="sinn-fein-ni",
        party_name="Sinn Féin (Northern Ireland branch)",
        jurisdiction="ni_assembly",
        source_url="https://www.sinnfein.ie/contact",
        electoral_commission_id="PP-10126",
        cohort_id="ni_assembly.sinn_fein_ni",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="ni_assembly/sinn_fein/",
    ),
    PartyCohort(
        party_id="alliance-ni",
        party_name="Alliance Party of Northern Ireland",
        jurisdiction="ni_assembly",
        source_url="https://www.allianceparty.org/contact",
        electoral_commission_id="PP-10119",
        cohort_id="ni_assembly.alliance_ni",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="ni_assembly/alliance/",
    ),
    PartyCohort(
        party_id="uup",
        party_name="Ulster Unionist Party",
        jurisdiction="ni_assembly",
        source_url="https://uup.org/contact/",
        electoral_commission_id="PP-10121",
        cohort_id="ni_assembly.uup",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="ni_assembly/uup/",
    ),
    PartyCohort(
        party_id="sdlp",
        party_name="Social Democratic and Labour Party",
        jurisdiction="ni_assembly",
        source_url="https://www.sdlp.ie/contact/",
        electoral_commission_id="PP-10120",
        cohort_id="ni_assembly.sdlp",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="ni_assembly/sdlp/",
    ),
    PartyCohort(
        party_id="tuv-ni",
        party_name="Traditional Unionist Voice",
        jurisdiction="ni_assembly",
        source_url="https://www.tuv.org.uk/contact/",
        electoral_commission_id="PP-10127",
        cohort_id="ni_assembly.tuv_ni",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="ni_assembly/tuv/",
    ),
    PartyCohort(
        party_id="pbp-ni",
        party_name="People Before Profit (Northern Ireland)",
        jurisdiction="ni_assembly",
        source_url="https://www.pbp.ie/contact/",
        electoral_commission_id="PP-10128",
        cohort_id="ni_assembly.pbp_ni",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="ni_assembly/pbp/",
    ),
    # === Wales Senedd → BIPP v1 m2 ===
    PartyCohort(
        party_id="plaid-cymru-senedd",
        party_name="Plaid Cymru — Party of Wales (Senedd scope)",
        jurisdiction="senedd",
        source_url="https://www.partyof.wales/contact/",
        electoral_commission_id="PP-10115",
        cohort_id="senedd.plaid_cymru_senedd",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="senedd/plaid_cymru/",
    ),
    PartyCohort(
        party_id="labour-wales",
        party_name="Welsh Labour",
        jurisdiction="senedd",
        source_url="https://www.welshlabour.wales/contact",
        electoral_commission_id="PP-10129",
        cohort_id="senedd.labour_wales",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="senedd/labour/",
    ),
    PartyCohort(
        party_id="conservative-wales",
        party_name="Welsh Conservatives",
        jurisdiction="senedd",
        source_url="https://www.welshconservatives.co.uk/contact",
        electoral_commission_id="PP-10130",
        cohort_id="senedd.conservative_wales",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="senedd/conservative/",
    ),
    PartyCohort(
        party_id="liberal-democrats-wales",
        party_name="Welsh Liberal Democrats",
        jurisdiction="senedd",
        source_url="https://www.welshlibdems.wales/contact",
        electoral_commission_id="PP-10131",
        cohort_id="senedd.liberal_democrats_wales",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="senedd/libdems/",
    ),
    # === Scotland Holyrood → BIPP v1 m2 ===
    PartyCohort(
        party_id="snp-scottish",
        party_name="Scottish National Party (Holyrood scope)",
        jurisdiction="holyrood",
        source_url="https://www.snp.org/contact/",
        electoral_commission_id="PP-10122",
        cohort_id="holyrood.snp_scottish",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="holyrood/snp/",
    ),
    PartyCohort(
        party_id="scottish-labour",
        party_name="Scottish Labour",
        jurisdiction="holyrood",
        source_url="https://www.scottishlabour.org.uk/contact",
        electoral_commission_id="PP-10132",
        cohort_id="holyrood.scottish_labour",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="holyrood/labour/",
    ),
    PartyCohort(
        party_id="scottish-conservatives",
        party_name="Scottish Conservatives",
        jurisdiction="holyrood",
        source_url="https://www.scottishconservatives.com/contact",
        electoral_commission_id="PP-10133",
        cohort_id="holyrood.scottish_conservatives",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="holyrood/conservative/",
    ),
    PartyCohort(
        party_id="scottish-liberal-democrats",
        party_name="Scottish Liberal Democrats",
        jurisdiction="holyrood",
        source_url="https://www.scotlibdems.org.uk/contact",
        electoral_commission_id="PP-10134",
        cohort_id="holyrood.scottish_liberal_democrats",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="holyrood/libdems/",
    ),
    PartyCohort(
        party_id="scottish-greens",
        party_name="Scottish Greens",
        jurisdiction="holyrood",
        source_url="https://greens.scot/contact/",
        electoral_commission_id="PP-10135",
        cohort_id="holyrood.scottish_greens",
        milestone_gate="BIPP v1 m2",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="holyrood/greens/",
    ),
    # === Crown Dependencies → BIPP v1 m3 ===
    PartyCohort(
        party_id="jersey-party",
        party_name="Jersey (parish-level independents + Reform Jersey)",
        jurisdiction="jsy",
        source_url="https://www.gov.je/Government/Pages/States.aspx",
        electoral_commission_id="nil",
        cohort_id="crown_dependencies.jersey_party",
        milestone_gate="BIPP v1 m3",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="crown_dependencies/jsy/",
    ),
    PartyCohort(
        party_id="guernsey-party",
        party_name="Guernsey (parish-level independents)",
        jurisdiction="ggy",
        source_url="https://www.gov.gg/StatesofGuernsey",
        electoral_commission_id="nil",
        cohort_id="crown_dependencies.guernsey_party",
        milestone_gate="BIPP v1 m3",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="crown_dependencies/ggy/",
    ),
    PartyCohort(
        party_id="iom-party",
        party_name="Isle of Man (Tinvaal + Liberal Vannin + others)",
        jurisdiction="iom",
        source_url="https://www.gov.im/parliament",
        electoral_commission_id="nil",
        cohort_id="crown_dependencies.iom_party",
        milestone_gate="BIPP v1 m3",
        extraction_function="ExtractPartyPressRelease",
        target_resource="press_releases",
        ingest_queue_subdir="crown_dependencies/iom/",
    ),
)


def get_cohort(party_id: str, jurisdiction: str) -> PartyCohort:
    """Return the cohort row for the given (party_id, jurisdiction).

    Raises:
        KeyError: If the (party_id, jurisdiction) pair is not registered.
    """
    for cohort in COHORTS:
        if cohort.party_id == party_id and cohort.jurisdiction == jurisdiction:
            return cohort
    raise KeyError(
        f"Unknown (party_id={party_id!r}, jurisdiction={jurisdiction!r})"
    )


def get_cohorts_by_milestone(milestone_gate: str) -> tuple[PartyCohort, ...]:
    """Return every cohort that unblocks the given milestone gate."""
    return tuple(c for c in COHORTS if c.milestone_gate == milestone_gate)


def get_cohorts_by_jurisdiction(jurisdiction: str) -> tuple[PartyCohort, ...]:
    """Return every cohort for the given jurisdiction."""
    return tuple(c for c in COHORTS if c.jurisdiction == jurisdiction)


def get_cohorts_by_party(party_id: str) -> tuple[PartyCohort, ...]:
    """Return every cohort for the given party_id (parties may span jurisdictions)."""
    return tuple(c for c in COHORTS if c.party_id == party_id)


def active_cohorts() -> tuple[PartyCohort, ...]:
    """Return every cohort with ``active=True`` (the default)."""
    return tuple(c for c in COHORTS if c.active)


# ── RENDERING ──────────────────────────────────────────────────────────


def _format_table() -> str:
    """Render the cohort grid as an aligned text table."""
    headers = (
        "party_id", "jurisdiction", "source_url",
        "cohort_id", "milestone_gate", "active",
    )
    # Compute widths against real rows + headers.
    real_widths = [
        max(
            len(str(getattr(c, h))),
            max(len(h) for h in headers),
        )
        for h in headers
    ]

    def _row(values: tuple[str, ...]) -> str:
        return "  ".join(
            f"{v:<{w}}" for v, w in zip(values, real_widths, strict=False)
        )

    sep = "  ".join("-" * w for w in real_widths)
    lines: list[str] = []
    lines.append(_row(headers))
    lines.append(sep)
    for c in COHORTS:
        lines.append(_row(tuple(str(getattr(c, h)) for h in headers)))
    lines.append(sep)
    active_count = len(active_cohorts())
    lines.append(
        f"{len(COHORTS)} cohort(s) registered ({active_count} active, "
        f"{len(COHORTS) - active_count} dormant) across "
        f"{len({c.jurisdiction for c in COHORTS})} jurisdiction(s) and "
        f"{len({c.party_id for c in COHORTS})} unique party/parties"
    )
    return "\n".join(lines)


def main() -> int:
    """Print the cohort registry table to stdout."""
    print(_format_table())
    return 0


__all__ = [
    "COHORTS",
    "PartyCohort",
    "active_cohorts",
    "get_cohort",
    "get_cohorts_by_jurisdiction",
    "get_cohorts_by_milestone",
    "get_cohorts_by_party",
    "main",
]


if __name__ == "__main__":
    raise SystemExit(main())