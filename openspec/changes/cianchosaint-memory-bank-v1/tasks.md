# Tasks: cianchosaint-memory-bank-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.11+ installed
- [x] Verify `cognee_store` + `graphiti_store` available in cianchosaint (per the existing `agents/meaisinfhoghlaim/firecrawl_mcp/memory/` package)

## 1. Author the memory_bank package

- [x] Write `agents/cianchosaint/memory_bank/__init__.py` (~20 LOC) — package marker + re-exports
- [x] Write `agents/cianchosaint/memory_bank/state.py` (~80 LOC) — defines the canonical key prefixes (`(none)` / `user:` / `app:` / `temp:`)
- [x] Write `agents/cianchosaint/memory_bank/topics.py` (~120 LOC) — defines `FILING["allowed_topics"]` governance per entity class
- [x] Write `agents/cianchosaint/memory_bank/_recall.py` (~120 LOC) — `candidates_from_session(...)` walks events and pulls out candidates

## 2. Author the canonical CianchosaintMemoryService

- [x] Write `agents/cianchosaint/memory_bank/service.py` (~250 LOC) with:
  - `CianchosaintMemoryService(BaseMemoryService)` subclass
  - `add_session_to_memory(session, custom_metadata=None)` — stores facts under `app:` prefix
  - `search_memory(*, app_name, user_id, query)` — searches `app:` scope

## 3. Wire the agents/cianchosaint/__init__.py

- [x] Modify `agents/cianchosaint/__init__.py` — export the 4 new memory_bank modules

## 4. Author the spec + the test

- [x] Write `openspec/changes/cianchosaint-memory-bank-v1/specs/cianchosaint-memory-bank/spec.md` — the canonical spec (Requirement: `app:` prefix scope + `FILING[allowed_topics]` governance + BaseMemoryService conformance; Scenario: every cianchosaint surface shares Farage investigations + disallowed topics are rejected)
- [x] Write `openspec/changes/cianchosaint-memory-bank-v1/cross-repo-sync.md` — sole repo cianchosaint
- [x] Write `tests/agents/cianchosaint/test_memory_bank.py` — verifies `app:` scope + `FILING[allowed_topics]` governance

## 5. CI gate

- [x] Run `openspec validate cianchosaint-memory-bank-v1 --strict`
- [x] Run `PYTHONPATH=. python3 tests/agents/cianchosaint/test_memory_bank.py`
- [x] Run regression tests for T1.1 + T1.2 + T1.3 + T2.1 + T2.2
- [x] Run `mise run lint:license`

## 6. Commit + archive

- [x] `git add openspec/changes/cianchosaint-memory-bank-v1/ agents/cianchosaint/memory_bank/ agents/cianchosaint/__init__.py tests/agents/cianchosaint/test_memory_bank.py`
- [x] `git commit -m "feat(cianchosaint): add CianchosaintMemoryService with app: prefix scope + FILING[allowed_topics] governance"`
- [x] `openspec archive cianchosaint-memory-bank-v1 --yes`

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-memory-bank-v1 --strict

# 2. test the memory bank
PYTHONPATH=. python3 tests/agents/cianchosaint/test_memory_bank.py

# 3. regression: existing tests still pass
PYTHONPATH=. python3 tests/agents/cianchosaint/test_agent_factory.py
PYTHONPATH=. python3 tests/agents/integrations/test_agent_registry_runtime.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_long_running_tools.py
PYTHONPATH=. python3 tests/cocoindex_flows/test_shared_lifespan.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_workflow_graphs.py

# 4. lint_license
mise run lint:license
```
