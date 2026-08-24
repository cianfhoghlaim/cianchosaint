## ADDED Requirements

### Requirement: The PoliticalGraphStore class

The system SHALL provide a `PoliticalGraphStore` class at `agents/cianchosaint/tools/political_graph_store.py`.

#### Scenario: The graph supports 13 entity types + 13 relationship types

- **WHEN** the operator inspects `PoliticalGraphStore`
- **THEN** the class SHALL define 13 entity types
- **AND** SHALL define 13 relationship types

#### Scenario: The BFS query_dossier method

- **WHEN** the operator invokes `await store.query_dossier(target_entity='richard_tice', cohort='bipp_v2_reform_uk_accountability')`
- **THEN** the method SHALL return a `PoliticalGraphQueryResult`