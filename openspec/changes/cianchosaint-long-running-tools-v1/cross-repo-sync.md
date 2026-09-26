# Cross-Repo Sync: cianchosaint-long-running-tools-v1

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `docs/google_examples/adk-examples/monstertix` remains the upstream reference (the `fence.py` + `memory.py` + `concert/budget.py` patterns). No changes to the cianfhoghlaim or leabharlann repos are needed.

## Order of Operations

```
[1] cianchosaint → openspec/changes/cianchosaint-long-running-tools-v1/
                   (proposal + tasks + cross-repo-sync + spec)
                   Adds: agents/cianchosaint/tools/long_running.py
                   Modifies: agents/cianchosaint/tools/{garda,met,psni}_form_fill.py + __init__.py
                   Adds: tests/agents/cianchosaint/test_long_running_tools.py
                   Pushed to main.
                       ↓
[2] operator    → cd cianchosaint && openspec validate cianchosaint-long-running-tools-v1 --strict
                  → openspec validate --all --strict
                  → All validations pass
                       ↓
[3] operator    → openspec archive cianchosaint-long-running-tools-v1 --yes
```

## Repo 1: cianchosaint (sole)

**Files to commit** (under `openspec/changes/cianchosaint-long-running-tools-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-long-running-tools/spec.md` (the canonical spec)

**New files**:
- `agents/cianchosaint/tools/long_running.py` (~150 LOC) — the `LongRunningFunctionTool` wrapper + staleness guard
- `tests/agents/cianchosaint/test_long_running_tools.py` (~100 LOC) — the smoke test

**Modified files**:
- `agents/cianchosaint/tools/garda_form_fill.py` — wrap with `LongRunningFunctionTool`
- `agents/cianchosaint/tools/met_form_fill.py` — same refactor
- `agents/cianchosaint/tools/psni_form_fill.py` — same refactor
- `agents/cianchosaint/tools/__init__.py` — export the new module + the staleness guard

## Repo 2: cianfhoghlaim (unchanged)

The upstream `docs/google_examples/adk-examples/monstertix/agent/concert/{fence,memory,budget}.py` remains unchanged. We wholesale-adapt the pattern in this change.

## Repo 3: leabharlann (unchanged)

The 87 politics PDFs in `leabharlann/gemini_deep_research/politics/` are read-only context for the politician pipeline (which T1.3 doesn't touch). No changes.
