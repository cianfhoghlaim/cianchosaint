# Change: cianchosaint-agent-registry-runtime-v1

## Why

Cianfhoghlaim's `agents/integrations/agent_registry_runtime.py` provides the canonical 3-helper surface for wiring any Google ADK agent to the CopilotKit runtime + the AG-UI protocol. The helpers are:

- `register_all_agents_with_copilotkit()` — calls `register_adk_agent(agent, name=name)` for every entry in `AGENT_REGISTRY`
- `collect_all_agui_events()` — collects the registration events emitted by `ag-ui-adk`
- `build_copilotkit_runtime_config()` — produces the canonical CopilotKit runtime configuration

Cianchosaint needs the same pattern. Currently:
- The `AGENT_FACTORY_REGISTRY` we just landed (T1.1) is the canonical dictionary — but it's just data, not wired to anything
- The 17 tools in `agents/cianchosaint/tools/__init__.py` are exported but never registered with the CopilotKit runtime
- The `agents/cianchosaint/tools/adjacent_context_resolver.py` depends on the google.adk.tools.AgentTool etc. that need the ag-ui-adk integration

This change lands the canonical runtime helpers + the ag-ui-adk integration so the BIOD v1 / BGARD v1 / BPSNI v1 specialists can be created by id from the workflow-graph orchestrator (T2.2) and registered with the CopilotKit runtime + AG-UI protocol.

## What changes

- **NEW file** `agents/integrations/__init__.py` (~30 LOC) — re-exports the cianfhoghlaim `agents/integrations` package (currently wholesale-copied to cianfhoghlaim, ready to be lifted to cianchosaint)
- **NEW file** `agents/integrations/agent_registry_runtime.py` (~200 LOC) — the canonical 3-helper surface
- **NEW file** `agents/integrations/agent_ui_bridge.py` (~180 LOC) — the canonical `register_adk_agent(agent, name=name)` helper that uses `ag-ui-adk.ADKAgent` + `CopilotKitRuntime`
- **NEW file** `agents/integrations/baml_function_tool.py` (~150 LOC) — wraps any `async def` BAML function as a Google ADK `FunctionTool` (mirror cianfhoghlaim's)
- **MODIFIED** `agents/cianchosaint/tools/__init__.py` — export the `ag_ui_registration_event` helper alongside the existing 17 tools
- **NEW test** `tests/agents/integrations/test_agent_registry_runtime.py` — verifies the 3 helpers work and that every registry entry round-trips through CopilotKit
- **NEW spec delta** `openspec/changes/cianchosaint-agent-registry-runtime-v1/specs/cianchosaint-agent-registry-runtime/spec.md`

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-agent-registry-runtime`)
- Affected code/config: 4 NEW files + 1 MODIFIED file
- **0 NEW DLT sources, 0 NEW BAML files, 0 NEW FunctionTools** — pure integration surface; existing tools register automatically
- Estimated LOC: ~600 LOC added
- **1 new optional dependency**: `ag-ui-adk` (the canonical ADK ↔ CopilotKit bridge)

## Out of scope (follow-up changes)

- The Langfuse prompt resolver integration (per `cianchosaint-langfuse-prompt-management-v1`) — that's Change T1.2 in the 14-change plan
- The per-constituency web surface (`web/apps/ciafagent-{ga,met,psni}-*`) — that's T3.4
- The CopilotKit front-end `web/packages/ciafagent-ui-kit/` — that's T3.4

## Dependencies

`Blocked by: cianchosaint-agent-factory-v1` (must archive first; it just did)
`Affected repos: cianchosaint only.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `agents/integrations/agent_registry_runtime.py` remains the upstream reference; we wholesale-adapt the pattern in this change.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-agent-registry-runtime-v1 --strict
# Expected: Validation passes

# 2. test the runtime
PYTHONPATH=. python3 tests/agents/integrations/test_agent_registry_runtime.py
# Expected: 3 helpers work; every AGENT_FACTORY_REGISTRY entry round-trips

# 3. lint_license
mise run lint:license
# Expected: 0 violations
```
