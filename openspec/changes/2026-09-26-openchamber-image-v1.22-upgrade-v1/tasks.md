# 2026-09-26 — OpenChamber image bump tasks

> Ordered checklist for shipping `2026-09-26-openchamber-image-v1.22-upgrade-v1` (Stage 2b.3 of the saga).

## Phase 1 — Firecrawl MCP research (the upstream validation)

- [x] 1.1 Fetch the OpenChamber v1.22.2 changelog — confirmed v1.22.2 is the latest (Sep 5, 2026)
- [x] 1.2 Verify the OpenCode 2.x requirement — confirmed: "Startup: connecting to an OpenCode 1.x server shows a clear 'update OpenCode to 2.x' screen"
- [x] 1.3 Verify the 22-minor-version gap — confirmed v1.0.0 → v1.22.2 spans 22 minor versions

## Phase 2 — Update the IaC stack (OpenChamber image)

- [x] 2.1 Update `bonnegar/stacks/openchamber/compose.yaml` — drop the SHA digest, bump to `:1.22.2`

## Phase 3 — Create the openspec change

- [x] 3.1 Create `openspec/changes/2026-09-26-openchamber-image-v1.22-upgrade-v1/proposal.md`
- [x] 3.2 Create `openspec/changes/2026-09-26-openchamber-image-v1.22-upgrade-v1/tasks.md` (this file)
- [x] 3.3 Create `openspec/changes/2026-09-26-openchamber-image-v1.22-upgrade-v1/specs/openchamber-image/spec.md`

## Phase 4 — Update the canonical version pinning table

- [x] 4.1 Update `bonnegar/stacks/PACKAGE-VERSIONS.md` — bump `openchamber` row to `1.22.2` (drop the SHA digest)
- [x] 4.2 Update `scripts/audit/audit_package_versions.py` — update the `openchamber` PACKAGE_TABLE entry

## Phase 5 — Verify + push

- [x] 5.1 `openspec validate 2026-09-26-openchamber-image-v1.22-upgrade-v1 --strict` exits 0
- [x] 5.2 `python3 scripts/audit/audit_package_versions.py` shows `openchamber` as `aligned`
- [x] 5.3 `openspec validate --all --strict` exits 0 (no regressions)
- [x] 5.4 Commit + force-push to `2026-08-27-kcg-rename-v1` + `main` via `--force-with-lease`

## MANUAL OPERATOR ACTION (NOT in scope of this change)

Per the v1.22 docs, the operator must upgrade OpenCode to 2.x BEFORE pulling the new OpenChamber image:

```bash
# Upgrade opencode via mise
mise install opencode@2.0.0
mise use opencode@2.0.0
```

Then verify the OpenChamber container comes up:

```bash
docker compose -f compose.yaml -f sidecar.yaml up -d
curl -fsSL https://openchamber.cianchosaint.ie/api/healthz
```

## What's NEXT (Stage 2c — Crawl4AI + Garage + Infisical)

This change ships Stage 2b.3 only. The NEXT openspec change:

- `2026-09-26-loc-data-storage-stack-upgrade-v1/` — bumps crawl4ai + garage + infisical

Per the saga timeline in the Stage 1 proposal.md.
