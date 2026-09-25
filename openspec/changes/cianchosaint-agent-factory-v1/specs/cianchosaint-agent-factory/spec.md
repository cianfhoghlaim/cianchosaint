# cianchosaint-agent-factory Capability

## Purpose

`cianchosaint-agent-factory` is the capability that provides the canonical `make_cianchosaint_agent()` factory for the per-constituency agent fleet. It mirrors the cianfhoghlaim pattern (per `agents/adk/litellm_agent.py` + `agents/adk/agent_registry.py`):

- One factory call replaces the manual `LlmAgent(...)` boilerplate
- The factory wires the LiteLLM gateway + the BuiltInPlanner + the Langfuse prompt resolver hook
- All 18 cianchosaint agents (3 root + 15 specialist) go through the factory

The factory eliminates ~30 lines of `LlmAgent(...)` boilerplate per agent with a single factory call, and the registry makes every cianchosaint agent reachable by canonical id (so the BIOD v1 / BIPP v2 / BGARD v1 / BPSNI v1 specialists can be created by id from the workflow-graph orchestrator).

## Background

Cianfhoghlaim's `make_litellm_agent()` helper (per `agents/adk/litellm_agent.py`) is the upstream reference. The wholesale-copy lives in cianfhoghlaim's `agents/adk/` directory but has not yet been adapted for cianchosaint.

The per-constituency agent fleet (3 root + 15 specialists = 18 agents in total) currently instantiates `LlmAgent(...)` directly. Adding a new agent requires 30+ lines of boilerplate. This is friction: every new agent the BIOD v1 / BIPP v2 / BGARD v1 / BPSNI v1 pipelines add will need this boilerplate.

