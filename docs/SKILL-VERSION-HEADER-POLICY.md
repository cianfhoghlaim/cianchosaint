# Skill Version-Header Refresh Policy

> **For:** Operators refreshing skill version headers across the 79 `.agents/skills/*/SKILL.md` files in cianchosaint + cianfhoghlaim.
> **Created:** 2026-09-26 (per the openspec/changes/2026-09-26-skill-version-header-refresh-v1/ Stage 6 of the package-version-drift saga).
> **Companion to:** `docs/VERSION-DRIFT-POLICY.md` (NEW Stage 7), `scripts/audit/refresh_skill_versions.py`, `scripts/audit/PACKAGE_TO_SKILL_MAP.md`.

## Purpose

Every `.agents/skills/*/SKILL.md` file has a version header near the top of the form:

```
**Version:** X.Y.Z | **Last Updated:** YYYY-MM-DD
```

This header is the canonical signal of which package version the skill documents. Without a refresh policy, the headers drift as upstream packages release new versions (this is exactly what the Stage 1 audit found).

## The refresh cadence

Per the Stage 7 monitoring workflow:

| Trigger | Action |
|---|---|
| Weekly GH workflow run | `python3 scripts/audit/refresh_skill_versions.py` reports any drift |
| Manual after a package bump | Update the version header + add a "Version policy" section |
| When opening a new openspec change | Run the audit script + update affected skills |

## The canonical command

```bash
# 1. Run the audit script — reports which skills are stale
python3 scripts/audit/refresh_skill_versions.py

# 2. For each stale skill, update the version header:
#    OLD: **Version:** 1.0.0 | **Last Updated:** 2026-06-29
#    NEW: **Version:** 1.22.2 | **Last Updated:** 2026-09-26

# 3. Add the "Version policy" section (see template below) just after the version header

# 4. Re-run the audit script — confirm 0 stale
python3 scripts/audit/refresh_skill_versions.py
```

## The version-header template

Every skill's SKILL.md should have the canonical header pattern:

```markdown
<!--
CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.

Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/...).

UPDATED YYYY-MM-DD (per openspec/changes/<relevant-change>/...):
- Bumped from X.Y.Z → A.B.C (the canonical bump rationale)
- Added the Version policy section (this policy)
-->
---
name: <skill-name>
description: <canonical skill description>
when_to_use: "<comma-separated trigger phrases>"
---

# <Skill Name>

**Version:** A.B.C | **Last Updated:** YYYY-MM-DD

## Version policy

Per [`docs/SKILL-VERSION-HEADER-POLICY.md`](../../../../docs/SKILL-VERSION-HEADER-POLICY.md)
(the canonical refresh policy):

- The canonical refresh cadence is weekly (Stage 7 GH workflow) + on-demand
  (per openspec change)
- The canonical command is `python3 scripts/audit/refresh_skill_versions.py`
- The canonical package→skill mapping is at
  [`scripts/audit/PACKAGE_TO_SKILL_MAP.md`](../../../../scripts/audit/PACKAGE_TO_SKILL_MAP.md)
```

## The canonical package→skill mapping

Per `scripts/audit/PACKAGE_TO_SKILL_MAP.md`:

| Package | Affected skill(s) |
|---|---|
| pangolin | pangolin/SKILL.md |
| newt (legacy) + pangolin-cli (v1.23+) | pangolin/SKILL.md (the "Sites in the Pangolin CLI" section) |
| gerbil | pangolin/SKILL.md (the "WireGuard tunnels" section) |
| litellm | litellm/SKILL.md |
| langfuse | langfuse/SKILL.md + agent-observability/SKILL.md |
| komodo | komodo/SKILL.md + stacks-sync/SKILL.md |
| openchamber | opencode/SKILL.md (the "OpenChamber browser UI" section) |
| crawl4ai | crawl4ai/SKILL.md + browser-tools/SKILL.md |
| garage | package-version-drift/SKILL.md (the "Bonneagar" section) |
| infisical | secrets-management/SKILL.md + setup-secrets/SKILL.md |
| dagster | dagster/SKILL.md + dagster-asset-sync/SKILL.md |
| dagster-dlt + dagster-dbt | dlthub/SKILL.md + dlthub-router/SKILL.md + dlt-sync/SKILL.md |
| cocoindex | cocoindex/SKILL.md + notebooks-sync/SKILL.md |
| baml-py | baml/SKILL.md + baml-schema-sync/SKILL.md |
| dlt | dlt/SKILL.md + dlt-sync/SKILL.md + dlthub/SKILL.md |
| duckdb | duckdb/SKILL.md + ducklake/SKILL.md + iceberg-lakekeeper/SKILL.md |
| motherduck | motherduck/SKILL.md + ducklake/SKILL.md |
| lancedb | lancedb/SKILL.md |
| google-adk | google-adk/SKILL.md + agent-fleet-orchestration/SKILL.md |
| cognee | cognee/SKILL.md + agent-memory-systems/SKILL.md |
| mlflow | mlflow/SKILL.md + agent-observability/SKILL.md |
| unsloth | unsloth/SKILL.md |
| graphiti | graphiti/SKILL.md + graphiti-core/SKILL.md + agent-memory-systems/SKILL.md |
| falkordb | falkordb/SKILL.md |
| ducklake | ducklake/SKILL.md |

## Cross-references

- [`docs/VERSION-DRIFT-POLICY.md`](./VERSION-DRIFT-POLICY.md) — the canonical package version policy (sister doc)
- [`scripts/audit/refresh_skill_versions.py`](../../../../scripts/audit/refresh_skill_versions.py) — the canonical audit script
- [`scripts/audit/PACKAGE_TO_SKILL_MAP.md`](../../../../scripts/audit/PACKAGE_TO_SKILL_MAP.md) — the canonical mapping
- [`openspec/changes/2026-09-26-skill-version-header-refresh-v1/`](../openspec/changes/2026-09-26-skill-version-header-refresh-v1/) — the Stage 6 openspec change
