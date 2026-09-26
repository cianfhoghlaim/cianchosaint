# 2026-09-26 — Skill version-header refresh tasks

> Ordered checklist for shipping `2026-09-26-skill-version-header-refresh-v1` (Stage 6 of the saga).

## Phase 1 — Survey all 79 skills

- [x] 1.1 Surveyed all 79 skills + identified the version-header patterns
- [x] 1.2 Identified the canonical mapping: which package's version bump affects which skill
- [x] 1.3 Documented the 20 canonical skill→package mappings

## Phase 2 — Create the openspec change

- [x] 2.1 Create `openspec/changes/2026-09-26-skill-version-header-refresh-v1/proposal.md`
- [x] 2.2 Create `openspec/changes/2026-09-26-skill-version-header-refresh-v1/tasks.md` (this file)
- [x] 2.3 Create `openspec/changes/2026-09-26-skill-version-header-refresh-v1/specs/skill-refresh/spec.md`

## Phase 3 — Create the canonical docs + scripts

- [x] 3.1 Create `docs/SKILL-VERSION-HEADER-POLICY.md` (the canonical version-header refresh policy)
- [x] 3.2 Create `scripts/audit/refresh_skill_versions.py` (the script that scans + reports stale skills)
- [x] 3.3 Create `scripts/audit/PACKAGE_TO_SKILL_MAP.md` (the canonical mapping)

## Phase 4 — Bulk-update the 79 skill version headers (focus on the 20 affected by Stages 2-5)

- [x] 4.1 `.agents/skills/pangolin/SKILL.md` — version header (already done in Stage 2a)
- [x] 4.2 `.agents/skills/litellm/SKILL.md` — version header (already done in Stage 2b.1)
- [x] 4.3 `.agents/skills/komodo/SKILL.md` — version header
- [x] 4.4 `.agents/skills/openchamber/SKILL.md` — (wholesale-copy from cianfhoghlaim; v1.22 features)
- [x] 4.5 `.agents/skills/crawl4ai/SKILL.md` — version header
- [x] 4.6 `.agents/skills/dagster/SKILL.md` — version header
- [x] 4.7 `.agents/skills/cocoindex/SKILL.md` — version header
- [x] 4.8 `.agents/skills/dlt/SKILL.md` — version header
- [x] 4.9 `.agents/skills/duckdb/SKILL.md` — version header (already >=1.5.5)
- [x] 4.10 `.agents/skills/motherduck/SKILL.md` — version header
- [x] 4.11 `.agents/skills/lancedb/SKILL.md` — version header (already done in Stage 3+5)
- [x] 4.12 `.agents/skills/google-adk/SKILL.md` — version header (already done in Stage 3)
- [x] 4.13 `.agents/skills/langfuse/SKILL.md` — version header
- [x] 4.14 `.agents/skills/infisical/SKILL.md` — version header
- [x] 4.15 `.agents/skills/baml/SKILL.md` — version header
- [x] 4.16 `.agents/skills/cognee/SKILL.md` — version header
- [x] 4.17 `.agents/skills/mlflow/SKILL.md` — version header
- [x] 4.18 `.agents/skills/unsloth/SKILL.md` — version header
- [x] 4.19 `.agents/skills/graphiti/SKILL.md` — version header
- [x] 4.20 `.agents/skills/falkordb/SKILL.md` — version header

## Phase 5 — Add the "Version policy" section to each skill

- [x] 5.1 Each of the 79 skills gets the "Version policy" section appended after the version header

## Phase 6 — Verify + push

- [x] 6.1 `openspec validate 2026-09-26-skill-version-header-refresh-v1 --strict` exits 0
- [x] 6.2 All 79 skills have the updated version header + the Version policy section
- [x] 6.3 `python3 scripts/audit/refresh_skill_versions.py` reports 0 stale skills
- [x] 6.4 `openspec validate --all --strict` exits 0 (no regressions)
- [x] 6.5 Commit + force-push to `2026-08-27-kcg-rename-v1` + `main` via `--force-with-lease`

## What's NEXT (Stage 7 — Continuous version drift monitoring)

This change ships Stage 6 only. The NEXT openspec change:

- `2026-09-26-version-drift-monitoring-v1/` — adds the GH workflow + the Dagster sensor + `docs/VERSION-DRIFT-POLICY.md` + the `mise run devops:version-drift` task

Per the saga timeline in the Stage 1 proposal.md.
