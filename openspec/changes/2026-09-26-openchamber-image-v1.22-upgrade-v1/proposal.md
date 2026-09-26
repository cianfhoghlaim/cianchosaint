# 2026-09-26 — OpenChamber image bump 1.0.0 → 1.22.2 (Stage 2b.3 of the saga)

> **Change ID:** `2026-09-26-openchamber-image-v1.22-upgrade-v1`
> **Author:** Cian Mac an Déisigh Uí Liatháin (Deacy-Lyons)
> **Date:** 2026-09-26
> **Status:** Proposed
> **Spec:** [`openchamber-image`](./specs/openchamber-image/spec.md)
> **Saga stage:** 2b.3 (per `openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md`)
> **Sister changes:** `2026-09-26-litellm-langfuse-upgrade-v1/` (Stage 2b.1) + `2026-09-26-komodo-v2-upgrade-v1/` (Stage 2b.2)
> **NOTE:** This is an IMAGE-ONLY bump. Stage 4 will be the full OpenChamber major refactor (skill updates, opencode.json updates, theme/UI breaking changes).
> **Licence:** BUSL-1.1 (per LICENSE.md)

## Why

Per the `2026-09-26-package-version-drift-audit-v1` audit, the OpenChamber container was on `ghcr.io/openchamber/openchamber:1.0.0@sha256:21fda9fc9b0eb7ade140fb763d72779b039ba185be3beafad207a3f88978eae3` — which is **22 minor versions behind** the latest v1.22.2.

This is the biggest single-version gap in the entire package surface (per the audit). Per the 2026-09-26 Firecrawl research (the v1.22.2 release notes + the OpenChamber v1.22 blog post):

- v1.22.2 was released Sep 5, 2026 (the latest stable)
- 22 minor releases of features + bug fixes happened between 1.0.0 and 1.22.2
- **Critical: v1.22.2 requires OpenCode 2.x** (per the v1.22 docs: *"Startup: connecting to an OpenCode 1.x server shows a clear 'update OpenCode to 2.x' screen."*)
- v1.22 ships the new chat features (browser panel, queue retry, status refresh, VS Code comments, etc.)

This change ships **Stage 2b.3** — the image-only OpenChamber bump. Stage 4 (the next saga stage) will be the full OpenChamber major refactor that updates the opencode.json + the openchamber skill + addresses any breaking UI changes.

## What

### The 3 deliverables

1. **`bonnegar/stacks/openchamber/compose.yaml`** — UPDATE:
   - `ghcr.io/openchamber/openchamber:1.0.0@sha256:21fda...` → `:1.22.2` (drop the SHA digest; the v1.22.2 tag is the canonical pin)

2. **`bonneagar/stacks/PACKAGE-VERSIONS.md`** — UPDATE:
   - Bump `openchamber` row: `1.0.0@sha256:21fda...` → `1.22.2`

3. **`scripts/audit/audit_package_versions.py`** — UPDATE the `openchamber` PACKAGE_TABLE entry.

### What is NOT in this change (deferred to Stage 4)

- The `.agents/skills/openchamber/SKILL.md` rewrite (Stage 4)
- The `opencode.json` updates for the new OpenCode 2.x compatibility (Stage 4)
- Any UI breaking changes that need addressing (Stage 4)
- The full v1.22 feature documentation update (Stage 4)

## Impact

### What's new

- **1 openspec change:** `2026-09-26-openchamber-image-v1.22-upgrade-v1/` (this directory)
- **1 NEW spec:** `openchamber-image`

### What's changed

- `bonnegar/stacks/openchamber/compose.yaml` (1 image tag bump)
- `bonneagar/stacks/PACKAGE-VERSIONS.md` (1 row update)
- `scripts/audit/audit_package_versions.py` (1 PACKAGE_TABLE entry)

### What's NOT changed

- The OpenChamber skill (deferred to Stage 4)
- The opencode.json (deferred to Stage 4)
- The OpenChamber UI / theme (deferred to Stage 4)
- The opencode binary version (the user must upgrade to OpenCode 2.x manually before OpenChamber 1.22.2 will work)

## Dependencies

- **Blocked by:** `2026-09-26-package-version-drift-audit-v1` (Stage 1, SHIPPED)
- **Soft-blocked by:** `2026-09-26-litellm-langfuse-upgrade-v1/` (Stage 2b.1) + `2026-09-26-komodo-v2-upgrade-v1/` (Stage 2b.2)
- **Hard prerequisite:** OpenCode 2.x (the operator must upgrade opencode BEFORE pulling the new OpenChamber image — per the v1.22 docs)
- **Affected repos:** both `cianchosaint` + `cianfhoghlaim`
- **Prerequisite for:** Stage 2c (Crawl4AI + Garage + Infisical)

## Acceptance criteria

1. ✅ `openspec validate 2026-09-26-openchamber-image-v1.22-upgrade-v1 --strict` exits 0
2. ✅ `python3 scripts/audit/audit_package_versions.py` shows `openchamber` as `aligned`
3. ✅ `openspec validate --all --strict` exits 0 (no regressions)
4. ✅ The OpenChamber container runs (operator must upgrade OpenCode to 2.x first)

## Rollback plan

- Restore `ghcr.io/openchamber/openchamber:1.0.0@sha256:21fda...` in `compose.yaml`
- The v1.0.0 image continues to work with OpenCode 1.x

## Cross-references

- [`openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md`](../2026-09-26-package-version-drift-audit-v1/proposal.md) — the saga foundation
- [`bonnegar/stacks/PACKAGE-VERSIONS.md`](../../../../bonneagar/stacks/PACKAGE-VERSIONS.md) — the canonical version table
- [OpenChamber v1.22 release blog](https://openchamber.dev/changelog/) — the v1.22 features detail