The factory eliminates the boilerplate AND wires the Langfuse prompt resolver (per `cianchosaint-langfuse-prompt-management-v1`) + the BuiltInPlanner (per the cianfhoghlaim ADK 2 codelab's `make_planner_agent()` helper) into every agent.

## ADDED Requirements

### Requirement: The make_cianchosaint_agent() factory contract

The system SHALL provide a `make_cianchosaint_agent()` function at `agents/cianchosaint/_factory.py` with the signature:

```python
def make_cianchosaint_agent(
    name: str,
    description: str,
    instruction: str,
    *,
    sub_agents: list | None = None,
    tools: list | None = None,
    model_alias: str = "minimax",
    temperature: float = 0.3,
    max_output_tokens: int = 8192,
    output_key: str | None = None,
    enable_thinking: bool = False,
) -> LlmAgent:
    """The canonical cianchosaint agent factory.
    ...
    """
```

#### Scenario: Every existing root agent is reachable via the factory

- **WHEN** the operator imports `make_cianchosaint_agent` from `agents.cianchosaint._factory`
- **THEN** calling `make_cianchosaint_agent(name="ga_root_agent", description=..., instruction=...)` SHALL return the canonical GA root agent
- **AND** the returned agent SHALL have the same `name` + `sub_agents` as the previous manual instantiation

#### Scenario: Every existing specialist is reachable via the factory

- **WHEN** the operator imports `make_cianchosaint_agent`
- **THEN** calling `make_cianchosaint_agent(name="ga_crime_statistics_agent", description=..., instruction=...)` SHALL return the canonical GA crime statistics specialist
- **AND** every one of the 18 agents SHALL be reachable via the factory

### Requirement: The AGENT_FACTORY_REGISTRY

The system SHALL provide an `AGENT_FACTORY_REGISTRY: dict[str, AgentWiring]` mapping canonical agent names to factory kwargs at `agents/cianchosaint/_factory.py`.

#### Scenario: The registry has all 18 agents

- **WHEN** the operator imports `AGENT_FACTORY_REGISTRY` from `agents.cianchosaint._factory`
- **THEN** the registry SHALL contain entries for all 18 agents (3 root + 15 specialist)
- **AND** each entry SHALL be an `AgentWiring` namedtuple with `name`, `description`, `instruction`, `sub_agents` (optional), `tools` (optional), and any factory kwargs

### Requirement: The cianchosaint_skill() helper

The system SHALL provide a `cianchosaint_skill(name: str, **kwargs: Any) -> str` helper at `agents/cianchosaint/_factory.py` that returns the agent name (for use with `LangfusePromptResolver`).

#### Scenario: cianchosaint_skill() returns the canonical name

- **WHEN** the operator calls `cianchosaint_skill("ga_crime_statistics_agent")`
- **THEN** it SHALL return `"ga_crime_statistics_agent"` as a `str`
- **AND** the function SHALL accept arbitrary `**kwargs` for forward compatibility (ignored in this version)

### Requirement: The BuiltInPlanner is wired when enable_thinking=True

The system SHALL wire `BuiltInPlanner(thinking_config=ThinkingConfig(include_thoughts=True))` into the agent when `enable_thinking=True`.

#### Scenario: BuiltInPlanner is auto-wired

- **WHEN** the operator calls `make_cianchosaint_agent(name=..., enable_thinking=True)`
- **THEN** the returned agent SHALL have `planner=BuiltInPlanner(...)` set
- **AND** the agent's instruction SHALL be the same as `make_cianchosaint_agent(name=..., enable_thinking=False)`

### Requirement: Conservative-posture guard

The system SHALL enforce the conservative-posture contract on every agent (per the existing `cianchosaint-per-constituency-agents` spec + the existing `cianchosaint-baml-schemas` spec): every returned agent SHALL have `osint_ceiling_enforced=True` (the OSINT allowlist is checked via `CianchosaintAgentBase.check_osint_source()`).

#### Scenario: OSINT allowlist gate is preserved

- **WHEN** the operator calls any of the factory-built agents
- **THEN** the agent SHALL preserve the existing `CianchosaintAgentBase.check_osint_source()` gate (no behaviour change vs the previous manual instantiation)

### Requirement: cianchosaint_skill() helper for LangfusePromptResolver integration

The system SHALL provide a `cianchosaint_skill(name: str, **kwargs: Any) -> str` helper at `agents/cianchosaint/_factory.py` that returns the agent name (for use with `LangfusePromptResolver` per `cianchosaint-langfuse-prompt-management-v1`).

#### Scenario: The helper is callable

- **WHEN** the operator calls `cianchosaint_skill("ga_crime_statistics_agent")`
- **THEN** the function SHALL return `"ga_crime_statistics_agent"` as a `str`
- **AND** the function SHALL accept arbitrary `**kwargs` for forward compatibility

### Requirement: Backward compatibility with CianchosaintAgentBase

The system SHALL preserve the existing `CianchosaintAgentBase.get_active_model()` API.

#### Scenario: get_active_model() still works

- **WHEN** the operator calls `ga_root_agent_instance.get_active_model()`
- **THEN** the method SHALL return the canonical model string (delegated to the factory's `model_for(model_alias)` helper)
- **AND** no behaviour change vs the previous implementation

### Requirement: Post-load hydration of the AGENT_FACTORY_REGISTRY

The system SHALL run a post-load hydration pass (via `_post_load_hydration()`) that resolves the strings in `AGENT_FACTORY_REGISTRY[name].sub_agents` and `AGENT_FACTORY_REGISTRY[name].tools` to the actual `LlmAgent` and `BaseTool` instances, AFTER all specialist modules have finished loading.

#### Scenario: The hydration runs after module load

- **WHEN** the operator imports any cianchosaint agent module (which triggers the loading chain `agents/cianchosaint/__init__.py` → root agents → specialists → factory)
- **THEN** the `_post_load_hydration()` function SHALL be called AFTER all 18 specialist modules have loaded
- **AND** `AGENT_FACTORY_REGISTRY["ga_root_agent"].sub_agents` SHALL contain 5 `LlmAgent` instances (one per GA specialist)
- **AND** `AGENT_FACTORY_REGISTRY["ga_crime_statistics_agent"].tools` SHALL contain 1 `FunctionTool` instance

## Cross-references

- [`../../agents/cianchosaint/_base.py`](../../agents/cianchosaint/_base.py) — the canonical base class (`CianchosaintAgentBase`)
- [`../../agents/cianchosaint/_factory.py`](../../agents/cianchosaint/_factory.py) — the factory itself
- [`../../tests/agents/cianchosaint/test_agent_factory.py`](../../tests/agents/cianchosaint/test_agent_factory.py) — the smoke test
- [`../../openspec/changes/cianchosaint-per-constituency-agents/spec.md`](../../openspec/changes/cianchosaint-per-constituency-agents/spec.md) — the umbrella spec
- [`../../openspec/changes/cianchosaint-langfuse-prompt-management/spec.md`](../../openspec/changes/cianchosaint-langfuse-prompt-management/spec.md) — the Langfuse prompt resolver integration
- cianfhoghlaim `agents/adk/litellm_agent.py` + `agents/adk/agent_registry.py` — upstream reference
- cianfhoghlaim `agents/integrations/baml_function_tool.py` — upstream reference for BAMLFunctionTool lazy loader
