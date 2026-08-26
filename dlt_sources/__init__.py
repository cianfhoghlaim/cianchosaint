"""cianchosaint.dlt_sources — DLT ingestion layer + cross-jurisdiction registry.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change +
`openspec/plans/2026-08-24-dlt-deep-analysis-v2.md` §Phase 4.1.

The wholesale-copy of cianfhoghlaim on 2026-08-23 (per the
`cianchosaint-repo-bootstrap-v2` openspec change) omitted the
canonical root `__init__.py` (the cianfhoghlaim file at
`dlt_sources/__init__.py` documents the v7 flattening + the
per-area contract surface). This file restores that surface for
the cianchosaint namespace.

The cianchosaint dlt_sources subtree exposes:

1. **`_cross/`** — the cross-jurisdiction aggregator registry (the
   BIEP v3 cross-cutting wholesale-copy + the new
   `law_enforcement_registry` carve-out per §21.2 of the parent
   change `2026-08-24-dlt-sources-to-multi-repo-scaffold-v1`).
2. **`law_enforcement/`** — the new BI law-enforcement + civil
   protection vertical (per Q1 user clarification:
   evidence-collection for law-enforcement purposes goes to
   cianchosaint). 8 per-jurisdiction skeletons
   (ireland / england / scotland / wales / northern_ireland /
   jersey / guernsey / isle_of_man).
3. **`cianchosaint/`** — the existing defence / policing /
   intelligence-oversight vertical (BIPP v1 / BIDP v1 / BIIP v1
   sub-verticals). Phase 4 (6 → 12 months) carves the
   per-jurisdiction law-enforcement sources OUT of these trees
   and INTO the new `law_enforcement/<jurisdiction>/` trees.
4. **`common/`** — the per-sister copy of the cianfhoghlaim
   `common/` helpers (`destinations_cianchosaint` + the HTTP
   client + the Firecrawl source + the endpoint recovery +
   the schema registry + the structured-logging helpers).
5. **`official_media_cianchosaint/`** — the existing
   official-media surface (the sister-repo counterpart of
   cianfhoghlaim's `official_media/`).

## Per-sister carve rule

Per the user-confirmed split (Q1 of the multi-repo-scaffold
conversation):

- **Court-facing procedural rules** → `ciandlíthe` (NOT here).
- **Evidence-collection for law-enforcement purposes** →
  cianchosaint (this repo).
- **UoG bilingual educational content** → `cianfhoghlaim`
  (stays there per the bilingual carve rule).
- **Pure Irish-language datasets + non-educational Celtic-language
  pipelines** → `ciancheiltis` (deferred past Phase 4).

## References

- Parent change: `openspec/changes/2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/`
- Companion plan: `openspec/plans/2026-08-24-dlt-deep-analysis-v2.md`
- Per-sister init change: `openspec/changes/2026-08-24-cianchosaint-init-v1/`
- Per-sister carve-out change: `openspec/changes/2026-09-XX-cianchosaint-initial-carveout-v1/`
"""
from __future__ import annotations

__all__: list[str] = [
    # The 5 canonical top-level subtrees (per-sister shape).
    "_cross",
    "law_enforcement",
    "cianchosaint",
    "common",
    "official_media_cianchosaint",
]