# Change: cianchosaint-budget-allocation-v1

## Why

Cianfhoghlaim's `docs/google_examples/adk-examples/monstertix/agent/concert/budget.py` shows the canonical budget-allocation pattern:

> "SESSION STATE, NOT `user:`. This is a decision worth making on purpose. A budget is agreed for one booking, not forever — 'two-fifty if they're the good ones' was about that band, that night. Put it under `user:` and it silently governs every run this person ever makes, including ones where they would have said something different, and they will never be asked again. So every new session starts with no budget and has to agree one."

> "The cost of that choice is real: an unattended run gets a fresh session, so it has nothing agreed and falls back to a default. That is the honest trade — a limit that has to be re-agreed, against a limit that quietly outlives the conversation it came from."

Plus the `ContextVar`-based `_ATTENDED` pattern (per `monstertix/agent/concert/budget.py::_UNATTENDED_BY_DEFAULT` + `_attended` + `someone_is_there()`):

> "is anybody there? `_UNATTENDED_BY_DEFAULT` env var + `_attended` ContextVar + `someone_is_there()`"

Cianchosaint has no budget-allocation layer — every per-person agent invocation is unbounded. An unattended 3am Pub/Sub wake (per T4.3) could spin up a chain of LLM calls that costs real money.

This change lands the canonical `temp:` / `user:` / `app:` scoping (per `cianchosaint-memory-bank-v1`'s `state.py`) PLUS the `_ATTENDED_BY_DEFAULT` `ContextVar` + `someone_is_there()` + the canonical budget-allocation API.

## What changes

- **NEW file** `agents/cianchosaint/budget/__init__.py` (~20 LOC) — package marker + re-exports
- **NEW file** `agents/cianchosaint/budget/scope.py` (~120 LOC) — the canonical `BudgetScope` enum + 4 `ContextVar`s (`_attended`, `_agreed_budget`, `_agreed_party_size`, `_agreed_city`)
- **NEW file** `agents/cianchosaint/budget/budget.py` (~200 LOC) — the canonical `Budget` dataclass + `load(scope)` + `save(scope)` + `mark_attended(value)` + `someone_is_there()` + `_ATTENDED_BY_DEFAULT` env var
- **NEW file** `agents/cianchosaint/budget/handlers.py` (~100 LOC) — the canonical `set_budget()` + `get_budget()` + `has_budget()` helpers (mirrors `concert/budget.py::set_budget` + `load`)
- **NEW test** `tests/agents/cianchosaint/test_budget_allocation.py` (~120 LOC) — the smoke test
- **NEW spec delta** `openspec/changes/cianchosaint-budget-allocation-v1/specs/cianchosaint-budget-allocation/spec.md`

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-budget-allocation`)
- Affected code/config: 5 NEW files
- Estimated LOC: ~600 LOC added
- **0 new dependencies**

## Out of scope (follow-up changes)

- The 3am Pub/Sub trigger integration (per T4.3) — uses `someone_is_there()` but is a separate change

## Dependencies

`Blocked by: cianchosaint-memory-bank-v1` (the budget scope uses the same `state.py` key prefixes)
`Affected repos: cianchosaint only.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `docs/google_examples/adk-examples/monstertix/agent/concert/budget.py` remains the upstream reference.

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
