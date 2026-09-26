# Cross-Repo Sync: cianchosaint-3am-workflow-v1

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `docs/google_examples/adk-examples/monstertix` remains the upstream reference. No changes to the cianfhoghlaim or leabharlann repos are needed.

## Order of Operations

```
[1] cianchosaint → openspec/changes/cianchosaint-3am-workflow-v1/
                   (proposal + tasks + cross-repo-sync + spec)
                   Adds: agents/cianchosaint/workflows/{nightly,trigger_server}.py + deploy.sh
                   Adds: tests/agents/cianchosaint/test_3am_workflow.py
                   Pushed to main.
                       ↓
[2] operator    → cd cianchosaint && openspec validate cianchosaint-3am-workflow-v1 --strict
                  → openspec validate --all --strict
                  → All validations pass
                       ↓
[3] operator    → openspec archive cianchosaint-3am-workflow-v1 --yes
```

## Repo 1: cianchosaint (sole)

**Files to commit** (under `openspec/changes/cianchosaint-3am-workflow-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-3am-workflow/spec.md` (the canonical spec)

**New files**:
- `agents/cianchosaint/workflows/nightly.py` (~250 LOC)
- `agents/cianchosaint/workflows/trigger_server.py` (~200 LOC)
- `agents/cianchosaint/workflows/deploy.sh` (~80 LOC)
- `tests/agents/cianchosaint/test_3am_workflow.py` (~100 LOC)

## Repo 2: cianfhoghlaim (unchanged)

The upstream `docs/google_examples/adk-examples/monstertix/` remains unchanged. We wholesale-adapt the pattern in this change.

## Repo 3: leabharlann (unchanged)

The 87 politics PDFs in `leabharlann/gemini_deep_research/politics/` are read-only context for the politician pipeline (which T4.3 doesn't touch). No changes.
