# Cross-Repo Sync: cianchosaint-agent-registry-runtime-v1

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `agents/integrations/` directory remains the upstream reference; we wholesale-adapt the pattern in this change. No changes to the cianfhoghlaim or leabharlann repos are needed.

## Order of Operations

```
[1] cianchosaint → openspec/changes/cianchosaint-agent-registry-runtime-v1/
                   (proposal + tasks + cross-repo-sync + spec)
                   Adds: agents/integrations/__init__.py + agent_registry_runtime.py + agent_ui_bridge.py + baml_function_tool.py
                   Modifies: agents/cianchosaint/tools/__init__.py
                   Adds: tests/agents/integrations/test_agent_registry_runtime.py
                   Pushed to main.
                       ↓
[2] operator    → cd cianchosaint && openspec validate cianchosaint-agent-registry-runtime-v1 --strict
                  → openspec validate --all --strict
                  → All validations pass
                       ↓
[3] operator    → openspec archive cianchosaint-agent-registry-runtime-v1 --yes
```

## Repo 1: cianchosaint (sole)

**Files to commit** (under `openspec/changes/cianchosaint-agent-registry-runtime-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-agent-registry-runtime/spec.md` (the canonical spec)

**New files**:
- `agents/integrations/__init__.py` (~30 LOC) — re-exports the cianfhoghlaim package
- `agents/integrations/agent_registry_runtime.py` (~200 LOC) — the 3-helper surface
- `agents/integrations/agent_ui_bridge.py` (~180 LOC) — the canonical `register_adk_agent()` helper
- `agents/integrations/baml_function_tool.py` (~150 LOC) — the canonical BAMLFunctionTool wrapper
- `tests/agents/integrations/test_agent_registry_runtime.py` (~100 LOC) — the smoke test

**Modified files**:
- `agents/cianchosaint/tools/__init__.py` — export `ag_ui_registration_event` helper

## Repo 2: cianfhoghlaim (unchanged)

The upstream `agents/integrations/agent_registry_runtime.py` + `agents/integrations/agent_ui_bridge.py` + `agents/integrations/baml_function_tool.py` remain unchanged. We wholesale-adapt the pattern into cianchosaint T1.2.

## Repo 3: leabharlann (unchanged)

The 87 politics PDFs in `leabharlann/gemini_deep_research/politics/` are read-only context for the politician pipeline (which T1.2 doesn't touch). No changes.
