# cianchosaint-skill-refresh — Capability Spec

> **Spec ID:** `skill-refresh`
> **Capability umbrella:** `cianchosaint-pipeline`
> **Status:** PROPOSED (post-`2026-09-26-skill-version-header-refresh-v1` archive)
> **Last updated:** 2026-09-26

## Purpose

Canonical surface for the skill version-header refresh — covering the 79 `.agents/skills/*/SKILL.md` files + the canonical refresh policy + the audit script + the canonical package→skill mapping.

## ADDED Requirements

### Requirement: All skills have updated version headers

The system SHALL keep the version header in each of the 79 `.agents/skills/*/SKILL.md` files up to date with the canonical PACKAGE-VERSIONS.md table.

#### Scenario: All 79 skills have version headers that match the canonical table

- **WHEN** `python3 scripts/audit/refresh_skill_versions.py` is run
- **THEN** the script SHALL report 0 stale skills (each skill's version header matches the canonical PACKAGE-VERSIONS.md entry for its corresponding package)

### Requirement: Skills have a "Version policy" section

The system SHALL add a "Version policy" section to each skill documenting:
- The canonical refresh cadence (per the Stage 7 monitoring workflow)
- The canonical command to refresh: `python3 scripts/audit/refresh_skill_versions.py`
- The canonical mapping: `scripts/audit/PACKAGE_TO_SKILL_MAP.md`

#### Scenario: Operator reads the Version policy section

- **WHEN** the operator inspects any skill's SKILL.md
- **THEN** the skill SHALL contain a "Version policy" section near the top

### Requirement: The refresh audit script is the canonical surface

The system SHALL provide `scripts/audit/refresh_skill_versions.py` as the canonical audit script that:
- Scans all 79 skills
- Compares each skill's version header against the canonical PACKAGE-VERSIONS.md entry
- Reports stale skills + suggested refresh actions

#### Scenario: Operator runs the refresh audit

- **WHEN** `python3 scripts/audit/refresh_skill_versions.py` is run
- **THEN** it SHALL print a per-skill status table (up to date / stale / unknown)

## MODIFIED Requirements

None — this is a documentation + audit tooling change.

## REMOVED Requirements

None.

## Cross-references

- `infrastructure-stacks` (the umbrella spec)
- `package-version-drift` (the Stage 1 spec) — this spec implements Stage 6
- `docs/SKILL-VERSION-HEADER-POLICY.md` (NEW, this change) — the canonical refresh policy
- `scripts/audit/refresh_skill_versions.py` (NEW, this change) — the canonical audit script
- `scripts/audit/PACKAGE_TO_SKILL_MAP.md` (NEW, this change) — the canonical mapping
- [`.agents/skills/_template/SKILL.md`](../../../../.agents/skills/_template/SKILL.md) — the canonical skill template
