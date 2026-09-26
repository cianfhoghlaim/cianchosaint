# Cross-Repo Sync: cianchosaint-codelab-v1

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `docs/google_examples/adk2-tutorial/codelab/` + `loop-lab-table/codelab/` remain the upstream reference. No changes to the cianfhoghlaim or leabharlann repos are needed.

## Order of Operations

```
[1] cianchosaint → openspec/changes/cianchosaint-codelab-v1/
                   (proposal + tasks + cross-repo-sync + spec)
                   Adds: codelab/politician-pipeline.md
                   Adds: notebooks/build.py
                   Adds: scripts/walk.py
                   Pushed to main.
                       ↓
[2] operator    → cd cianchosaint && openspec validate cianchosaint-codelab-v1 --strict
                  → openspec validate --all --strict
                  → All validations pass
                       ↓
[3] operator    → openspec archive cianchosaint-codelab-v1 --yes
```

## Repo 1: cianchosaint (sole)

**Files to commit** (under `openspec/changes/cianchosaint-codelab-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-codelab/spec.md` (the canonical spec)

**New files**:
- `codelab/politician-pipeline.md` (~400 lines) — the markdown walkthrough
- `notebooks/build.py` (~150 lines) — the Colab-style notebook builder
- `scripts/walk.py` (~120 lines) — the assertion-as-sentence runner

## Repo 2: cianfhoghlaim (unchanged)

The upstream `docs/google_examples/adk2-tutorial/codelab/` + `loop-lab-table/codelab/` remain unchanged. We wholesale-adapt the pattern in this change.

## Repo 3: leabharlann (unchanged)

The 87 politics PDFs in `leabharlann/gemini_deep_research/politics/` are read-only context for the politician pipeline (which T3.2 doesn't touch). No changes.
