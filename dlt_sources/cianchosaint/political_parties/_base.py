# CIANCHOSAINT new-build: PoliticalPartyPipelineBase class — the
# canonical contract for the 24 per-party DLT source modules.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The PoliticalPartyPipelineBase
#   class + the per-jurisdiction cohort registry, Scenario:
#   PoliticalPartyPipelineBase provides the canonical contract).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# NOTE: The wholesale-copied ``dlt_sources/_cross/jurisdiction_pipeline_base.py``
# has a stale import (``dlt_sources.common.destinations_cianfhoghlaim``)
# and cannot be imported in the current cianchosaint tree (the typo was
# never fixed when the namespace was renamed). This file therefore
# re-implements the same contract directly against the corrected
# ``destinations_cianchosaint`` module, mirroring the shape of the
# wholesale-copied class (PARTY_ID / PARTY_NAME / JURISDICTION /
# SOURCE_BASE / ELECTORAL_COMMISSION_ID / VALID_JURISDICTIONS /
# party_to_row / build_pipeline) so the structure is recognisable to
# anyone reading the upstream spec.

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties._base — base class.

Phase 4 of the openspec change. Provides the
``PoliticalPartyPipelineBase`` contract that all 24 per-party DLT
source subclasses share:

- ``PARTY_ID``           — the canonical id used as ``natural_key``
- ``PARTY_NAME``         — the human-readable display name
- ``JURISDICTION``       — ``uk_hoc`` / ``roi_dail`` / ``ni_assembly`` /
                           ``senedd`` / ``holyrood`` / ``jsy`` / ``ggy`` /
                           ``iom``
- ``SOURCE_BASE``        — the party's official website (news / press URL)
- ``ELECTORAL_COMMISSION_ID`` — the Electoral Commission register id
                           (``PP-…`` for UK parties; ``nil`` for ROI parties
                           under the Electoral Reform Act 2022 register
                           transition period)
- ``@dlt.resource``      — ``press_releases`` (the canonical entry point
                           that downstream BAML extracts against)

Subclasses only need to set the 5 class attributes; the base class
yields the canonical cohort row + builds the destination pipeline.

Example::

    class ReformUKPipeline(PoliticalPartyPipelineBase):
        PARTY_ID = "reform-uk"
        PARTY_NAME = "Reform UK"
        JURISDICTION = "uk_hoc"
        SOURCE_BASE = "https://www.reformparty.uk/news"
        ELECTORAL_COMMISSION_ID = "PP-12345"

        @dlt.resource(name="reform_uk_press_releases", write_disposition="replace")
        def press_releases(self):
            yield from self._iter_press_releases()
