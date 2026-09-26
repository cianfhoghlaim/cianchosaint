# cianchosaint-cocoindex-shared-lifespan Capability

## Purpose

`cianchosaint-cocoindex-shared-lifespan` consolidates the CocoIndex v1 Apps' shared lifespan into one canonical module. Mirrors cianfhoghlaim's `cocoindex_flows/_shared/_lifespan.py`:

- 3 shared `ContextKey`s: `LANCE_DB` (LanceDB async connection), `EMBEDDER` (sentence-transformer), `RESOLVED_FILE_REGISTRY` (file registry)
- The `shared_lifespan` async context manager
- The `make_coanco_app()` factory helper

## Background

Cianfhoghlaim's `cocoindex_flows/_shared/_lifespan.py` consolidates 14 CocoIndex v1 Apps' lifespan into one shared module. Every app reuses the same `LANCE_DB` connection + `EMBEDDER` instance + `RESOLVED_FILE_REGISTRY`. The `R1-R4 conformance gate` enforces this:

- R1: `from .._shared._lifespan import shared_lifespan` (this module)
- R2: imports the canonical `ContextKey`s
- R3: `App = coco.App(coco.AppConfig(name=...))` at module scope
- R4: ≥1 `@coco.fn` decorator AND uses `lancedb.mount_table_target(LANCE_DB, ...)`

Cianchosaint has CocoIndex flows at `cocoindex_flows/cianchosaint/` (`source_policy_aggregator.py`, `vlm_pipeline_aggregator.py`, plus the upcoming `politician_dossier_aggregator.py` from BIPP v2). Each one is hand-rolled — none of them share a lifespan.

This change lands the canonical `shared_lifespan.py` so every CocoIndex v1 App in cianchosaint can use one module-load connection + one embedder instance.

## ADDED Requirements

### Requirement: The shared lifespan module

The system SHALL provide a module at `cocoindex_flows/cianchosaint/_shared/_lifespan.py` with:

1. 3 shared `ContextKey`s: `LANCE_DB`, `EMBEDDER`, `RESOLVED_FILE_REGISTRY`
2. The `shared_lifespan` async context manager
3. The lazy connection establishment (so import-time failures don't break the lifespan)

#### Scenario: The lifespan module is importable

- **WHEN** the operator imports `from cocoindex_flows.cianchosaint._shared._lifespan import shared_lifespan, LANCE_DB, EMBEDDER, RESOLVED_FILE_REGISTRY`
- **THEN** the imports SHALL succeed
- **AND** the 3 `ContextKey`s SHALL be the canonical cianfhoghlaim-style keys

#### Scenario: The lifespan establishes the LanceDB connection lazily

- **WHEN** the operator enters `async with shared_lifespan():` for the first time
- **THEN** the lifespan SHALL establish the LanceDB async connection
- **AND** the embedder SHALL be initialized lazily on first use

### Requirement: The CocoIndex App factory helper

The system SHALL provide a `make_coanco_app()` helper at `cocoindex_flows/cianchosaint/_shared/_factory.py` that wraps the canonical lifespan setup.

#### Scenario: Every CocoIndex App uses the factory

- **WHEN** the operator imports `from cocoindex_flows.cianchosaint._shared._factory import make_coanco_app`
- **THEN** calling `make_coanco_app(name="MyApp")` SHALL return an `App` instance configured with the canonical lifespan

#### Scenario: The factory wires the R1-R4 conformance markers

- **WHEN** the operator calls `make_coanco_app(name="MyApp")`
- **THEN** the returned App SHALL import `shared_lifespan` (R1)
- **AND** SHALL register the canonical `ContextKey`s (R2)
- **AND** SHALL mount tables via `lancedb.mount_table_target(LANCE_DB, ...)` (R4)

### Requirement: The 2 existing CocoIndex flows use the shared lifespan

The system SHALL refactor `source_policy_aggregator.py` + `vlm_pipeline_aggregator.py` to use the shared lifespan + factory.

#### Scenario: Both existing flows use the shared lifespan

- **WHEN** the operator imports either `source_policy_aggregator` or `vlm_pipeline_aggregator`
- **THEN** the module SHALL import `shared_lifespan` from `.._shared._lifespan`
- **AND** SHALL use the canonical `LANCE_DB` + `EMBEDDER` ContextKeys (not local copies)

### Requirement: The politician dossier aggregator (new)

The system SHALL provide a new `politician_dossier_aggregator.py` that uses the shared lifespan + the new BAML politician extraction (per `cianchosaint-politician-schema-v1`).

#### Scenario: The new flow mounts a LanceDB table

- **WHEN** the operator runs `politician_dossier_aggregator`
- **THEN** the flow SHALL create a new LanceDB table for the dossier corpus
- **AND** SHALL use the shared `EMBEDDER` ContextKey for embeddings

### Requirement: The shared lifespan survives process death

The system SHALL ensure the LanceDB connection + embedder are reusable across multiple CocoIndex App instantiations within the same process.

#### Scenario: Multiple flows share the same connection

- **WHEN** the operator imports both `source_policy_aggregator` and `vlm_pipeline_aggregator` in the same process
- **THEN** both flows SHALL use the same LanceDB connection (no double-connect)
- **AND** both flows SHALL use the same embedder instance (no double-load)

## Cross-references

- [`../../cocoindex_flows/cianchosaint/_shared/_lifespan.py`](../../cocoindex_flows/cianchosaint/_shared/_lifespan.py) — the canonical lifespan
- [`../../cocoindex_flows/cianchosaint/_shared/_factory.py`](../../cocoindex_flows/cianchosaint/_shared/_factory.py) — the canonical factory
- [`../../cocoindex_flows/cianchosaint/source_policy_aggregator.py`](../../cocoindex_flows/cianchosaint/source_policy_aggregator.py) — the first consumer
- [`../../cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py`](../../cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py) — the second consumer
- [`../../cocoindex_flows/cianchosaint/politician_dossier_aggregator.py`](../../cocoindex_flows/cianchosaint/politician_dossier_aggregator.py) — the new BIPP v2 flow
- cianfhoghlaim `cocoindex_flows/_shared/_lifespan.py` — upstream reference
- cianfhoghlaim `docs/google_examples/adk2-tutorial/shared/scenarios.py` — the schema pattern
