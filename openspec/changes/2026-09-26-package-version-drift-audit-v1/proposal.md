# 2026-09-26 — Package version drift audit + saga foundation

> **Change ID:** `2026-09-26-package-version-drift-audit-v1`
> **Author:** Cian Mac an Déisigh Uí Liatháin (Deacy-Lyons)
> **Date:** 2026-09-26
> **Status:** Proposed
> **Spec:** [`package-version-drift`](./specs/package-version-drift/spec.md)
> **Sister change:** none (this is the foundation for the 7-stage saga)
> **Licence:** BUSL-1.1 (per LICENSE.md)

## Why

After the canonical BAML centralised MODEL_REGISTRY change (`cianchosaint-baml-centralised-model-registry-v1`) shipped and the `pangolin-cli/SKILL.md` was refreshed, it became clear that **the opensource packages underpinning the entire cianchosaint + cianfhoghlaim platform have drifted significantly from their latest releases** — and there's no canonical surface that surfaces this drift.

Examples (sourced from the 2026-09-26 Firecrawl MCP research of 80+ packages):

| Package | Pinned | Latest | Drift |
|---|---|---|---|
| `pangolin` (cianfhoghlaim) | `ee-1.21.1` | `1.23.0` (Sep 16, 2026) | 2 minor behind |
| `openchamber` (both repos) | `1.0.0` | `1.22.2` (Sep 5, 2026) | **22 minor behind** |
| `litellm` (both repos) | `v1.97.0` | `v1.102.0` (Sep 19, 2026) | 5 minor behind (LiteLLM rolling-window: "only 4 most recent minor lines supported") |
| `lancedb` (cianchosaint) | `>=0.20.0` | `0.39.0` (Aug 31, 2026) | 19 minor behind |
| `lancedb` (cianfhoghlaim) | `>=0.15` | `0.39.0` | **24 minor behind** |
| `dlt` (cianchosaint) | `>=1.4.0` | `1.30.0` | 26 minor behind |
| `duckdb` (cianfhoghlaim) | `>=1.4,<1.6.0` | `1.5.5` LTS | 1 minor behind (MotherDuck CLI minimum) |
| `google-adk` (cianfhoghlaim) | `>=2.5.0,<3` | `2.10.0` (Sep 10, 2026) | 5 minor behind |
| `garage` (both repos) | `v2.3.0` | `v2.4.1` (Sep 8, 2026) | 1 minor behind |
| `crawl4ai` (both repos) | `v0.9.2` | `v0.9.4` (Sep 23, 2026) | 2 patch behind |

The drift isn't just a numbers problem — it causes **real canonical clashes**:

- **Pangolin 1.23.0 renamed Newt → "Pangolin Site"** — any container using `newt` as the binary name now needs to migrate to the renamed entrypoint.
- **LiteLLM only actively supports 4 most recent stable minor lines** — we are on 1.97.0 and 1.102.0 is the latest; we're at risk of EOL in the next release.
- **Langfuse v4 needs Python SDK ≥4.7.0 for real-time ingestion** — we pin `>=4.0.0` in cianchosaint; data from Python SDK <4.7.0 can be delayed up to 15 minutes.
- **MotherDuck CLI minimum is DuckDB 1.5.5** — cianfhoghlaim caps at `<1.6.0` so this is fine, but cianchosaint pins `>=1.4.0` (the floor is fine; the cap is the concern).

This change ships **Stage 1 (the foundation)** of a 7-stage saga to refactor the entire cianchosaint + cianfhoghlaim package surface to latest, in dependency order, with audit gates.

## What

### The 7-stage saga

| Stage | Scope | Openspec changes | Status |
|---|---|---|---|
| **1** | Foundation audit | `2026-09-26-package-version-drift-audit-v1` (THIS) | NEW (this change) |
| 2a | Pangolin + Newt + Gerbil | `2026-09-26-pangolin-newt-v1.23-upgrade-v1/` | NEXT |
| 2b | Litellm + Langfuse + Komodo + OpenChamber image | 3 changes | pending |
| 2c | Crawl4AI + Garage + Infisical | `2026-09-26-loc-data-storage-stack-upgrade-v1/` | pending |
| 3 | Python BIEP data platform deps | `2026-09-26-biep-data-platform-deps-bump-v1/` | pending |
| 4 | OpenChamber major refactor (1.0 → 1.22) | `2026-09-26-openchamber-v1.22-major-upgrade-v1/` | pending |
| 5 | LanceDB major refactor (Lance v1 → Lance v2 in-place) | `2026-09-26-lancedb-v0.39-lance-v2-upgrade-v1/` | pending |
| 6 | Skill version-header refresh | `2026-09-26-skill-version-header-refresh-v1/` | pending |
| 7 | Continuous version drift monitoring | `2026-09-26-version-drift-monitoring-v1/` | pending |

### The 4 deliverables (Stage 1)

1. **`openspec/changes/2026-09-26-package-version-drift-audit-v1/`** — the proposal + tasks + spec delta bundle (this directory)
2. **`bonneagar/stacks/PACKAGE-VERSIONS.md`** — the canonical version pinning table for all 80+ packages across both repos
3. **`scripts/audit/audit_package_versions.py`** — the runtime audit script (Python) that compares pinned vs latest via PyPI + Docker Hub + GitHub Releases APIs
4. **`.agents/skills/package-version-drift/SKILL.md`** — the canonical skill that documents how to add a new package to the audit + how to bump an existing one

## Impact

### What's new (Stage 1)

- **1 openspec change** (this directory)
- **1 new spec:** `package-version-drift` (the canonical registry spec)
- **1 new doc:** `bonneagar/stacks/PACKAGE-VERSIONS.md`
- **1 new script:** `scripts/audit/audit_package_versions.py`
- **1 new skill:** `.agents/skills/package-version-drift/SKILL.md`

### What's NOT new (Stage 1)

- No code changes (Stage 1 is documentation + tooling only)
- No IaC stack version bumps (Stages 2a-2c)
- No Python dep bumps (Stage 3)
- No OpenChamber refactor (Stage 4)
- No LanceDB migration (Stage 5)
- No skill refresh (Stage 6)
- No monitoring automation (Stage 7)

## Dependencies

- **Blocked by:** none
- **Soft-blocked by:** the existing `cianchosaint-baml-centralised-model-registry-v1` change (which shipped 2026-09-26 and provides the canonical surface that this change extends)
- **Affected repos:** both `cianchosaint` + `cianfhoghlaim`
- **Prerequisite for:** Stages 2-7 of the saga

## Acceptance criteria

1. ✅ `openspec validate 2026-09-26-package-version-drift-audit-v1 --strict` exits 0
2. ✅ `scripts/audit/audit_package_versions.py` runs successfully against the canonical package table
3. ✅ `bonneagar/stacks/PACKAGE-VERSIONS.md` lists every IaC stack Docker image + Python dep across both repos
4. ✅ `.agents/skills/package-version-drift/SKILL.md` documents how to add a new package + how to bump an existing one
5. ✅ `mise run lint:skills` (the existing skill validator) passes — the new skill has a valid `SKILL.md` frontmatter

## Rollback plan

- Delete `openspec/changes/2026-09-26-package-version-drift-audit-v1/` (the openspec change)
- Delete `bonneagar/stacks/PACKAGE-VERSIONS.md`
- Delete `scripts/audit/audit_package_versions.py`
- Delete `.agents/skills/package-version-drift/SKILL.md`
- No data migration; no API changes; no breaking changes
