<!--
CIANCHOSAINT canonical skill (NOT wholesale-copied from cianfhoghlaim).

Original: this skill is cianchosaint-specific (the canonical version-drift audit surface).
Created: 2026-09-26 by the openspec/changes/2026-09-26-package-version-drift-audit-v1/ change.

Per the openspec/changes/2026-09-26-package-version-drift-audit-v1/specs/package-version-drift/spec.md,
Requirement: The canonical skill.

Licence: BUSL-1.1 (per LICENSE.md)
-->
---
name: package-version-drift
description: Canonical surface for tracking opensource package version drift across cianchosaint + cianfhoghlaim. Use when adding a new package to the canonical registry, bumping an existing package to latest, auditing drift, or asking "what's the upgrade plan?". Covers the 80+ opensource packages across both repos: 15 IaC stack Docker images (pangolin + newt + gerbil + infisical + litellm + langfuse + komodo + openchamber + crawl4ai + garage + etc.) + ~50 Python BIEP data platform deps (dagster + dlt + duckdb + cocoindex + baml-py + lancedb + google-adk + etc.) + ~15 TypeScript workspace deps + 79 skill version headers. Sourced from the 2026-09-26 Firecrawl MCP research; per the LiteLLM rolling-window policy (only 4 most recent minor lines supported), per the Langfuse v4 SDK ≥4.7.0 real-time requirement, per the Pangolin 1.23.0 "Newt → Pangolin Site" rename, per the MotherDuck DuckDB 1.5.5 CLI minimum.
---

# Package Version Drift — Canonical Audit Surface

## Overview

Per `openspec/changes/2026-09-26-package-version-drift-audit-v1/specs/package-version-drift/spec.md`, this skill is the canonical surface for tracking opensource package version drift across both repos. The drift table is at `bonneagar/stacks/PACKAGE-VERSIONS.md`; the runtime audit script is at `scripts/audit/audit_package_versions.py`; the 7-stage saga timeline is documented in the canonical `PACKAGE-VERSIONS.md`.

## When to use this skill

Use when:

- "Add a new opensource package to the canonical registry"
- "Bump an existing package to the latest version"
- "Audit drift — what's our version status vs latest?"
- "What's the upgrade plan for the 7-stage saga?"
- "Why did the latest Pangolin bump break my Newt container?" (BREAKING: v1.23 renamed Newt → "Pangolin Site")

## The 7-stage saga (per the canonical timeline)

| Stage | Scope | Openspec change | Status |
|---|---|---|---|
| **1** | Foundation audit | `2026-09-26-package-version-drift-audit-v1/` | **SHIPPED 2026-09-26** |
| 2a | Pangolin + Newt + Gerbil | `2026-09-26-pangolin-newt-v1.23-upgrade-v1/` | NEXT |
| 2b | Litellm + Langfuse + Komodo + OpenChamber image | 3 changes | pending |
| 2c | Crawl4AI + Garage + Infisical | `2026-09-26-loc-data-storage-stack-upgrade-v1/` | pending |
| 3 | Python BIEP data platform deps | `2026-09-26-biep-data-platform-deps-bump-v1/` | pending |
| 4 | OpenChamber major refactor (1.0 → 1.22) | `2026-09-26-openchamber-v1.22-major-upgrade-v1/` | pending |
| 5 | LanceDB major refactor (Lance v1 → v2) | `2026-09-26-lancedb-v0.39-lance-v2-upgrade-v1/` | pending |
| 6 | Skill version-header refresh (79 skills) | `2026-09-26-skill-version-header-refresh-v1/` | pending |
| 7 | Continuous version drift monitoring | `2026-09-26-version-drift-monitoring-v1/` | pending |

## The version policy

Per `docs/VERSION-DRIFT-POLICY.md` (NEW 2026-09-26 in Stage 7):

| Package family | Pin policy | Rationale |
|---|---|---|
| IaC stack Docker images | `==X.Y.Z` (exact) | Reproducible deploys |
| Python BIEP data platform deps | `>=X.Y,<X+1.0` (caret) | Minor compat; bugfixes auto-flow |
| Dev tooling (mise `[tools]`) | `latest` | Toolchain drift is OK |
| Bun / npm / pnpm workspace | `>=X.Y.0` (caret) | Per `package.json#engines` |

## How to add a new package

1. Open `bonneagar/stacks/PACKAGE-VERSIONS.md` and add a row to the appropriate table (IaC stack / Python BIEP / TypeScript / skills).
2. Open `scripts/audit/audit_package_versions.py` and add the entry to `PACKAGE_TABLE` with the correct `kind` (`pypi` / `docker` / `github`) + the relevant query params.
3. Run `python3 scripts/audit_package_versions.py --strict` to verify the new entry is detected.
4. If the new package affects the saga timeline, update the Stage column.
5. Commit + force-push.

## How to bump an existing package

