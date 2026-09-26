# cianchosaint-lancedb-lance-v2 — Capability Spec

> **Spec ID:** `lancedb-lance-v2`
> **Capability umbrella:** `cianchosaint-pipeline`
> **Status:** PROPOSED (post-`2026-09-26-lancedb-v0.39-lance-v2-upgrade-v1` archive)
> **Last updated:** 2026-09-26

## Purpose

Canonical surface for the LanceDB Lance v1 → Lance v2 in-place migration — covering the 24 BIEP companion tables + the canonical `_lifespan.py` + the migration script.

## ADDED Requirements

### Requirement: Lance v2 format on all BIEP companion tables

The system SHALL migrate all 24 BIEP companion tables from Lance v1 → Lance v2 format in a single transaction per table (in-place migration; no parallel-write dual-track).

#### Scenario: All 24 tables are v2 after migration

- **WHEN** the operator runs `python3 scripts/migrate_lance_v1_to_v2.py`
- **THEN** all 24 BIEP companion tables SHALL be in Lance v2 format (`data_storage_version='v2'`)
- **AND** the row count per table SHALL match the pre-migration count (zero data loss)

### Requirement: LanceDB ContextKey uses the v2 API

The system SHALL use the Lance v2 API in the canonical `cocoindex_flows/_shared/_lifespan.py`:

```python
db.create_table(
    name=...,
    data_storage_version='v2',  # the Lance v2 format (added in lancedb 0.10)
    enable_v2_manifest_paths=True,  # the v2 manifest paths optimisation
    ...
)
```

#### Scenario: New BIEP companion tables are created as v2

- **WHEN** a CocoIndex flow creates a new table via the canonical LanceDB ContextKey
- **THEN** the new table SHALL be created with `data_storage_version='v2'`

### Requirement: Migration is atomic per-table

The system SHALL provide a migration script that runs the v1 → v2 migration as a single transaction per table (with rollback on failure).

#### Scenario: Migration rollback on failure

- **WHEN** the migration fails on a table
- **THEN** that table SHALL be rolled back to v1 (the v2 partial write is discarded)
- **AND** the next table in the sequence is NOT attempted (the migration halts)

## MODIFIED Requirements

None.

## REMOVED Requirements

None.

## Cross-references

- `infrastructure-stacks` (the umbrella spec)
- `package-version-drift` (the Stage 1 spec) — this spec implements Stage 5
- [Lance File Format 2.2 blog](https://www.lancedb.com/blog/lance-file-format-2-2-taming-complex-data)
- [LanceDB Python API reference](https://lancedb.github.io/lancedb/python/python/)
- [lancedb v0.10.2 fix issue](https://github.com/lancedb/lancedb/issues/1457)
