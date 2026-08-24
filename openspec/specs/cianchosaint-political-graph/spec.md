# cianchosaint-political-graph Capability

## Purpose

`cianchosaint-political-graph` is the canonical political-accountability graph store for cianchosaint. It extends the existing Cognee + Graphiti stores with the BIPP v2-specific entity + relationship types and provides the cross-source dossier composition query.

## Background

The 7 BIPP v2 BAML extraction schemas (per `cianchosaint-bipp-v2-baml-v1`) extract entities + relationships from the 87 leabharlann politics PDFs. These entities + relationships are stored in the political-accountability graph and queried via the cross-source dossier composition.

## Requirements

### Requirement: The PoliticalGraphStore class

The system SHALL provide a `PoliticalGraphStore` class at `agents/cianchosaint/tools/political_graph_store.py`.

#### Scenario: The graph supports 13 entity types + 13 relationship types

- **WHEN** the operator inspects `PoliticalGraphStore`
- **THEN** the class SHALL define 13 entity types (politician, donor, company, agency, court, event, media_outlet, trade_union, think_tank, lobbyist, regulator, publication, source_pdf)
- **AND** SHALL define 13 relationship types (donates_to, employed_by, owns, regulates, sued_by, sues, investigates, investigated_by, reports_on, member_of, sp_legates_to, employs, linked_to)

#### Scenario: The BFS query_dossier method

- **WHEN** the operator invokes `await store.query_dossier(target_entity='richard_tice', cohort='bipp_v2_reform_uk_accountability')`
- **THEN** the method SHALL return a `PoliticalGraphQueryResult` with the entities + relationships + source PDFs

## Cross-references

- [`../../agents/cianchosaint/tools/political_graph_store.py`](../../agents/cianchosaint/tools/political_graph_store.py) — the canonical store
- [`../../agents/meaisinfhoghlaim/firecrawl_mcp/memory/cognee_store.py`](../../agents/meaisinfhoghlaim/firecrawl_mcp/memory/cognee_store.py) — the upstream Cognee store
- [`../../agents/meaisinfhoghlaim/firecrawl_mcp/memory/graphiti_store.py`](../../agents/meaisinfhoghlaim/firecrawl_mcp/memory/graphiti_store.py) — the upstream Graphiti store
- [`../../openspec/specs/cianchosaint-bipp-v2/spec.md`](../../openspec/specs/cianchosaint-bipp-v2/spec.md) — the BIPP v2 vertical