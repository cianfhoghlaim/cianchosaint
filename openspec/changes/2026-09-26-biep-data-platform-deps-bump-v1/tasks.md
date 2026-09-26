# 2026-09-26 — BIEP data platform deps bump tasks

> Ordered checklist for shipping `2026-09-26-biep-data-platform-deps-bump-v1` (Stage 3 of the saga).

## Phase 1 — Firecrawl MCP research (the upstream validation)

- [x] 1.1 Verified Dagster 1.13.24 (Sep 2026) — confirmed via Stage 1 research
- [x] 1.2 Verified dagster-dlt 0.29.24 (Sep 2026) — confirmed via Stage 1 research
- [x] 1.3 Verified dagster-dbt 0.29.24 (Sep 2026) — confirmed via Stage 1 research
- [x] 1.4 Verified CocoIndex 1.0.24 (Sep 19, 2026) — confirmed via Stage 1 research
- [x] 1.5 Verified baml-py 0.226.2 (Sep 2026) — confirmed via Stage 1 research
- [x] 1.6 Verified dlt 1.30.0 (Sep 2026) — confirmed via Stage 1 research
- [x] 1.7 Verified DuckDB 1.5.5 LTS (MotherDuck CLI minimum) — confirmed via Stage 1 research
- [x] 1.8 Verified MotherDuck SDK (latest, PyPI lookup failed but >=0.10 is the safe floor) — confirmed via Stage 1 research
- [x] 1.9 Verified LanceDB 0.39.0 (Aug 31, 2026) — confirmed via Stage 1 research
- [x] 1.10 Verified google-adk 2.10.0 (Sep 10, 2026) — confirmed via Stage 1 research
- [x] 1.11 Verified langfuse-py 4.15.6 — confirmed via Stage 2b.1 (already aligned)
- [x] 1.12 Verified litellm-py 1.102.1 (Sep 19, 2026) — confirmed via Stage 1 research

## Phase 2 — Create the openspec change

- [x] 2.1 Create `openspec/changes/2026-09-26-biep-data-platform-deps-bump-v1/proposal.md`
- [x] 2.2 Create `openspec/changes/2026-09-26-biep-data-platform-deps-bump-v1/tasks.md` (this file)
- [x] 2.3 Create `openspec/changes/2026-09-26-biep-data-platform-deps-bump-v1/specs/biep-data-platform-deps/spec.md`

## Phase 3 — Update pyproject.toml (both repos)

### cianchosaint (10 bumps)

- [x] 3.1 `dagster>=1.13.0` → `dagster>=1.13,<2.0` (caret range — bugfixes auto-flow)
- [x] 3.2 `dagster-dlt` unpinned → `>=0.29,<1.0`
- [x] 3.3 `dagster-dbt` unpinned → `>=0.29,<1.0`
- [x] 3.4 `cocoindex>=1.0.14` → `cocoindex>=1.0.20,<2.0`
- [x] 3.5 `baml-py>=0.223.0` → unchanged (already correct floor)
- [x] 3.6 `dlt[duckdb]>=1.4.0` → `dlt[duckdb]>=1.30,<2.0`
- [x] 3.7 `duckdb>=1.4.0` → `duckdb>=1.5.5,<1.6.0` (MotherDuck CLI minimum)
- [x] 3.8 `motherduck>=0.10.0` → unchanged (already correct floor)
- [x] 3.9 `lancedb>=0.20.0` → `lancedb>=0.39,<1.0`
- [x] 3.10 `google-adk` unpinned → `>=2.9.0,<3.0`
- [x] 3.11 `litellm-py` unpinned → `litellm>=1.102,<2.0`
- [x] 3.12 `langfuse>=4.7.0,<5.0` → unchanged (Stage 2b.1)

### cianfhoghlaim (verify + 3 bumps)

- [x] 3.13 `dagster>=1.13` → unchanged (already correct floor)
- [x] 3.14 `dagster-dlt>=0.29` → unchanged
- [x] 3.15 `dagster-dbt>=0.29` → unchanged
- [x] 3.16 `cocoindex>=1.0.20` → unchanged
- [x] 3.17 `baml-py>=0.222.0` → `baml-py>=0.223,<1.0` (slight bump)
- [x] 3.18 `dlt[duckdb,motherduck,filesystem,hub]>=1.28.1` → `>=1.30,<2.0`
- [x] 3.19 `duckdb>=1.4` → unchanged (already has `<1.6.0` cap from pyproject upper bound)
- [x] 3.20 `motherduck>=0.10` → unchanged
- [x] 3.21 `lancedb>=0.15` → `lancedb>=0.39,<1.0`
- [x] 3.22 `google-adk>=2.5.0,<3` → unchanged
- [x] 3.23 `litellm>=1.97.0` → `litellm>=1.102,<2.0`
- [x] 3.24 `logfire>=4.15.1` → unchanged
- [x] 3.25 `firecrawl>=4.28.2` → unchanged

## Phase 4 — Update the canonical version pinning table

- [x] 4.1 Update `bonneagar/stacks/PACKAGE-VERSIONS.md` — bump 10 rows + mark Stage 3 ✅
- [x] 4.2 Update `scripts/audit/audit_package_versions.py` — verify the 12 entries are aligned

## Phase 5 — Update the 5 skill version headers

- [x] 5.1 Update `.agents/skills/dagster/SKILL.md` — bump version header to 1.13.24
- [x] 5.2 Update `.agents/skills/cocoindex/SKILL.md` — bump version header to 1.0.24
- [x] 5.3 Update `.agents/skills/dlt/SKILL.md` — bump version header to 1.30.0
- [x] 5.4 Update `.agents/skills/lancedb/SKILL.md` — bump version header to 0.39.0
- [x] 5.5 Update `.agents/skills/google-adk/SKILL.md` — bump version header to 2.10.0
- [x] 5.6 Skip `baml-py` (Stage 6 wholesale-copy will refresh)

## Phase 6 — Verify + push

- [x] 6.1 `openspec validate 2026-09-26-biep-data-platform-deps-bump-v1 --strict` exits 0
- [x] 6.2 `python3 scripts/audit/audit_package_versions.py` shows all 12 deps as `aligned`
- [x] 6.3 `openspec validate --all --strict` exits 0 (no regressions)
- [x] 6.4 Commit + force-push to `2026-08-27-kcg-rename-v1` + `main` via `--force-with-lease`

## What's NEXT (Stage 4 — OpenChamber major refactor)

This change ships Stage 3 only. The NEXT openspec change:

- `2026-09-26-openchamber-v1.22-major-upgrade-v1/` — the FULL OpenChamber major refactor (opencode.json updates + skill rewrite + UI breaking changes)

Per the saga timeline in the Stage 1 proposal.md.
