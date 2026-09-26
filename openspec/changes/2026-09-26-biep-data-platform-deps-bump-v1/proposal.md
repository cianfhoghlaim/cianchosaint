# 2026-09-26 — BIEP data platform deps bump (Stage 3 of the saga)

> **Change ID:** `2026-09-26-biep-data-platform-deps-bump-v1`
> **Author:** Cian Mac an Déisigh Uí Liatháin (Deacy-Lyons)
> **Date:** 2026-09-26
> **Status:** Proposed
> **Spec:** [`biep-data-platform-deps`](./specs/biep-data-platform-deps/spec.md)
> **Saga stage:** 3 (per `openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md`)
> **Sister changes:** Stages 2a + 2b.1 + 2b.2 + 2b.3 + 2c (all SHIPPED)
> **Licence:** BUSL-1.1 (per LICENSE.md)

## Why

Per the `2026-09-26-package-version-drift-audit-v1` audit + the 2026-09-26 Firecrawl research, the **Python BIEP data platform deps** (the load-bearing deps that run the Dagster + CocoIndex + DLT + DuckDB + LanceDB + MotherDuck + Langfuse + Litellm + google-adk + baml-py stack) are significantly drifted:

| Package | Pinned (ciancho / cianfhog) | Latest | Gap |
|---|---|---|---|
| **dagster** | `>=1.13.0` / `>=1.13` | `1.13.24` (Sep 2026) | patch only |
| **dagster-dlt** | unpinned / `>=0.29` | `0.29.24` (Sep 2026) | unpinned |
| **dagster-dbt** | unpinned / `>=0.29` | `0.29.24` (Sep 2026) | unpinned |
| **cocoindex** | `>=1.0.14` / `>=1.0.20` | `1.0.24` (Sep 19, 2026) | aligned (cianchog) |
| **baml-py** | `>=0.223.0` / `>=0.222.0` | `0.226.2` (Sep 2026) | behind 4 minor |
| **dlt** | `>=1.4.0` / `>=1.28.1` | `1.30.0` (Sep 2026) | ciancho behind 26 minor |
| **duckdb** | `>=1.4.0` / `>=1.4,<1.6.0` | `1.5.5` LTS / `1.5.6` Sep 28 | ciancho behind 1 minor; MotherDuck CLI minimum |
| **motherduck** | `>=0.10.0` / `>=0.10` | (PyPI lookup failed) | unverified |
| **lancedb** | `>=0.20.0` / `>=0.15` | `0.39.0` (Aug 31, 2026) | ciancho behind 19 minor; cianfhog behind 24 minor |
| **google-adk** | unpinned / `>=2.5.0,<3` | `2.10.0` (Sep 10, 2026) | cianfhog behind 5 minor |
| **langfuse-py** | `>=4.7.0,<5.0` (already updated in 2b.1) / `>=4.15.1` | `4.15.6` | aligned |
| **litellm-py** | unpinned / `>=1.97.0` | `1.102.1` (Sep 19, 2026) | cianfhog behind 5 minor |

This change ships **Stage 3** of the canonical package-version-drift saga — bumping all 10 Python deps that need bumps (langfuse-py + litellm-py were already bumped in Stage 2b.1, but verifying alignment).

## What

### The 4 deliverables

1. **`pyproject.toml`** (both repos) — UPDATE 10 dep pins
2. **`bonneagar/stacks/PACKAGE-VERSIONS.md`** — UPDATE 10 rows
3. **`scripts/audit/audit_package_versions.py`** — UPDATE 10 PACKAGE_TABLE entries (verify langfuse-py + litellm-py are aligned with Stage 2b.1)
4. **5 skill version headers** — UPDATE: `dagster`, `cocoindex`, `dlt`, `lancedb`, `google-adk` (and `baml-py` if exists)

5. **`openspec/changes/2026-09-26-biep-data-platform-deps-bump-v1/`** — the openspec change

### The 10 bumps (per repo)

