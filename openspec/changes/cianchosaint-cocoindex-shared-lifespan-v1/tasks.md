# Tasks: cianchosaint-cocoindex-shared-lifespan-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.11+ installed
- [x] Verify `cocoindex` + `lancedb` packages installed (per cianfhoghlaim's `_lifespan.py`)

## 1. Author the canonical shared lifespan

- [x] Write `cocoindex_flows/cianchosaint/_shared/__init__.py` (~20 LOC) — package marker + re-exports
- [x] Write `cocoindex_flows/cianchosaint/_shared/_lifespan.py` (~150 LOC) — the canonical `shared_lifespan` async context manager + 3 shared `ContextKey`s (LANCE_DB, EMBEDDER, RESOLVED_FILE_REGISTRY)
- [x] Write `cocoindex_flows/cianchosaint/_shared/_factory.py` (~100 LOC) — the `make_coanco_app()` helper

## 2. Refactor the 2 existing CocoIndex flows

- [x] Modify `cocoindex_flows/cianchosaint/source_policy_aggregator.py` — use the shared lifespan + factory
- [x] Modify `cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py` — use the shared lifespan + factory

## 3. Add the politician dossier aggregator

- [x] Write `cocoindex_flows/cianchosaint/politician_dossier_aggregator.py` (~200 LOC) — the BIOD v1 / BIPP v2 cohort flow

## 4. Author the spec + the test

- [x] Write `openspec/changes/cianchosaint-cocoindex-shared-lifespan-v1/specs/cianchosaint-cocoindex-shared-lifespan/spec.md` — the canonical spec (Requirement: shared lifespan contract + R1-R4 conformance; Scenario: every app uses shared connection + embedder)
- [x] Write `openspec/changes/cianchosaint-cocoindex-shared-lifespan-v1/cross-repo-sync.md` — sole repo cianchosaint
- [x] Write `tests/cocoindex_flows/test_shared_lifespan.py` — verifies the lifespan shares the connection + embedder

## 5. CI gate

- [x] Run `openspec validate cianchosaint-cocoindex-shared-lifespan-v1 --strict`
- [x] Run `PYTHONPATH=. python3 tests/cocoindex_flows/test_shared_lifespan.py`
- [x] Run `mise run lint:license`

## 6. Commit + archive

- [x] `git add openspec/changes/cianchosaint-cocoindex-shared-lifespan-v1/ cocoindex_flows/cianchosaint/_shared/ cocoindex_flows/cianchosaint/{source_policy_aggregator,vlm_pipeline_aggregator,politician_dossier_aggregator}.py tests/cocoindex_flows/`
- [x] `git commit -m "feat(cianchosaint): add shared CocoIndex lifespan + factory + 3rd flow"`
- [x] `openspec archive cianchosaint-cocoindex-shared-lifespan-v1 --yes`

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-cocoindex-shared-lifespan-v1 --strict

# 2. test the shared lifespan
PYTHONPATH=. python3 tests/cocoindex_flows/test_shared_lifespan.py

# 3. regression: existing CocoIndex flows still work
PYTHONPATH=. python3 -c "from cocoindex_flows.cianchosaint.source_policy_aggregator import *"

# 4. lint_license
mise run lint:license
```
