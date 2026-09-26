# Tasks: cianchosaint-codelab-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.11+ installed
- [x] Verify `codelab/` + `notebooks/` + `scripts/` directories are new

## 1. Author the canonical codelab markdown

- [x] Write `openspec/changes/cianchosaint-codelab-v1/codelab/politician-pipeline.md` (~400 lines) with:
  - Overview of the cianchosaint politician pipeline
  - Setup instructions
  - 5 runnable levels (mirrors `loop-lab-table/codelab/loop-lab-table.md`)
  - Sentence-form assertions (per cianfhoghlaim's codelab convention)
  - Exercises ("change the instruction and re-run")

## 2. Author the canonical notebook builder

- [x] Write `openspec/changes/cianchosaint-codelab-v1/notebooks/build.py` (~150 lines) with:
  - `build_politician_pipeline_notebook()` — generates the Colab-style notebook from the runnable modules
  - `main()` — writes `notebooks/politician_pipeline.ipynb`
  - Mirrors `loop-lab-table/notebooks/build.py`

## 3. Author the canonical walk.py

- [x] Write `openspec/changes/cianchosaint-codelab-v1/scripts/walk.py` (~120 lines) with:
  - `main()` — runs every assertion as a sentence against the real pipeline
  - Mirrors `loop-lab-table/scripts/walk.py`

## 4. Author the spec

- [x] Write `openspec/changes/cianchosaint-codelab-v1/specs/cianchosaint-codelab/spec.md` — the canonical spec (Requirement: codelab convention; Scenario: every assertion passes)
- [x] Write `openspec/changes/cianchosaint-codelab-v1/cross-repo-sync.md` — sole repo cianchosaint
- [x] Write `openspec/changes/cianchosaint-codelab-v1/tasks.md` — the task breakdown

## 5. CI gate

- [x] Run `openspec validate cianchosaint-codelab-v1 --strict`
- [x] Run `PYTHONPATH=. python3 openspec/changes/cianchosaint-codelab-v1/scripts/walk.py`
- [x] Run regression tests for T1.1 + T1.2 + T1.3 + T2.1 + T2.2 + T2.3 + T2.4 + T3.1
- [x] Run `mise run lint:license`

## 6. Commit + archive

- [x] `git add openspec/changes/cianchosaint-codelab-v1/`
- [x] `git commit -m "feat(cianchosaint): add codelab for the politician pipeline (markdown + notebook + walk.py)"`
- [x] `openspec archive cianchosaint-codelab-v1 --yes`

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-codelab-v1 --strict

# 2. run the codelab walk
PYTHONPATH=. python3 openspec/changes/cianchosaint-codelab-v1/scripts/walk.py

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
