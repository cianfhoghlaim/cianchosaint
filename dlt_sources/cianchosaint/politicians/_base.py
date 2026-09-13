# CIANCHOSAINT — PoliticianPipelineBase class — the canonical contract for the
# per-politician DLT source modules.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The politicians/
# DLT source tree.
#
# Mirrors the cianchosaint `dlt_sources/cianchosaint/political_parties/_base.py`
# + the `dlt_sources/cianchosaint/bipp_v2/_base.py` patterns.
#
# Subclasses only need to set the 7 class attributes; the base class
# yields the canonical Politician cohort row + builds the destination pipeline.
#
# Example::
#
#     class NigelFaragePipeline(PoliticianPipelineBase):
#         POLITICIAN_ID = "nigel_farage"
#         CANONICAL_NAME = "Nigel Farage"
#         HONORIFIC = "MP"
#         PARTY_ID = "reform-uk"
#         PARTY_NAME = "Reform UK"
#         JURISDICTION = "uk_hoc"
#         CONSTITUENCY = "Clacton"
#         SOURCE_BASE = "https://www.reformparty.uk/people/nigel-farage"
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.politicians._base — base class.

Provides the `PoliticianPipelineBase` contract that all per-politician
DLT source subclasses share:

- `POLITICIAN_ID`        — the canonical id (e.g. "nigel_farage")
- `CANONICAL_NAME`       — the human-readable display name (e.g. "Nigel Farage")
- `HONORIFIC`            — the office ("MP" / "MLA" / "MSP" / "MS" / "TD" /
                           "Senator" / "Lord" / "Cllr" / "")
- `PARTY_ID`             — the canonical party_id (one of the 24 parties in
                           `dlt_sources/cianchosaint/political_parties/`)
- `PARTY_NAME`           — the human-readable party name
- `JURISDICTION`         — `uk_hoc` / `ni_assembly` / `holyrood` / `senedd` /
                           `roi_dail` / `roi_seanad` / `uk_hoc_lords` /
                           `local_council`
- `CONSTITUENCY`         — the constituency name
- `SOURCE_BASE`          — the politician's official party profile URL

