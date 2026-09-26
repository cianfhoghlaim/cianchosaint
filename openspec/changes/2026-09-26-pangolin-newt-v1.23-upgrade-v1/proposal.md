# 2026-09-26 — Pangolin + Newt + Gerbil upgrade to v1.23 (Stage 2a of the saga)

> **Change ID:** `2026-09-26-pangolin-newt-v1.23-upgrade-v1`
> **Author:** Cian Mac an Déisigh Uí Liatháin (Deacy-Lyons)
> **Date:** 2026-09-26
> **Status:** Proposed
> **Spec:** [`pangolin-stack`](./specs/pangolin-stack/spec.md)
> **Saga stage:** 2a (per `openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md`)
> **Sister changes:** none (Stages 2b, 2c, 3, 4, 5, 6, 7 are pending)
> **Licence:** BUSL-1.1 (per LICENSE.md)

## Why

Per the `2026-09-26-package-version-drift-audit-v1` audit, cianfhoghlaim's Pangolin is on `ee-1.21.1` and cianchosaint's is on `ee-latest` (effectively 1.23.0). This drift caused 2 minor-version gap, and more importantly, **Pangolin 1.23.0 introduced the "Newt → Pangolin Site" rename + self-service HA/clustering**.

Per the 2026-09-26 Firecrawl research:

- **Pangolin 1.23.0 (Sep 15, 2026)** introduced:
  1. **Self-service high availability and clustering** on Scale + Enterprise tiers
  2. **Newt renamed to Pangolin Site** (the dashboard now calls it that; the CLI is `fosrl/pangolin-cli`)
  3. Sites integrated into the Pangolin CLI (no separate binary needed)
  4. Master list of organizations in server admin panel
  5. Multiple server admin users supported
  6. Resource Launcher side panel improvements

- **Gerbil v1.5.1 (Aug 31, 2026)** is the latest (we're on `latest` which works but unpinned)
- **Newt (legacy) continues to work** — per the v1.23 docs: *"Existing Newt deployments keep working. Leave them as they are, or switch to the CLI when you want to. Newt will continue to be provided in all of its current forms for the foreseeable future."*

This change ships **Stage 2a** of the canonical package-version-drift saga — bumping Pangolin + Gerbil + adding the new Pangolin Site pattern.

## What

### The 6 deliverables

1. **`bonneagar/stacks/pangolin/compose.yaml`** — UPDATE:
   - `pangolin: image: fosrl/pangolin:ee-latest` → `fosrl/pangolin:ee-1.23.0` (exact pin)
   - `gerbil: image: fosrl/gerbil:latest` → `fosrl/gerbil:1.5.1` (exact pin)

2. **`bonneagar/stacks/pangolin-site/`** (NEW directory) — the canonical new site pattern using `fosrl/pangolin-cli` per the v1.23 docs:
   - `compose.yaml` (the new `pangolin-site` container using `fosrl/pangolin-cli:latest`)
   - `secrets.env` (the credentials template)
   - `sidecar.yaml` (Locket secret injection)
   - `README.md` (the migration guide from newt.yaml → pangolin-site.yaml)

3. **`bonneagar/stacks/pangolin/newt.yaml`** — KEEP (backward compat per v1.23 docs)
   - Add a header comment that says: "NEW: use pangolin-site.yaml per Pangolin v1.23; this file is kept for backward compat"

4. **`.agents/skills/pangolin/SKILL.md`** — UPDATE:
   - Bump version header from `1.19.4` (or current) → `1.23.0`
   - Add "What's new in Pangolin 1.23" section
   - Add migration notes for the "Newt → Pangolin Site" rename

5. **`.agents/skills/pangolin-cli/SKILL.md`** — UPDATE:
   - Add "Site installation via the Pangolin CLI" section (the v1.23 new pattern)

6. **`.agents/skills/pangolin-ai-gateway/SKILL.md`** — UPDATE:
   - Note the v1.22+ AI Gateway feature + the v1.23 HA/clustering implications

7. **`bonneagar/stacks/PACKAGE-VERSIONS.md`** — UPDATE:
   - Bump `pangolin` row: `pinned_ciancho = ee-latest` → `ee-1.23.0`, `pinned_cianfhog = ee-1.21.1` → `ee-1.23.0`
   - Bump `gerbil` row: `pinned_ciancho = latest` → `1.5.1`, `pinned_cianfhog = 1.5.0` → `1.5.1`
   - Bump `newt` row: note the v1.23 rename; bump `pinned_cianfhog = latest` → `1.16.x`
   - Move Stage 2a to "complete"

## Impact

### What's new

- **1 new directory:** `bonneagar/stacks/pangolin-site/` (4 files)
- **1 openspec change:** `2026-09-26-pangolin-newt-v1.23-upgrade-v1/` (this directory)

### What's changed

- `bonneagar/stacks/pangolin/compose.yaml` (UPDATE: 2 image tags)
- `bonneagar/stacks/pangolin/newt.yaml` (UPDATE: header comment only)
- `.agents/skills/pangolin/SKILL.md` (UPDATE)
- `.agents/skills/pangolin-cli/SKILL.md` (UPDATE)
- `.agents/skills/pangolin-ai-gateway/SKILL.md` (UPDATE)
- `bonneagar/stacks/PACKAGE-VERSIONS.md` (UPDATE: 3 rows)

### What's NOT changed

- The existing `newt.yaml` (kept for backward compat per v1.23 docs)
- The Pangolin dashboard (no manual UI changes needed)
- The PocketID + TinyAuth SSO flow
- The 89 Docker Compose stacks' private-resource targets (they continue to work)

## Dependencies

- **Blocked by:** `2026-09-26-package-version-drift-audit-v1` (Stage 1, SHIPPED 2026-09-26)
- **Soft-blocked by:** none
- **Affected repos:** both `cianchosaint` + `cianfhoghlaim`
- **Prerequisite for:** Stage 4 (OpenChamber major refactor — needs the v1.23 HA/clustering context)

## Acceptance criteria

1. ✅ `openspec validate 2026-09-26-pangolin-newt-v1.23-upgrade-v1 --strict` exits 0
2. ✅ `python3 scripts/audit/audit_package_versions.py` shows `pangolin` + `gerbil` + `newt` as `aligned` after the bump
3. ✅ `openspec validate --all --strict` exits 0 (no regressions)
4. ✅ The 3 updated skills (`pangolin/SKILL.md` + `pangolin-cli/SKILL.md` + `pangolin-ai-gateway/SKILL.md`) have updated version headers
5. ✅ `PACKAGE-VERSIONS.md` shows Stage 2a as `complete`

## Rollback plan

- Restore `pangolin: image: fosrl/pangolin:ee-latest` in `compose.yaml`
- Restore `gerbil: image: fosrl/gerbil:latest` in `compose.yaml`
- Delete `bonneagar/stacks/pangolin-site/` (the new directory)
- Revert the 3 skill updates
- Revert the `PACKAGE-VERSIONS.md` row updates
- No data migration; no API changes; the v1.23 server is backward-compatible with v1.21.1 clients

## Cross-references

- [`openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md`](../2026-09-26-package-version-drift-audit-v1/proposal.md) — the saga foundation
- [`bonneagar/stacks/PACKAGE-VERSIONS.md`](../../../../bonneagar/stacks/PACKAGE-VERSIONS.md) — the canonical version table
- [Pangolin 1.23 release notes](https://github.com/fosrl/pangolin/releases/tag/1.23.0) — the upstream release
- [Pangolin 1.23 blog post](https://pangolin.net/news/1-23-release) — the v1.23 features detail
