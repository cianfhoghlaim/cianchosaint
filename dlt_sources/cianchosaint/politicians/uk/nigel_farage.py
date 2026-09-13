# CIANCHOSAINT new-build: per-politician DLT source for Nigel Farage (Reform UK / Clacton / UK HoC).
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The 7 case-study
# politician DLT source modules.
#
# Canonical sources:
# - https://www.reformparty.uk/people/nigel-farage (Reform UK profile)
# - https://www.nigelfarage.com (personal website)
# - https://www.parliament.uk/biographies/commons/mr-nigel-farage/4677 (UK Parliament)
# - https://www.theyworkforyou.com/mp/nigel_farage/clacton (TWFY)
# - https://www.electoralcommission.org.uk/ (Electoral Commission register)
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.politicians.uk.nigel_farage — Nigel Farage.

Canonical sources:
- Reform UK profile: https://www.reformparty.uk/people/nigel-farage
- Personal website:  https://www.nigelfarage.com
- UK Parliament:     https://www.parliament.uk/biographies/commons/mr-nigel-farage/4677
- TheyWorkForYou:    https://www.theyworkforyou.com/mp/nigel_farage/clacton

Honours `USE_LOCAL_SCRAPES=true` falling back to
`stedding/ingest_queue/uk_hoc/nigel_farage/`.
"""
from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import dlt
import structlog

from dlt_sources.cianchosaint.politicians._base import (
    PoliticianPipelineBase,
)

logger = structlog.get_logger(__name__)


REFORM_UK_FARAGE_PROFILE = "https://www.reformparty.uk/people/nigel-farage"
FARAGE_PERSONAL_WEBSITE = "https://www.nigelfarage.com"
FARAGE_PARLIAMENT_URL = "https://www.parliament.uk/biographies/commons/mr-nigel-farage/4677"
FARAGE_TWFY_URL = "https://www.theyworkforyou.com/mp/nigel_farage/clacton"


class NigelFaragePipeline(PoliticianPipelineBase):
    """Nigel Farage — Reform UK MP for Clacton."""

    POLITICIAN_ID = "nigel_farage"
    CANONICAL_NAME = "Nigel Farage"
    HONORIFIC = "MP"
    PARTY_ID = "reform-uk"
    PARTY_NAME = "Reform UK"
    JURISDICTION = "uk_hoc"
    CONSTITUENCY = "Clacton"
    SOURCE_BASE = REFORM_UK_FARAGE_PROFILE

    def _iter_politician_records(self) -> Iterator[dict[str, Any]]:
        """Yield the canonical Nigel Farage Politician cohort row.

        The politician_to_row() base class yields the static row from the
        class attributes; subclasses MAY extend with scraped social_handles +
        public_metrics (the canonical place to do that is the
        `politician_account_resolver` FunctionTool — see
        `agents/cianchosaint/tools/politician_account_resolver.py`).
        """
        yield self.politician_to_row()


@dlt.source(name="nigel_farage")
def nigel_farage_source() -> list:
    """DLT source for Nigel Farage (Reform UK / Clacton / UK HoC)."""

    @dlt.resource(
        name="nigel_farage_politician",
        write_disposition="merge",
        primary_key=["politician_id"],
    )
    def politician() -> Iterator[dict[str, Any]]:
        pipeline = NigelFaragePipeline()
        yield from pipeline._iter_politician_records()

    return [politician()]


__all__ = [
    "FARAGE_PARLIAMENT_URL",
    "FARAGE_PERSONAL_WEBSITE",
    "FARAGE_TWFY_URL",
    "NigelFaragePipeline",
    "REFORM_UK_FARAGE_PROFILE",
    "nigel_farage_source",
]
