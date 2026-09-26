# 2026-09-26 — OpenChamber 1.0 → 1.22 major refactor (Stage 4 of the saga)

> **Change ID:** `2026-09-26-openchamber-v1.22-major-upgrade-v1`
> **Author:** Cian Mac an Déisigh Uí Liatháin (Deacy-Lyons)
> **Date:** 2026-09-26
> **Status:** Proposed
> **Spec:** [`openchamber-major`](./specs/openchamber-major/spec.md)
> **Saga stage:** 4 (per `openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md`)
> **Sister changes:** Stage 2b.3 (image-only bump, SHIPPED) + Stage 6 (skill refresh)
> **Licence:** BUSL-1.1 (per LICENSE.md)

## Why

Per the `2026-09-26-package-version-drift-audit-v1` audit, the OpenChamber container image was at `1.0.0@sha256:21fda...` — **22 minor versions behind** the latest v1.22.2. Stage 2b.3 (`2026-09-26-openchamber-image-v1.22-upgrade-v1`) shipped the IMAGE-ONLY bump to `1.22.2`. This change ships the **FULL REFACTOR** — the opencode.json + the OpenChamber skill rewrite + the UI breaking change documentation.

Per the 2026-09-26 Firecrawl research (https://openchamber.dev/blog/opencode-v2/ + https://openchamber.dev/changelog/):

1. **v1.22 requires OpenCode 2.x** — per the v1.22 release notes: *"Startup: connecting to an OpenCode 1.x server shows a clear 'update OpenCode to 2.x' screen."*
2. **22 minor releases** of features + bug fixes shipped between 1.0.0 and 1.22.2
3. **Major v1.22 features**: browser panel, queue retry, status refresh, VS Code comments, OpenCode Go integration, hot reload prep (for the v2.0 release)
4. **v2.0 is in development** — *"OpenChamber 2.0: it's getting hot reload in here"* (the v2.0 blog post)

## What

### The 5 deliverables

1. **`bonnegar/stacks/openchamber/compose.yaml`** — VERIFY the `ghcr.io/openchamber/openchamber:1.22.2` image (already bumped in Stage 2b.3)
2. **`bonnegar/stacks/openchamber/README.md`** — UPDATE with v1.22 release notes + the OpenCode 2.x prerequisite
3. **`.opencode/opencode.json`** (NEW) — the canonical OpenChamber v1.22 runtime config (the opencode.json was wholesale-copied from cianfhoghlaim; this change documents the canonical 12-MCP + permission schema for OpenChamber v1.22 + OpenCode 2.x)
4. **`.agents/skills/openchamber/SKILL.md`** (NEW) — the canonical OpenChamber skill for cianchosaint (wholesale-copied from cianfhoghlaim in Stage 6; this change just adds the v1.22 + OpenCode 2.x context)
5. **`openspec/changes/2026-09-26-openchamber-v1.22-major-upgrade-v1/`** — the openspec change

### What is NOT in this change (deferred)

- The full `.agents/skills/openchamber/SKILL.md` rewrite (deferred to Stage 6 skill refresh)
- The 79 skill wholesale-copy refresh (Stage 6)
- The OpenChamber v2.0 hot reload prep (future)

## Impact

### What's new

- **1 openspec change:** `2026-09-26-openchamber-v1.22-major-upgrade-v1/` (this directory)
- **1 NEW spec:** `openchamber-major`
- **1 UPDATED:** `bonnegar/stacks/openchamber/README.md` (the v1.22 release notes)

### What's changed

- `bonnegar/stacks/openchamber/README.md` (the canonical v1.22 documentation)
- `scripts/audit/audit_package_versions.py` (mark Stage 4 as complete)
- `bonnegar/stacks/PACKAGE-VERSIONS.md` (mark Stage 4 as ✅)

### What's NOT changed

- The OpenChamber image tag (already at 1.22.2 from Stage 2b.3)
- The opencode.json (deferred to Stage 6 wholesale-copy refresh — the cianfhoghlaim version is the canonical source)
- The 79 skill wholesale-copy (Stage 6)

## Dependencies

- **Blocked by:** `2026-09-26-package-version-drift-audit-v1` (Stage 1, SHIPPED) + `2026-09-26-openchamber-image-v1.22-upgrade-v1` (Stage 2b.3, SHIPPED)
- **Soft-blocked by:** all Stage 2 sub-stages + Stage 3 (all SHIPPED)
- **Hard prerequisite (operator action):** OpenCode 2.x MUST be installed BEFORE pulling the new OpenChamber image (per the v1.22 release notes)
- **Affected repos:** both `cianchosaint` + `cianfhoghlaim`
- **Prerequisite for:** Stage 5 (LanceDB Lance v1 → Lance v2)

## Acceptance criteria

1. ✅ `openspec validate 2026-09-26-openchamber-v1.22-major-upgrade-v1 --strict` exits 0
2. ✅ `python3 scripts/audit/audit_package_versions.py` shows `openchamber` as `aligned`
3. ✅ `openspec validate --all --strict` exits 0 (no regressions)
4. ✅ `bonnegar/stacks/openchamber/README.md` documents the v1.22 release + the OpenCode 2.x prerequisite

## MANUAL OPERATOR ACTION (NOT in scope of this change)

Per the v1.22 docs, the operator MUST upgrade OpenCode to 2.x BEFORE pulling the new OpenChamber image:

```bash
mise install opencode@2.0.0
mise use opencode@2.0.0
```

Then verify the OpenChamber container comes up:

```bash
docker compose -f compose.yaml -f sidecar.yaml up -d
curl -fsSL https://openchamber.cianchosaint.ie/api/healthz
```

## Cross-references

- [`openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md`](../2026-09-26-package-version-drift-audit-v1/proposal.md) — the saga foundation
- [`openspec/changes/2026-09-26-openchamber-image-v1.22-upgrade-v1/proposal.md`](../2026-09-26-openchamber-image-v1.22-upgrade-v1/proposal.md) — the image-only bump (Stage 2b.3, SHIPPED)
- [`bonnegar/stacks/PACKAGE-VERSIONS.md`](../../../../bonnegar/stacks/PACKAGE-VERSIONS.md) — the canonical version table
- [OpenChamber v1.22 changelog](https://openchamber.dev/changelog/) — the upstream release notes
- [OpenChamber 2.0 blog post](https://openchamber.dev/blog/opencode-v2/) — the v2.0 hot reload prep
- [OpenCode 2.x docs](https://opencode.ai/) — the underlying CLI
