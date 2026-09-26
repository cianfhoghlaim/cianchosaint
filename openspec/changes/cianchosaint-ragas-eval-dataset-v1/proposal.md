# Change: cianchosaint-ragas-eval-dataset-v1

## Why

The cianfhoghlaim `loop-lab-table/03_optimize` shows the canonical RAGAS pattern with adversarial judges:

- A **deterministic judge** (`everyone_ate`) — Python only, no LLM, walks the table seat-by-seat against hard constraints (allergies, budget, walk time, last orders)
- A **gameable judge** (`rating_score`) — just returns star rating, never reads the party
- An eval config that registers BOTH metrics into ADK's `MetricEvaluatorRegistry`
- A reward-hacking study — 4 measured runs showing the same coach pointed at different judges produces different scores

Cianchosaint has the spec for a RAGAS pipeline (per `openspec/changes/cianchosaint-ragas-eval-pipeline-v1/`) but no gold-standard Q/A pairs + no canonical judge functions. The politician BAML extraction has no measured quality.

This change lands the canonical cianchosaint RAGAS dataset:
- Gold-standard Q/A pairs for the 7 case-study politicians (Nigel Farage, Zack Polanski, John O'Dowd, Gordon Lyons, Paul Givan, Gavin Robinson, Lara Bird)
- Two adversarial judges: `every_politician_account_collected` (honest) + `star_rating` (gameable)
- The `world.py` analogue that provides the deterministic evaluation logic

## What changes

- **NEW file** `tests/evals/politician/__init__.py` (~20 LOC) — the evals package marker
- **NEW file** `tests/evals/politician/world.py` (~300 LOC) — the deterministic world (7 politicians + 5 fact categories + the `every_politician_account_collected` judge + the `star_rating` gameable judge)
- **NEW file** `tests/evals/politician/metrics.py` (~150 LOC) — the `politician_score` + `is_deterministic` + `politician_metrics` MetricEvaluatorRegistry helpers
- **NEW file** `tests/evals/politician/eval_config.json` — the canonical RAGAS eval config (mirrors cianfhoghlaim's `loop-lab-table/03_optimize/eval_config.json`)
- **NEW file** `tests/evals/politician/optimizer_config.json` — the canonical GEPA optimizer config
- **NEW file** `tests/evals/politician/train.evalset.json` (~150 LOC) — the gold-standard Q/A pairs for the 7 politicians
- **NEW file** `tests/evals/politician/val.evalset.json` — the validation split
- **NEW file** `tests/evals/politician/walk.py` (~120 LOC) — runs every assertion as a sentence against the real agent
- **NEW spec delta** `openspec/changes/cianchosaint-ragas-eval-dataset-v1/specs/cianchosaint-ragas-eval-dataset/spec.md`

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-ragas-eval-dataset`)
- Affected code/config: 8 NEW files
- **0 NEW DLT sources, 0 NEW BAML files** — pure eval surface
- Estimated LOC: ~900 LOC added
- **0 new dependencies** — uses the existing `ragas` (per `cianchosaint-ragas-eval-pipeline-v1`)

## Out of scope (follow-up changes)

- The GEPA prompt-optimizer integration (T3.1) — uses this dataset but is a separate change
- The reward-hacking measurement study — also a separate change

## Dependencies

`Blocked by: cianchosaint-agent-factory-v1` (the agents under test are factory-built)
`Blocked by: cianchosaint-workflow-graph-v1` (the politician_resolver_graph is one of the under-test agents)
`Affected repos: cianchosaint only.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `loop-lab-table/03_optimize` remains the upstream reference.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-ragas-eval-dataset-v1 --strict
# Expected: Validation passes

# 2. run the eval walk
PYTHONPATH=. python3 tests/evals/politician/walk.py
# Expected: All 7 politicians are checked; every assertion passes

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
