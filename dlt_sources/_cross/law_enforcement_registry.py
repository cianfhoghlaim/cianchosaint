# CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch, with
# the `law_enforcement_registry` carve-out per the
# `2026-09-XX-cianchosaint-initial-carveout-v1` change +
# `openspec/plans/2026-08-24-dlt-deep-analysis-v2.md` §Phase 4.1.
#
# Original pattern: cianfhoghlaim/dlt_sources/british_isles/_cross/registry_api.py.
# This file is the cianchosaint-side analogue of
# `ciandlíthe/dlt_sources/_cross/legal_registry.py` (the per-vertical
# registry aggregator that the per-jurisdiction sources subscribe to).

"""Law-enforcement intelligence registry — the per-jurisdiction aggregator.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.

The canonical cross-jurisdiction aggregator for the
`dlt_sources/law_enforcement/<jurisdiction>/` vertical. Same shape as
`ciandlíthe/dlt_sources/_cross/legal_registry.py` (the legal-pipeline
sister surface).

## API surface

- `LAW_ENFORCEMENT_PER_JURISDICTION` — the canonical dict mapping every
  BI jurisdiction → `*(<law_enforcement source>, ...)` tuple.
- `law_enforcement_intelligence_sources(jurisdiction)` — the per-jurisdiction
  `@dlt.source` factory dispatcher.
- `LAW_ENFORCEMENT_JURISDICTIONS` — the canonical 8-row tuple
  (ireland + england + scotland + wales + northern_ireland +
  jersey + guernsey + isle_of_man).

## Per-jurisdiction rows

The 8 per-jurisdiction skeletons expose the
`*_law_enforcement_intelligence_sources()` `@dlt.source` factory +
the `<Jurisdiction>LawEnforcementPipeline` class +
the `<jurisdiction>_law_enforcement_pipeline` singleton.

This module aggregates them into one cross-jurisdiction surface so a
single DAGSTER asset can iterate all 8 jurisdictions in one
materialisation.

## KCG patterns used

- `JurisdictionPipelineBase` (per the
  `2026-08-24-dlt-sources-to-multi-repo-scaffold-v1` §11 / the
  `2026-09-XX-cianchosaint-initial-carveout-v1` carve-out) — the
  shared base class at `dlt_sources/_cross/jurisdiction_pipeline_base.py`.
- ibis (per `.agents/skills/ibis/SKILL.md`) — every query uses
  ``ibis.duckdb.connect()`` (NO raw ``duckdb.connect``).
- dlt 1.30 §6.3 (`.add_limit(1)`) + §6.4 (`retry_schema_update`) +
  §6.5 (`abort_packages`) — inherited from the base class.
"""
from __future__ import annotations

from collections.abc import Iterator
from typing import Any, Literal

import dlt

# The per-jurisdiction sources are imported lazily inside each
# `_ireland_intel_sources` / `_england_intel_sources` etc. dispatcher
# function below to avoid the circular import between
# `dlt_sources._cross.law_enforcement_registry` (imported by
# `dlt_sources._cross.__init__.py`) and the per-jurisdiction
# `_factory.py` (which imports `dlt_sources._cross.__init__.py`
# transitively).


LAW_ENFORCEMENT_JURISDICTIONS: tuple[str, ...] = (
    "ireland", "england", "scotland", "wales",
    "northern_ireland", "jersey", "guernsey", "isle_of_man",
)
"""The canonical 8 British-Isles jurisdictions for the
`law_enforcement/` vertical (parity with the BIEP v3
`VALID_JURISDICTIONS`)."""

LawEnforcementJurisdiction = Literal[
    "ireland", "england", "scotland", "wales",
    "northern_ireland", "jersey", "guernsey", "isle_of_man",
]
"""The canonical type-literal for the 8 BI jurisdictions."""


# ─── Per-jurisdiction @dlt.source dispatchers ─────────────────────────────
# Each dispatcher returns the per-jurisdiction `@dlt.source` factory
# (parity with `ciandlíthe/dlt_sources/_cross/legal_registry.py`).