Subclasses only need to set the 8 class attributes; the base class
yields the canonical cohort row + builds the destination pipeline.
"""

from __future__ import annotations

import logging
import os
from typing import Any, ClassVar

logger = logging.getLogger(__name__)


# The canonical jurisdictions (per cianchosaint-political-party-pipeline spec).
VALID_JURISDICTIONS: ClassVar[set[str]] = {
    "uk_hoc",
    "uk_hoc_lords",
    "ni_assembly",
    "holyrood",
    "senedd",
    "roi_dail",
    "roi_seanad",
    "local_council",
    "cross_border",
}


# The canonical 24 party_ids (from dlt_sources/cianchosaint/political_parties/_registry.py).
VALID_PARTY_IDS: ClassVar[set[str]] = {
    # UK HoC
    "conservative-uk",
    "labour-uk",
    "liberal-democrats-uk",
    "reform-uk",
    "green-party-ew",
    "plaid-cymru",
    "snp",
    # NI Assembly
    "dup",
    "sinn-fein",
    "alliance",
    "sdlp",
    "uup",
    "tuv",
    # Scotland Holyrood
    "scottish-conservatives",
    "scottish-labour",
    "scottish-liberal-democrats",
    "scottish-greens",
    # ROI Dáil + Seanad
    "fianna-fail",
    "fine-gael",
    "social-democrats",
    "labour-ireland",
    "green-ireland",
    "aontu",
    "pbp-solidarity",
    "independent-ireland",
    "100-redress",
}


# The canonical leabharlann root (the user's private leabharlann repo).
DEFAULT_LEABHARLANN_ROOT = os.environ.get(
    "CIANCHOSAINT_LEABHARLANN_ROOT",
    str(os.path.expanduser("~/dev/cianfhoghlaim/leabharlann")),
)


class PoliticianCohort:
    """A single (politician_id, party_id, jurisdiction, source_url, constituency) tuple."""

    __slots__ = (
        "politician_id",
        "canonical_name",
        "honorific",
        "party_id",
        "party_name",
        "jurisdiction",
        "constituency",
        "source_url",
        "electoral_commission_id",
        "theyworkforyou_id",
        "parliament_member_id",
        "mla_id",
        "msp_id",
        "official_website",
        "social_handles",
        "public_metrics",
        "extraction_source",
        "source_urls",
        "extracted_at",
        "extraction_confidence",
        "milestone_gate",
        "active",
    )

    def __init__(
        self,
        *,
        politician_id: str,
        canonical_name: str,
        honorific: str = "",
        party_id: str,
        party_name: str,
        jurisdiction: str,
        constituency: str = "",
        source_url: str = "",
        electoral_commission_id: str | None = None,
        theyworkforyou_id: str | None = None,
        parliament_member_id: str | None = None,
        mla_id: str | None = None,
        msp_id: str | None = None,
        official_website: str | None = None,
        social_handles: list[dict[str, Any]] | None = None,
        public_metrics: list[dict[str, Any]] | None = None,
        extraction_source: str = "manual",
        source_urls: list[str] | None = None,
        extracted_at: str = "",
        extraction_confidence: float = 1.0,
        milestone_gate: str = "cianchosaint:politician:bulk-resolve",
        active: bool = True,
    ) -> None:
        self.politician_id = politician_id
        self.canonical_name = canonical_name
        self.honorific = honorific
        self.party_id = party_id
        self.party_name = party_name
        self.jurisdiction = jurisdiction
        self.constituency = constituency
        self.source_url = source_url
        self.electoral_commission_id = electoral_commission_id
        self.theyworkforyou_id = theyworkforyou_id
        self.parliament_member_id = parliament_member_id
        self.mla_id = mla_id
        self.msp_id = msp_id
        self.official_website = official_website
        self.social_handles = social_handles or []
        self.public_metrics = public_metrics or []
        self.extraction_source = extraction_source
        self.source_urls = source_urls or []
        self.extracted_at = extracted_at
        self.extraction_confidence = extraction_confidence
        self.milestone_gate = milestone_gate
        self.active = active

    def to_dlt_row(self) -> dict[str, Any]:
        """Return the canonical DLT row dict for this politician cohort."""
        return {
            "politician_id": self.politician_id,
            "canonical_name": self.canonical_name,
            "honorific": self.honorific,
            "party_id": self.party_id,
            "party_name": self.party_name,
            "jurisdiction": self.jurisdiction,
            "constituency": self.constituency,
            "source_url": self.source_url,
            "electoral_commission_id": self.electoral_commission_id,
            "theyworkforyou_id": self.theyworkforyou_id,
            "parliament_member_id": self.parliament_member_id,
            "mla_id": self.mla_id,
            "msp_id": self.msp_id,
            "official_website": self.official_website,
            "social_handles": self.social_handles,
            "public_metrics": self.public_metrics,
            "extraction_source": self.extraction_source,
            "source_urls": self.source_urls,
            "extracted_at": self.extracted_at,
            "extraction_confidence": self.extraction_confidence,
            "milestone_gate": self.milestone_gate,
            "active": self.active,
            "osint_ceiling_enforced": True,
            "analyst_review_required": True,
        }


class PoliticianPipelineBase:
    """The canonical PoliticianPipelineBase contract.

    Subclasses set the 8 class attributes and inherit the
    `_iter_politician_records()` + `politician_to_row()` helpers.
    """

    # Subclasses set these:
    POLITICIAN_ID: ClassVar[str] = ""
    CANONICAL_NAME: ClassVar[str] = ""
    HONORIFIC: ClassVar[str] = ""
    PARTY_ID: ClassVar[str] = ""
    PARTY_NAME: ClassVar[str] = ""
    JURISDICTION: ClassVar[str] = ""
    CONSTITUENCY: ClassVar[str] = ""
    SOURCE_BASE: ClassVar[str] = ""

    def politician_to_row(self) -> dict[str, Any]:
        """Build the canonical Politician cohort row from the class attributes."""
        if not self.POLITICIAN_ID:
            raise ValueError(f"{type(self).__name__}.POLITICIAN_ID is not set")
        if self.PARTY_ID not in VALID_PARTY_IDS:
            raise ValueError(
                f"{type(self).__name__}.PARTY_ID = {self.PARTY_ID!r} is not in VALID_PARTY_IDS"
            )
        if self.JURISDICTION not in VALID_JURISDICTIONS:
            raise ValueError(
                f"{type(self).__name__}.JURISDICTION = {self.JURISDICTION!r} is not in VALID_JURISDICTIONS"
            )

        return PoliticianCohort(
            politician_id=self.POLITICIAN_ID,
            canonical_name=self.CANONICAL_NAME,
            honorific=self.HONORIFIC,
            party_id=self.PARTY_ID,
            party_name=self.PARTY_NAME,
            jurisdiction=self.JURISDICTION,
            constituency=self.CONSTITUENCY,
            source_url=self.SOURCE_BASE,
            extraction_source="manual",
            source_urls=[self.SOURCE_BASE] if self.SOURCE_BASE else [],
            extracted_at="",
            extraction_confidence=1.0,
        ).to_dlt_row()

    def _iter_politician_records(self) -> "PoliticianPipelineBase":
        """Yield the canonical Politician cohort row.

        Subclasses MAY override to add scraped social_handles + public_metrics.
        The base implementation yields a single record from `politician_to_row()`.
        """
        yield self.politician_to_row()


__all__ = [
    "DEFAULT_LEABHARLANN_ROOT",
    "VALID_JURISDICTIONS",
    "VALID_PARTY_IDS",
    "PoliticianCohort",
    "PoliticianPipelineBase",
]
