# Change: cianchosaint-codelab-v1

## Why

Cianfhoghlaim follows the convention (per `docs/google_examples/adk2-tutorial/codelab/`):

> "Every codelab follows the same convention: `codelab/<name>.md` is the markdown walkthrough, `notebooks/<name>.ipynb` is the buildable notebook, `solutions/` has the finished code, `scripts/walk.py` runs every assertion as a sentence."

Cianfhoghlaim has multiple codelabs:
- `loop-lab-table/codelab/loop-lab-table.md` — the 6-rung marathon coach codelab
- `loop-lab-table/notebooks/build.py` — builds the Colab notebook from the runnable modules
- `support-memory-lab/codelab/` + `notebooks/` — the 5-rung memory codelab
- `monstertix/codelab/` — the long-running agent codelab

Cianchosaint has NO codelabs. The existing `openspec/changes/cianchosaint-politician-schema-v1/` change shipped the 7 case-study politicians + the BAML extraction + the 4 FunctionTools, but there's no narrative walkthrough that ties them together for a new analyst.

This change lands the canonical codelab for the cianchosaint politician pipeline:

1. A `codelab/politician-pipeline.md` markdown walkthrough (the prose)
2. A `notebooks/build.py` that builds a Colab-style notebook from the runnable modules (mirrors `loop-lab-table/notebooks/build.py`)
3. A `scripts/walk.py` that runs every assertion as a sentence against the real pipeline

## What changes

- **NEW file** `openspec/changes/cianchosaint-codelab-v1/codelab/politician-pipeline.md` (~400 lines) — the markdown walkthrough
- **NEW file** `openspec/changes/cianchosaint-codelab-v1/notebooks/build.py` (~150 lines) — the Colab-style notebook builder
- **NEW file** `openspec/changes/cianchosaint-codelab-v1/scripts/walk.py` (~120 lines) — the assertion-as-sentence runner
- **NEW file** `openspec/changes/cianchosaint-codelab-v1/specs/cianchosaint-codelab/spec.md`

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-codelab`)
- Affected code/config: 4 NEW files
- Estimated LOC: ~700 LOC added
- **0 new dependencies**

## Out of scope (follow-up changes)

- The web-app adapters (`webapps/politician-pipeline/`) — separate change (T3.4)
- The Dagster integration (T3.3) — uses the codelab but is a separate change

## Dependencies

`Blocked by: cianchosaint-agent-factory-v1` (the codelab uses the factory)
`Blocked by: cianchosaint-workflow-graph-v1` (the codelab uses the workflow graphs)
`Blocked by: cianchosaint-ragas-eval-dataset-v1` (the codelab uses the eval dataset)
`Affected repos: cianchosaint only.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `docs/google_examples/adk2-tutorial/codelab/` + `loop-lab-table/codelab/` remain the upstream reference.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-codelab-v1 --strict
# Expected: Validation passes

# 2. run the codelab walk
PYTHONPATH=. python3 openspec/changes/cianchosaint-codelab-v1/scripts/walk.py
# Expected: All 10 assertions pass

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