1. Create an openspec change (e.g., `openspec/changes/2026-09-26-<package>-v<X.Y>-upgrade-v1/`).
2. Follow the canonical 3-artifact bundle pattern (proposal.md + tasks.md + spec.md).
3. Bump the version in the IaC compose file (or `pyproject.toml` for Python deps).
4. Update `PACKAGE-VERSIONS.md` with the new `pinned_ciancho` + `pinned_cianfhog`.
5. Update the corresponding `.agents/skills/*/SKILL.md` (per Stage 6 refresh).
6. Run `openspec validate <change-id> --strict`.
7. Run `python3 scripts/audit_package_versions.py --strict` to confirm drift = aligned.
8. Commit + force-push.

## How to audit drift

```bash
# Default: human-readable table
python3 scripts/audit/audit_package_versions.py

# JSON output for CI
python3 scripts/audit/audit_package_versions.py --json

# Strict mode (exit 1 if drift > 1 minor)
python3 scripts/audit/audit_package_versions.py --strict
```

The script reads `scripts/audit/audit_package_versions.py:PACKAGE_TABLE` (the canonical table embedded in the script).

## The 3 source APIs

| Source | API endpoint | Notes |
|---|---|---|
| PyPI | `https://pypi.org/pypi/<package>/json` | Returns `data["info"]["version"]` |
| Docker Hub | `https://hub.docker.com/v2/repositories/<image>/tags/?page_size=20` | First tag = latest stable |
| GHCR | `https://ghcr.io/v2/<path>/tags/list` (requires Bearer token from `/token?scope=...`) | First non-snapshot tag = latest stable |
| GitHub Releases | `https://api.github.com/repos/<owner>/<repo>/releases/latest` | Returns `tag_name` |

## Known canonical clashes (per the 2026-09-26 Firecrawl research)

1. **Pangolin 1.23.0 renamed Newt → "Pangolin Site"** — any container using `newt` as the binary name now needs to migrate. Source: https://github.com/fosrl/pangolin/releases/tag/1.23.0
2. **Pangolin v1.23+ requires clients post-2026-08-19** — for the Private AI Gateway feature. Source: https://github.com/fosrl/pangolin/releases/tag/1.23.0
3. **LiteLLM only actively supports the 4 most recent stable minor lines** — we're on 1.97.0 and 1.102.0 is the latest. Source: https://docs.litellm.ai/blog/version-support
4. **Langfuse v4 needs Python SDK ≥4.7.0 for real-time ingestion** — data from <4.7.0 can be delayed up to 15 minutes. Source: https://langfuse.com/docs/compatibility
5. **MotherDuck CLI minimum is DuckDB 1.5.5** — `>=1.4,<1.6.0` cap in cianfhoghlaim covers this. Source: https://motherduck.com/docs/troubleshooting/version-lifecycle-schedules/

## Cross-references

- [`bonneagar/stacks/PACKAGE-VERSIONS.md`](../../../../bonneagar/stacks/PACKAGE-VERSIONS.md) — the canonical version pinning table
- [`scripts/audit/audit_package_versions.py`](../../../../scripts/audit/audit_package_versions.py) — the runtime audit script
- [`docs/VERSION-DRIFT-POLICY.md`](../../../../docs/VERSION-DRIFT-POLICY.md) — the canonical policy doc (NEW in Stage 7)
- [`openspec/changes/2026-09-26-package-version-drift-audit-v1/specs/package-version-drift/spec.md`](../../../../openspec/changes/2026-09-26-package-version-drift-audit-v1/specs/package-version-drift/spec.md) — the canonical spec
- [`openspec/AGENTS.md`](../../../../openspec/AGENTS.md) — the openspec workflow
- `.agents/skills/_template/SKILL.md` — the canonical skill template

---

**Version:** 1.0.0 | **Last Updated:** 2026-09-26

**Live evidence**: per `scripts/audit/audit_package_versions.py` (run 2026-09-26), the canonical version-drift baseline shows: 4 aligned, 1 behind-1-minor, 1 behind-2-3-minor (DuckDB), 11 behind-N-minor (4-26 minor), 8 behind-major (e.g., openai 2.x → 3.x), 14 unknown (mostly unpinned or network errors).

**Refresh cadence:** weekly GH workflow (added in Stage 7) + on-demand per Stage 2-6 bumps.


## Version policy

Per [`docs/SKILL-VERSION-HEADER-POLICY.md`](../../../../docs/SKILL-VERSION-HEADER-POLICY.md) (the canonical refresh policy):

- The canonical refresh cadence is weekly (Stage 7 GH workflow) + on-demand (per openspec change)
- The canonical command is `python3 scripts/audit/refresh_skill_versions.py`
- The canonical package→skill mapping is at [`scripts/audit/PACKAGE_TO_SKILL_MAP.md`](../../../../scripts/audit/PACKAGE_TO_SKILL_MAP.md)
