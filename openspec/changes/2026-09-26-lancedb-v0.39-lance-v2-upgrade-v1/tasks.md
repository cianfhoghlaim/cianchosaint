# 2026-09-26 — LanceDB Lance v1 → Lance v2 in-place migration tasks

> Ordered checklist for shipping `2026-09-26-lancedb-v0.39-lance-v2-upgrade-v1` (Stage 5 of the saga).

## Phase 1 — Firecrawl MCP research (the upstream validation)

- [x] 1.1 Fetch the Lance File Format 2.2 blog — confirmed "The migration path is straightforward: new projects should use the v2 API directly; existing projects can follow the batched migration examples"
- [x] 1.2 Fetch the LanceDB Python API reference — confirmed `create_table` accepts `data_storage_version='v2'` + `enable_v2_manifest_paths=True`
- [x] 1.3 Verify lancedb 0.10.2 introduced the v2 format fix (per the GitHub issue)
- [x] 1.4 Confirm lancedb 0.39.0 (our pinned version from Stage 3) supports Lance v2

## Phase 2 — Create the migration script

- [x] 2.1 Create `scripts/migrate_lance_v1_to_v2.py` (the canonical in-place migration script)
  - Iterates over the 24 BIEP companion tables
  - For each table: reads v1 data → creates v2 table → atomic swap
  - Single transaction per table; rollback on failure
  - Langfuse logging for the audit trail
  - `--dry-run` mode prints the plan without executing

## Phase 3 — Update the canonical LanceDB ContextKey

- [x] 3.1 Update `cocoindex_flows/_shared/_lifespan.py` — add `data_storage_version='v2'` parameter to the `create_table` call (the canonical LanceDB ContextKey)

## Phase 4 — Update the lancedb skill

- [x] 4.1 Update `.agents/skills/lancedb/SKILL.md` — bump version header (already done in Stage 3 to >=0.39)
- [x] 4.2 Add "Lance v2 format migration" section to the lancedb skill

## Phase 5 — Create the openspec change

- [x] 5.1 Create `openspec/changes/2026-09-26-lancedb-v0.39-lance-v2-upgrade-v1/proposal.md`
- [x] 5.2 Create `openspec/changes/2026-09-26-lancedb-v0.39-lance-v2-upgrade-v1/tasks.md` (this file)
- [x] 5.3 Create `openspec/changes/2026-09-26-lancedb-v0.39-lance-v2-upgrade-v1/specs/lancedb-lance-v2/spec.md`

## Phase 6 — Update the canonical version pinning table

- [x] 6.1 Update `bonnegar/stacks/PACKAGE-VERSIONS.md` — bump lancedb row to "v0.39.0 (Lance v2 format migration Stage 5 complete)"
- [x] 6.2 Update `scripts/audit/audit_package_versions.py` — verify the lancedb PACKAGE_TABLE entry

## Phase 7 — Verify + push

- [x] 7.1 `openspec validate 2026-09-26-lancedb-v0.39-lance-v2-upgrade-v1 --strict` exits 0
- [x] 7.2 `python3 scripts/migrate_lance_v1_to_v2.py --dry-run` prints the plan without error
- [x] 7.3 `openspec validate --all --strict` exits 0 (no regressions)
- [x] 7.4 Commit + force-push to `2026-08-27-kcg-rename-v1` + `main` via `--force-with-lease`

## MANUAL OPERATOR ACTION (REQUIRED)

The in-place migration script MUST be run by the operator AFTER the lancedb >=0.39 bump (Stage 3 already shipped this) and AFTER the OpenChamber major refactor (Stage 4 already shipped this):

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

## What's NEXT (Stage 6 — Skill version-header refresh)

This change ships Stage 5 only. The NEXT openspec change:

- `2026-09-26-skill-version-header-refresh-v1/` — bulk refreshes the version headers in all 79 `.agents/skills/*/SKILL.md` files to match the bumped package versions from Stages 1-5

Per the saga timeline in the Stage 1 proposal.md.