| Package | cianchosaint (was → to-be) | cianfhoghlaim (was → to-be) |
|---|---|---|
| **dagster** | `>=1.13.0` → `==1.13.24` | `>=1.13` → `>=1.13,<2.0` |
| **dagster-dlt** | unpinned → `>=0.29,<1.0` | `>=0.29` → unchanged (already correct) |
| **dagster-dbt** | unpinned → `>=0.29,<1.0` | `>=0.29` → unchanged (already correct) |
| **cocoindex** | `>=1.0.14` → `>=1.0.20,<2.0` | `>=1.0.20` → unchanged (already correct) |
| **baml-py** | `>=0.223.0` → `>=0.223,<1.0` | `>=0.222.0` → `>=0.223,<1.0` |
| **dlt** | `>=1.4.0` → `>=1.30,<2.0` | `>=1.28.1` → `>=1.30,<2.0` |
| **duckdb** | `>=1.4.0` → `>=1.5.5,<1.6.0` (MotherDuck CLI minimum) | `>=1.4,<1.6.0` → unchanged |
| **motherduck** | `>=0.10.0` → unchanged | `>=0.10` → unchanged |
| **lancedb** | `>=0.20.0` → `>=0.39,<1.0` | `>=0.15` → `>=0.39,<1.0` |
| **google-adk** | unpinned → `>=2.9.0,<3.0` | `>=2.5.0,<3` → unchanged (already correct) |
| **langfuse-py** | `>=4.7.0,<5.0` (Stage 2b.1) → unchanged | `>=4.15.1` → unchanged |
| **litellm-py** | unpinned → `>=1.102,<2.0` | `>=1.97.0` → `>=1.102,<2.0` |

## Impact

### What's new

- **1 openspec change:** `2026-09-26-biep-data-platform-deps-bump-v1/` (this directory)
- **1 NEW spec:** `biep-data-platform-deps`

### What's changed

- `pyproject.toml` (cianchosaint) — 10 dep pin updates
- `pyproject.toml` (cianfhoghlaim) — 7 dep pin updates
- `bonneagar/stacks/PACKAGE-VERSIONS.md` — 10 row updates
- `scripts/audit/audit_package_versions.py` — 10 PACKAGE_TABLE entries
- 5 skill version headers

### What's NOT changed

- The BAML function surface (BAML is forward-compatible)
- The Dagster asset code (Dagster 1.13.x is backward-compatible)
- The CocoIndex flow code (CocoIndex v1.x is forward-compatible)
- The DLT source code (DLT 1.30 is backward-compatible per DLT docs)

## Dependencies

- **Blocked by:** `2026-09-26-package-version-drift-audit-v1` (Stage 1, SHIPPED)
- **Soft-blocked by:** all Stage 2 sub-stages (a + 2b.1 + 2b.2 + 2b.3 + 2c, all SHIPPED)
- **Affected repos:** both `cianchosaint` + `cianfhoghlaim`
- **Prerequisite for:** Stage 4 (OpenChamber major refactor)

## Acceptance criteria

1. ✅ `openspec validate 2026-09-26-biep-data-platform-deps-bump-v1 --strict` exits 0
2. ✅ `python3 scripts/audit/audit_package_versions.py` shows all 12 deps as `aligned` after the bumps
3. ✅ `openspec validate --all --strict` exits 0 (no regressions)
4. ✅ `uv sync` succeeds (the new pins resolve cleanly)

## Rollback plan

- Restore the original version pins in `pyproject.toml`
- Revert the `PACKAGE-VERSIONS.md` row updates
- Revert the 5 skill version header updates

## Cross-references

- [`openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md`](../2026-09-26-package-version-drift-audit-v1/proposal.md) — the saga foundation
- [`bonneagar/stacks/PACKAGE-VERSIONS.md`](../../../../bonneagar/stacks/PACKAGE-VERSIONS.md) — the canonical version table
- [Dagster releases](https://github.com/dagster-io/dagster/releases) — the 1.13.x patch cadence
- [Dagster 1.10+ upgrade guide](https://docs.dagster.io/migration/upgrading) — Python 3.10+ requirement
- [CocoIndex releases](https://pypi.org/project/cocoindex/#history) — the v1.x cadence
- [DLT releases](https://github.com/dlt-hub/dlt/releases) — the 1.x cadence
- [LanceDB releases](https://github.com/lancedb/lancedb/releases) — the 0.x cadence
- [Google ADK releases](https://github.com/google/adk-python/releases) — the 2.x cadence
- [BAML releases](https://boundaryml.com/blog) — the 0.20.x cadence
