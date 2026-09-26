# Tasks: cianchosaint-budget-allocation-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.11+ installed

## 1. Author the budget package

- [x] Write `agents/cianchosaint/budget/__init__.py` (~20 LOC) — package marker + re-exports
- [x] Write `agents/cianchosaint/budget/scope.py` (~120 LOC) — the canonical `BudgetScope` enum + 4 `ContextVar`s
- [x] Write `agents/cianchosaint/budget/budget.py` (~200 LOC) — the canonical `Budget` dataclass + `load(scope)` + `save(scope)` + `mark_attended(value)` + `someone_is_there()`
- [x] Write `agents/cianchosaint/budget/handlers.py` (~100 LOC) — the canonical `set_budget()` + `get_budget()` + `has_budget()` helpers

## 2. Author the spec

- [x] Write `openspec/changes/cianchosaint-budget-allocation-v1/specs/cianchosaint-budget-allocation/spec.md` — the canonical spec (Requirement: budget scope contract + ContextVar contract + someone_is_there contract; Scenario: per-call budget enforcement + per-analyst override + per-run override)
- [x] Write `openspec/changes/cianchosaint-budget-allocation-v1/cross-repo-sync.md` — sole repo cianchosaint
- [x] Write `openspec/changes/cianchosaint-budget-allocation-v1/tasks.md` — the task breakdown

## 3. CI gate

- [x] Run `openspec validate cianchosaint-budget-allocation-v1 --strict`
- [x] Run `PYTHONPATH=. python3 tests/agents/cianchosaint/test_budget_allocation.py`
- [x] Run regression tests for T1.1 + T1.2 + T1.3 + T2.1 + T2.2 + T2.3 + T2.4 + T3.1 + T3.2 + T3.3 + T3.4 + T4.1
- [x] Run `mise run lint:license`

## 4. Commit + archive

- [x] `git add openspec/changes/cianchosaint-budget-allocation-v1/ agents/cianchosaint/budget/ tests/agents/cianchosaint/test_budget_allocation.py`
- [x] `git commit -m "feat(cianchosaint): add BudgetScope + ContextVar-based per-call/per-analyst/per-run budget allocation"`
- [x] `openspec archive cianchosaint-budget-allocation-v1 --yes`

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-budget-allocation-v1 --strict

# 2. run the smoke test
PYTHONPATH=. python3 tests/agents/cianchosaint/test_budget_allocation.py

# 3. regression: existing tests still pass
PYTHONPATH=. python3 tests/agents/cianchosaint/test_agent_factory.py
PYTHONPATH=. python3 tests/agents/integrations/test_agent_registry_runtime.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_long_running_tools.py
PYTHONPATH=. python3 tests/cocoindex_flows/test_shared_lifespan.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_workflow_graphs.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_memory_bank.py
PYTHONPATH=. python3 tests/evals/politician/walk.py
PYTHONPATH=. python3 tests/orchestration/test_dagster_orchestration.py
PYTHONPATH=. python3 tests/openspec/test_sister_mirrors.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_narrative_deep_dive.py

# 4. lint_license
mise run lint:license
```
