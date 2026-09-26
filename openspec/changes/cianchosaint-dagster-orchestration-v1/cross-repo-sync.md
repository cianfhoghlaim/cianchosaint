# Cross-Repo Sync: cianchosaint-dagster-orchestration-v1

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `orchestration/defs/2_materials/_base/jurisdiction_assets_base.py` remains the upstream reference. No changes to the cianfhoghlaim or leabharlann repos are needed.

## Order of Operations

```
[1] cianchosaint → openspec/changes/cianchosaint-dagster-orchestration-v1/
                   (proposal + tasks + cross-repo-sync + spec)
                   Adds: orchestration/defs/2_materials/_base/{__init__,jurisdiction_assets_base}.py
                   Adds: orchestration/defs/2_materials/_ga/ga_politician_pipeline_assets.py
                   Pushed to main.
                       ↓
[2] operator    → cd cianchosaint && openspec validate cianchosaint-dagster-orchestration-v1 --strict
                  → openspec validate --all --strict
                  → All validations pass
                       ↓
[3] operator    → openspec archive cianchosaint-dagster-orchestration-v1 --yes
```

## Repo 1: cianchosaint (sole)

**Files to commit** (under `openspec/changes/cianchosaint-dagster-orchestration-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-dagster-orchestration/spec.md` (the canonical spec)

**New files**:
- `orchestration/defs/2_materials/_base/__init__.py` (~20 LOC)
- `orchestration/defs/2_materials/_base/jurisdiction_assets_base.py` (~250 LOC)
- `orchestration/defs/2_materials/_ga/ga_politician_pipeline_assets.py` (~100 LOC)

## Repo 2: cianfhoghlaim (unchanged)

The upstream `orchestration/defs/2_materials/_base/jurisdiction_assets_base.py` remains unchanged. We wholesale-adapt the pattern in this change.

## Repo 3: leabharlann (unchanged)

The 87 politics PDFs in `leabharlann/gemini_deep_research/politics/` are read-only context for the politician pipeline (which T3.3 doesn't touch). No changes.
