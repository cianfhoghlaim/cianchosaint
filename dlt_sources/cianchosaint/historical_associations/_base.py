# CIANCHOSAINT — HistoricalAssociationPipelineBase class — the canonical
# contract for the historical-association DLT source modules.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The historical_associations/
# DLT source tree.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.historical_associations._base — base class."""

from __future__ import annotations

import logging
from typing import Any, ClassVar

logger = logging.getLogger(__name__)


VALID_ASSOCIATION_TYPES: ClassVar[set[str]] = {
    "past_party_membership",
    "past_directorship",
    "past_education",
    "past_employment",
    "public_controversy",
    "court_appearance",
    "family_in_politics",
    "honorary_award",
    "dissolved_company_association",
}


class HistoricalAssociationCohort:
    """The canonical HistoricalAssociation cohort row."""

    __slots__ = (
        "source_id",
        "source_name",
        "source_url",
        "association_id",
        "subject_canonical_name",
        "type",
        "description",
        "start_date",
        "end_date",
        "source_urls",
        "extraction_confidence",
    )

    def __init__(
        self,
        *,
        source_id: str,
        source_name: str,
        source_url: str,
        association_id: str = "",
        subject_canonical_name: str = "",
        type: str = "past_party_membership",
        description: str = "",
        start_date: str | None = None,
        end_date: str | None = None,
        source_urls: list[str] | None = None,
        extraction_confidence: float = 0.85,
    ) -> None:
        self.source_id = source_id
        self.source_name = source_name
        self.source_url = source_url
        self.association_id = association_id
        self.subject_canonical_name = subject_canonical_name
        self.type = type
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.source_urls = source_urls or [source_url]
        self.extraction_confidence = extraction_confidence

    def to_dlt_row(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_name": self.source_name,
            "source_url": self.source_url,
            "association_id": self.association_id,
            "subject_canonical_name": self.subject_canonical_name,
            "type": self.type,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "source_urls": self.source_urls,
            "extraction_confidence": self.extraction_confidence,
            "osint_ceiling_enforced": True,
            "analyst_review_required": True,
        }


class HistoricalAssociationPipelineBase:
    """The canonical HistoricalAssociationPipelineBase contract."""

    # Subclasses set these:
    SOURCE_ID: ClassVar[str] = ""
    SOURCE_NAME: ClassVar[str] = ""
    SOURCE_BASE: ClassVar[str] = ""

    def historical_association_to_row(self) -> dict[str, Any]:
        """Build the canonical HistoricalAssociation cohort row from the class attributes."""
        if not self.SOURCE_ID:
            raise ValueError(f"{type(self).__name__}.SOURCE_ID is not set")

        return HistoricalAssociationCohort(
            source_id=self.SOURCE_ID,
            source_name=self.SOURCE_NAME,
            source_url=self.SOURCE_BASE,
            source_urls=[self.SOURCE_BASE],
        ).to_dlt_row()

    def _iter_historical_association_records(self) -> "HistoricalAssociationPipelineBase":
        """Yield the canonical HistoricalAssociation cohort row."""
        yield self.historical_association_to_row()


__all__ = [
    "HistoricalAssociationCohort",
    "HistoricalAssociationPipelineBase",
    "VALID_ASSOCIATION_TYPES",
]
