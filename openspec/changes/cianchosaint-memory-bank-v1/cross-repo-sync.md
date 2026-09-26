# Cross-Repo Sync: cianchosaint-memory-bank-v1

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `docs/google_examples/adk-examples/agent-valley-archive/archive/` remains the upstream reference. No changes to the cianfhoghlaim or leabharlann repos are needed.

## Order of Operations

```
[1] cianchosaint → openspec/changes/cianchosaint-memory-bank-v1/
                   (proposal + tasks + cross-repo-sync + spec)
                   Adds: agents/cianchosaint/memory_bank/{__init__,state,topics,_recall,service}.py
                   Modifies: agents/cianchosaint/__init__.py
                   Adds: tests/agents/cianchosaint/test_memory_bank.py
                   Pushed to main.
                       ↓
[2] operator    → cd cianchosaint && openspec validate cianchosaint-memory-bank-v1 --strict
                  → openspec validate --all --strict
                  → All validations pass
                       ↓
[3] operator    → openspec archive cianchosaint-memory-bank-v1 --yes
```

## Repo 1: cianchosaint (sole)

**Files to commit** (under `openspec/changes/cianchosaint-memory-bank-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-memory-bank/spec.md` (the canonical spec)

**New files**:
- `agents/cianchosaint/memory_bank/__init__.py` (~20 LOC) — package marker
- `agents/cianchosaint/memory_bank/state.py` (~80 LOC) — key prefixes
- `agents/cianchosaint/memory_bank/topics.py` (~120 LOC) — `FILING["allowed_topics"]`
- `agents/cianchosaint/memory_bank/_recall.py` (~120 LOC) — `candidates_from_session`
- `agents/cianchosaint/memory_bank/service.py` (~250 LOC) — `CianchosaintMemoryService`
- `tests/agents/cianchosaint/test_memory_bank.py` (~120 LOC) — the smoke test

**Modified files**:
- `agents/cianchosaint/__init__.py` — export the 4 new modules

## Repo 2: cianfhoghlaim (unchanged)

The upstream `docs/google_examples/adk-examples/agent-valley-archive/archive/` remains unchanged. We wholesale-adapt the pattern in this change.

## Repo 3: leabharlann (unchanged)

The 87 politics PDFs in `leabharlann/gemini_deep_research/politics/` are read-only context for the politician pipeline (which T2.3 doesn't touch). No changes.
