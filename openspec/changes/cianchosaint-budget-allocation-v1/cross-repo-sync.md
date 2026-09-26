# Cross-Repo Sync: cianchosaint-budget-allocation-v1

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `docs/google_examples/adk-examples/monstertix/agent/concert/budget.py` remains the upstream reference. No changes to the cianfhoghlaim or leabharlann repos are needed.

## Order of Operations

```
[1] cianchosaint → openspec/changes/cianchosaint-budget-allocation-v1/
                   (proposal + tasks + cross-repo-sync + spec)
                   Adds: agents/cianchosaint/budget/{__init__,scope,budget,handlers}.py
                   Adds: tests/agents/cianchosaint/test_budget_allocation.py
                   Pushed to main.
                       ↓
[2] operator    → cd cianchosaint && openspec validate cianchosaint-budget-allocation-v1 --strict
                  → openspec validate --all --strict
                  → All validations pass
                       ↓
[3] operator    → openspec archive cianchosaint-budget-allocation-v1 --yes
```

## Repo 1: cianchosaint (sole)

**Files to commit** (under `openspec/changes/cianchosaint-budget-allocation-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-budget-allocation/spec.md` (the canonical spec)

**New files**:
- `agents/cianchosaint/budget/__init__.py` (~20 LOC)
- `agents/cianchosaint/budget/scope.py` (~120 LOC)
- `agents/cianchosaint/budget/budget.py` (~200 LOC)
- `agents/cianchosaint/budget/handlers.py` (~100 LOC)
- `tests/agents/cianchosaint/test_budget_allocation.py` (~120 LOC)

## Repo 2: cianfhoghlaim (unchanged)

The upstream `monstertix/agent/concert/budget.py` remains unchanged. We wholesale-adapt the pattern in this change.

## Repo 3: leabharlann (unchanged)

The 87 politics PDFs in `leabharlann/gemini_deep_research/politics/` are read-only context for the politician pipeline (which T4.2 doesn't touch). No changes.
