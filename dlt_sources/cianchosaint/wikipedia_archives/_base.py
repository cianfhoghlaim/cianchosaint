# CIANCHOSAINT — WikipediaArchivesPipelineBase class — the canonical contract for
# the multilingual Wikipedia + Wikidata DLT source modules.
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The wikipedia_archives/
# DLT source tree.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.wikipedia_archives._base — base class."""

from __future__ import annotations

import logging
from typing import Any, ClassVar

logger = logging.getLogger(__name__)


VALID_LANGUAGE_CODES: ClassVar[set[str]] = {
    "en",  # English
    "ga",  # Irish (Gaeilge)
    "cy",  # Welsh (Cymraeg)
    "gd",  # Scottish Gaelic (Gàidhlig)
    "sco", # Scots
    "fr",  # French (for Channel Islands)
}


class WikipediaArchivesCohort:
    """The canonical WikipediaArchives cohort row."""

    __slots__ = (
        "source_id",
        "source_name",
        "source_url",
        "language_code",
        "wikipedia_archives_id",
        "subject_canonical_name",
        "wikidata_qid",
        "wikipedia_title",
        "wikidata_statements",
        "wikipedia_categories",
        "wikidata_last_updated",
        "commons_category_url",
        "source_urls",
        "extraction_confidence",
    )

    def __init__(
        self,
        *,
        source_id: str,
        source_name: str,
        source_url: str,
        language_code: str = "en",
        wikipedia_archives_id: str = "",
        subject_canonical_name: str = "",
        wikidata_qid: str | None = None,
        wikipedia_title: str | None = None,
        wikidata_statements: list[str] | None = None,
        wikipedia_categories: list[str] | None = None,
        wikidata_last_updated: str | None = None,
        commons_category_url: str | None = None,
        source_urls: list[str] | None = None,
        extraction_confidence: float = 0.95,
    ) -> None:
        self.source_id = source_id
        self.source_name = source_name
        self.source_url = source_url
        self.language_code = language_code
        self.wikipedia_archives_id = wikipedia_archives_id
        self.subject_canonical_name = subject_canonical_name
        self.wikidata_qid = wikidata_qid
        self.wikipedia_title = wikipedia_title
        self.wikidata_statements = wikidata_statements or []
        self.wikipedia_categories = wikipedia_categories or []
        self.wikidata_last_updated = wikidata_last_updated
        self.commons_category_url = commons_category_url
        self.source_urls = source_urls or [source_url]
        self.extraction_confidence = extraction_confidence

    def to_dlt_row(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_name": self.source_name,
            "source_url": self.source_url,
            "language_code": self.language_code,
            "wikipedia_archives_id": self.wikipedia_archives_id,
            "subject_canonical_name": self.subject_canonical_name,
            "wikidata_qid": self.wikidata_qid,
            "wikipedia_title": self.wikipedia_title,
            "wikidata_statements": self.wikidata_statements,
            "wikipedia_categories": self.wikipedia_categories,
            "wikidata_last_updated": self.wikidata_last_updated,
            "commons_category_url": self.commons_category_url,
            "source_urls": self.source_urls,
            "extraction_confidence": self.extraction_confidence,
            "osint_ceiling_enforced": True,
            "analyst_review_required": True,
        }


class WikipediaArchivesPipelineBase:
    """The canonical WikipediaArchivesPipelineBase contract."""

    # Subclasses set these:
    SOURCE_ID: ClassVar[str] = ""
    SOURCE_NAME: ClassVar[str] = ""
    SOURCE_BASE: ClassVar[str] = ""
    LANGUAGE_CODE: ClassVar[str] = "en"

    def wikipedia_archives_to_row(self) -> dict[str, Any]:
        """Build the canonical WikipediaArchives cohort row from the class attributes."""
        if not self.SOURCE_ID:
            raise ValueError(f"{type(self).__name__}.SOURCE_ID is not set")
        if self.LANGUAGE_CODE not in VALID_LANGUAGE_CODES:
            raise ValueError(
                f"{type(self).__name__}.LANGUAGE_CODE = {self.LANGUAGE_CODE!r} is not in VALID_LANGUAGE_CODES"
            )

        return WikipediaArchivesCohort(
            source_id=self.SOURCE_ID,
            source_name=self.SOURCE_NAME,
            source_url=self.SOURCE_BASE,
            language_code=self.LANGUAGE_CODE,
            source_urls=[self.SOURCE_BASE],
        ).to_dlt_row()

    def _iter_wikipedia_archive_records(self) -> "WikipediaArchivesPipelineBase":
        """Yield the canonical WikipediaArchives cohort row."""
        yield self.wikipedia_archives_to_row()


__all__ = [
    "VALID_LANGUAGE_CODES",
    "WikipediaArchivesCohort",
    "WikipediaArchivesPipelineBase",
]
