# 2026-09-26 — Litellm + Langfuse upgrade to latest (Stage 2b.1 of the saga)

> **Change ID:** `2026-09-26-litellm-langfuse-upgrade-v1`
> **Author:** Cian Mac an Déisigh Uí Liatháin (Deacy-Lyons)
> **Date:** 2026-09-26
> **Status:** Proposed
> **Spec:** [`litellm-stack`](./specs/litellm-stack/spec.md) + [`langfuse-stack`](./specs/langfuse-stack/spec.md)
> **Saga stage:** 2b.1 (per `openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md`)
> **Sister changes:** `2026-09-26-komodo-v2-upgrade-v1/` + `2026-09-26-openchamber-image-v1.22-upgrade-v1/` (the other 2 Stage 2b changes)
> **Licence:** BUSL-1.1 (per LICENSE.md)

## Why

Per the `2026-09-26-package-version-drift-audit-v1` audit + the 2026-09-26 Firecrawl research:

1. **Litellm v1.97.0 → v1.102.0** (5 minor versions behind). This is **CRITICAL** because per the official LiteLLM release-support policy: *"LiteLLM will only actively support the four most recent stable minor lines. Everything 1.85.x and earlier has reached end of life."* Our v1.97 is approaching EOL; v1.102 is the current latest. The bump is straightforward (just image tag + Python SDK pin).

2. **Langfuse Docker image**: `langfuse/langfuse:4` and `langfuse/langfuse-worker:4` are on major version 4 but need to track the latest patch. Per the Langfuse v4 release (Aug 17, 2026), the latest is `4.x`.

3. **Langfuse Python SDK**: cianchosaint pins `>=4.0.0` but needs `>=4.7.0` for real-time ingestion (per Langfuse v4 docs: *"data from Python SDK < 4.7.0 [...] can be delayed by up to 15 minutes"*).

This change ships **Stage 2b.1** of the canonical package-version-drift saga — bumping Litellm + Langfuse.

## What

### The 4 deliverables

1. **`bonnegar/stacks/litellm/compose.yaml`** — UPDATE:
   - `litellm-database: image: ghcr.io/berriai/litellm-database:v1.97.0` → `:v1.102.0`

2. **`bonnegar/stacks/langfuse/compose.yaml`** — UPDATE:
   - `langfuse/langfuse-worker:4` → `:4.7.0` (real-time SDK compatible)
   - `langfuse/langfuse:4` → `:4.7.0`

3. **`pyproject.toml`** (cianchosaint) — UPDATE:
   - `langfuse>=4.0.0` → `langfuse>=4.7.0,<5.0`

4. **`.agents/skills/litellm/SKILL.md`** + **`.agents/skills/langfuse/SKILL.md`** (if exists) — UPDATE:
   - Bump version headers to match the new pinned versions
   - Document the LiteLLM rolling-window policy (4 most recent minor lines supported)
   - Document the Langfuse Python SDK ≥4.7.0 requirement

5. **`bonneagar/stacks/PACKAGE-VERSIONS.md`** + **`scripts/audit/audit_package_versions.py`** — UPDATE the litellm + langfuse rows + PACKAGE_TABLE entries.

6. **`openspec/changes/2026-09-26-litellm-langfuse-upgrade-v1/`** — the openspec change (proposal + tasks + 2 spec deltas: `litellm-stack` + `langfuse-stack`).

## Impact

### What's new

- **1 openspec change:** `2026-09-26-litellm-langfuse-upgrade-v1/` (this directory)
- **2 NEW specs:** `litellm-stack` + `langfuse-stack`

### What's changed

- `bonnegar/stacks/litellm/compose.yaml` (1 image tag bump)
- `bonnegar/stacks/langfuse/compose.yaml` (2 image tag bumps)
- `pyproject.toml` (1 dependency bump)
- `.agents/skills/litellm/SKILL.md` (version header + LiteLLM rolling-window note)
- `.agents/skills/langfuse/SKILL.md` (version header + Python SDK ≥4.7.0 note)
- `bonnegar/stacks/PACKAGE-VERSIONS.md` (2 row updates)
- `scripts/audit/audit_package_versions.py` (2 PACKAGE_TABLE entries updated)

### What's NOT changed

- The Litellm proxy config (`bonnegar/stacks/litellm/config/config.yaml`) — the v1.97 → v1.102 bump is backward compatible
- The Langfuse Postgres schema — no migration needed for v4 minor bumps
- The 4-tier provider chain — unchanged

## Dependencies

- **Blocked by:** `2026-09-26-package-version-drift-audit-v1` (Stage 1, SHIPPED 2026-09-26)
- **Soft-blocked by:** none
- **Affected repos:** both `cianchosaint` + `cianfhoghlaim`
- **Prerequisite for:** Stage 2c (Crawl4AI + Garage + Infisical)

## Acceptance criteria

1. ✅ `openspec validate 2026-09-26-litellm-langfuse-upgrade-v1 --strict` exits 0
2. ✅ `python3 scripts/audit/audit_package_versions.py` shows `litellm` + `langfuse` as `aligned` after the bump
3. ✅ `openspec validate --all --strict` exits 0 (no regressions)
4. ✅ The 2 updated skills have updated version headers

## Rollback plan

- Restore `litellm-database: v1.97.0` in `litellm/compose.yaml`
- Restore `langfuse/langfuse:4` + `langfuse-worker:4` in `langfuse/compose.yaml`
- Restore `langfuse>=4.0.0` in `pyproject.toml`
- Revert the 2 skill updates
- Revert the `PACKAGE-VERSIONS.md` row updates

## Cross-references

- [`openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md`](../2026-09-26-package-version-drift-audit-v1/proposal.md) — the saga foundation
- [`bonnegar/stacks/PACKAGE-VERSIONS.md`](../../../../bonneagar/stacks/PACKAGE-VERSIONS.md) — the canonical version table
- [LiteLLM version-support policy](https://docs.litellm.ai/blog/version-support) — "only 4 most recent stable minor lines"
- [Langfuse v4 docs](https://langfuse.com/docs/compatibility) — Python SDK ≥4.7.0 for real-time ingestion
