# 2026-09-26 — Litellm + Langfuse upgrade tasks

> Ordered checklist for shipping `2026-09-26-litellm-langfuse-upgrade-v1` (Stage 2b.1 of the saga).

## Phase 1 — Firecrawl MCP research (the upstream validation)

- [x] 1.1 Fetch the Litellm v1.102.0 release notes — confirmed v1.102 is the latest (Sep 19, 2026); "Auto router controls, native OCR, gateway reliability"
- [x] 1.2 Verify Litellm rolling-window policy — "only 4 most recent stable minor lines supported" (per https://docs.litellm.ai/blog/version-support)
- [x] 1.3 Verify Langfuse latest patch — v4.x is the latest major; need latest patch for real-time ingestion
- [x] 1.4 Verify Langfuse Python SDK requirement — ≥4.7.0 for real-time ingestion

## Phase 2 — Create the openspec change

- [x] 2.1 Create `openspec/changes/2026-09-26-litellm-langfuse-upgrade-v1/proposal.md`
- [x] 2.2 Create `openspec/changes/2026-09-26-litellm-langfuse-upgrade-v1/tasks.md` (this file)
- [x] 2.3 Create `openspec/changes/2026-09-26-litellm-langfuse-upgrade-v1/specs/litellm-stack/spec.md`
- [x] 2.4 Create `openspec/changes/2026-09-26-litellm-langfuse-upgrade-v1/specs/langfuse-stack/spec.md`

## Phase 3 — Update the IaC stacks (Litellm + Langfuse)

- [x] 3.1 Update `bonnegar/stacks/litellm/compose.yaml` — `litellm-database: v1.97.0` → `:v1.102.0`
- [x] 3.2 Update `bonnegar/stacks/langfuse/compose.yaml` — `langfuse/langfuse-worker:4` → `:4.7.0`; `langfuse/langfuse:4` → `:4.7.0`

## Phase 4 — Update the Python dependency

- [x] 4.1 Update `pyproject.toml` (cianchosaint) — `langfuse>=4.0.0` → `langfuse>=4.7.0,<5.0`
- [x] 4.2 Note: cianfhoghlaim uses `>=4.15.1` (via logfire pin) which already covers 4.7.0; no change needed

## Phase 5 — Update the 2 skills

- [x] 5.1 Update `.agents/skills/litellm/SKILL.md` — bump version header to `1.102.0` + add LiteLLM rolling-window note
- [x] 5.2 Update `.agents/skills/langfuse/SKILL.md` (if exists in cianchosaint; otherwise skip — Stage 6 wholesale-copies) — bump version header to `4.7.0` + Python SDK ≥4.7.0 requirement

## Phase 6 — Update the canonical version pinning table

- [x] 6.1 Update `bonnegar/stacks/PACKAGE-VERSIONS.md` — bump `litellm` row to `v1.102.0`
- [x] 6.2 Update `bonnegar/stacks/PACKAGE-VERSIONS.md` — bump `langfuse` row to `4.7.0`
- [x] 6.3 Update `bonnegar/stacks/PACKAGE-VERSIONS.md` — bump `langfuse-py` row to `>=4.7.0,<5.0`
- [x] 6.4 Update `scripts/audit/audit_package_versions.py` — bump the 3 entries in PACKAGE_TABLE

## Phase 7 — Verify + push

- [x] 7.1 `openspec validate 2026-09-26-litellm-langfuse-upgrade-v1 --strict` exits 0
- [x] 7.2 `python3 scripts/audit/audit_package_versions.py` shows `litellm` + `langfuse` + `langfuse-py` as `aligned`
- [x] 7.3 `openspec validate --all --strict` exits 0 (no regressions)
- [x] 7.4 Commit + force-push to `2026-08-27-kcg-rename-v1` + `main` via `--force-with-lease`

## What's NEXT (Stage 2b.2 — Komodo v2)

This change ships Stage 2b.1 only. The NEXT openspec change:

- `2026-09-26-komodo-v2-upgrade-v1/` — bumps komodo-core + komodo-periphery to `:2`

Per the saga timeline in the Stage 1 proposal.md.
