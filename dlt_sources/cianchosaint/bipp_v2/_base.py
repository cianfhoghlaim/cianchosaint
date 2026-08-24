# CIANCHOSAINT — BIPP v2 Political Accountability Pipeline base class.
#
# Per the openspec/changes/cianchosaint-bipp-v2-political-party-v2-v1/
# specs/cianchosaint-bipp-v2/spec.md.
#
# Mirrors the cianchosaint `dlt_sources/cianchosaint/political_parties/_base.py`
# + the `dlt_sources/cianchosaint/uk/intelligence_agencies/_base.py`.
#
# License: BUSL-1.1 (per LICENSE.md).

"""cianchosaint.cianchosaint.dlt.british_isles.bipp_v2._base — base class.

Provides the `PoliticalAccountabilityPipelineBase` contract that all
7 BIPP v2 cohort DLT source subclasses share:

- `COHORT_ID`         — the canonical id (one of the 7 cohorts)
- `COHORT_NAME`       — the human-readable display name
- `JURISDICTION`      — the British Isles sub-nation
- `SOURCE_BASE`       — the OSINT-allowlisted official source URL
- `SOURCE_PDFS`       — the leabharlann PDFs (read-only context)
- `LEABHARLANN_ROOT`  — the path to leabharlann/gemini_deep_research/
- `MILESTONE_GATE`    — the BIPP v2 milestone gate

Subclasses only need to set the class attributes; the base class
yields the canonical cohort row + builds the destination pipeline.

Example::

    class ReformUKAccountabilityPipeline(PoliticalAccountabilityPipelineBase):
        COHORT_ID = "reform_uk_accountability"
        COHORT_NAME = "Reform UK Accountability"
        JURISDICTION = "uk_hoc"
        SOURCE_BASE = "https://www.reformparty.uk/news"
        SOURCE_PDFS = ["leabharlann/gemini_deep_research/politics/reform_richard_tice_debt_fraud.pdf"]
        MILESTONE_GATE = "cianchosaint:bipp:v2:m2"

The base class yields the canonical cohort row + builds the
destination pipeline.
"""

from __future__ import annotations

import logging
import os
from typing import Any, ClassVar

logger = logging.getLogger(__name__)


# The canonical BIPP v2 cohorts (per openspec/specs/cianchosaint-bipp-v2/spec.md §Purpose).
VALID_COHORT_IDS: ClassVar[set[str]] = {
    "reform_uk_accountability",
    "reform_uk_devolved_branches",
    "ni_political_accountability",
    "scottish_political_accountability",
    "welsh_london_political_accountability",
    "roi_political_accountability",
    "cross_cutting_intelligence_cybersecurity",
}


# The canonical British Isles sub-nations (per the 8-nation jurisdiction enum).
VALID_JURISDICTIONS: ClassVar[set[str]] = {
    "ireland",
    "uk",
    "ni",
    "scotland",
    "wales",
    "england",
    "jersey",
    "guernsey",
    "iom",
    "cross_border",
}


# The canonical leabharlann root (the user's private leabharlann repo).
DEFAULT_LEABHARLANN_ROOT = os.environ.get(
    "CIANCHOSAINT_LEABHARLANN_ROOT",
    str(os.path.expanduser("~/dev/cianfhoghlaim/leabharlann")),
)


def _normalize_pdf_path(rel_path: str, leabharlann_root: str) -> str:
    """Normalize a relative leabharlann PDF path against the root.

    Handles two cases:
    - LEABHARLANN_ROOT is the leabharlann parent dir (e.g.
      /Users/.../cianfhoghlaim) and SOURCE_PDFS paths start with
      "leabharlann/"
    - LEABHARLANN_ROOT is the leabharlann dir itself (e.g.
      /Users/.../cianfhoghlaim/leabharlann) and SOURCE_PDFS paths
      do NOT start with "leabharlann/"
    """
    if rel_path.startswith("leabharlann/"):
        rel_path = rel_path[len("leabharlann/"):]
    return os.path.join(leabharlann_root, rel_path)


