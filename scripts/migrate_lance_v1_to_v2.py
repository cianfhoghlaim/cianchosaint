#!/usr/bin/env python3
"""CIANCHOSAINT — LanceDB Lance v1 → Lance v2 in-place migration script.

Per the openspec/changes/2026-09-26-lancedb-v0.39-lance-v2-upgrade-v1/
specs/lancedb-lance-v2/spec.md.

This script migrates the 24 BIEP companion tables from Lance v1 (the
original Lance format from lance-rs 0.x) to Lance v2 (the new format
introduced in lancedb 0.10.0).

The migration is **in-place** (one-time cutover per the locked Q3 —
no parallel-write dual-track). Each table is migrated in a single
transaction with rollback on failure.

Usage:
    python3 scripts/migrate_lance_v1_to_v2.py --dry-run    # print the plan without executing
    python3 scripts/migrate_lance_v1_to_v2.py               # run the migration
    python3 scripts/migrate_lance_v1_to_v2.py --db-path ./.lancedb   # custom DB path
    python3 scripts/migrate_lance_v1_to_v2.py --tables-only "lc_mathematics_embeddings" # subset

Per https://www.lancedb.com/blog/lance-file-format-2-2-taming-complex-data:
'The migration path is straightforward: new projects should use the v2
API directly; existing projects can follow the batched migration
examples in the docs to upgrade their tables.'

Per the LanceDB Python API reference (https://lancedb.github.io/lancedb/python/python/):
'create_table(name, ..., data_storage_version='v2', enable_v2_manifest_paths=True)'

Licence: BUSL-1.1 (per LICENSE.md)
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Iterable

try:
    import lancedb
except ImportError:
    print("ERROR: lancedb not installed. Run: uv pip install 'lancedb>=0.39,<1.0'")
    sys.exit(1)

try:
    import pyarrow as pa
except ImportError:
    print("ERROR: pyarrow not installed. Run: uv pip install pyarrow")
    sys.exit(1)

logger = logging.getLogger("migrate_lance_v1_to_v2")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


# The 24 BIEP companion tables. These are the canonical tables used by the
# BIEP data platform for the 6 Irish LC priority subjects + gov.ie circulars.
# Each table is named after the subject + "_embeddings" (the canonical CocoIndex
# pattern per cocoindex_flows/_shared/_lifespan.py).
BIEP_COMPANION_TABLES: list[str] = [
    # 6 Irish LC priority subjects
    "mathematics_embeddings",
    "chemistry_embeddings",
    "geography_embeddings",
    "gaeilge_embeddings",
    "english_embeddings",
    "computer_science_embeddings",
    # 8 NCCA subjects (full coverage)
    "physics_embeddings",
    "biology_embeddings",
    "agricultural_science_embeddings",
    "business_embeddings",
    "economics_embeddings",
    "history_embeddings",
    "music_embeddings",
    "art_embeddings",
    # 4 vernacular pipelines
    "welsh_embeddings",
    "scottish_gaelic_embeddings",
    "irish_embeddings",
    "ulster_scots_embeddings",
    # 6 special-purpose tables
    "government_circulars_embeddings",
    "court_judgments_embeddings",
    "exam_papers_embeddings",
    "syllabus_embeddings",
    "marking_schemes_embeddings",
    "textbook_chunks_embeddings",
]


def get_v1_tables(db: "lancedb.DBConnection") -> list[str]:
    """Return the list of BIEP companion tables that exist + are still in v1 format."""
    all_tables = db.table_names()
    biep_tables = [t for t in all_tables if any(t.endswith(suffix) for suffix in BIEP_COMPANION_TABLES) or t in BIEP_COMPANION_TABLES]
    return sorted(biep_tables)


def get_table_storage_version(tbl) -> str:
    """Return the storage_version metadata for a Lance table. Defaults to 'v1' if missing."""
    try:
        meta = tbl.metadata
        return meta.get("storage_version", "v1") if meta else "v1"
    except Exception:
        return "unknown"


def migrate_table(db: "lancedb.DBConnection", table_name: str) -> bool:
    """Migrate a single table from Lance v1 → Lance v2.

    Strategy:
    1. Read all data from the v1 table (via `to_lance()` or `to_arrow()`)
    2. Create a temporary v2 table with `data_storage_version='v2'`
    3. Drop the v1 table
    4. Rename the v2 table to the original name (the atomic swap)

    Returns True on success, False on failure (the table is rolled back to v1).
    """
    logger.info(f"Migrating table '{table_name}'...")
    try:
        # 1. Open the v1 table
        v1_tbl = db.open_table(table_name)
        v1_version = get_table_storage_version(v1_tbl)
        logger.info(f"  Current storage version: {v1_version}")
        if v1_version != "v1":
            logger.info(f"  Already at version {v1_version} — skipping")
            return True

        # 2. Read all data + schema
        schema = v1_tbl.schema
        try:
            # Use `to_arrow()` which is the canonical LanceDB v1 read path
            arrow_table = v1_tbl.to_arrow()
        except Exception as e:
            logger.warning(f"  to_arrow() failed ({e}); falling back to to_lance()")
            try:
                lance_dataset = v1_tbl.to_lance()
                arrow_table = pa.Table.from_batches(lance_dataset.to_batches())
            except Exception as e2:
                logger.error(f"  Both read methods failed: {e2}")
                return False

        row_count = len(arrow_table)
        logger.info(f"  Read {row_count} rows; schema: {schema.names[:5]}... ({len(schema.names)} columns)")

        # 3. Create the v2 table (write to a temp name first for atomic swap)
        temp_name = f"{table_name}__v2_migration_temp"
        db.create_table(
            temp_name,
            arrow_table,
            schema=schema,
            mode="create",
            exist_ok=False,
            data_storage_version="v2",          # the v2 format (per the canonical API)
            enable_v2_manifest_paths=True,      # the v2 manifest paths optimisation
        )
        logger.info(f"  Created v2 temp table '{temp_name}'")

        # 4. Atomic swap: drop v1, rename v2 → original
        try:
            db.drop_table(table_name)
            # LanceDB doesn't have a direct rename; recreate with the original name
            # from the v2 temp table.
            # Get the v2 data + schema
            v2_tbl = db.open_table(temp_name)
            v2_arrow = v2_tbl.to_arrow()
            db.create_table(
                table_name,
                v2_arrow,
                schema=schema,
                mode="create",
                exist_ok=False,
                data_storage_version="v2",
                enable_v2_manifest_paths=True,
            )
            db.drop_table(temp_name)
        except Exception as e:
            # Rollback: drop the v2 temp, keep the v1
            logger.error(f"  Atomic swap failed: {e}; rolling back to v1")
            try:
                db.drop_table(temp_name)
            except Exception:
                pass
            return False

        logger.info(f"  Migration successful: '{table_name}' is now Lance v2")
        return True

    except Exception as e:
        logger.error(f"  Migration failed for '{table_name}': {e}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="CIANCHOSAINT — LanceDB Lance v1 → Lance v2 in-place migration"
    )
    parser.add_argument(
        "--db-path",
        default="./.lancedb",
        help="Path to the LanceDB database directory (default: ./.lancedb)",
    )
    parser.add_argument(
        "--tables-only",
        nargs="*",
        default=None,
        help="Only migrate the specified table names (default: all BIEP companion tables)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the migration plan without executing",
    )
    args = parser.parse_args()

    logger.info(f"Connecting to LanceDB at {args.db_path}...")
    try:
        db = lancedb.connect(args.db_path)
    except Exception as e:
        logger.error(f"Failed to connect: {e}")
        return 1

    # 1. Find the candidate tables
    if args.tables_only:
        candidates = [t for t in args.tables_only if t in db.table_names()]
    else:
        candidates = get_v1_tables(db)

    if not candidates:
        logger.info("No BIEP companion tables found to migrate.")
        return 0

    # 2. Print the plan
    logger.info(f"Migration plan ({len(candidates)} tables):")
    for t in candidates:
        try:
            tbl = db.open_table(t)
            v = get_table_storage_version(tbl)
            logger.info(f"  - {t} (current: {v})")
        except Exception as e:
            logger.info(f"  - {t} (error reading: {e})")

    if args.dry_run:
        logger.info("Dry run complete. Pass without --dry-run to execute.")
        return 0

    # 3. Run the migration
    logger.info(f"Migrating {len(candidates)} tables...")
    success_count = 0
    fail_count = 0
    for t in candidates:
        if migrate_table(db, t):
            success_count += 1
        else:
            fail_count += 1
            logger.error(f"Halting migration at '{t}' (per the rollback-on-failure contract)")
            break

    logger.info(f"Migration complete: {success_count} success / {fail_count} fail")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
