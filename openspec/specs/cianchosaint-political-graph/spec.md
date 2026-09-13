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

### Requirement: PoliticianAccount entity type

The system SHALL extend the `PoliticalGraphStore.EntityType` enum to include `politician_account` (the entity that holds the per-politician schema) plus 3 adjacent entity types: `advisor`, `funder`, `historical_association`, `wikipedia_archives`.

#### Scenario: The 4 new entity types support the BAML class hierarchy

- **WHEN** the operator inspects `agents/cianchosaint/tools/political_graph_store.py`
- **THEN** `EntityType` SHALL extend to 17 types: `politician`, `donor`, `company`, `agency`, `court`, `event`, `media_outlet`, `trade_union`, `think_tank`, `lobbyist`, `regulator`, `publication`, `source_pdf`, `advisor`, `funder`, `historical_association`, `wikipedia_archives`
- **AND** the existing 13 types SHALL remain unchanged (no deletions)

### Requirement: 4 new relationship types

The system SHALL extend the `PoliticalGraphStore.RelationshipType` enum with 4 new types: `advises`, `advised_by` (the bidirectional advisor ↔ politician edge), `was_member_of` (politician → historical_association), `holds_wikidata_qid` (politician → wikipedia_archives).

#### Scenario: 4 new relationships extend the existing 13

- **WHEN** the operator inspects `agents/cianchosaint/tools/political_graph_store.py`
- **THEN** `RelationshipType` SHALL extend to 17 types (existing 13 + the 4 new)
- **AND** the `PoliticalGraphStore.query_dossier()` BFS SHALL traverse the new edges automatically (no code change required — the existing BFS visits all edges in `self._relationships.values()`)

## Cross-references

- [`../../agents/cianchosaint/tools/political_graph_store.py`](../../agents/cianchosaint/tools/political_graph_store.py) — the canonical store
- [`../../agents/meaisinfhoghlaim/firecrawl_mcp/memory/cognee_store.py`](../../agents/meaisinfhoghlaim/firecrawl_mcp/memory/cognee_store.py) — the upstream Cognee store
- [`../../agents/meaisinfhoghlaim/firecrawl_mcp/memory/graphiti_store.py`](../../agents/meaisinfhoghlaim/firecrawl_mcp/memory/graphiti_store.py) — the upstream Graphiti store
- [`../../openspec/specs/cianchosaint-bipp-v2/spec.md`](../../openspec/specs/cianchosaint-bipp-v2/spec.md) — the BIPP v2 vertical
