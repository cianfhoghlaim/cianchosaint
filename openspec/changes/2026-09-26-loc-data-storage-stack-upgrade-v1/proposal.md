# 2026-09-26 — Crawl4AI + Garage + Infisical upgrade (Stage 2c of the saga)

> **Change ID:** `2026-09-26-loc-data-storage-stack-upgrade-v1`
> **Author:** Cian Mac an Déisigh Uí Liatháin (Deacy-Lyons)
> **Date:** 2026-09-26
> **Status:** Proposed
> **Spec:** [`crawl4ai-stack`](./specs/crawl4ai-stack/spec.md) + [`garage-stack`](./specs/garage-stack/spec.md) + [`infisical-stack`](./specs/infisical-stack/spec.md)
> **Saga stage:** 2c (per `openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md`)
> **Sister changes:** `2026-09-26-litellm-langfuse-upgrade-v1/` (Stage 2b.1) + `2026-09-26-komodo-v2-upgrade-v1/` (Stage 2b.2) + `2026-09-26-openchamber-image-v1.22-upgrade-v1/` (Stage 2b.3)
> **Licence:** BUSL-1.1 (per LICENSE.md)

## Why

Per the `2026-09-26-package-version-drift-audit-v1` audit + the 2026-09-26 Firecrawl research:

1. **Crawl4AI v0.9.2 → v0.9.4** (Sep 23, 2026). Per the GitHub README: *"v0.9.4: Security release. v0.9.3: Security release."* — 2 patch bumps, both security releases. Critical.

2. **Garage v2.3.0 → v2.4.1** (Sep 8, 2026). Per the v2.4.0 release notes: *"There are no breaking changes when migrating from Garage v2.3.0."* Plus v2.4.1 is a stable patch (no other changes). The bump is safe.

3. **Infisical v0.161.12 → v0.165.15** (latest). Per the Infisical upgrade guide: *"We release updates approximately once a week, which may include new features, bug fixes, performance enhancements, and critical security patches."* We're 4 minor behind; this is a security concern.

This change ships **Stage 2c** of the canonical package-version-drift saga — the data + storage + secrets stacks (the final Stage 2 sub-stage).

## What

### The 6 deliverables

1. **`bonnegar/stacks/crawl4ai/compose.yaml`** — UPDATE:
   - `${TAG:-v0.9.2}` → `${TAG:-v0.9.4}`

2. **`bonnegar/stacks/lakehouse/compose.yaml`** — UPDATE:
   - `dxflrs/garage:v2.3.0` → `dxflrs/garage:v2.4.1`

3. **`bonnegar/stacks/infisical/compose.yaml`** — UPDATE:
   - `infisical/infisical:v0.161.12` → `infisical/infisical:v0.165.15`

4. **`bonneagar/stacks/PACKAGE-VERSIONS.md`** — UPDATE 3 rows: crawl4ai, garage, infisical.

5. **`scripts/audit/audit_package_versions.py`** — UPDATE 3 PACKAGE_TABLE entries.

6. **`openspec/changes/2026-09-26-loc-data-storage-stack-upgrade-v1/`** — the openspec change (proposal + tasks + 3 spec deltas: `crawl4ai-stack` + `garage-stack` + `infisical-stack`).

## Impact

### What's new

- **1 openspec change:** `2026-09-26-loc-data-storage-stack-upgrade-v1/` (this directory)
- **3 NEW specs:** `crawl4ai-stack` + `garage-stack` + `infisical-stack`

### What's changed

- `bonnegar/stacks/crawl4ai/compose.yaml` (1 image tag bump)
- `bonnegar/stacks/lakehouse/compose.yaml` (1 image tag bump)
- `bonnegar/stacks/infisical/compose.yaml` (1 image tag bump)
- `bonneagar/stacks/PACKAGE-VERSIONS.md` (3 row updates)
- `scripts/audit/audit_package_versions.py` (3 PACKAGE_TABLE entries)

### What's NOT changed

- The Postgres + Redis images (those are unchanged across these bumps)
- The Crawl4AI browser dependency (Playwright bundled in v0.9.4)
- The Garage config schema (v2.4.0 is backward-compatible with v2.3.0)
- The Infisical secrets.env (the URI refs are version-agnostic)

## Dependencies

- **Blocked by:** `2026-09-26-package-version-drift-audit-v1` (Stage 1, SHIPPED)
- **Soft-blocked by:** Stages 2a + 2b.1 + 2b.2 + 2b.3 (all SHIPPED)
- **Affected repos:** both `cianchosaint` + `cianfhoghlaim`
- **Prerequisite for:** Stage 3 (Python BIEP data platform deps bump)

## Acceptance criteria

1. ✅ `openspec validate 2026-09-26-loc-data-storage-stack-upgrade-v1 --strict` exits 0
2. ✅ `python3 scripts/audit/audit_package_versions.py` shows `crawl4ai` + `garage` + `infisical` as `aligned` after the bumps
3. ✅ `openspec validate --all --strict` exits 0 (no regressions)
4. ✅ The Garage + Infisial + Crawl4AI containers come up healthy

## Rollback plan

- Restore the original image tags in the 3 compose files
- No data migration needed (all 3 bumps are backward-compatible per upstream docs)

## Cross-references

- [`openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md`](../2026-09-26-package-version-drift-audit-v1/proposal.md) — the saga foundation
- [`bonnegar/stacks/PACKAGE-VERSIONS.md`](../../../../bonnegar/stacks/PACKAGE-VERSIONS.md) — the canonical version table
- [Garage v2.4.1 release](https://git.deuxfleurs.fr/Deuxfleurs/garage/releases/tag/v2.4.1)
- [Crawl4AI v0.9.4 release](https://github.com/unclecode/crawl4AI/releases/tag/v0.9.4)
- [Infisical releases](https://github.com/Infisical/infisical/releases) — weekly cadence
