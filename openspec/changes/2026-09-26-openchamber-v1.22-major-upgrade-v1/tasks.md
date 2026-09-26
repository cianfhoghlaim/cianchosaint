# 2026-09-26 — OpenChamber 1.0 → 1.22 major refactor tasks

> Ordered checklist for shipping `2026-09-26-openchamber-v1.22-major-upgrade-v1` (Stage 4 of the saga).

## Phase 1 — Firecrawl MCP research (the upstream validation)

- [x] 1.1 Fetch the OpenChamber v1.22 changelog — confirmed v1.22 features (browser panel, queue retry, status refresh, VS Code comments, OpenCode Go integration)
- [x] 1.2 Verify the OpenCode 2.x prerequisite — confirmed: "Startup: connecting to an OpenCode 1.x server shows a clear 'update OpenCode to 2.x' screen"
- [x] 1.3 Fetch the OpenChamber 2.0 blog post — confirmed v2.0 is in development (hot reload prep)

## Phase 2 — Verify the canonical OpenChamber v1.22 state

- [x] 2.1 Verify `bonnegar/stacks/openchamber/compose.yaml` has `ghcr.io/openchamber/openchamber:1.22.2` (already bumped in Stage 2b.3) — VERIFIED
- [x] 2.2 Verify `python3 scripts/audit/audit_package_versions.py` shows `openchamber` as `aligned` — VERIFIED

## Phase 3 — Update the canonical OpenChamber README

- [x] 3.1 Update `bonnegar/stacks/openchamber/README.md` — document the v1.22 release + the OpenCode 2.x prerequisite
- [x] 3.2 Update `bonnegar/stacks/openchamber/README.md` — add the "What's new in OpenChamber 1.22" section
- [x] 3.3 Update `bonnegar/stacks/openchamber/README.md` — document the OpenChamber 2.0 hot reload prep (the roadmap)

## Phase 4 — Create the openspec change

- [x] 4.1 Create `openspec/changes/2026-09-26-openchamber-v1.22-major-upgrade-v1/proposal.md`
- [x] 4.2 Create `openspec/changes/2026-09-26-openchamber-v1.22-major-upgrade-v1/tasks.md` (this file)
- [x] 4.3 Create `openspec/changes/2026-09-26-openchamber-v1.22-major-upgrade-v1/specs/openchamber-major/spec.md`

## Phase 5 — Update the canonical version pinning table

- [x] 5.1 Update `bonnegar/stacks/PACKAGE-VERSIONS.md` — mark Stage 4 as ✅ SHIPPED 2026-09-26
- [x] 5.2 Update `scripts/audit/audit_package_versions.py` — verify the `openchamber` PACKAGE_TABLE entry is aligned

## Phase 6 — Verify + push

- [x] 6.1 `openspec validate 2026-09-26-openchamber-v1.22-major-upgrade-v1 --strict` exits 0
- [x] 6.2 `python3 scripts/audit/audit_package_versions.py` shows `openchamber` as `aligned`
- [x] 6.3 `openspec validate --all --strict` exits 0 (no regressions)
- [x] 6.4 Commit + force-push to `2026-08-27-kcg-rename-v1` + `main` via `--force-with-lease`

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

## What's NEXT (Stage 5 — LanceDB Lance v1 → Lance v2 in-place migration)

This change ships Stage 4 only. The NEXT openspec change:

- `2026-09-26-lancedb-v0.39-lance-v2-upgrade-v1/` — migrates the 24 BIEP companion tables from Lance v1 to Lance v2 (in-place, one-time cutover)

Per the saga timeline in the Stage 1 proposal.md.
