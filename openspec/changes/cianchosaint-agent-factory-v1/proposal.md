# Change: cianchosaint-agent-factory-v1

## Why

The current cianchosaint per-constituency agent fleet (`agents/cianchosaint/ga_root_agent.py`, `met_root_agent.py`, `psni_root_agent.py` + the 15 specialists under `ga_specialists/`, `met_specialists/`, `psni_specialists/`) instantiates `LlmAgent(name=..., model=self.get_active_model() or DEFAULT_MODEL, description=..., instruction=..., sub_agents=[...], output_key=...)` directly. Each of the 18 agents repeats this boilerplate with subtle differences (temperature, max_output_tokens, output_key naming), and the LiteLLM gateway wiring is hidden inside `CianchosaintAgentBase.get_active_model()`.

The cianfhoghlaim sibling repo has the canonical pattern (per `agents/adk/litellm_agent.py`):
- A `make_litellm_agent(name, description, instruction, tools, *, model_alias="minimax", temperature=0.3, max_output_tokens=8192)` factory
- The factory calls `litellm_model("minimax")` to resolve the model via the LiteLLM gateway
- The factory auto-wires `BuiltInPlanner(thinking_config=...)` if the caller doesn't pass `disable_thinking`
- All 15 agents in the cianfhoghlaim fleet go through this factory — no manual `LlmAgent(...)` anywhere

Cianchosaint needs the same pattern. Currently:
- The `litellm_agent.py` helper hasn't been adapted for cianchosaint (the wholesale-copied file is in cianfhoghlaim, not cianchosaint)
- Every cianchosaint agent manually constructs `LlmAgent(...)` with subtle differences (some pass `output_key`, some don't; some have temperature baked into the instruction string; some have ad-hoc `BuiltInPlanner` while others have none)
- Adding a new agent (per the BIOD v1 / BIPP v2 / BGARD v1 plans) requires writing 30+ lines of boilerplate each time

This change lands the canonical `make_cianchosaint_agent()` factory + the canonical `cianchosaint_skill()` helper that wraps the Langfuse prompt resolver + the BuiltInPlanner pattern. It also wires the factory into a new `AGENT_FACTORY_REGISTRY` (canonical id → kwargs tuple) so the BIOD v1 / BIPP v2 / BIPP v2 specialists can be created by id.

## What changes

- **NEW file** `agents/cianchosaint/_factory.py` (~150 LOC) with:
  - `make_cianchosaint_agent(name, description, instruction, *, sub_agents=None, tools=None, model_alias="minimax", temperature=0.3, max_output_tokens=8192, output_key=None, enable_thinking=False)` — the canonical factory call
  - `cianchosaint_skill(name, **kwargs)` — convenience wrapper that returns `name` (for use with `LangfusePromptResolver`)
  - `AGENT_FACTORY_REGISTRY` — `dict[str, AgentWiring]` mapping canonical agent names to factory kwargs (the cianfhoghlaim-style registry)
  - `_try_import_baml_function_tool()` — lazy loader for `agents.integrations.baml_function_tool.BAMLFunctionTool` (mirror cianfhoghlaim's `agents/integrations/baml_function_tool.py`)
- **MODIFIED** `agents/cianchosaint/ga_root_agent.py`, `met_root_agent.py`, `psni_root_agent.py` — replace the manual `LlmAgent(...)` instantiation with a single `make_cianchosaint_agent(...)` call
- **MODIFIED** `agents/cianchosaint/ga_specialists/*.py`, `met_specialists/*.py`, `psni_specialists/*.py` — same refactor (15 specialist agents)
- **MODIFIED** `agents/cianchosaint/_base.py` — `CianchosaintAgentBase.get_active_model()` is preserved (no behaviour change) but delegates to the factory's `model_for(model_alias)` helper
- **NEW test** `tests/agents/cianchosaint/test_agent_factory.py` — verifies every root + specialist is reachable via the factory, that the factory kwargs are stable (snapshot test), and that the BuiltInPlanner is wired when `enable_thinking=True`
- **NEW spec delta** `openspec/changes/cianchosaint-agent-factory-v1/specs/cianchosaint-agent-factory/spec.md` (the canonical spec — see below)

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-agent-factory`)
- Affected code/config: 19 NEW/MODIFIED files (1 factory + 3 root agents + 15 specialists + 1 base update + 1 test + 1 spec)
- **0 NEW DLT sources, 0 NEW BAML files, 0 NEW FunctionTools** — pure refactor; agents behave identically
- Estimated LOC: ~200 LOC added, ~150 LOC removed (net +50 LOC for the factory + registry + test)
- **No new dependencies** — reuses `google.adk`, `structlog`, `strenum` (already present)

## Out of scope (follow-up changes)

- The per-subject (60-subject) factory in the cianfhoghlaim-nua v6-era plan (per `agents/adk/subjects/_factory.py` + the `_factory.py` `_subject_agents` registry)
- The Langfuse prompt resolver integration into the factory — that's `cianchosaint-agent-registry-runtime-v1` (Change T1.2)
- CocoIndex integration into the factory — that's `cianchosaint-cocoindex-shared-lifespan-v1` (Change T2.1)

## Dependencies

`Blocked by: none` — pure refactor; no upstream changes needed.
`Affected repos: cianchosaint only.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `agents/adk/litellm_agent.py` remains the upstream reference; we wholesale-adapt it in T1.1 + T1.2.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-agent-factory-v1 --strict
# Expected: Validation passes

# 2. lint: every agent reachable via the factory
python3 tests/agents/cianchosaint/test_agent_factory.py
# Expected: 18 agents reachable; factory kwargs stable; BuiltInPlanner wired when enabled

# 3. smoke: agent instantiation (no LLM call required)
python3 -c "
import sys; sys.path.insert(0, '.')
from agents.cianchosaint._factory import make_cianchosaint_agent, AGENT_FACTORY_REGISTRY
print(f'Factory registry has {len(AGENT_FACTORY_REGISTRY)} agents')
for name in sorted(AGENT_FACTORY_REGISTRY):
    print(f'  {name}')
"
# Expected: 18 agents listed

# 4. regression: agents behave identically
python3 -c "
import sys; sys.path.insert(0, '.')
from agents.cianchosaint.ga_root_agent import ga_root_agent
from agents.cianchosaint.met_root_agent import met_root_agent
from agents.cianchosaint.psni_root_agent import psni_root_agent
print(f'GA: {ga_root_agent.name}')
print(f'MET: {met_root_agent.name}')
print(f'PSNI: {psni_root_agent.name}')
"
# Expected: 3 root agents with their original names + tool wiring

# 5. lint_license (OSINT allowlist still passes)
mise run lint:license
# Expected: exit 0
```
