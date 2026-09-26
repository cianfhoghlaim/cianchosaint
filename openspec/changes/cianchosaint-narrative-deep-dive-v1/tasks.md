# Tasks: cianchosaint-narrative-deep-dive-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.11+ installed

## 1. Author the narrative package

- [x] Write `agents/cianchosaint/narrative/__init__.py` (~20 LOC) — package marker + re-exports
- [x] Write `agents/cianchosaint/narrative/context.py` (~120 LOC) — the canonical `NarrativeContext` class
- [x] Write `agents/cianchosaint/narrative/season.py` (~150 LOC) — the canonical `season_search` function
- [x] Write `agents/cianchosaint/narrative/dossier.py` (~120 LOC) — the canonical `season_known_issue` function

## 2. Author the canonical BAML extraction function

- [x] Write `baml_src/cianchosaint/politics/bipp_v2_narrative.baml` (~80 LOC) — the `NarrativeContext` extraction

## 3. Author the spec

- [x] Write `openspec/changes/cianchosaint-narrative-deep-dive-v1/specs/cianchosaint-narrative-deep-dive/spec.md` — the canonical spec (Requirement: NarrativeContext + season_search + season_known_issue; Scenario: every dossier has a narrative arc + every search returns relevant docs + every graph walk finds known issues)
- [x] Write `openspec/changes/cianchosaint-narrative-deep-dive-v1/cross-repo-sync.md` — sole repo cianchosaint
- [x] Write `openspec/changes/cianchosaint-narrative-deep-dive-v1/tasks.md` — the task breakdown

## 4. CI gate

- [x] Run `openspec validate cianchosaint-narrative-deep-dive-v1 --strict`
- [x] Run `PYTHONPATH=. python3 tests/agents/cianchosaint/test_narrative_deep_dive.py`
- [x] Run regression tests for T1.1 + T1.2 + T1.3 + T2.1 + T2.2 + T2.3 + T2.4 + T3.1 + T3.2 + T3.3 + T3.4
- [x] Run `mise run lint:license`

## 5. Commit + archive

- [x] `git add openspec/changes/cianchosaint-narrative-deep-dive-v1/ agents/cianchosaint/narrative/ baml_src/cianchosaint/politics/bipp_v2_narrative.baml tests/agents/cianchosaint/test_narrative_deep_dive.py`
- [x] `git commit -m "feat(cianchosaint): add NarrativeContext + season_search + season_known_ive for BIOD v1 dossiers"`
- [x] `openspec archive cianchosaint-narrative-deep-dive-v1 --yes`

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-narrative-deep-dive-v1 --strict

# 2. run the smoke test
PYTHONPATH=. python3 tests/agents/cianchosaint/test_narrative_deep_dive.py

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

# 4. lint_license
mise run lint:license
```
