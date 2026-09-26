# Change: cianchosaint-ragas-prompt-optimizer-v1

## Why

Cianfhoghlaim's `loop-lab-table/03_optimize` shows the canonical RAGAS-driven prompt optimization pattern:

- The `adk optimize` (GEPA — Genetic-Pareto prompt Optimizer) rewrites the agent's instruction from its own scored failures
- A `reflection_minibatch_size=3` (default) drives the reflection loop
- A `max_metric_calls=150` budget caps the total cost
- A `run_dir="./gepa_run"` persists the run
- Pre-baked candidates (`prebaked/`) ship the day-one draft + the GEPA winner + the ratings-hack version

The `loop-lab-table/04_reward_hacking` shows the canonical reward-hacking study:
- 4 measured runs of the same coach pointed at the honest vs gameable judge
- The coach's output is the same string in both cases — but the score differs by an order of magnitude

The `loop-lab-table/06_refuel` shows the production-deployment pattern:
- Real traffic (`send_traffic.py`) → real dinners (`harvest.py` mints failures) → next round's exam

Cianchosaint has the RAGAS dataset (T2.4) but no GEPA integration + no reward-hacking study + no production-deployment loop. The politician BAML extraction has no measured quality improvement.

This change lands the canonical `adk optimize` (GEPA) integration + the reward-hacking study + the production-deployment loop, all modelled on `loop-lab-table/{03_optimize, 04_reward_hacking, 06_refuel}`.

## What changes

- **NEW file** `scripts/politician_optimize.py` (~200 LOC) — the canonical GEPA optimization runner
- **NEW file** `scripts/politician_reward_hacking_study.py` (~150 LOC) — the canonical reward-hacking study runner
- **NEW file** `scripts/politician_send_traffic.py` (~120 LOC) — the canonical production-traffic runner
- **NEW file** `scripts/politician_harvest.py` (~120 LOC) — the canonical harvest runner
- **NEW file** `scripts/politician_gepa_run_draft.txt` — the pre-baked day-one draft
- **NEW file** `scripts/politician_gepa_run_winner.txt` — the pre-baked GEPA winner
- **NEW file** `scripts/politician_gepa_run_hacked.txt` — the pre-baked ratings-hack version
- **NEW spec delta** `openspec/changes/cianchosaint-ragas-prompt-optimizer-v1/specs/cianchosaint-ragas-prompt-optimizer/spec.md`

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-ragas-prompt-optimizer`)
- Affected code/config: 7 NEW files
- **0 NEW DLT sources, 0 NEW BAML files** — pure eval/optimization surface
- Estimated LOC: ~700 LOC added
- **0 new dependencies** — uses the existing `adk` + `ragas`

## Out of scope (follow-up changes)

- The codelab (T3.2) — uses the optimizer as a reference but is a separate change
- The Dagster integration (T3.3) — uses the optimizer output but is a separate change

## Dependencies

`Blocked by: cianchosaint-ragas-eval-dataset-v1` (the dataset is required for the GEPA optimizer)
`Blocked by: cianchosaint-agent-factory-v1` (the agent under optimization is factory-built)
`Affected repos: cianchosaint only.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `loop-lab-table/{03_optimize, 04_reward_hacking, 06_refuel}` remain the upstream reference.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-ragas-prompt-optimizer-v1 --strict
# Expected: Validation passes

# 2. smoke-test the optimizer + study runners
PYTHONPATH=. python3 -c "from scripts.politician_optimize import run_optimization; print('optimizer ok')"
PYTHONPATH=. python3 -c "from scripts.politician_reward_hacking_study import run_study; print('study ok')"

# 3. regression: existing tests still pass
PYTHONPATH=. python3 tests/agents/cianchosaint/test_agent_factory.py
PYTHONPATH=. python3 tests/agents/integrations/test_agent_registry_runtime.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_long_running_tools.py
PYTHONPATH=. python3 tests/cocoindex_flows/test_shared_lifespan.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_workflow_graphs.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_memory_bank.py
PYTHONPATH=. python3 tests/evals/politician/walk.py

# 4. lint_license
mise run lint:license
```
