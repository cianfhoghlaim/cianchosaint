# 2026-09-26 — Komodo v2 upgrade tasks

> Ordered checklist for shipping `2026-09-26-komodo-v2-upgrade-v1` (Stage 2b.2 of the saga).

## Phase 1 — Firecrawl MCP research (the upstream validation)

- [x] 1.1 Fetch the Komodo v2.0.0 release blog — confirmed v2 GA March 2026, "largely backward compatible"
- [x] 1.2 Fetch the Komodo v2 upgrade docs — confirmed the upgrade path (bump `image: :2`, add `init: true`)
- [x] 1.3 Verify FerretDB v2 requirement — confirmed "Komodo 1.18.0+ requires FerretDB v2 · SQLite and PostgreSQL via FerretDB v1 are no longer supported"

## Phase 2 — Verify the canonical Komodo v2 state across both repos

- [x] 2.1 Verify `bonnegar/stacks/komodo/.env.example` has `KOMODO_IMAGE_TAG=2` (both repos) — VERIFIED
- [x] 2.2 Verify `bonnegar/stacks/komodo/compose.yaml` has `ghcr.io/moghtech/komodo-core:${KOMODO_IMAGE_TAG:-2}` (both repos) — VERIFIED
- [x] 2.3 Verify `bonnegar/stacks/komodo/periphery.yaml` has `ghcr.io/moghtech/komodo-periphery:${KOMODO_IMAGE_TAG:-2-dev}` (both repos) — VERIFIED
- [x] 2.4 Verify `init: true` is set on both Core + Periphery services (per the v2 upgrade docs) — VERIFIED

## Phase 3 — Create the openspec change

- [x] 3.1 Create `openspec/changes/2026-09-26-komodo-v2-upgrade-v1/proposal.md`
- [x] 3.2 Create `openspec/changes/2026-09-26-komodo-v2-upgrade-v1/tasks.md` (this file)
- [x] 3.3 Create `openspec/changes/2026-09-26-komodo-v2-upgrade-v1/specs/komodo-stack/spec.md`

## Phase 4 — Update the canonical version pinning table

- [x] 4.1 Update `bonnegar/stacks/PACKAGE-VERSIONS.md` — bump `komodo` row to `komodo-core:2` + `komodo-periphery:2-dev`
- [x] 4.2 Update `scripts/audit/audit_package_versions.py` — verify the `komodo-core` + `komodo-periphery` PACKAGE_TABLE entries

## Phase 5 — Manual follow-ups (NOT in scope of this openspec change)

- [ ] 5.1 **MANUAL**: Regenerate Core ↔ Periphery PKI keys (per v2 release notes — "Core and Periphery now authenticate with auto-generated keys")
- [ ] 5.2 **MANUAL**: Verify any `komodo.execute_terminal` Actions (per v2 upgrade docs § "Fix any `komodo.execute_terminal` in Actions")
- [ ] 5.3 **MANUAL**: Confirm the v1 FerretDB data has been migrated to v2 (the v1 → v2 data migration was completed earlier per the cianchosaint/cianfhoghlaim deployment history)

## Phase 6 — Verify + push

- [x] 6.1 `openspec validate 2026-09-26-komodo-v2-upgrade-v1 --strict` exits 0
- [x] 6.2 `python3 scripts/audit/audit_package_versions.py` shows `komodo-core` + `komodo-periphery` as `aligned`
- [x] 6.3 `openspec validate --all --strict` exits 0 (no regressions)
- [x] 6.4 Commit + force-push to `2026-08-27-kcg-rename-v1` + `main` via `--force-with-lease`

## What's NEXT (Stage 2b.3 — OpenChamber image)

This change ships Stage 2b.2 only. The NEXT openspec change:

- `2026-09-26-openchamber-image-v1.22-upgrade-v1/` — bumps openchamber image 1.0.0 → 1.22.2 (image-only bump; Stage 4 is the full refactor)

Per the saga timeline in the Stage 1 proposal.md.
