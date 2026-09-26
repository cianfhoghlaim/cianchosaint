# Change: cianchosaint-memory-bank-v1

## Why

The cianfhoghlaim ADK 2 codelab's `docs/google_examples/adk-examples/agent-valley-archive` shows the canonical Memory Bank pattern:

- `agent_valley-archive.archive.service` defines a `MarkdownMemoryService(BaseMemoryService)` — a custom memory service whose `add_session_to_memory(session)` + `search_memory(...)` work over a Markdown file
- The `state.py` defines 3 key prefixes: `(none)` (this visit), `user:` (this analyst, forever), `app:` (everyone, forever)
- The `topics.py` defines `FILING["allowed_topics"]` — governance at write time, not at read time

The user selected the `app:` prefix scope (per the prior conversation). This means: every cianchosaint web app + every BIPP/BIDP/BIIP worker + every cross-cutting workflow shares Farage investigations across all 8 surfaces.

Cianchosaint has a `cognee_store` + `graphiti_store` (general-purpose knowledge graphs) but no notion of `user:` / `app:` scoped memory. Every conversation is independent; the system has no cross-session learning.

This change lands the canonical `CianchosaintMemoryService(BaseMemoryService)` with `app:` prefix scope + the `FILING["allowed_topics"]` governance — per the user's selection.

## What changes

- **NEW file** `agents/cianchosaint/memory_bank/__init__.py` (~20 LOC) — package marker
- **NEW file** `agents/cianchosaint/memory_bank/service.py` (~250 LOC) — the canonical `CianchosaintMemoryService` (subclass of `BaseMemoryService`) with `add_session_to_memory` + `search_memory` + `app:` scope
- **NEW file** `agents/cianchosaint/memory_bank/state.py` (~80 LOC) — the `state.py` analogue: defines the canonical key prefixes `(none)` / `user:` / `app:` / `temp:`
- **NEW file** `agents/cianchosaint/memory_bank/topics.py` (~120 LOC) — the `topics.py` analogue: defines `FILING["allowed_topics"]` governance (what topics may be filed for each entity class)
- **NEW file** `agents/cianchosaint/memory_bank/_recall.py` (~120 LOC) — the `recall.py` analogue: `candidates_from_session(...)` walks events and pulls out candidates (the canonical agent-valley-archive pattern)
- **MODIFIED** `agents/cianchosaint/agents/cianchosaint/__init__.py` — export the 4 new modules
- **NEW test** `tests/agents/cianchosaint/test_memory_bank.py` — verifies the `app:` prefix scope + the `FILING["allowed_topics"]` governance
- **NEW spec delta** `openspec/changes/cianchosaint-memory-bank-v1/specs/cianchosaint-memory-bank/spec.md`

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-memory-bank`)
- Affected code/config: 5 NEW files + 1 MODIFIED file
- **0 NEW DLT sources, 0 NEW BAML files** — pure memory layer
- Estimated LOC: ~600 LOC added
- **0 new dependencies** — uses `cognee_store` + `graphiti_store` already in cianchosaint

## Out of scope (follow-up changes)

- The vertex_memory_bank integration (per `cianchosaint-vertex-ai-migration`) — separate change
- The RAGAS eval dataset (T2.4) — uses the memory bank but is a separate surface

## Dependencies

`Blocked by: cianchosaint-agent-factory-v1` (the memory bank uses the factory pattern)
`Blocked by: cianchosaint-agent-registry-runtime-v1` (the memory bank is registered with the runtime)
`Affected repos: cianchosaint only.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `docs/google_examples/adk-examples/agent-valley-archive/archive/` remains the upstream reference.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-memory-bank-v1 --strict
# Expected: Validation passes

# 2. test the memory bank
PYTHONPATH=. python3 tests/agents/cianchosaint/test_memory_bank.py
# Expected: app: scope works; FILING[allowed_topics] governance works

# 3. regression: existing tests still pass
PYTHONPATH=. python3 tests/agents/cianchosaint/test_agent_factory.py
PYTHONPATH=. python3 tests/agents/integrations/test_agent_registry_runtime.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_long_running_tools.py
PYTHONPATH=. python3 tests/cocoindex_flows/test_shared_lifespan.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_workflow_graphs.py

# 4. lint_license
mise run lint:license
```
