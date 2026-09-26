# Change: cianchosaint-3am-workflow-v1

## Why

Cianfhoghlaim's `docs/google_examples/adk-examples/monstertix` shows the canonical "long-running workflow + Pub/Sub trigger" pattern:

- A `Workflow` graph with `LongRunningFunctionTool` nodes that survive process death
- A Pub/Sub trigger endpoint that wakes the graph at 3am (per `monstertix/cloud-scheduler.yaml`)
- A `handlers.wake()` helper that detects the pending interrupt + answers it
- An `Idempotency-Key` header pattern that prevents double-purchase on retry

Per cianfhoghlaim's `monstertix/main.py`:

> "One container, two front doors."
> "One container, two front doors. ┌─ Cloud Run: concert-you ─────────────────┐ │  │ /                          MonsterTix, for a person │ /wake                      what that page posts to │ /apps/concert/trigger/     what Pub/Sub posts to │      pubsub                                                │  │            one Runner, one session store, one graph │ └──────────────────────────────────────────────────────┘"
> "`get_fast_api_app` does the heavy half: it discovers every agent package in AGENTS_DIR, builds the session and artifact services from the same two URIs you have been passing to `adk web` since Module 3, and mounts a Pub/Sub endpoint per app."

Cianchosaint has the workflow graphs (per T2.2) and the long-running tools (per T1.3), but no `3am-workflow` that ties them together + no Pub/Sub trigger endpoint.

This change lands the canonical 3am-workflow for cianchosaint.

## What changes

- **NEW file** `agents/cianchosaint/workflows/nightly.py` (~250 LOC) — the canonical Workflow graph with `LongRunningFunctionTool` nodes (mirrors `monstertix/agent/concert/nightly.py`)
- **NEW file** `agents/cianchosaint/workflows/trigger_server.py` (~200 LOC) — the canonical FastAPI trigger server (mirrors `monstertix/agent/concert/monstertix/server.py`)
- **NEW file** `agents/cianchosaint/workflows/deploy.sh` (~80 LOC) — the canonical Cloud Run deployment script (mirrors `monstertix/deploy-agent.sh`)
- **NEW file** `tests/agents/cianchosaint/test_3am_workflow.py` (~100 LOC) — the smoke test
- **NEW spec delta** `openspec/changes/cianchosaint-3am-workflow-v1/specs/cianchosaint-3am-workflow/spec.md`

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-3am-workflow`)
- Affected code/config: 4 NEW files
- Estimated LOC: ~630 LOC added

## Out of scope (follow-up changes)

- The Cloud Scheduler setup — separate change
- The actual Cloud Run deployment — separate change

## Dependencies

`Blocked by: cianchosaint-long-running-tools-v1` (the workflow uses LongRunningFunctionTool)
`Blocked by: cianchosaint-workflow-graph-v1` (the workflow builds on the existing politician resolver graph)
`Affected repos: cianchosaint only.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `docs/google_examples/adk-examples/monstertix` remains the upstream reference.

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
