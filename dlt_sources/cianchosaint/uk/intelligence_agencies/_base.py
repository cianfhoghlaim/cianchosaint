# CIANCHOSAINT new-build: IntelligenceAgencyPipelineBase class — the
# canonical contract for the 5 UK intelligence agency DLT source modules.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-intelligence-agency-pipeline-v1/specs/cianchosaint-
#   intelligence-agency-pipeline/spec.md, Requirement: The
#   IntelligenceAgencyPipelineBase class + the cross-agency cohort
#   registry, Scenario: IntelligenceAgencyPipelineBase provides the
#   canonical contract).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# NOTE: The wholesale-copied ``dlt_sources/_cross/jurisdiction_pipeline_base.py``
# has a stale import (``dlt_sources.common.destinations_cianfhoghlaim``)
# and cannot be imported in the current cianchosaint tree. This file
# re-implements the same contract directly against the corrected
# ``destinations_cianchosaint`` module (mirroring the recently-authored
# ``PoliticalPartyPipelineBase`` shape).

"""cianchosaint.cianchosaint.dlt.british_isles.intelligence_agencies._base — base class.

Phase 4 of the openspec change. Provides the
``IntelligenceAgencyPipelineBase`` contract that all 5 UK
intelligence agency DLT source subclasses share:

- ``AGENCY_ID``   — the canonical id (``mi5`` / ``mi6`` / ``gchq`` /
                   ``defence_intelligence`` / ``hmgcc``)
- ``AGENCY_NAME`` — the human-readable display name
- ``SOURCE_BASE``  — the agency's official website (news / press URL)
- ``@dlt.resource`` — ``public_statements`` (the canonical entry point
                   that downstream BAML extracts against)

Subclasses only need to set the 3 class attributes; the base class
yields the canonical cohort row + builds the destination pipeline.

Example::

    class MI5Pipeline(IntelligenceAgencyPipelineBase):
        AGENCY_ID = "mi5"
        AGENCY_NAME = "MI5 (Security Service)"
        SOURCE_BASE = "https://www.mi5.gov.uk/"
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar

import dlt
from dlt.common.typing import TDataItems

logger = logging.getLogger(__name__)

VALID_AGENCY_IDS: ClassVar[set[str]] = {
    "mi5",
    "mi6",
    "gchq",
    "defence_intelligence",
    "hmgcc",
}


class IntelligenceAgencyPipelineBase:
    """Base class for the 5 UK intelligence agency DLT source modules.

    All 5 agency sources (mi5 / mi6 / gchq / defence_intelligence /
    hmgcc_rolling_window) subclass this base + set the 3 class
    attributes + define the @dlt.resource method.
    """

    AGENCY_ID: ClassVar[str] = ""
    AGENCY_NAME: ClassVar[str] = ""
    SOURCE_BASE: ClassVar[str] = ""

    def __post_init__(self) -> None:
        if self.AGENCY_ID not in VALID_AGENCY_IDS:
            raise ValueError(
                f"{type(self).__name__}.AGENCY_ID={self.AGENCY_ID!r} "
                f"not in VALID_AGENCY_IDS={sorted(VALID_AGENCY_IDS)}"
            )
        if not self.AGENCY_NAME:
            raise ValueError(f"{type(self).__name__}.AGENCY_NAME is required")
        if not self.SOURCE_BASE:
            raise ValueError(f"{type(self).__name__}.SOURCE_BASE is required")

    def cohort_row(self) -> dict[str, Any]:
        """The canonical cohort registry row for this agency."""
        return {
            "agency_id": self.AGENCY_ID,
            "agency_name": self.AGENCY_NAME,
            "source_base": self.SOURCE_BASE,
            "cohort_id": f"uk.intelligence_agency.{self.AGENCY_ID}",
            "milestone_gate": "cianchosaint:biip:v1:m1",
            "public_facing_only": True,
        }

    def build_pipeline(self, dataset_name: str | None = None) -> Any:
        """Build the canonical destination pipeline."""
        try:
            from dlt import pipeline as _dlt_pipeline
        except ImportError:  # noqa: BLE001
            return None
        return _dlt_pipeline(
            pipeline_name=f"cianchosaint.intelligence_agency.{self.AGENCY_ID}",
            dataset_name=dataset_name or f"cianchosaint.intelligence_agency.{self.AGENCY_ID}",
        )

    def __init__(self) -> None:
        self.__post_init__()
