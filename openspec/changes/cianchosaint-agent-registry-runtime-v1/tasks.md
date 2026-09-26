# Tasks: cianchosaint-agent-registry-runtime-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.11+ installed
- [x] Verify `ag-ui-adk` is the canonical ADK ↔ CopilotKit bridge (per cianfhoghlaim's `agents/integrations/agent_ui_bridge.py`)
- [x] Verify `copilotkit.runtime.CopilotKitRuntime` is the canonical runtime (per cianfhoghlaim's `agents/integrations/agent_registry_runtime.py`)

## 1. Author the canonical 3-helper surface

- [x] Write `agents/integrations/__init__.py` (~30 LOC) — re-exports the cianfhoghlaim `agents/integrations` package
- [x] Write `agents/integrations/agent_registry_runtime.py` (~200 LOC) with:
  - `register_all_agents_with_copilotkit()` — calls `register_adk_agent(agent, name=name)` for every entry in `AGENT_FACTORY_REGISTRY`
  - `collect_all_agui_events()` — collects the registration events emitted by `ag-ui-adk`
  - `build_copilotkit_runtime_config()` — produces the canonical CopilotKit runtime configuration

## 2. Author the canonical ADK ↔ CopilotKit bridge

- [x] Write `agents/integrations/agent_ui_bridge.py` (~180 LOC) with:
  - `register_adk_agent(agent, name=name)` — wraps an `LlmAgent` as an `ag-ui-adk.ADKAgent` and registers it with the CopilotKit runtime
  - `make_planner_agent(name, description, *, model_alias="minimax", temperature=0.3, max_output_tokens=8192, instruction="", tools=None)` — the canonical planner-enabled agent helper

## 3. Author the BAMLFunctionTool wrapper

- [x] Write `agents/integrations/baml_function_tool.py` (~150 LOC) — wraps any `async def` BAML function as a Google ADK `FunctionTool` (mirror cianfhoghlaim's `agents/integrations/baml_function_tool.py`)
- [x] The helper auto-detects the BAML function from `baml_client.async_client.b` and exposes it as a tool with the right schema (parameter names, types, descriptions)

## 4. Wire the tools `__init__.py`

- [x] Modify `agents/cianchosaint/tools/__init__.py` — export the `ag_ui_registration_event` helper alongside the existing 17 tools

## 5. Author the spec + the test

- [x] Write `openspec/changes/cianchosaint-agent-registry-runtime-v1/specs/cianchosaint-agent-registry-runtime/spec.md` — the canonical spec (Requirement: runtime surface + BAMLFunctionTool contract + conservative-posture guard; Scenario: every registry entry round-trips + every BAML function is wrapped + Langfuse resolver hook is preserved)
- [x] Write `openspec/changes/cianchosaint-agent-registry-runtime-v1/cross-repo-sync.md` — sole repo cianchosaint
- [x] Write `tests/agents/integrations/test_agent_registry_runtime.py` — verifies the 3 helpers work and that every registry entry round-trips through CopilotKit

## 6. CI gate

- [x] Run `openspec validate cianchosaint-agent-registry-runtime-v1 --strict`
- [x] Run `PYTHONPATH=. python3 tests/agents/integrations/test_agent_registry_runtime.py`
- [x] Run `mise run lint:license`

## 7. Commit + archive

- [x] `git add openspec/changes/cianchosaint-agent-registry-runtime-v1/ agents/integrations/`
- [x] `git commit -m "feat(cianchosaint): add AGENT_REGISTRY runtime + BAMLFunctionTool + ag-ui-adk bridge"`
- [x] `openspec archive cianchosaint-agent-registry-runtime-v1 --yes`

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-agent-registry-runtime-v1 --strict

# 2. test the runtime
PYTHONPATH=. python3 tests/agents/integrations/test_agent_registry_runtime.py

# 3. lint_license
mise run lint:license
```
