# cianchosaint-workflow-graph Capability

## Purpose

`cianchosaint-workflow-graph` graph-ifies the 3 case-study politician tools (`politician_account_resolver`, `funder_network_graph`, `wikipedia_bridge`) as `Workflow(edges=[...])` graphs. Mirrors cianfhoghlaim's ADK 2 codelab's three pillars (`L2a_parallel_join` + `L2b_router` + `L4a_flat_research`):

- **Pillar 1**: `Workflow(edges=[...])` with function nodes + agent nodes as peers
- **JoinNode**: bundles parallel outputs into one typed payload
- **Dict-edge router**: `{"HOT": hot_agent, "NORMAL": normal_agent, "COLD": cold_agent}`

## Background

Cianfhoghlaim's `docs/google_examples/adk2-tutorial/{L2a_parallel_join, L2b_router, L4a_flat_research}` teaches the canonical pattern:

- **L2a (Graph)**: parallel fan-out + JoinNode, then a single agent
- **L2b (Router)**: same plus a deterministic `if`-statement router
- **L4a (Dynamic)**: runtime-decided fan-out via `@node(parallel_worker=True)`

The cianchosaint politician tools (`politician_account_resolver`, `funder_network_graph`, `wikipedia_bridge`) are currently plain async functions. They do useful work but are not graph-shaped — no function nodes (zero-LLM fetches), no JoinNode (no parallel bundling), no router (no scrape-failure fallback).

This change lands all 3 as `Workflow(edges=[...])` graphs (per the user's selection: "graph-ify all 3").

## ADDED Requirements

### Requirement: The politician_resolver_graph workflow

The system SHALL provide `agents/cianchosaint/workflows/politician_resolver_graph.py` with a 5-node graph:

```
START → fetch_party_profile (function, 0 LLM) → JoinNode
      → fetch_wikipedia (function, 0 LLM)      ↗
      → router (if scrape fails → fallback regex)
      → agent(BAML ExtractPoliticianFromWebPage) → done
```

#### Scenario: The graph builds + bundles correctly

- **WHEN** the operator imports `politician_resolver_graph`
- **THEN** the graph SHALL build with 5 edges (per `Workflow(edges=[...])`)
- **AND** the JoinNode SHALL bundle `fetch_party_profile` + `fetch_wikipedia` outputs into one typed payload keyed by upstream function name

#### Scenario: The router branches correctly

- **WHEN** the router determines the scrape failed
- **THEN** it SHALL route to the fallback regex extraction (per the dict-edge pattern)
- **AND** the graph SHALL emit the fallback's Politician record as the final output

### Requirement: The funder_network_graph workflow

The system SHALL provide `agents/cianchosaint/workflows/funder_network_graph.py` with a 5-node graph:

```
START → fetch_electoral_commission (function, 0 LLM) → JoinNode
      → fetch_companies_house (function, 0 LLM)     ↗
      → router (if EC/CH fail → fallback to declared-interests only)
      → agent(adjacent_context_resolver: Funder) → done
```

#### Scenario: The funder graph bundles correctly

- **WHEN** the operator imports `funder_network_graph`
- **THEN** the graph SHALL build with 5 edges
- **AND** the JoinNode SHALL bundle the EC + CH lookup results into one typed payload

### Requirement: The wikipedia_bridge_graph workflow

The system SHALL provide `agents/cianchosaint/workflows/wikipedia_bridge_graph.py` with a parallel wikipedia-bridge graph:

```
START → fetch_sparql_qid (function, 0 LLM) → JoinNode
      → fetch_multilingual_article (function, 0 LLM, parallel) ↗
      → agent(political-context enrichment) → done
```

#### Scenario: The wikipedia graph fans out in parallel

- **WHEN** the operator imports `wikipedia_bridge_graph`
- **THEN** the graph SHALL build with at least 5 edges
- **AND** the `fetch_multilingual_article` node SHALL use `@node(parallel_worker=True)` to fan out across en/ga/cy/gd

### Requirement: The workflow graphs are composable

The system SHALL ensure all 3 workflow graphs can be invoked from the cianchosaint factory pattern (per `cianchosaint-agent-factory-v1`) + the runtime helpers (per `cianchosaint-agent-registry-runtime-v1`).

#### Scenario: Each graph is registered with the runtime

- **WHEN** the operator calls `register_all_agents_with_copilotkit()`
- **THEN** every workflow graph SHALL be wrapped as an `ag-ui-adk.ADKAgent`
- **AND** every graph SHALL be registered with the CopilotKit runtime

### Requirement: Conservative-posture guard

The system SHALL preserve the OSINT allowlist gate on every workflow graph (per `cianchosaint-per-constituency-agents` spec + `cianchosaint-baml-schemas` spec).

#### Scenario: OSINT allowlist is checked in the graph

- **WHEN** any workflow graph fetches a URL
- **THEN** the graph SHALL route the URL through `CianchosaintAgentBase.check_osint_source()`
- **AND** the graph SHALL NOT proceed if the URL is not allowlisted

## Cross-references

- [`../../agents/cianchosaint/workflows/politician_resolver_graph.py`](../../agents/cianchosaint/workflows/politician_resolver_graph.py) — the politician graph
- [`../../agents/cianchosaint/workflows/funder_network_graph.py`](../../agents/cianchosaint/workflows/funder_network_graph.py) — the funder graph
- [`../../agents/cianchosaint/workflows/wikipedia_bridge_graph.py`](../../agents/cianchosaint/workflows/wikipedia_bridge_graph.py) — the wikipedia graph
- [`../../agents/cianchosaint/tools/politician_account_resolver.py`](../../agents/cianchosaint/tools/politician_account_resolver.py) — the underlying tool the politician graph wraps
- cianfhoghlaim `docs/google_examples/adk2-tutorial/{L2a_parallel_join, L2b_router, L4a_flat_research}` — upstream reference
