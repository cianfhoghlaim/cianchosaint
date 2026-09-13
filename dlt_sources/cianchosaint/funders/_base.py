# CIANCHOSAINT — FunderPipelineBase class — the canonical contract for the
# per-jurisdiction funder surfaces (Electoral Commission + Companies House +
# Registers of Interests).
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The funders/ DLT
# source tree.
#
# Subclasses set the 6 class attributes; the base class yields the canonical
# cohort row.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.funders._base — base class + Donation + FunderCohort."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, ClassVar

logger = logging.getLogger(__name__)


VALID_JURISDICTIONS: ClassVar[set[str]] = {
    "uk_hoc",
    "uk_hoc_lords",
    "ni_assembly",
    "holyrood",
    "senedd",
    "roi_dail",
    "roi_seanad",
}


VALID_DONOR_TYPES: ClassVar[set[str]] = {
    "individual",
    "company",
    "trade_union",
    "think_tank",
    "overseas_government",
    "shell_company",
    "lobbyist",
    "unincorporated_association",
}


@dataclass
class Donation:
    """One donation made by a funder to a politician or party."""

    date: str
    amount_gbp: float | None
    receiving_party_id: str
    receiving_politician_id: str | None = None
    electoral_commission_id: str | None = None
    donation_type: str = "cash"  # "cash" | "non_cash" | "visit" | "loan" | "gift" | "hospitality" | "subscription"
    source_url: str = ""
    notes: str | None = None


@dataclass
class FunderCohort:
    """The canonical Funder cohort row."""

    source_id: str
    source_name: str
    jurisdiction: str
    source_url: str
    source_type: str  # "electoral_commission" | "companies_house" | "register_of_interests"
    funder_id: str = ""
    canonical_name: str = ""
    donor_type: str = ""
    donations: list[dict[str, Any]] = field(default_factory=list)
    total_donations_gbp: float | None = None
    declared_interests: list[str] = field(default_factory=list)
    apparent_discrepancies: list[str] = field(default_factory=list)
    source_urls: list[str] = field(default_factory=list)
    extraction_confidence: float = 0.95
    active: bool = True

    def to_dlt_row(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_name": self.source_name,
            "jurisdiction": self.jurisdiction,
            "source_url": self.source_url,
            "source_type": self.source_type,
            "funder_id": self.funder_id,
            "canonical_name": self.canonical_name,
            "donor_type": self.donor_type,
            "donations": self.donations,
            "total_donations_gbp": self.total_donations_gbp,
            "declared_interests": self.declared_interests,
            "apparent_discrepancies": self.apparent_discrepancies,
            "source_urls": self.source_urls,
            "extraction_confidence": self.extraction_confidence,
            "active": self.active,
            "osint_ceiling_enforced": True,
            "analyst_review_required": True,
        }


class FunderPipelineBase:
    """The canonical FunderPipelineBase contract."""

    # Subclasses set these:
    SOURCE_ID: ClassVar[str] = ""
    SOURCE_NAME: ClassVar[str] = ""
    JURISDICTION: ClassVar[str] = ""
    SOURCE_BASE: ClassVar[str] = ""
    SOURCE_TYPE: ClassVar[str] = ""

    def funder_to_row(self) -> dict[str, Any]:
        """Build the canonical Funder cohort row from the class attributes."""
        if not self.SOURCE_ID:
            raise ValueError(f"{type(self).__name__}.SOURCE_ID is not set")
        if self.JURISDICTION not in VALID_JURISDICTIONS:
            raise ValueError(
                f"{type(self).__name__}.JURISDICTION = {self.JURISDICTION!r} is not in VALID_JURISDICTIONS"
            )

        return FunderCohort(
            source_id=self.SOURCE_ID,
            source_name=self.SOURCE_NAME,
            jurisdiction=self.JURISDICTION,
            source_url=self.SOURCE_BASE,
            source_type=self.SOURCE_TYPE,
            source_urls=[self.SOURCE_BASE],
        ).to_dlt_row()

    def _iter_funder_records(self) -> "FunderPipelineBase":
        """Yield the canonical Funder cohort row.

        Subclasses MAY override to add per-funder records scraped from the
        Electoral Commission / Companies House / Register of Interests page.
        """
        yield self.funder_to_row()


__all__ = [
    "Donation",
    "FunderCohort",
    "FunderPipelineBase",
    "VALID_DONOR_TYPES",
    "VALID_JURISDICTIONS",
]
