# CIANCHOSAINT — AdvisorPipelineBase class — the canonical contract for the
# per-jurisdiction SpAd register DLT source modules.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The advisors/ DLT
# source tree.
#
# Mirrors the cianchosaint `dlt_sources/cianchosaint/politicians/_base.py`
# + the `dlt_sources/cianchosaint/bipp_v2/_base.py` patterns.
#
# Subclasses set the 5 class attributes (SOURCE_BASE + the 4 jurisdiction
# fields); the base class yields the canonical cohort row.
#
# Example::
#
#     class UKHoCSpadRegister(AdvisorPipelineBase):
#         SOURCE_ID = "uk_hoc_spad_register"
#         SOURCE_NAME = "UK Cabinet Office Special Adviser Register"
#         JURISDICTION = "uk_hoc"
#         SOURCE_BASE = "https://www.gov.uk/government/publications/special-adviser-data"
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.advisors._base — base class.

Provides the `AdvisorPipelineBase` contract that all per-jurisdiction
advisor DLT source subclasses share:

- `SOURCE_ID`            — the canonical id (e.g. "uk_hoc_spad_register")
- `SOURCE_NAME`          — the human-readable display name (e.g. "UK Cabinet
                           Office Special Adviser Register")
- `JURISDICTION`         — `uk_hoc` / `ni_assembly` / `holyrood` / `roi_dail`
                           / `roi_seanad` / `senedd`
- `SOURCE_BASE`          — the OSINT-allowlisted official source URL
- `COVERAGE`             — the canonical coverage description
"""

from __future__ import annotations

import logging
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


class AdvisorCohort:
    """The canonical Advisor / SpAd cohort row."""

    __slots__ = (
        "source_id",
        "source_name",
        "jurisdiction",
        "source_url",
        "advisor_id",
        "canonical_name",
        "role",
        "employing_politician_ids",
        "employing_party_id",
        "start_date",
        "end_date",
        "cabinet_office_registered_at",
        "gov_uk_publication_url",
        "source_urls",
        "extraction_confidence",
        "active",
    )

    def __init__(
        self,
        *,
        source_id: str,
        source_name: str,
        jurisdiction: str,
        source_url: str,
        advisor_id: str = "",
        canonical_name: str = "",
        role: str = "spad_special_adviser",
        employing_politician_ids: list[str] | None = None,
        employing_party_id: str = "",
        start_date: str | None = None,
        end_date: str | None = None,
        cabinet_office_registered_at: str | None = None,
        gov_uk_publication_url: str | None = None,
        source_urls: list[str] | None = None,
        extraction_confidence: float = 0.95,
        active: bool = True,
    ) -> None:
        self.source_id = source_id
        self.source_name = source_name
        self.jurisdiction = jurisdiction
        self.source_url = source_url
        self.advisor_id = advisor_id
        self.canonical_name = canonical_name
        self.role = role
        self.employing_politician_ids = employing_politician_ids or []
        self.employing_party_id = employing_party_id
        self.start_date = start_date
        self.end_date = end_date
        self.cabinet_office_registered_at = cabinet_office_registered_at
        self.gov_uk_publication_url = gov_uk_publication_url
        self.source_urls = source_urls or [source_url]
        self.extraction_confidence = extraction_confidence
        self.active = active

    def to_dlt_row(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_name": self.source_name,
            "jurisdiction": self.jurisdiction,
            "source_url": self.source_url,
            "advisor_id": self.advisor_id,
            "canonical_name": self.canonical_name,
            "role": self.role,
            "employing_politician_ids": self.employing_politician_ids,
            "employing_party_id": self.employing_party_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "cabinet_office_registered_at": self.cabinet_office_registered_at,
            "gov_uk_publication_url": self.gov_uk_publication_url,
            "source_urls": self.source_urls,
            "extraction_confidence": self.extraction_confidence,
            "active": self.active,
            "osint_ceiling_enforced": True,
            "analyst_review_required": True,
        }


class AdvisorPipelineBase:
    """The canonical AdvisorPipelineBase contract."""

    # Subclasses set these:
    SOURCE_ID: ClassVar[str] = ""
    SOURCE_NAME: ClassVar[str] = ""
    JURISDICTION: ClassVar[str] = ""
    SOURCE_BASE: ClassVar[str] = ""

    def advisor_to_row(self) -> dict[str, Any]:
        """Build the canonical Advisor cohort row from the class attributes."""
        if not self.SOURCE_ID:
            raise ValueError(f"{type(self).__name__}.SOURCE_ID is not set")
        if self.JURISDICTION not in VALID_JURISDICTIONS:
            raise ValueError(
                f"{type(self).__name__}.JURISDICTION = {self.JURISDICTION!r} is not in VALID_JURISDICTIONS"
            )

        return AdvisorCohort(
            source_id=self.SOURCE_ID,
            source_name=self.SOURCE_NAME,
            jurisdiction=self.JURISDICTION,
            source_url=self.SOURCE_BASE,
            source_urls=[self.SOURCE_BASE],
        ).to_dlt_row()

    def _iter_advisor_records(self) -> "AdvisorPipelineBase":
        """Yield the canonical Advisor cohort row.

        Subclasses MAY override to add per-advisor records scraped from the
        SpAd register. The base implementation yields a single row that
        describes the source itself.
        """
        yield self.advisor_to_row()


__all__ = [
    "AdvisorCohort",
    "AdvisorPipelineBase",
    "VALID_JURISDICTIONS",
]
