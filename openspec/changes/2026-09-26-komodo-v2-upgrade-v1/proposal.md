# 2026-09-26 — Komodo v2 upgrade verification (Stage 2b.2 of the saga)

> **Change ID:** `2026-09-26-komodo-v2-upgrade-v1`
> **Author:** Cian Mac an Déisigh Uí Liatháin (Deacy-Lyons)
> **Date:** 2026-09-26
> **Status:** Proposed
> **Spec:** [`komodo-stack`](./specs/komodo-stack/spec.md)
> **Saga stage:** 2b.2 (per `openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md`)
> **Sister changes:** `2026-09-26-litellm-langfuse-upgrade-v1/` (Stage 2b.1, SHIPPED) + `2026-09-26-openchamber-image-v1.22-upgrade-v1/` (Stage 2b.3, NEXT)
> **Licence:** BUSL-1.1 (per LICENSE.md)

## Why

Per the `2026-09-26-package-version-drift-audit-v1` audit, the Komodo GitOps orchestrator images were reported as "ferretdb:2 (indirect)" / "needs-verification" because:
1. The canonical `komodo-core` image tag was using `KOMODO_IMAGE_TAG:-2` as a default (technically correct but unverified)
2. The Komodo v2.0.0 GA release (March 2026) introduced **PKI authentication for Core↔Periphery** + a database migration from SQLite/PostgreSQL via FerretDB v1 to FerretDB v2

Per the 2026-09-26 Firecrawl research of the v2 upgrade docs + the ProxmoxVE community migration guide:

- **Komodo v1.18.0+ requires FerretDB v2** (SQLite/PostgreSQL via FerretDB v1 are no longer supported)
- **v2 upgrade path is largely backward compatible** per https://komo.do/docs/releases/v2.0.0: *"It is largely backward compatible with Komodo v1 configuration, and users can upgrade from v1 in place by following the steps below."*

This change ships **Stage 2b.2** of the canonical package-version-drift saga — verifying the Komodo v2 upgrade + documenting the FerretDB v2 requirement.

## What

### The 3 deliverables

1. **`bonnegar/stacks/komodo/.env.example`** — VERIFY `KOMODO_IMAGE_TAG=2` is the canonical default (it already is; no change needed beyond documentation)
2. **`bonnegar/stacks/PACKAGE-VERSIONS.md`** — UPDATE:
   - Bump `komodo` row: `ferretdb:2 (indirect)` + `needs-verification` → `komodo-core:2 + komodo-periphery:2-dev` (both repos aligned)
3. **`openspec/changes/2026-09-26-komodo-v2-upgrade-v1/`** — the openspec change (proposal + tasks + spec delta) documenting the v2 verification

### What needs manual attention (NOT in scope)

The following Komodo v2 upgrade steps require **manual action** (per the v2 docs):

1. **Core ↔ Periphery PKI authentication** — the new auth model requires regenerating keys (per the v2 release notes: *"PKI authentication: Core and Periphery now authenticate with auto-generated keys"*)
2. **`init: true`** must be added to both Core + Periphery services (the existing compose.yaml likely has this — verify)
3. **`komodo.execute_terminal` Action fixes** — the v2 upgrade docs note this needs review (likely no changes for our surface; verify)

## Impact

### What's new

- **1 openspec change:** `2026-09-26-komodo-v2-upgrade-v1/` (this directory)
- **1 NEW spec:** `komodo-stack`

### What's changed

- `bonnegar/stacks/PACKAGE-VERSIONS.md` (1 row update)
- `scripts/audit/audit_package_versions.py` (1 PACKAGE_TABLE entry — verify the `komodo-core` + `komodo-periphery` entries)

### What's NOT changed

- The Komodo compose.yaml + periphery.yaml + .env.example (already on `:2` + `:2-dev`)
- The Komodo Periphery + Core container definitions (no manual config change needed beyond verifying `init: true` is set)
- The Komodo secrets.env (no changes needed)

## Dependencies

- **Blocked by:** `2026-09-26-package-version-drift-audit-v1` (Stage 1, SHIPPED 2026-09-26)
- **Soft-blocked by:** `2026-09-26-litellm-langfuse-upgrade-v1/` (Stage 2b.1, SHIPPED)
- **Affected repos:** both `cianchosaint` + `cianfhoghlaim`
- **Prerequisite for:** Stage 2b.3 (OpenChamber image)

## Acceptance criteria

1. ✅ `openspec validate 2026-09-26-komodo-v2-upgrade-v1 --strict` exits 0
2. ✅ `bonnegar/stacks/komodo/.env.example` has `KOMODO_IMAGE_TAG=2`
3. ✅ `bonnegar/stacks/komodo/compose.yaml` has `ghcr.io/moghtech/komodo-core:${KOMODO_IMAGE_TAG:-2}`
4. ✅ `bonnegar/stacks/komodo/periphery.yaml` has `ghcr.io/moghtech/komodo-periphery:${KOMODO_IMAGE_TAG:-2-dev}`
5. ✅ `python3 scripts/audit/audit_package_versions.py` shows `komodo-core` + `komodo-periphery` as `aligned` after the bump

## Rollback plan

- Revert `KOMODO_IMAGE_TAG=2` → `KOMODO_IMAGE_TAG=latest` in `.env.example`
- No code rollback needed (the `:2` images are backward compatible per v2 docs)

## Cross-references

- [`openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md`](../2026-09-26-package-version-drift-audit-v1/proposal.md) — the saga foundation
- [`bonnegar/stacks/PACKAGE-VERSIONS.md`](../../../../bonneagar/stacks/PACKAGE-VERSIONS.md) — the canonical version table
- [Komodo v2.0.0 upgrade docs](https://komo.do/docs/releases/v2.0.0) — the upstream upgrade guide
- [Komodo Migration Guide (FerretDB v1 → v2)](https://github.com/community-scripts/ProxmoxVE/discussions/5689) — the FerretDB v2 migration context
