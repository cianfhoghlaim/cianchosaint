# Tasks: cianchosaint-plugin-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.11+ installed

## 1. Author the canonical plugin package

- [x] Write `agents/cianchosaint/plugins/__init__.py` (~20 LOC) — package marker + re-exports
- [x] Write `agents/cianchosaint/plugins/base_plugin.py` (~150 LOC) — the canonical `BasePlugin` subclass with `before_tool_callback` + `after_tool_callback`
- [x] Write `agents/cianchosaint/plugins/panel_plugin.py` (~200 LOC) — the canonical `PanelPlugin` (mirrors `monstertix/agent/concert/panel.py`)
- [x] Write `agents/cianchosaint/plugins/control_panel.html` (~80 lines) — the canonical control-panel HTML (mirrors `monstertix/venue/control_panel.html`)

## 2. Author the spec + the test

- [x] Write `openspec/changes/cianchosaint-plugin-v1/specs/cianchosaint-plugin/spec.md` — the canonical spec (Requirement: BasePlugin contract + PanelPlugin contract + control-panel contract; Scenario: every tool call narrates to the panel + no observer is needed for the plugin to work)
- [x] Write `openspec/changes/cianchosaint-plugin-v1/cross-repo-sync.md` — sole repo cianchosaint
- [x] Write `openspec/changes/cianchosaint-plugin-v1/tasks.md` — the task breakdown
- [x] Write `tests/agents/cianchosaint/test_plugin.py` — the smoke test

## 3. CI gate

- [x] Run `openspec validate cianchosaint-plugin-v1 --strict`
- [x] Run `PYTHONPATH=. python3 tests/agents/cianchosaint/test_plugin.py`
- [x] Run regression tests for T1.1 + T1.2 + T1.3 + T2.1 + T2.2 + T2.3 + T2.4 + T3.1 + T3.2 + T3.3 + T3.4 + T4.1 + T4.2 + T4.3
- [x] Run `mise run lint:license`

## 4. Commit + archive

- [x] `git add openspec/changes/cianchosaint-plugin-v1/ agents/cianchosaint/plugins/ tests/agents/cianchosaint/test_plugin.py`
- [x] `git commit -m "feat(cianchosaint): add PanelPlugin + canonical BasePlugin + control panel"`
- [x] `openspec archive cianchosaint-plugin-v1 --yes`

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-plugin-v1 --strict

# 2. run the smoke test
PYTHONPATH=. python3 tests/agents/cianchosaint/test_plugin.py

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
PYTHONPATH=. python3 tests/agents/cianchosaint/test_budget_allocation.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_3am_workflow.py

# 4. lint_license
mise run lint:license
```
