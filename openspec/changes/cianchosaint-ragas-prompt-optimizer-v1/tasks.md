# Tasks: cianchosaint-ragas-prompt-optimizer-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.11+ installed
- [x] Verify `adk optimize` available in cianchosaint (per the loop-lab-table/03_optimize pattern)

## 1. Author the canonical GEPA optimization runner

- [x] Write `scripts/politician_optimize.py` (~200 LOC) with:
  - `run_optimization(num_politicians=7, eval_split="train", max_metric_calls=100)` — the canonical GEPA runner
  - Mirrors `loop-lab-table/03_optimize/host/run_optimizer.py` (the day-one draft → measured scores → GEPA winner pipeline)

## 2. Author the reward-hacking study runner

- [x] Write `scripts/politician_reward_hacking_study.py` (~150 LOC) with:
  - `run_study(num_runs=4)` — runs the same coach pointed at honest vs gameable judges
  - Mirrors `loop-lab-table/04_reward_hacking/hack_2sec.py` (the reward-hacking measurement pattern)

## 3. Author the production-traffic runner

- [x] Write `scripts/politician_send_traffic.py` (~120 LOC) with:
  - `send_traffic(num_parties=8, num_seeds=5)` — sends the canonical 13 conversations (8 holdout + 5 seeds)
  - Mirrors `loop-lab-table/06_refuel/send_traffic.py`

## 4. Author the harvest runner

- [x] Write `scripts/politician_harvest.py` (~120 LOC) with:
  - `harvest_failures()` — grades real dinners offline, mints failures into the eval set
  - Mirrors `loop-lab-table/06_refuel/harvest.py`

## 5. Author the pre-baked candidates

- [x] Write `scripts/politician_gepa_run_draft.txt` — the day-one draft (mirrors `loop-lab-table/03_optimize/prebaked/instruction_before.txt`)
- [x] Write `scripts/politician_gepa_run_winner.txt` — the GEPA winner (mirrors `loop-lab-table/03_optimize/prebaked/instruction_after.txt`)
- [x] Write `scripts/politician_gepa_run_hacked.txt` — the ratings-hack version (mirrors `loop-lab-table/03_optimize/prebaked/instruction_after.txt`)

## 6. Author the spec + the test

- [x] Write `openspec/changes/cianchosaint-ragas-prompt-optimizer-v1/specs/cianchosaint-ragas-prompt-optimizer/spec.md` — the canonical spec (Requirement: GEPA integration + reward-hacking study + production-deployment loop; Scenario: every politician's profile accuracy improves + reward-hacking is measured + real traffic mints failures)
- [x] Write `openspec/changes/cianchosaint-ragas-prompt-optimizer-v1/cross-repo-sync.md` — sole repo cianchosaint
- [x] Run smoke test that the optimizer + study modules import cleanly

## 7. CI gate

- [x] Run `openspec validate cianchosaint-ragas-prompt-optimizer-v1 --strict`
- [x] Run smoke tests
- [x] Run regression tests for T1.1 + T1.2 + T1.3 + T2.1 + T2.2 + T2.3 + T2.4
- [x] Run `mise run lint:license`

## 8. Commit + archive

- [x] `git add openspec/changes/cianchosaint-ragas-prompt-optimizer-v1/ scripts/politician_*.py`
- [x] `git commit -m "feat(cianchosaint): add RAGAS-driven prompt optimizer + reward-hacking study + production traffic loop"`
- [x] `openspec archive cianchosaint-ragas-prompt-optimizer-v1 --yes`

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-ragas-prompt-optimizer-v1 --strict

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
