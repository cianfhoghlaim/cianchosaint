# Cross-Repo Sync: cianchosaint-narrative-deep-dive-v1

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `docs/google_examples/adk-examples/agent-valley-archive` remains the upstream reference. No changes to the cianfhoghlaim or leabharlann repos are needed.

## Order of Operations

```
[1] cianchosaint → openspec/changes/cianchosaint-narrative-deep-dive-v1/
                   (proposal + tasks + cross-repo-sync + spec)
                   Adds: agents/cianchosaint/narrative/{__init__,context,season,dossier}.py
                   Adds: baml_src/cianchosaint/politics/bipp_v2_narrative.baml
                   Adds: tests/agents/cianchosaint/test_narrative_deep_dive.py
                   Pushed to main.
                       ↓
[2] operator    → cd cianchosaint && openspec validate cianchosaint-narrative-deep-dive-v1 --strict
                  → openspec validate --all --strict
                  → All validations pass
                       ↓
[3] operator    → openspec archive cianchosaint-narrative-deep-dive-v1 --yes
```

## Repo 1: cianchosaint (sole)

**Files to commit** (under `openspec/changes/cianchosaint-narrative-deep-dive-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-narrative-deep-dive/spec.md` (the canonical spec)

**New files**:
- `agents/cianchosaint/narrative/__init__.py` (~20 LOC)
- `agents/cianchosaint/narrative/context.py` (~120 LOC)
- `agents/cianchosaint/narrative/season.py` (~150 LOC)
- `agents/cianchosaint/narrative/dossier.py` (~120 LOC)
- `baml_src/cianchosaint/politics/bipp_v2_narrative.baml` (~80 LOC)
- `tests/agents/cianchosaint/test_narrative_deep_dive.py` (~120 LOC)

## Repo 2: cianfhoghlaim (unchanged)

The upstream `docs/google_examples/adk-examples/agent-valley-archive` remains unchanged. We wholesale-adapt the pattern in this change.

## Repo 3: leabharlann (unchanged)

The 87 politics PDFs in `leabharlann/gemini_deep_research/politics/` are read-only context for the politician pipeline (which T4.1 doesn't touch). No changes.