def _ireland_intel_sources(language: str = "en") -> list[Any]:
    """Return the 6 Éire law-enforcement `@dlt.resource` stubs."""
    from dlt_sources.law_enforcement.ireland.sources import (
        ireland_law_enforcement_intelligence_sources,
    )
    return ireland_law_enforcement_intelligence_sources(language=language)


def _england_intel_sources(language: str = "en") -> list[Any]:
    """Return the 6 England law-enforcement `@dlt.resource` stubs."""
    from dlt_sources.law_enforcement.england.sources import (
        england_law_enforcement_intelligence_sources,
    )
    return england_law_enforcement_intelligence_sources(language=language)


def _scotland_intel_sources(language: str = "en") -> list[Any]:
    """Return the 6 Scotland law-enforcement `@dlt.resource` stubs."""
    from dlt_sources.law_enforcement.scotland.sources import (
        scotland_law_enforcement_intelligence_sources,
    )
    return scotland_law_enforcement_intelligence_sources(language=language)


def _wales_intel_sources(language: str = "en") -> list[Any]:
    """Return the 6 Wales law-enforcement `@dlt.resource` stubs."""
    from dlt_sources.law_enforcement.wales.sources import (
        wales_law_enforcement_intelligence_sources,
    )
    return wales_law_enforcement_intelligence_sources(language=language)


def _northern_ireland_intel_sources(language: str = "en") -> list[Any]:
    """Return the 6 NI law-enforcement `@dlt.resource` stubs."""
    from dlt_sources.law_enforcement.northern_ireland.sources import (
        northern_ireland_law_enforcement_intelligence_sources,
    )
    return northern_ireland_law_enforcement_intelligence_sources(language=language)


def _jersey_intel_sources(language: str = "en") -> list[Any]:
    """Return the 6 Jersey law-enforcement `@dlt.resource` stubs."""
    from dlt_sources.law_enforcement.jersey.sources import (
        jersey_law_enforcement_intelligence_sources,
    )
    return jersey_law_enforcement_intelligence_sources(language=language)


def _guernsey_intel_sources(language: str = "en") -> list[Any]:
    """Return the 6 Guernsey law-enforcement `@dlt.resource` stubs."""
    from dlt_sources.law_enforcement.guernsey.sources import (
        guernsey_law_enforcement_intelligence_sources,
    )
    return guernsey_law_enforcement_intelligence_sources(language=language)


def _isle_of_man_intel_sources(language: str = "en") -> list[Any]:
    """Return the 6 IoM law-enforcement `@dlt.resource` stubs."""
    from dlt_sources.law_enforcement.isle_of_man.sources import (
        isle_of_man_law_enforcement_intelligence_sources,
    )
    return isle_of_man_law_enforcement_intelligence_sources(language=language)


# ─── The canonical per-jurisdiction registry dict ─────────────────────────


LAW_ENFORCEMENT_PER_JURISDICTION: dict[
    LawEnforcementJurisdiction,
    Any,
] = {
    "ireland": _ireland_intel_sources,
    "england": _england_intel_sources,
    "scotland": _scotland_intel_sources,
    "wales": _wales_intel_sources,
    "northern_ireland": _northern_ireland_intel_sources,
    "jersey": _jersey_intel_sources,
    "guernsey": _guernsey_intel_sources,
    "isle_of_man": _isle_of_man_intel_sources,
}
"""The canonical per-jurisdiction dispatcher dict.

Maps each of the 8 BI jurisdictions to its per-jurisdiction
`@dlt.source` factory. Used by the BIEP v3 cross-jurisdiction bridge
sensors + the marimo sister-repo dashboard."""


# ─── The cross-jurisdiction @dlt.source aggregator ────────────────────────