"""
from __future__ import annotations

import hashlib
from collections.abc import Iterator
from datetime import UTC, datetime
from typing import Any, ClassVar

import dlt
import structlog

import dlt_sources
from dlt_sources.common.destinations_cianchosaint import get_dlt_destination

logger = structlog.get_logger(__name__)


VALID_JURISDICTIONS: tuple[str, ...] = (
    "uk_hoc", "senedd", "holyrood",
    "ni_assembly", "roi_dail", "roi_seanad",
    "jsy", "ggy", "iom",
)


class PoliticalPartyPipelineBase:
    """Shared base for the 24 per-political-party DLT pipelines.

    Provides:
    - ``VALID_JURISDICTIONS`` validation
    - destination factory via ``dlt_sources.common.destinations_cianchosaint``
    - ``party_to_row()`` helper — the canonical cohort row shape
    - ``build_pipeline()`` factory — the canonical ``dlt.pipeline`` config
    - ``_iter_press_releases()`` — the per-party generator hook

    Subclasses MUST set the 5 class attributes and MAY override the
    ``_iter_press_releases()`` generator to yield the per-party press
    release rows. The default generator yields a single seed row so a
    fresh subclass can be instantiated + validated before its
    implementation lands.
    """

    VALID_JURISDICTIONS: ClassVar[tuple[str, ...]] = VALID_JURISDICTIONS
    WRITE_DISPOSITION: ClassVar[str] = "merge"
    PRIMARY_KEY: ClassVar[list[str]] = ["natural_key"]

    # Subclass-overridable class attributes (declared here for IDE/mypy).
    PARTY_ID: ClassVar[str] = ""
    PARTY_NAME: ClassVar[str] = ""
    JURISDICTION: ClassVar[str] = ""
    SOURCE_BASE: ClassVar[str] = ""
    ELECTORAL_COMMISSION_ID: ClassVar[str] = ""

    def __init__(
        self,
        *,
        use_md: bool = True,
        valid_jurisdictions: tuple[str, ...] | None = None,
    ):
        valid_j = valid_jurisdictions or self.VALID_JURISDICTIONS
        if self.JURISDICTION and self.JURISDICTION not in valid_j:
            raise ValueError(
                f"jurisdiction={self.JURISDICTION!r} not in {valid_j}"
            )
        self.valid_jurisdictions = valid_j
        self.destination = get_dlt_destination(use_ducklake=use_md)
        self.ingested_at = datetime.now(UTC).isoformat()

    def _require(self, attr: str) -> str:
        """Return the class attribute or raise NotImplementedError."""
        value = getattr(type(self), attr, "")
        if not value:
            raise NotImplementedError(
                f"{type(self).__name__}: set {attr} class attribute"
            )
        return value

    def party_to_row(self, record: Any) -> dict[str, Any]:
        """Convert one raw press-release record to the canonical cohort row dict."""
        source_url = (
            getattr(record, "source_url", None)
            or (record.get("source_url") if isinstance(record, dict) else "")
            or ""
        )
        title = (
            getattr(record, "title", None)
            or (record.get("title") if isinstance(record, dict) else "")
            or ""
        )
        published_at = (
            getattr(record, "published_at", None)
            or (record.get("published_at") if isinstance(record, dict) else None)
            or self.ingested_at
        )
        party_id = self._require("PARTY_ID")
        natural_key = f"{party_id}|{source_url}|{published_at}"
        # content_sha256: a real hash, but only of the metadata fields we
        # capture (source_url + title + published_at + party_id). Real
        # per-document content hashing belongs in the DLT resources that
        # actually download bytes — see
        # dlt_sources.common.content_deduplication.py for that primitive.
        content_sha256 = hashlib.sha256(
            "|".join(
                str(v)
                for v in (source_url, title, published_at, party_id)
            ).encode("utf-8")
        ).hexdigest()
        return {
            "party_id": party_id,
            "party_name": self.PARTY_NAME,
            "jurisdiction": self.JURISDICTION,
            "source_url": source_url,
            "title": title,
            "published_at": published_at,
            "electoral_commission_id": self.ELECTORAL_COMMISSION_ID,
            "source_base": self.SOURCE_BASE,
            "natural_key": natural_key,
            "content_sha256": content_sha256,
            "ingested_at": self.ingested_at,
            "namespace": (
                f"cianchosaint.political_parties.{self.JURISDICTION}."
                f"{party_id}"
            ),
        }

    def build_pipeline(self, dataset_name: str | None = None) -> Any:
        """Build the canonical DLT pipeline for this party."""
        party_id = self._require("PARTY_ID")
        dataset = dataset_name or f"political_parties_{party_id.replace('-', '_')}"
        return dlt.pipeline(
            pipeline_name=f"{party_id}_pipeline",
            dataset_name=dataset,
            destination=self.destination,
        )

    # ----- generator hook -----

    def _iter_press_releases(self) -> Iterator[dict[str, Any]]:
        """Default generator — yields a single seed row.

        Subclasses override this to yield the per-party press releases
        (typically by calling ``self.party_to_row(record)`` over a list
        of raw records from ``dlt_sources.common.site_crawler``).
        """
        yield self.party_to_row({
            "source_url": self.SOURCE_BASE,
            "title": f"{self.PARTY_NAME} — seed record",
            "published_at": self.ingested_at,
        })

    def run(self, dataset_name: str | None = None) -> Any:
        """Convenience: build pipeline + run the press_releases resource + return load_info.

        Passes WRITE_DISPOSITION/PRIMARY_KEY through explicitly (mirrors
        the wholesale-copied JurisdictionPipelineBase.run contract).
        """
        party_id = self._require("PARTY_ID")
        pipeline = self.build_pipeline(dataset_name=dataset_name)

        @dlt.resource(
            name=f"{party_id.replace('-', '_')}_press_releases",
            write_disposition=self.WRITE_DISPOSITION,
            primary_key=self.PRIMARY_KEY,
        )
        def press_releases() -> Iterator[dict[str, Any]]:
            yield from self._iter_press_releases()

        load_info = pipeline.run(press_releases())
        return load_info


__all__ = [
    "PoliticalPartyPipelineBase",
    "VALID_JURISDICTIONS",
]