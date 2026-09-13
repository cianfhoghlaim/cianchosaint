## ADDED Requirements

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
