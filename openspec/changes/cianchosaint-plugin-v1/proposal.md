# Change: cianchosaint-plugin-v1

## Why

Cianfhoghlaim's `monstertix/agent/concert/panel.py` shows the canonical BasePlugin pattern with control-panel narration:

- A `BasePlugin` subclass with `before_tool_callback` + `after_tool_callback`
- A control panel that shows what the agent is doing (per cianfhoghlaim's monstertix `venue/control_panel.html`)
- `mark_attended(True)` is called on every wake so the panel knows someone is there
- "A blank projector loses the room" — the panel narrates tool calls

Per cianfhoghlaim's `monstertix/agent/concert/panel.py`:

> "What you said, lifting off the desk at closing time. Before the write policy exists it fades halfway; after it, it lands on floor three. One animation, two meanings — which is the whole of chapter 3."

> "The PanelPlugin narrates tool calls to the venue control panel. A blank projector loses the room."

Cianchosaint has no BasePlugin integration. The agents don't narrate their work to a control panel. There's no observability into what an agent is currently doing beyond the terminal output.

This change lands the canonical BasePlugin + control-panel narration for cianchosaint.

## What changes

- **NEW file** `agents/cianchosaint/plugins/__init__.py` (~20 LOC) — package marker
- **NEW file** `agents/cianchosaint/plugins/base_plugin.py` (~150 LOC) — the canonical `BasePlugin` subclass with `before_tool_callback` + `after_tool_callback`
- **NEW file** `agents/cianchosaint/plugins/panel_plugin.py` (~200 LOC) — the canonical `PanelPlugin` (mirrors `monstertix/agent/concert/panel.py`)
- **NEW file** `agents/cianchosaint/plugins/control_panel.html` (~80 lines) — the canonical control-panel HTML (mirrors `monstertix/venue/control_panel.html`)
- **NEW test** `tests/agents/cianchosaint/test_plugin.py` (~100 LOC) — the smoke test
- **NEW spec delta** `openspec/changes/cianchosaint-plugin-v1/specs/cianchosaint-plugin/spec.md`

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-plugin`)
- Affected code/config: 5 NEW files
- Estimated LOC: ~550 LOC added

## Out of scope (follow-up changes)

- The Prometheus metrics integration — separate change
- The OpenTelemetry tracing — separate change

## Dependencies

`Blocked by: cianchosaint-long-running-tools-v1` (the BasePlugin hooks before/after tool callbacks)
`Affected repos: cianchosaint only.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `monstertix/agent/concert/panel.py` remains the upstream reference.

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
