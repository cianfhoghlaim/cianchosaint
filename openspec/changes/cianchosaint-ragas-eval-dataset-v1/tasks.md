# Tasks: cianchosaint-ragas-eval-dataset-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.11+ installed
- [x] Verify `ragas` package available in cianchosaint (per `cianchosaint-ragas-eval-pipeline-v1`)

## 1. Author the canonical politician world

- [x] Write `tests/evals/politician/__init__.py` (~20 LOC) — the evals package marker
- [x] Write `tests/evals/politician/world.py` (~300 LOC) with:
  - 7 politicians (Farage, Polanski, O'Dowd, Lyons, Givan, Robinson, Bird)
  - 5 fact categories (canonical_name, party_id, jurisdiction, social_handles[], public_metrics[])
  - `every_politician_account_collected` honest judge (deterministic)
  - `star_rating` gameable judge (returns random rating, never reads context)

## 2. Author the canonical MetricEvaluatorRegistry helpers

- [x] Write `tests/evals/politician/metrics.py` (~150 LOC) with:
  - `politician_score(actual, expected)` — the canonical score function
  - `is_deterministic(fn)` — checks if a function is deterministic
  - `politician_metrics` — the canonical `MetricEvaluatorRegistry` registration helper

## 3. Author the eval + optimizer configs

- [x] Write `tests/evals/politician/eval_config.json` — mirrors cianfhoghlaim's `loop-lab-table/03_optimize/eval_config.json`
- [x] Write `tests/evals/politician/optimizer_config.json` — mirrors the GEPA optimizer config

## 4. Author the gold-standard Q/A pairs

- [x] Write `tests/evals/politician/train.evalset.json` (~150 LOC) — the training split with gold-standard Q/A pairs for the 7 politicians
- [x] Write `tests/evals/politician/val.evalset.json` — the validation split

## 5. Author the canonical walk.py

- [x] Write `tests/evals/politician/walk.py` (~120 LOC) — runs every assertion as a sentence against the real agent

## 6. Author the spec + the test

- [x] Write `openspec/changes/cianchosaint-ragas-eval-dataset-v1/specs/cianchosaint-ragas-eval-dataset/spec.md` — the canonical spec (Requirement: adversarial judges contract + gold-standard Q/A contract + RAGAS conformance; Scenario: every politician's account is collected correctly + the gameable judge doesn't correlate with correctness)
- [x] Write `openspec/changes/cianchosaint-ragas-eval-dataset-v1/cross-repo-sync.md` — sole repo cianchosaint
- [x] Run `PYTHONPATH=. python3 tests/evals/politician/walk.py`

## 7. CI gate

- [x] Run `openspec validate cianchosaint-ragas-eval-dataset-v1 --strict`
- [x] Run `PYTHONPATH=. python3 tests/evals/politician/walk.py`
- [x] Run regression tests for T1.1 + T1.2 + T1.3 + T2.1 + T2.2 + T2.3
- [x] Run `mise run lint:license`

## 8. Commit + archive

- [x] `git add openspec/changes/cianchosaint-ragas-eval-dataset-v1/ tests/evals/politician/`
- [x] `git commit -m "feat(cianchosaint): add RAGAS eval dataset + adversarial judges (every_politician_account_collected + star_rating)"`
- [x] `openspec archive cianchosaint-ragas-eval-dataset-v1 --yes`

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-ragas-eval-dataset-v1 --strict

# 2. run the eval walk
PYTHONPATH=. python3 tests/evals/politician/walk.py

# 3. regression: existing tests still pass
PYTHONPATH=. python3 tests/agents/cianchosaint/test_agent_factory.py
PYTHONPATH=. python3 tests/agents/integrations/test_agent_registry_runtime.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_long_running_tools.py
PYTHONPATH=. python3 tests/cocoindex_flows/test_shared_lifespan.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_workflow_graphs.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_memory_bank.py

# 4. lint_license
mise run lint:license
```
