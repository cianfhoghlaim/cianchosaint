# 2026-09-26 — Pangolin + Newt + Gerbil upgrade tasks

> Ordered checklist for shipping `2026-09-26-pangolin-newt-v1.23-upgrade-v1` (Stage 2a of the saga).

## Phase 1 — Firecrawl MCP research (the upstream validation)

- [x] 1.1 Fetch the Pangolin v1.23.0 GitHub release notes — confirmed the "Newt → Pangolin Site" rename + the v1.22 AI Gateway (Sep 16, 2026 release date)
- [x] 1.2 Fetch the Pangolin v1.23 blog post — confirmed the v1.23 features detail + the migration path
- [x] 1.3 Verify Gerbil latest version — v1.5.1 (Aug 31, 2026)
- [x] 1.4 Verify Newt latest version — v1.16.x (per Pangolin v1.23 docs; existing Newt deployments keep working)

## Phase 2 — Create the openspec change

- [x] 2.1 Create `openspec/changes/2026-09-26-pangolin-newt-v1.23-upgrade-v1/proposal.md`
- [x] 2.2 Create `openspec/changes/2026-09-26-pangolin-newt-v1.23-upgrade-v1/tasks.md` (this file)
- [x] 2.3 Create `openspec/changes/2026-09-26-pangolin-newt-v1.23-upgrade-v1/specs/pangolin-stack/spec.md`

## Phase 3 — Update the IaC stack (Pangolin + Gerbil)

- [x] 3.1 Update `bonneagar/stacks/pangolin/compose.yaml` — `pangolin: image: fosrl/pangolin:ee-latest` → `fosrl/pangolin:ee-1.23.0`
- [x] 3.2 Update `bonneagar/stacks/pangolin/compose.yaml` — `gerbil: image: fosrl/gerbil:latest` → `fosrl/gerbil:1.5.1`

## Phase 4 — Create the new Pangolin Site pattern

- [x] 4.1 Create `bonneagar/stacks/pangolin-site/compose.yaml` (the new `pangolin-site` container using `fosrl/pangolin-cli:latest`)
- [x] 4.2 Create `bonneagar/stacks/pangolin-site/secrets.env` (the credentials template)
- [x] 4.3 Create `bonneagar/stacks/pangolin-site/sidecar.yaml` (Locket secret injection)
- [x] 4.4 Create `bonneagar/stacks/pangolin-site/README.md` (the migration guide from newt.yaml → pangolin-site.yaml)

## Phase 5 — Backward-compat annotation on the existing newt.yaml

- [x] 5.1 Update `bonneagar/stacks/pangolin/newt.yaml` — add header comment: "NEW: use pangolin-site.yaml per Pangolin v1.23; this file is kept for backward compat"

## Phase 6 — Update the 3 skills

- [x] 6.1 Update `.agents/skills/pangolin/SKILL.md` — bump version header to `1.23.0` + add "What's new in Pangolin 1.23" section + migration notes
- [x] 6.2 Update `.agents/skills/pangolin-cli/SKILL.md` — add "Site installation via the Pangolin CLI" section
- [x] 6.3 Update `.agents/skills/pangolin-ai-gateway/SKILL.md` — note the v1.22+ AI Gateway + the v1.23 HA/clustering implications

## Phase 7 — Update the canonical version pinning table

- [x] 7.1 Update `bonneagar/stacks/PACKAGE-VERSIONS.md` — bump `pangolin` row (both repos → `ee-1.23.0`)
- [x] 7.2 Update `bonneagar/stacks/PACKAGE-VERSIONS.md` — bump `gerbil` row (both repos → `1.5.1`)
- [x] 7.3 Update `bonneagar/stacks/PACKAGE-VERSIONS.md` — update `newt` row (note the rename; bump to `1.16.x`)
- [x] 7.4 Update `scripts/audit/audit_package_versions.py` — bump the `pangolin` + `gerbil` + `newt` entries in `PACKAGE_TABLE`
- [x] 7.5 Update `scripts/audit/audit_package_versions.py` — add the new `pangolin-site` entry

## Phase 8 — Verify + push

- [x] 8.1 `openspec validate 2026-09-26-pangolin-newt-v1.23-upgrade-v1 --strict` exits 0
- [x] 8.2 `python3 scripts/audit/audit_package_versions.py` shows `pangolin` + `gerbil` as `aligned`
- [x] 8.3 `openspec validate --all --strict` exits 0 (no regressions)
- [x] 8.4 Commit + force-push to `2026-08-27-kcg-rename-v1` + `main` via `--force-with-lease`

## What's NEXT (Stage 2b — Litellm + Langfuse + Komodo + OpenChamber image)

This change ships Stage 2a only. The NEXT openspec changes (per the saga timeline):

- `2026-09-26-litellm-langfuse-v1.102-upgrade-v1/` (1 change)
- `2026-09-26-komodo-v2-upgrade-v1/` (1 change)
- `2026-09-26-openchamber-image-v1.22-upgrade-v1/` (1 change)

Per the saga timeline in the Stage 1 proposal.md.
