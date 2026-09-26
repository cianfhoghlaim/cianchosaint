# Cross-Repo Sync: cianchosaint-workflow-graph-v1

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `docs/google_examples/adk2-tutorial/{L2a_parallel_join, L2b_router, L4a_flat_research}` remain the upstream reference. No changes to the cianfhoghlaim or leabharlann repos are needed.

## Order of Operations

```
[1] cianchosaint → openspec/changes/cianchosaint-workflow-graph-v1/
                   (proposal + tasks + cross-repo-sync + spec)
                   Adds: agents/cianchosaint/workflows/{politician_resolver,funder_network,wikipedia_bridge}_graph.py + __init__.py
                   Adds: tests/agents/cianchosaint/test_workflow_graphs.py
                   Pushed to main.
                       ↓
[2] operator    → cd cianchosaint && openspec validate cianchosaint-workflow-graph-v1 --strict
                  → openspec validate --all --strict
                  → All validations pass
                       ↓
[3] operator    → openspec archive cianchosaint-workflow-graph-v1 --yes
```

## Repo 1: cianchosaint (sole)

**Files to commit** (under `openspec/changes/cianchosaint-workflow-graph-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-workflow-graph/spec.md` (the canonical spec)

**New files**:
- `agents/cianchosaint/workflows/politician_resolver_graph.py` (~250 LOC)
- `agents/cianchosaint/workflows/funder_network_graph.py` (~250 LOC)
- `agents/cianchosaint/workflows/wikipedia_bridge_graph.py` (~250 LOC)
- `agents/cianchosaint/workflows/__init__.py` (~30 LOC)
- `tests/agents/cianchosaint/test_workflow_graphs.py` (~120 LOC)

## Repo 2: cianfhoghlaim (unchanged)

The upstream `docs/google_examples/adk2-tutorial/L2a_parallel_join` + `L2b_router` + `L4a_flat_research` remain unchanged. We wholesale-adapt the pattern in this change.

## Repo 3: leabharlann (unchanged)

The 87 politics PDFs in `leabharlann/gemini_deep_research/politics/` are read-only context for the politician pipeline (which T2.2 doesn't touch). No changes.
