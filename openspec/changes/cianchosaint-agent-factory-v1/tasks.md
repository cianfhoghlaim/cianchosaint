# Tasks: cianchosaint-agent-factory-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.11+ installed
- [x] Verify cianfhoghlaim `agents/adk/litellm_agent.py` wholesale-copy is accessible as reference
- [x] Verify `google-adk` >= 2.x is installed in cianchosaint

## 1. Author the factory + the registry

- [x] Write `agents/cianchosaint/_factory.py` (~150 LOC) with:
  - `make_cianchosaint_agent(name, description, instruction, *, sub_agents=None, tools=None, model_alias="minimax", temperature=0.3, max_output_tokens=8192, output_key=None, enable_thinking=False)` — the canonical factory call
  - `cianchosaint_skill(name, **kwargs)` — convenience wrapper that returns `name` (for use with `LangfusePromptResolver`)
  - `AGENT_FACTORY_REGISTRY` — `dict[str, AgentWiring]` mapping canonical agent names to factory kwargs (the cianfhoghlaim-style registry)
  - `_try_import_baml_function_tool()` — lazy loader for `agents.integrations.baml_function_tool.BAMLFunctionTool` (mirror cianfhoghlaim's `agents/integrations/baml_function_tool.py`)

## 2. Refactor the 3 root agents

- [x] Modify `agents/cianchosaint/ga_root_agent.py` — replace the manual `LlmAgent(...)` instantiation with a single `make_cianchosaint_agent(...)` call
- [x] Modify `agents/cianchosaint/met_root_agent.py` — same refactor
- [x] Modify `agents/cianchosaint/psni_root_agent.py` — same refactor

## 3. Refactor the 15 specialists

- [x] Modify `agents/cianchosaint/ga_specialists/crime_statistics_agent.py` — same refactor
- [x] Modify `agents/cianchosaint/ga_specialists/traffic_law_agent.py`
- [x] Modify `agents/cianchosaint/ga_specialists/foia_requests_agent.py`
- [x] Modify `agents/cianchosaint/ga_specialists/irish_statute_book_agent.py`
- [x] Modify `agents/cianchosaint/ga_specialists/courts_ie_agent.py`
- [x] Modify `agents/cianchosaint/met_specialists/crime_statistics_agent.py`
- [x] Modify `agents/cianchosaint/met_specialists/stop_and_search_agent.py`
- [x] Modify `agents/cianchosaint/met_specialists/met_press_releases_agent.py`
- [x] Modify `agents/cianchosaint/met_specialists/met_public_contact_agent.py`
- [x] Modify `agents/cianchosaint/met_specialists/crime_prevention_agent.py`
- [x] Modify `agents/cianchosaint/psni_specialists/crime_statistics_agent.py`
- [x] Modify `agents/cianchosaint/psni_specialists/psni_press_releases_agent.py`
- [x] Modify `agents/cianchosaint/psni_specialists/psni_public_contact_agent.py`
- [x] Modify `agents/cianchosaint/psni_specialists/ni_justice_agent.py`
- [x] Modify `agents/cianchosaint/psni_specialists/policing_board_agent.py`

## 4. Wire the base class

- [x] Modify `agents/cianchosaint/_base.py` — `CianchosaintAgentBase.get_active_model()` is preserved (no behaviour change) but delegates to the factory's `model_for(model_alias)` helper

## 5. Author the spec + the test

- [x] Write `openspec/changes/cianchosaint-agent-factory-v1/specs/cianchosaint-agent-factory/spec.md` — the canonical spec (Requirement: factory contract + registry contract + conservative-posture guard; Scenario: every agent reachable + factory kwargs stable + Langfuse resolver hook)
- [x] Write `openspec/changes/cianchosaint-agent-factory-v1/cross-repo-sync.md` — sole repo cianchosaint
- [x] Write `tests/agents/cianchosaint/test_agent_factory.py` — verifies every root + specialist is reachable via the factory, factory kwargs are stable (snapshot test), and BuiltInPlanner is wired when `enable_thinking=True`

## 6. CI gate

- [x] Run `openspec validate cianchosaint-agent-factory-v1 --strict`
- [x] Run `python3 tests/agents/cianchosaint/test_agent_factory.py`
- [x] Run `mise run lint:license`

## 7. Commit + archive

- [x] `git add openspec/changes/cianchosaint-agent-factory-v1/ agents/cianchosaint/_factory.py tests/agents/cianchosaint/test_agent_factory.py`
- [x] `git commit -m "feat(cianchosaint): add make_cianchosaint_agent() factory + AGENT_FACTORY_REGISTRY"`
- [x] `openspec archive cianchosaint-agent-factory-v1 --yes`

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-agent-factory-v1 --strict

# 2. test the factory
python3 tests/agents/cianchosaint/test_agent_factory.py

# 3. smoke: agent instantiation
python3 -c "
import sys; sys.path.insert(0, '.')
from agents.cianchosaint._factory import make_cianchosaint_agent, AGENT_FACTORY_REGISTRY
print(f'Factory registry has {len(AGENT_FACTORY_REGISTRY)} agents')
"

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

# 5. lint_license
mise run lint:license
```
