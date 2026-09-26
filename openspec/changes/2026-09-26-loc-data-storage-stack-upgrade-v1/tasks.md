# 2026-09-26 — Crawl4AI + Garage + Infisical upgrade tasks

> Ordered checklist for shipping `2026-09-26-loc-data-storage-stack-upgrade-v1` (Stage 2c of the saga).

## Phase 1 — Firecrawl MCP research (the upstream validation)

- [x] 1.1 Fetch the Crawl4AI v0.9.4 release notes — confirmed v0.9.4 (Sep 23, 2026) is a security release
- [x] 1.2 Verify Garage v2.4.1 release — confirmed v2.4.1 (Sep 8, 2026) is the latest stable; v2.4.0 has NO breaking changes from v2.3.0
- [x] 1.3 Verify Infisical latest — confirmed v0.165.15 is the latest (weekly release cadence)

## Phase 2 — Update the IaC stacks (Crawl4AI + Garage + Infisical)

- [x] 2.1 Update `bonnegar/stacks/crawl4ai/compose.yaml` — `${TAG:-v0.9.2}` → `${TAG:-v0.9.4}`
- [x] 2.2 Update `bonnegar/stacks/lakehouse/compose.yaml` — `dxflrs/garage:v2.3.0` → `dxflrs/garage:v2.4.1`
- [x] 2.3 Update `bonnegar/stacks/infisical/compose.yaml` — `infisical/infisical:v0.161.12` → `infisical/infisical:v0.165.15`

## Phase 3 — Create the openspec change

- [x] 3.1 Create `openspec/changes/2026-09-26-loc-data-storage-stack-upgrade-v1/proposal.md`
- [x] 3.2 Create `openspec/changes/2026-09-26-loc-data-storage-stack-upgrade-v1/tasks.md` (this file)
- [x] 3.3 Create `openspec/changes/2026-09-26-loc-data-storage-stack-upgrade-v1/specs/crawl4ai-stack/spec.md`
- [x] 3.4 Create `openspec/changes/2026-09-26-loc-data-storage-stack-upgrade-v1/specs/garage-stack/spec.md`
- [x] 3.5 Create `openspec/changes/2026-09-26-loc-data-storage-stack-upgrade-v1/specs/infisical-stack/spec.md`

## Phase 4 — Update the canonical version pinning table

- [x] 4.1 Update `bonnegar/stacks/PACKAGE-VERSIONS.md` — bump `crawl4ai` row to `v0.9.4`
- [x] 4.2 Update `bonnegar/stacks/PACKAGE-VERSIONS.md` — bump `garage` row to `v2.4.1`
- [x] 4.3 Update `bonnegar/stacks/PACKAGE-VERSIONS.md` — bump `infisical` row to `v0.165.15`
- [x] 4.4 Update `scripts/audit/audit_package_versions.py` — update the 3 PACKAGE_TABLE entries

## Phase 5 — Verify + push

- [x] 5.1 `openspec validate 2026-09-26-loc-data-storage-stack-upgrade-v1 --strict` exits 0
- [x] 5.2 `python3 scripts/audit/audit_package_versions.py` shows `crawl4ai` + `garage` + `infisical` as `aligned`
- [x] 5.3 `openspec validate --all --strict` exits 0 (no regressions)
- [x] 5.4 Commit + force-push to `2026-08-27-kcg-rename-v1` + `main` via `--force-with-lease`

## What's NEXT (Stage 3 — Python BIEP data platform deps)

This change ships Stage 2c only (the last Stage 2 sub-stage). The NEXT openspec change:

- `2026-09-26-biep-data-platform-deps-bump-v1/` — bumps Dagster + dagster-dlt + dagster-dbt + cocoindex + baml-py + dlt + duckdb + motherduck + lancedb + google-adk + langfuse-py + litellm-py

Per the saga timeline in the Stage 1 proposal.md.
