# Cross-Repo Sync: cianchosaint-agent-factory-v1

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `agents/adk/litellm_agent.py` remains the upstream reference; we wholesale-adapt the pattern (per the cianfhoghlaim ADK 2 codelab's `make_litellm_agent()` factory) in `agents/cianchosaint/_factory.py`. No changes to the cianfhoghlaim or leabharlann repos are needed.

## Order of Operations

```
[1] cianchosaint → openspec/changes/cianchosaint-agent-factory-v1/
                  (proposal + tasks + cross-repo-sync + spec)
                  Adds: agents/cianchosaint/_factory.py
                  Modifies: 18 agent files + 1 _base.py file
                  Adds: tests/agents/cianchosaint/test_agent_factory.py
                  Pushed to main.
                       ↓
[2] operator    → cd cianchosaint && openspec validate cianchosaint-agent-factory-v1 --strict
                  → openspec validate --all --strict
                  → All validations pass
                       ↓
[3] operator    → openspec archive cianchosaint-agent-factory-v1 --yes
```

## Repo 1: cianchosaint (sole)

**Files to commit** (under `openspec/changes/cianchosaint-agent-factory-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-agent-factory/spec.md` (the canonical spec)

**New files**:
- `agents/cianchosaint/_factory.py` (~150 LOC) — the canonical factory + registry
- `tests/agents/cianchosaint/test_agent_factory.py` (~80 LOC) — the smoke test

**Modified files** (pure refactor; no behaviour change):
- `agents/cianchosaint/_base.py` — delegate to the factory
- `agents/cianchosaint/ga_root_agent.py`
- `agents/cianchosaint/met_root_agent.py`
- `agents/cianchosaint/psni_root_agent.py`
- `agents/cianchosaint/ga_specialists/crime_statistics_agent.py`
- `agents/cianchosaint/ga_specialists/traffic_law_agent.py`
- `agents/cianchosaint/ga_specialists/foia_requests_agent.py`
- `agents/cianchosaint/ga_specialists/irish_statute_book_agent.py`
- `agents/cianchosaint/ga_specialists/courts_ie_agent.py`
- `agents/cianchosaint/met_specialists/crime_statistics_agent.py`
- `agents/cianchosaint/met_specialists/stop_and_search_agent.py`
- `agents/cianchosaint/met_specialists/met_press_releases_agent.py`
- `agents/cianchosaint/met_specialists/met_public_contact_agent.py`
- `agents/cianchosaint/met_specialists/crime_prevention_agent.py`
- `agents/cianchosaint/psni_specialists/crime_statistics_agent.py`
- `agents/cianchosaint/psni_specialists/psni_press_releases_agent.py`
- `agents/cianchosaint/psni_specialists/psni_public_contact_agent.py`
- `agents/cianchosaint/psni_specialists/ni_justice_agent.py`
- `agents/cianchosaint/psni_specialists/policing_board_agent.py`

## Repo 2: cianfhoghlaim (unchanged)

The upstream `agents/adk/litellm_agent.py` + `agents/adk/agent_registry.py` patterns are wholesale-copied into cianchosaint T1.1. No changes to cianfhoghlaim.

## Repo 3: leabharlann (unchanged)

The 87 politics PDFs in `leabharlann/gemini_deep_research/politics/` are read-only context for the politician pipeline (which T1.1 doesn't touch). No changes.
