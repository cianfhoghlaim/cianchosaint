# Change: cianchosaint-cocoindex-shared-lifespan-v1

## Why

Cianfhoghlaim's `cocoindex_flows/_shared/_lifespan.py` consolidates 14 CocoIndex v1 Apps' shared lifespan into one module. Every app reuses:

- 3 shared `ContextKey`s: `LANCE_DB` (the LanceDB async connection), `EMBEDDER` (the sentence-transformer embedder), and `RESOLVED_FILE_REGISTRY` (the file registry)
- The canonical `shared_lifespan` async context manager

Cianchosaint has CocoIndex flows at `cocoindex_flows/cianchosaint/` (`source_policy_aggregator.py`, `vlm_pipeline_aggregator.py`, plus the upcoming `politician_dossier_aggregator.py` from BIPP v2). Each one is hand-rolled — none of them share a lifespan.

This change lands the canonical `shared_lifespan.py` so every CocoIndex v1 App in cianchosaint can use one module-load connection + one embedder instance, mirroring the cianfhoghlaim `R1-R4 conformance gate`.

## What changes

- **NEW file** `cocoindex_flows/cianchosaint/_shared/__init__.py` (~20 LOC) — the package marker + canonical re-exports
- **NEW file** `cocoindex_flows/cianchosaint/_shared/_lifespan.py` (~150 LOC) — the canonical shared lifespan (mirrors cianfhoghlaim's `_lifespan.py`)
- **NEW file** `cocoindex_flows/cianchosaint/_shared/_factory.py` (~100 LOC) — the canonical CocoIndex App factory helper (`make_coanco_app()`)
- **MODIFIED** `cocoindex_flows/cianchosaint/source_policy_aggregator.py` — use the shared lifespan + factory
- **MODIFIED** `cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py` — use the shared lifespan + factory
- **NEW file** `cocoindex_flows/cianchosaint/politician_dossier_aggregator.py` (~200 LOC) — the BIOD v1 / BIPP v2 cohort flow that uses the shared lifespan
- **NEW test** `tests/cocoindex_flows/test_shared_lifespan.py` — verifies the lifespan shares the connection + embedder
- **NEW spec delta** `openspec/changes/cianchosaint-cocoindex-shared-lifespan-v1/specs/cianchosaint-cocoindex-shared-lifespan/spec.md`

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-cocoindex-shared-lifespan`)
- Affected code/config: 4 NEW files + 2 MODIFIED files
- **0 NEW DLT sources, 0 NEW BAML files** — pure CocoIndex refactor
- Estimated LOC: ~650 LOC added
- **0 new dependencies** — uses the existing `cocoindex` + `lancedb` packages

## Out of scope (follow-up changes)

- The per-constituency CocoIndex flows (the BIOD v1 / BIPP v2 / BGARD v1 / BPSNI v1 cohorts) — those land in T4.1 (per-intelligence-deep-dive) and downstream
- The Dagster asset integration (T3.3) — uses the same lifespan but orchestrates scheduling

## Dependencies

`Blocked by: none` — pure refactor
`Affected repos: cianchosaint only.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `cocoindex_flows/_shared/_lifespan.py` remains the upstream reference.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-cocoindex-shared-lifespan-v1 --strict
# Expected: Validation passes

# 2. test the shared lifespan
PYTHONPATH=. python3 tests/cocoindex_flows/test_shared_lifespan.py
# Expected: connection + embedder are shared

# 3. regression: existing CocoIndex flows still work
PYTHONPATH=. python3 -c "from cocoindex_flows.cianchosaint.source_policy_aggregator import *"

# 4. lint_license
mise run lint:license
```
