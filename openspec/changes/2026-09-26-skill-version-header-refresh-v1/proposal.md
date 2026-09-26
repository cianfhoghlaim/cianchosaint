# 2026-09-26 — Skill version-header refresh (Stage 6 of the saga)

> **Change ID:** `2026-09-26-skill-version-header-refresh-v1`
> **Author:** Cian Mac an Déisigh Uí Liatháin (Deacy-Lyons)
> **Date:** 2026-09-26
> **Status:** Proposed
> **Spec:** [`skill-refresh`](./specs/skill-refresh/spec.md)
> **Saga stage:** 6 (per `openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md`)
> **Sister changes:** Stages 1-5 (all SHIPPED)
> **Licence:** BUSL-1.1 (per LICENSE.md)

## Why

Per the `2026-09-26-package-version-drift-audit-v1` audit, 79 `.agents/skills/*/SKILL.md` files exist across both repos. Many have **stale version headers** (from the 2025-01 to 2026-08 wholesale-copy migrations from cianfhoghlaim). After Stages 2-5 shipped, the canonical package versions are:

| Package | Stage | New version |
|---|---|---|
| pangolin | 2a | 1.23.0 (was 1.19.4 / 1.21.1) |
| gerbil | 2a | 1.5.1 (was latest) |
| newt | 2a | 1.16.x (was latest) |
| litellm | 2b.1 | 1.102.0 (was 1.97.0) |
| langfuse | 2b.1 | 4.7.0 (was 4) |
| langfuse-py | 2b.1 | >=4.7.0,<5.0 (was >=4.0.0) |
| komodo | 2b.2 | 2 (was ferretdb:2 indirect) |
| openchamber | 2b.3+4 | 1.22.2 (was 1.0.0@sha256:21fda...) |
| crawl4ai | 2c | v0.9.4 (was v0.9.2) |
| garage | 2c | v2.4.1 (was v2.3.0) |
| infisical | 2c | v0.165.15 (was v0.161.12) |
| dagster | 3 | >=1.13,<2.0 (was >=1.13.0) |
| dagster-dlt + dagster-dbt | 3 | >=0.29,<1.0 (was unpinned / >=0.29) |
| cocoindex | 3 | >=1.0.20,<2.0 (was >=1.0.14) |
| baml-py | 3 | >=0.223,<1.0 (was >=0.223.0 / >=0.222.0) |
| dlt | 3 | >=1.30,<2.0 (was >=1.4.0 / >=1.28.1) |
| duckdb | 3 | >=1.5.5,<1.6.0 (was >=1.4.0) |
| motherduck | 3 | >=0.10,<1.0 (was >=0.10.0) |
| lancedb | 3+5 | >=0.39,<1.0 (was >=0.20.0 / >=0.15) |
| google-adk | 3 | >=2.9.0,<3 (was unpinned / >=2.5.0,<3) |

Plus a "Version policy" section needs to be added to each skill documenting when/how to refresh.

## What

### The 5 deliverables

1. **`docs/SKILL-VERSION-HEADER-POLICY.md`** (NEW) — the canonical policy documenting the version-header refresh cadence
2. **`scripts/audit/refresh_skill_versions.py`** (NEW) — a script that scans all skills + reports which are stale
3. **`scripts/audit/PACKAGE_TO_SKILL_MAP.md`** (NEW) — the canonical mapping: which package's version bump affects which skill
4. **The 79 `.agents/skills/*/SKILL.md` files** — bulk-update the version headers (focus on the ones that map to bumped packages)
5. **`openspec/changes/2026-09-26-skill-version-header-refresh-v1/`** — the openspec change

## Impact

### What's new

- **1 openspec change:** `2026-09-26-skill-version-header-refresh-v1/` (this directory)
- **1 NEW spec:** `skill-refresh`
- **1 NEW doc:** `docs/SKILL-VERSION-HEADER-POLICY.md`
- **1 NEW script:** `scripts/audit/refresh_skill_versions.py`
- **1 NEW map:** `scripts/audit/PACKAGE_TO_SKILL_MAP.md`
- **79 UPDATED:** the SKILL.md version headers

### What's changed

- `.agents/skills/{pangolin,gerbil,newt,litellm,langfuse,komodo,openchamber,crawl4ai,garage,infisical,dagster,cocoindex,baml,dlt,duckdb,motherduck,lancedb,google-adk,cognee,mlflow,unsloth,graphiti,falkordb,dlthub,dlt-sync,dlthub-router,browser-tools,firecrawl,firecrawl-cli,package-version-drift,dagster-asset-sync,knowledge-sync-loop,stacks-sync,agents-sync,notebooks-sync,baml-schema-sync,setup-secrets,secrets-management,mise,improve-skills,opencode,openspec,centralized-registry,cocoindex,apple-photos-ingestion,marimo,memorygraph,motherduck,etc.}/SKILL.md`

### What's NOT changed

- The wholesale-copy migration banners (those are correct — they're from cianfhoghlaim)
- The functional content of each skill

## Dependencies

- **Blocked by:** Stages 1-5 (all SHIPPED)
- **Affected repos:** both `cianchosaint` + `cianfhoghlaim`
- **Prerequisite for:** Stage 7 (continuous version drift monitoring — the monitoring workflow needs the version-header refresh policy)

## Acceptance criteria

1. ✅ `openspec validate 2026-09-26-skill-version-header-refresh-v1 --strict` exits 0
2. ✅ All 79 skills have updated version headers + the "Version policy" section
3. ✅ `python3 scripts/audit/refresh_skill_versions.py` reports 0 stale skills (post-refresh)
4. ✅ `openspec validate --all --strict` exits 0 (no regressions)

## Cross-references

- [`openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md`](../2026-09-26-package-version-drift-audit-v1/proposal.md) — the saga foundation
- [`bonnegar/stacks/PACKAGE-VERSIONS.md`](../../../../bonnegar/stacks/PACKAGE-VERSIONS.md) — the canonical version table
- [`.agents/skills/_template/SKILL.md`](../../../../.agents/skills/_template/SKILL.md) — the canonical skill template
- [`.agents/skills/litellm/SKILL.md`](../../../../.agents/skills/litellm/SKILL.md) — the model for a well-versioned skill (already updated in Stage 2b.1)
