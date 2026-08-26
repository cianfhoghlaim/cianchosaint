"""dlt_sources/law_enforcement — BI law-enforcement + civil-protection vertical.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change +
`openspec/plans/2026-08-24-dlt-deep-analysis-v2.md` §Phase 4.1.

The `law_enforcement/` vertical is a **NEW** British-Isles per-vertical
subtree that did NOT exist in cianfhoghlaim (the legal/procedural side
goes to ciandlíthe; the evidence-collection + civil-protection side
goes here, in cianchosaint).

## Per-jurisdiction subtrees (8 / 8 BI jurisdictions)

| Jurisdiction | Skeleton path | Defence | Policing | Intel oversight |
|---|---|:--:|:--:|:--:|
| Ireland | `law_enforcement/ireland/` | IDF + Air Corps + Naval | An Garda Síochána | Garda Inspectorate |
| England | `law_enforcement/england/` | RAF + RN + Army (UK-wide) | 43 forces + Met + BTP | IPCO + IPT |
| Scotland | `law_enforcement/scotland/` | UK-wide (shared) | Police Scotland | Scottish IPA |
| Wales | `law_enforcement/wales/` | UK-wide (shared) | 4 Welsh forces | IPCO (Wales) |
| Northern Ireland | `law_enforcement/northern_ireland/` | UK-wide (shared) | PSNI | NI Policing Board + IPO |
| Jersey | `law_enforcement/jersey/` | UK MoD (Crown dep.) | States of Jersey Police | Jersey IPA |
| Guernsey | `law_enforcement/guernsey/` | UK MoD (Crown dep.) | Guernsey Police | Guernsey IPA |
| Isle of Man | `law_enforcement/isle_of_man/` | UK MoD (Crown dep.) | Isle of Man Constabulary | IoM IPA |

## Carve rule (per the user-confirmed split)

- **Court-facing procedural rules** → `ciandlíthe` (per the Q1 clarification).
- **Evidence-collection for law-enforcement purposes** → `cianchosaint` (this repo).
- **NAO + C&AG reports** of Éire + UK + Crown Dependencies → `cianchosaint` (per the cianchosaint description).

## The 5 canonical skeleton files (per-jurisdiction)

1. `__init__.py` — 1-line re-export
2. `_factory.py` — `JurisdictionPipelineBase` subclass with `STAGE = "law_enforcement"`
3. `sources.py` — skeleton `@dlt.source` / `@dlt.resource` defs (with TODO markers)
4. `schema.py` — skeleton pydantic schemas
5. `AGENTS.md` — per-jurisdiction routing doc

## Phase 4 wire-up (per the v2 plan)

Phase 4 (6 → 12 months) carves the per-jurisdiction law-enforcement
sources OUT of the existing `dlt_sources/cianchosaint/<jurisdiction>/`
trees (the ones already in this repo) and INTO the per-jurisdiction
`law_enforcement/<jurisdiction>/` skeletons created by this change.
Until then, the existing `dlt_sources/cianchosaint/<jurisdiction>/`
trees remain the source of truth.
"""
from __future__ import annotations

from dlt_sources.law_enforcement import ireland  # noqa: F401

__all__ = ["ireland"]