@dlt.source(name="law_enforcement_intelligence_all_jurisdictions")
def law_enforcement_intelligence_sources(
    jurisdiction: LawEnforcementJurisdiction | None = None,
    language: str = "en",
) -> list[Any]:
    """Cross-jurisdiction BI law-enforcement + civil-protection intelligence.

    Pass `jurisdiction="ireland"` (or any of the 8 BI jurisdictions)
    to get the per-jurisdiction sources. Pass `jurisdiction=None`
    (the default) to get all 8 jurisdictions × 6 sub-verticals
    = 48 `@dlt.resource` stubs in one materialisation.

    TODO(2026-09-XX): once Phase 4 wires the actual sources,
    the per-resource stubs become real data emitters. The
    cross-jurisdiction aggregator stays unchanged.
    """
    if jurisdiction is not None:
        if jurisdiction not in LAW_ENFORCEMENT_PER_JURISDICTION:
            raise ValueError(
                f"jurisdiction={jurisdiction!r} not in "
                f"{LAW_ENFORCEMENT_JURISDICTIONS}"
            )
        factory = LAW_ENFORCEMENT_PER_JURISDICTION[jurisdiction]
        return factory(language=language)
    out: list[Any] = []
    for jur in LAW_ENFORCEMENT_JURISDICTIONS:
        factory = LAW_ENFORCEMENT_PER_JURISDICTION[jur]
        out.extend(factory(language=language))
    return out


# ─── Per-jurisdiction pipeline singleton accessor ─────────────────────────


def get_law_enforcement_pipeline(jurisdiction: LawEnforcementJurisdiction) -> Any:
    """Return the per-jurisdiction `<jurisdiction>_law_enforcement_pipeline`
    singleton (mirrors the BIEP v3 per-jurisdiction accessor pattern).

    TODO(2026-09-XX): once Phase 4 wires the real sources, this
    becomes the canonical accessor used by the marimo
    `notebooks/law_enforcement_dashboard.py` notebook.
    """
    if jurisdiction == "ireland":
        from dlt_sources.law_enforcement.ireland._factory import (
            ireland_law_enforcement_pipeline,
        )
        return ireland_law_enforcement_pipeline
    if jurisdiction == "england":
        from dlt_sources.law_enforcement.england._factory import (
            england_law_enforcement_pipeline,
        )
        return england_law_enforcement_pipeline
    if jurisdiction == "scotland":
        from dlt_sources.law_enforcement.scotland._factory import (
            scotland_law_enforcement_pipeline,
        )
        return scotland_law_enforcement_pipeline
    if jurisdiction == "wales":
        from dlt_sources.law_enforcement.wales._factory import (
            wales_law_enforcement_pipeline,
        )
        return wales_law_enforcement_pipeline
    if jurisdiction == "northern_ireland":
        from dlt_sources.law_enforcement.northern_ireland._factory import (
            northern_ireland_law_enforcement_pipeline,
        )
        return northern_ireland_law_enforcement_pipeline
    if jurisdiction == "jersey":
        from dlt_sources.law_enforcement.jersey._factory import (
            jersey_law_enforcement_pipeline,
        )
        return jersey_law_enforcement_pipeline
    if jurisdiction == "guernsey":
        from dlt_sources.law_enforcement.guernsey._factory import (
            guernsey_law_enforcement_pipeline,
        )
        return guernsey_law_enforcement_pipeline
    if jurisdiction == "isle_of_man":
        from dlt_sources.law_enforcement.isle_of_man._factory import (
            isle_of_man_law_enforcement_pipeline,
        )
        return isle_of_man_law_enforcement_pipeline
    raise ValueError(
        f"jurisdiction={jurisdiction!r} not in {LAW_ENFORCEMENT_JURISDICTIONS}"
    )


def iter_law_enforcement_pipelines() -> Iterator[tuple[str, Any]]:
    """Yield every (jurisdiction, pipeline-singleton) pair.

    Convenience for Dagster asset materialisation + marimo dashboard
    iteration.
    """
    for jurisdiction in LAW_ENFORCEMENT_JURISDICTIONS:
        yield jurisdiction, get_law_enforcement_pipeline(jurisdiction)


__all__ = [
    "LAW_ENFORCEMENT_JURISDICTIONS",
    "LawEnforcementJurisdiction",
    "LAW_ENFORCEMENT_PER_JURISDICTION",
    "law_enforcement_intelligence_sources",
    "get_law_enforcement_pipeline",
    "iter_law_enforcement_pipelines",
]