class PoliticalAccountabilityPipelineBase:
    """Base class for the 7 BIPP v2 cohort DLT source modules.

    All 7 cohort sources subclass this base + set the 5 class
    attributes + define the @dlt.resource method.
    """

    COHORT_ID: ClassVar[str] = ""
    COHORT_NAME: ClassVar[str] = ""
    JURISDICTION: ClassVar[str] = ""
    SOURCE_BASE: ClassVar[str] = ""
    SOURCE_PDFS: ClassVar[list[str]] = []
    MILESTONE_GATE: ClassVar[str] = ""

    def __post_init__(self) -> None:
        if self.COHORT_ID not in VALID_COHORT_IDS:
            raise ValueError(
                f"{type(self).__name__}.COHORT_ID={self.COHORT_ID!r} "
                f"not in VALID_COHORT_IDS={sorted(VALID_COHORT_IDS)}"
            )
        if not self.COHORT_NAME:
            raise ValueError(f"{type(self).__name__}.COHORT_NAME is required")
        if self.JURISDICTION not in VALID_JURISDICTIONS:
            raise ValueError(
                f"{type(self).__name__}.JURISDICTION={self.JURISDICTION!r} "
                f"not in VALID_JURISDICTIONS={sorted(VALID_JURISDICTIONS)}"
            )
        if not self.SOURCE_BASE:
            raise ValueError(f"{type(self).__name__}.SOURCE_BASE is required")
        if not self.MILESTONE_GATE:
            raise ValueError(f"{type(self).__name__}.MILESTONE_GATE is required")

    def cohort_row(self) -> dict[str, Any]:
        """The canonical cohort registry row for this BIPP v2 cohort."""
        return {
            "cohort_id": self.COHORT_ID,
            "cohort_name": self.COHORT_NAME,
            "jurisdiction": self.JURISDICTION,
            "source_base": self.SOURCE_BASE,
            "source_pdfs": self.SOURCE_PDFS,
            "cohort_full_id": f"uk.bipp_v2.{self.COHORT_ID}.{self.JURISDICTION}",
            "milestone_gate": self.MILESTONE_GATE,
            "public_facing_only": True,
            "leabharlann_root": DEFAULT_LEABHARLANN_ROOT,
        }

    def leabharlann_pdfs_for_cohort(self) -> list[str]:
        """Return the canonical leabharlann PDF paths for this cohort.

        Returns:
            A list of absolute paths to the leabharlann PDFs for this
            cohort (per the SOURCE_PDFS class attribute + the
            LEABHARLANN_ROOT env var).

        Handles two cases:
        - LEABHARLANN_ROOT is the leabharlann parent dir (e.g.
          /Users/.../cianfhoghlaim) and SOURCE_PDFS paths start with
          "leabharlann/"
        - LEABHARLANN_ROOT is the leabharlann dir itself (e.g.
          /Users/.../cianfhoghlaim/leabharlann) and SOURCE_PDFS paths
          do NOT start with "leabharlann/"
        """
        leabharlann_root = os.environ.get(
            "CIANCHOSAINT_LEABHARLANN_ROOT", DEFAULT_LEABHARLANN_ROOT
        )
        return [_normalize_pdf_path(pdf, leabharlann_root) for pdf in self.SOURCE_PDFS]

    def validate_leabharlann_pdfs(self) -> dict[str, Any]:
        """Validate that every leabharlann PDF exists on disk.

        Returns:
            A dict with `valid: bool` + `pdfs: list[dict]` (each
            dict has `relative_path`, `absolute_path`, `exists`).
        """
        # Re-read the env var at call time so the env var override works.
        leabharlann_root = os.environ.get(
            "CIANCHOSAINT_LEABHARLANN_ROOT", DEFAULT_LEABHARLANN_ROOT
        )
        results: list[dict[str, Any]] = []
        for pdf in self.SOURCE_PDFS:
            abs_path = _normalize_pdf_path(pdf, leabharlann_root)
            results.append({
                "relative_path": pdf,
                "absolute_path": abs_path,
                "exists": os.path.exists(abs_path),
                "size_bytes": os.path.getsize(abs_path) if os.path.exists(abs_path) else 0,
            })
        return {
            "cohort_id": self.COHORT_ID,
            "valid": all(r["exists"] for r in results),
            "pdfs": results,
        }


__all__ = [
    "DEFAULT_LEABHARLANN_ROOT",
    "PoliticalAccountabilityPipelineBase",
    "VALID_COHORT_IDS",
    "VALID_JURISDICTIONS",
]