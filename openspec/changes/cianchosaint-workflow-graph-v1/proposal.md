# Change: cianchosaint-workflow-graph-v1

## Why

The cianfhoghlaim ADK 2 codelab's three pillars (per `docs/google_examples/adk2-tutorial`) teach the canonical `Workflow(edges=[...])` graph pattern:

- **Pillar 1 (Graph)**: `Workflow(edges=[(START, fn1, fn2, fn3), ...])` with function nodes + agent nodes as peers
- **JoinNode**: bundles parallel outputs into one typed payload keyed by upstream function name
- **Dict-edge router**: `{"HOT": hot_agent, "NORMAL": normal_agent, "COLD": cold_agent}` for explicit branching

The 3 case-study politician tools (`politician_account_resolver`, `funder_network_graph`, `wikipedia_bridge`) are currently plain async functions in `agents/cianchosaint/tools/`. They do useful work but they're not graph-shaped — they have no function nodes (zero-LLM fetches), no JoinNode (no parallel bundling), no router (no scrape-failure fallback).

This change graph-ifies all 3 (per the user's selection in the prior conversation: "all 3"). Each becomes a `Workflow(edges=[...])` with the canonical cianfhoghlaim pattern.

## What changes

- **NEW file** `agents/cianchosaint/workflows/politician_resolver_graph.py` (~250 LOC) — the 5-node graph: function(scrap party profile) → function(scrap wikipedia) → JoinNode → agent(BAML ExtractPoliticianFromWebPage) → router (if scrape fails → fallback regex extraction)
- **NEW file** `agents/cianchosaint/workflows/funder_network_graph.py` (~250 LOC) — the 5-node graph: function(electoral commission query) → function(companies house lookup) → JoinNode → agent(adjacent_context_resolver: Funder) → router (if EC/CH fail → fallback to declared-interests only)
- **NEW file** `agents/cianchosaint/workflows/wikipedia_bridge_graph.py` (~250 LOC) — the parallel wikipedia-bridge graph: function(SPARQL QID lookup) → function(multilingual article fetch) → JoinNode → agent(political-context enrichment) → parallel_worker (3-7 parallel wikipedia fetches across en/ga/cy/gd)
- **NEW file** `agents/cianchosaint/workflows/__init__.py` (~30 LOC) — package marker + re-exports
- **NEW test** `tests/agents/cianchosaint/test_workflow_graphs.py` — verifies each graph builds, the JoinNode bundles correctly, the router branches correctly, the parallel_worker fans out correctly
- **NEW spec delta** `openspec/changes/cianchosaint-workflow-graph-v1/specs/cianchosaint-workflow-graph/spec.md`

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-workflow-graph`)
- Affected code/config: 4 NEW files
- **0 NEW DLT sources, 0 NEW BAML files** — pure graph refactor; the existing tools stay intact as the function nodes
- Estimated LOC: ~780 LOC added
- **0 new dependencies** — uses the existing `google.adk.workflow` + `google.adk.workflow.JoinNode` + `google.adk.workflow.START` classes

## Out of scope (follow-up changes)

- The Dagster asset integration (T3.3) — uses the same graphs but orchestrates scheduling
- The CocoIndex embedder integration (T2.4) — uses the same graphs but for offline indexing

## Dependencies

`Blocked by: cianchosaint-agent-factory-v1` (the factory pattern is the canonical surface for tool wiring)
`Blocked by: cianchosaint-long-running-tools-v1` (the workflow graphs use `LongRunningFunctionTool` nodes for the 40-minute PULSE queries)
`Affected repos: cianchosaint only.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `docs/google_examples/adk2-tutorial/L2a_parallel_join` + `L2b_router` + `L4a_flat_research` remain the upstream reference.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-workflow-graph-v1 --strict
# Expected: Validation passes

# 2. test the workflow graphs
PYTHONPATH=. python3 tests/agents/cianchosaint/test_workflow_graphs.py
# Expected: Each graph builds; JoinNode bundles correctly; router branches correctly

# 3. regression: existing tests still pass
PYTHONPATH=. python3 tests/agents/cianchosaint/test_agent_factory.py
PYTHONPATH=. python3 tests/agents/integrations/test_agent_registry_runtime.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_long_running_tools.py
PYTHONPATH=. python3 tests/cocoindex_flows/test_shared_lifespan.py

# 4. lint_license
mise run lint:license
```
