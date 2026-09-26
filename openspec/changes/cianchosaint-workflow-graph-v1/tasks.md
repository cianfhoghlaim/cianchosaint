# Tasks: cianchosaint-workflow-graph-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.11+ installed
- [x] Verify `google.adk.workflow.Workflow` + `JoinNode` + `START` available

## 1. Author the politician_resolver_graph workflow

- [x] Write `agents/cianchosaint/workflows/politician_resolver_graph.py` (~250 LOC) with:
  - 5-node graph: function(scrap_party_profile) → function(scrap_wikipedia) → JoinNode → agent(BAML ExtractPoliticianFromWebPage) → router (if scrape fails → fallback regex extraction)
  - Use the existing `politician_account_resolver_tool` as the fallback regex-extraction node
  - The router uses a dict-edge pattern (per cianfhoghlaim's `L2b_router`)

## 2. Author the funder_network_graph workflow

- [x] Write `agents/cianchosaint/workflows/funder_network_graph.py` (~250 LOC) with:
  - 5-node graph: function(electoral_commission_query) → function(companies_house_lookup) → JoinNode → agent(adjacent_context_resolver: Funder) → router (if EC/CH fail → fallback to declared-interests only)

## 3. Author the wikipedia_bridge_graph workflow

- [x] Write `agents/cianchosaint/workflows/wikipedia_bridge_graph.py` (~250 LOC) with:
  - Parallel wikipedia-bridge graph: function(SPARQL QID lookup) → function(multilingual article fetch) → JoinNode → agent(political-context enrichment) → parallel_worker (3-7 parallel wikipedia fetches across en/ga/cy/gd)

## 4. Author the workflows package

- [x] Write `agents/cianchosaint/workflows/__init__.py` (~30 LOC) — package marker + re-exports

## 5. Author the spec + the test

- [x] Write `openspec/changes/cianchosaint-workflow-graph-v1/specs/cianchosaint-workflow-graph/spec.md` — the canonical spec (Requirement: workflow contract + JoinNode contract + dict-edge router contract; Scenario: each graph builds + each graph bundles + each router branches)
- [x] Write `openspec/changes/cianchosaint-workflow-graph-v1/cross-repo-sync.md` — sole repo cianchosaint
- [x] Write `tests/agents/cianchosaint/test_workflow_graphs.py` — verifies each graph builds, the JoinNode bundles correctly, the router branches correctly, the parallel_worker fans out correctly

## 6. CI gate

- [x] Run `openspec validate cianchosaint-workflow-graph-v1 --strict`
- [x] Run `PYTHONPATH=. python3 tests/agents/cianchosaint/test_workflow_graphs.py`
- [x] Run regression tests for T1.1 + T1.2 + T1.3 + T2.1
- [x] Run `mise run lint:license`

## 7. Commit + archive

- [x] `git add openspec/changes/cianchosaint-workflow-graph-v1/ agents/cianchosaint/workflows/`
- [x] `git commit -m "feat(cianchosaint): graph-ify politician resolver + funder network + wikipedia bridge as ADK Workflows"`
- [x] `openspec archive cianchosaint-workflow-graph-v1 --yes`

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-workflow-graph-v1 --strict

# 2. test the workflow graphs
PYTHONPATH=. python3 tests/agents/cianchosaint/test_workflow_graphs.py

# 3. regression: existing tests still pass
PYTHONPATH=. python3 tests/agents/cianchosaint/test_agent_factory.py
PYTHONPATH=. python3 tests/agents/integrations/test_agent_registry_runtime.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_long_running_tools.py
PYTHONPATH=. python3 tests/cocoindex_flows/test_shared_lifespan.py

# 4. lint_license
mise run lint:license
```
