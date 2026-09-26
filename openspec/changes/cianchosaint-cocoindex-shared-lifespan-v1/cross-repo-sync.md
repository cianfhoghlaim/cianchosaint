# Cross-Repo Sync: cianchosaint-cocoindex-shared-lifespan-v1

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `cocoindex_flows/_shared/_lifespan.py` remains the upstream reference. No changes to the cianfhoghlaim or leabharlann repos are needed.

## Order of Operations

```
[1] cianchosaint → openspec/changes/cianchosaint-cocoindex-shared-lifespan-v1/
                   (proposal + tasks + cross-repo-sync + spec)
                   Adds: cocoindex_flows/cianchosaint/_shared/{__init__,_lifespan,_factory}.py
                   Adds: cocoindex_flows/cianchosaint/politician_dossier_aggregator.py
                   Modifies: cocoindex_flows/cianchosaint/{source_policy,vlm_pipeline}_aggregator.py
                   Adds: tests/cocoindex_flows/test_shared_lifespan.py
                   Pushed to main.
                       ↓
[2] operator    → cd cianchosaint && openspec validate cianchosaint-cocoindex-shared-lifespan-v1 --strict
                  → openspec validate --all --strict
                  → All validations pass
                       ↓
[3] operator    → openspec archive cianchosaint-cocoindex-shared-lifespan-v1 --yes
```

## Repo 1: cianchosaint (sole)

**Files to commit** (under `openspec/changes/cianchosaint-cocoindex-shared-lifespan-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-cocoindex-shared-lifespan/spec.md` (the canonical spec)

**New files**:
- `cocoindex_flows/cianchosaint/_shared/__init__.py` (~20 LOC) — the package marker
- `cocoindex_flows/cianchosaint/_shared/_lifespan.py` (~150 LOC) — the canonical shared lifespan
- `cocoindex_flows/cianchosaint/_shared/_factory.py` (~100 LOC) — the `make_coanco_app()` helper
- `cocoindex_flows/cianchosaint/politician_dossier_aggregator.py` (~200 LOC) — the BIOD v1 / BIPP v2 cohort flow
- `tests/cocoindex_flows/test_shared_lifespan.py` (~80 LOC) — the smoke test

**Modified files**:
- `cocoindex_flows/cianchosaint/source_policy_aggregator.py` — use the shared lifespan + factory
- `cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py` — use the shared lifespan + factory

## Repo 2: cianfhoghlaim (unchanged)

The upstream `cocoindex_flows/_shared/_lifespan.py` remains unchanged. We wholesale-adapt the pattern in this change.

## Repo 3: leabharlann (unchanged)

The 87 politics PDFs in `leabharlann/gemini_deep_research/politics/` are read-only context. No changes.
