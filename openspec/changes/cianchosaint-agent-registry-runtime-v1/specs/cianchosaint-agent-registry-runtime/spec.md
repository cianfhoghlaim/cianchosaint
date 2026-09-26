# cianchosaint-agent-registry-runtime Capability

## Purpose

`cianchosaint-agent-registry-runtime` provides the canonical runtime surface for wiring every cianchosaint ADK agent to the CopilotKit runtime + the AG-UI 17-event protocol. It mirrors cianfhoghlaim's `agents/integrations/agent_registry_runtime.py` + `agents/integrations/agent_ui_bridge.py`:

- `register_all_agents_with_copilotkit()` — calls `register_adk_agent(agent, name=name)` for every entry in `AGENT_FACTORY_REGISTRY`
- `collect_all_agui_events()` — collects the registration events emitted by `ag-ui-adk`
- `build_copilotkit_runtime_config()` — produces the canonical CopilotKit runtime configuration
- `BAMLFunctionTool(func)` — wraps any `async def` BAML function as a Google ADK `FunctionTool`

## Background

Cianfhoghlaim's `agents/integrations/agent_registry_runtime.py` provides 3 helpers that wire any `LlmAgent` to the CopilotKit runtime + the AG-UI protocol. The wholesale-copy lives in cianfhoghlaim's `agents/integrations/` directory but has not yet been adapted for cianchosaint.

Cianchosaint's `AGENT_FACTORY_REGISTRY` (per the T1.1 change) is the canonical dictionary of every cianchosaint agent. Today the registry is just data — no agent is wired to CopilotKit, no event is collected for AG-UI, and no BAML function is exposed as a Google ADK tool.

This change lands the 3-helper runtime surface + the ag-ui-adk integration so the BIOD v1 / BGARD v1 / BPSNI v1 specialists can be created by id from the workflow-graph orchestrator (T2.2) and registered with the CopilotKit runtime + AG-UI protocol.

## ADDED Requirements

### Requirement: The 3-helper runtime surface

The system SHALL provide a module at `agents/integrations/agent_registry_runtime.py` with 3 helpers:

1. `register_all_agents_with_copilotkit()` — calls `register_adk_agent(agent, name=name)` for every entry in `AGENT_FACTORY_REGISTRY`
2. `collect_all_agui_events()` — collects the registration events emitted by `ag-ui-adk`
3. `build_copilotkit_runtime_config()` — produces the canonical CopilotKit runtime configuration

#### Scenario: Every AGENT_FACTORY_REGISTRY entry is registered

- **WHEN** the operator calls `register_all_agents_with_copilotkit()`
- **THEN** every entry in `AGENT_FACTORY_REGISTRY` SHALL be wrapped as an `ag-ui-adk.ADKAgent`
- **AND** the wrapper SHALL be registered with the CopilotKit runtime

#### Scenario: The runtime config is canonical

- **WHEN** the operator calls `build_copilotkit_runtime_config()`
- **THEN** the returned dict SHALL contain `agents` (every registered agent), `tools` (every FunctionTool wrapper), `metadata` (the runtime metadata)
- **AND** the structure SHALL be compatible with the cianfhoghlaim-style CopilotKit runtime

### Requirement: The BAMLFunctionTool wrapper

The system SHALL provide a `BAMLFunctionTool(func)` wrapper in `agents/integrations/baml_function_tool.py` that takes any `async def` BAML function and exposes it as a Google ADK `FunctionTool`.

#### Scenario: Every async BAML function is wrapped

- **WHEN** the operator calls `BAMLFunctionTool(some_async_function)`
- **THEN** the returned wrapper SHALL have `.name` (the function name), `.description` (the docstring), and `.parameters` (the type signature)
- **AND** calling `await wrapper.run_async(**kwargs)` SHALL execute the BAML function and return its result

#### Scenario: The LangfusePromptResolver hook is preserved

- **WHEN** the BAMLFunctionTool wrapper is created
- **THEN** the wrapper SHALL register with the LangfusePromptResolver (per `cianchosaint-langfuse-prompt-management-v1`) so the Langfuse prompt name is the canonical lookup key

### Requirement: Backward compatibility with CianchosaintAgentBase

The system SHALL preserve the existing `CianchosaintAgentBase.get_active_model()` API and the OSINT allowlist gate.

#### Scenario: get_active_model() still works

- **WHEN** the operator calls `ga_root_agent_instance.get_active_model()`
- **THEN** the method SHALL return the canonical model string (delegated to the factory's `model_for(model_alias)` helper)
- **AND** no behaviour change vs the previous implementation

#### Scenario: OSINT allowlist gate is preserved

- **WHEN** the operator calls any of the factory-built agents
- **THEN** the agent SHALL preserve the existing `CianchosaintAgentBase.check_osint_source()` gate (no behaviour change vs the previous manual instantiation)

### Requirement: The `ag_ui_registration_event` helper

The system SHALL provide an `ag_ui_registration_event(agent_name, metadata)` helper in `agents/cianchosaint/tools/__init__.py` that emits the canonical AG-UI registration event for an agent.

#### Scenario: The helper emits a valid event

- **WHEN** the operator calls `ag_ui_registration_event(agent_name="ga_root_agent", metadata={"jurisdiction": "Republic of Ireland"})`
- **THEN** the returned dict SHALL contain `agent_name`, `metadata`, `event_type="agent_registered"`, and `timestamp` (ISO 8601)
- **AND** the dict SHALL be serializable to JSON

## Cross-references

- [`../../agents/cianchosaint/_base.py`](../../agents/cianchosaint/_base.py) — the canonical base class
- [`../../agents/cianchosaint/_factory.py`](../../agents/cianchosaint/_factory.py) — the canonical factory
- [`../../tests/agents/integrations/test_agent_registry_runtime.py`](../../tests/agents/integrations/test_agent_registry_runtime.py) — the smoke test
- [`../../openspec/changes/cianchosaint-agent-factory/spec.md`](../../openspec/changes/cianchosaint-agent-factory/spec.md) — the umbrella spec
- [`../../openspec/changes/cianchosaint-langfuse-prompt-management/spec.md`](../../openspec/changes/cianchosaint-langfuse-prompt-management/spec.md) — the Langfuse prompt resolver integration
- cianfhoghlaim `agents/integrations/agent_registry_runtime.py` — upstream reference
- cianfhoghlaim `agents/integrations/agent_ui_bridge.py` — upstream reference
- cianfhoghlaim `agents/integrations/baml_function_tool.py` — upstream reference
