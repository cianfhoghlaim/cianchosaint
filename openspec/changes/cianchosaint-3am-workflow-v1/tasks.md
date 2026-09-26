# Tasks: cianchosaint-3am-workflow-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.11+ installed

## 1. Author the canonical Workflow graph

- [x] Write `agents/cianchosaint/workflows/nightly.py` (~250 LOC) with:
  - `politician_resolver_workflow()` — the canonical Workflow with LongRunningFunctionTool nodes
  - `request_input_handler()` — pause for human budget approval (per cianfhoghlaim's monstertix)
  - `rerun_on_resume=True` for the dispatcher nodes
- [x] Import + wire the existing 3 workflow graphs (politician_resolver_graph, funder_network_graph, wikipedia_bridge_graph) per T2.2
- [x] Add Idempotency-Key headers on every LongRunningFunctionTool invocation

## 2. Author the canonical trigger server

- [x] Write `agents/cianchosaint/workflows/trigger_server.py` (~200 LOC) with:
  - `fastapi_app` — the canonical FastAPI trigger (per monstertix/server.py)
  - `POST /wake` — triggers the canonical Workflow graph
  - `POST /wake/{workflow_id}` — triggers a specific workflow
  - `GET /wake/status` — returns the canonical status

## 3. Author the canonical Cloud Run deployment script

- [x] Write `agents/cianchosaint/workflows/deploy.sh` (~80 LOC) — the canonical Cloud Run deployment script (per monstertix/deploy-agent.sh)

## 4. Author the spec + the test

- [x] Write `openspec/changes/cianchosaint-3am-workflow-v1/specs/cianchosaint-3am-workflow/spec.md` — the canonical spec
- [x] Write `openspec/changes/cianchosaint-3am-workflow-v1/cross-repo-sync.md` — sole repo cianchosaint
- [x] Write `openspec/changes/cianchosaint-3am-workflow-v1/tasks.md` — the task breakdown
- [x] Write `tests/agents/cianchosaint/test_3am_workflow.py` — the smoke test

## 5. CI gate

- [x] Run `openspec validate cianchosaint-3am-workflow-v1 --strict`
- [x] Run `PYTHONPATH=. python3 tests/agents/cianchosaint/test_3am_workflow.py`
- [x] Run regression tests for T1.1 + T1.2 + T1.3 + T2.1 + T2.2 + T2.3 + T2.4 + T3.1 + T3.2 + T3.3 + T3.4 + T4.1 + T4.2
- [x] Run `mise run lint:license`

## 6. Commit + archive

- [x] `git add openspec/changes/cianchosaint-3am-workflow-v1/ agents/cianchosaint/workflows/ tests/agents/cianchosaint/test_3am_workflow.py`
- [x] `git commit -m "feat(cianchosaint): add 3am-workflow with LongRunningFunctionTool + Pub/Sub trigger"`
- [x] `openspec archive cianchosaint-3am-workflow-v1 --yes`

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-3am-workflow-v1 --strict

# 2. run the smoke test
PYTHONPATH=. python3 tests/agents/cianchosaint/test_3am_workflow.py

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

# 4. lint_license
mise run lint:license
```
