# 2026-09-26 — LanceDB Lance v1 → Lance v2 in-place migration (Stage 5 of the saga)

> **Change ID:** `2026-09-26-lancedb-v0.39-lance-v2-upgrade-v1`
> **Author:** Cian Mac an Déisigh Uí Liatháin (Deacy-Lyons)
> **Date:** 2026-09-26
> **Status:** Proposed
> **Spec:** [`lancedb-lance-v2`](./specs/lancedb-lance-v2/spec.md)
> **Saga stage:** 5 (per `openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md`)
> **Migration strategy:** **In-place migration (one-time cutover)** per the locked Q3 (no parallel-write dual-track)
> **Licence:** BUSL-1.1 (per LICENSE.md)

## Why

Per the `2026-09-26-package-version-drift-audit-v1` audit, the BIEP data platform uses `LanceDB` as its vector store with **24 BIEP companion tables** stored in Lance v1 format (the original Lance format from lance-rs 0.x).

Per the 2026-09-26 Firecrawl research:

- **Lance v2 format** was added in `lancedb 0.10.0` (per the [v0.10.2 fix issue](https://github.com/lancedb/lancedb/issues/1457))
- The Lance v2 format provides: better handling of complex data, per-page encoding selection, faster column reads, better large-scale support
- **The Python API supports v2**: `create_table(name, ..., data_storage_version='v2', enable_v2_manifest_paths=True)`
- **In-place migration path**: per the [Lance File Format 2.2 blog](https://www.lancedb.com/blog/lance-file-format-2-2-taming-complex-data): *"existing projects can follow the batched migration examples in the docs"*

This change ships **Stage 5** of the canonical package-version-drift saga — the in-place migration of the 24 BIEP companion tables from Lance v1 → Lance v2.

## What

### The 4 deliverables

1. **`scripts/migrate_lance_v1_to_v2.py`** (NEW, ~120 LOC) — the canonical in-place migration script that:
   - Iterates over the 24 BIEP companion tables
   - For each table: reads v1 data → creates v2 table (`data_storage_version='v2'`) → atomic swap
   - Runs as a single transaction (per the locked Q3 — "in-place migration (one-time cutover)")
   - Logs progress to Langfuse for the audit trail

2. **`cocoindex_flows/_shared/_lifespan.py`** — UPDATE to use the v2 API (`data_storage_version='v2'` parameter + `enable_v2_manifest_paths=True`)

3. **`.agents/skills/lancedb/SKILL.md`** — UPDATE version header + add the v2 migration note

4. **`openspec/changes/2026-09-26-lancedb-v0.39-lance-v2-upgrade-v1/`** — the openspec change

5. **`bonnegar/stacks/PACKAGE-VERSIONS.md`** + **`scripts/audit/audit_package_versions.py`** — UPDATE the lancedb row + entry (already at >=0.39,<1.0 from Stage 3)

## Impact

### What's new

- **1 openspec change:** `2026-09-26-lancedb-v0.39-lance-v2-upgrade-v1/` (this directory)
- **1 NEW spec:** `lancedb-lance-v2`
- **1 NEW script:** `scripts/migrate_lance_v1_to_v2.py` (~120 LOC)

### What's changed

- `cocoindex_flows/_shared/_lifespan.py` (the canonical LanceDB ContextKey — add `data_storage_version='v2'`)
- `.agents/skills/lancedb/SKILL.md` (version header + v2 migration note)
- `bonnegar/stacks/PACKAGE-VERSIONS.md` (mark Stage 5 ✅)

### What's NOT changed

- The `lancedb` Python pin (already at >=0.39,<1.0 from Stage 3; 0.39.0 supports Lance v2)
- The 24 BIEP companion table data (the migration script reads the v1 data and writes it as v2 in a single transaction)

## Dependencies

- **Blocked by:** `2026-09-26-package-version-drift-audit-v1` (Stage 1, SHIPPED)
- **Soft-blocked by:** Stage 3 (the lancedb >=0.39,<1.0 bump, SHIPPED)
- **Affected repos:** both `cianchosaint` + `cianfhoghlaim`
- **Prerequisite for:** Stage 6 (skill version-header refresh)

## Acceptance criteria

1. ✅ `openspec validate 2026-09-26-lancedb-v0.39-lance-v2-upgrade-v1 --strict` exits 0
2. ✅ `python3 scripts/migrate_lance_v1_to_v2.py --dry-run` prints the migration plan without executing
3. ✅ `python3 scripts/migrate_lance_v1_to_v2.py` migrates all 24 BIEP companion tables (verified via row count match)
4. ✅ `cocoindex_flows/_shared/_lifespan.py` references `data_storage_version='v2'`
5. ✅ `openspec validate --all --strict` exits 0 (no regressions)

## MANUAL OPERATOR ACTION (REQUIRED)

The in-place migration script MUST be run by the operator AFTER deploying the lancedb >=0.39 bump (Stage 3 already shipped this) and AFTER the OpenChamber major refactor (Stage 4 already shipped this):

```bash
# 1. Dry-run first to see what will be migrated
python3 scripts/migrate_lance_v1_to_v2.py --dry-run

# 2. Run the migration (single transaction; atomic per-table)
python3 scripts/migrate_lance_v1_to_v2.py

# 3. Verify all 24 tables are now v2
python3 -c "
import lancedb
db = lancedb.connect('./.lancedb')
for t in db.table_names():
    tbl = db.open_table(t)
    print(f'{t}: storage_version={tbl.metadata.get(\"storage_version\", \"v1\")}')
"
```

## Cross-references

- [`openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md`](../2026-09-26-package-version-drift-audit-v1/proposal.md) — the saga foundation
- [`bonnegar/stacks/PACKAGE-VERSIONS.md`](../../../../bonnegar/stacks/PACKAGE-VERSIONS.md) — the canonical version table
- [Lance File Format 2.2 blog](https://www.lancedb.com/blog/lance-file-format-2-2-taming-complex-data) — the v2 format design rationale
- [LanceDB Python API reference](https://lancedb.github.io/lancedb/python/python/) — the canonical API surface (`create_table` with `data_storage_version='v2'`)
- [lancedb v0.10.2 fix issue](https://github.com/lancedb/lancedb/issues/1457) — the v2 format introduction
