# cianchosaint-package-version-drift — Capability Spec

> **Spec ID:** `package-version-drift`
> **Capability umbrella:** `cianchosaint-pipeline` (the broader British Isles defence / policing / intelligence-oversight pipeline)
> **Status:** PROPOSED (post-`2026-09-26-package-version-drift-audit-v1` archive)
> **Last updated:** 2026-09-26

## Purpose

Canonical surface for tracking opensource package version drift across the cianchosaint + cianfhoghlaim platform. The drift table is the canonical registry; the audit script is the runtime detector; the skill is the operator-facing documentation; this spec is the load-bearing constraint.

## ADDED Requirements

### Requirement: The canonical version pinning table

The system SHALL provide a canonical version pinning table at `bonneagar/stacks/PACKAGE-VERSIONS.md` that lists every opensource package used across the cianchosaint + cianfhoghlaim platform (IaC stack Docker images + Python BIEP deps + TypeScript workspace deps + the 79 skills).

#### Scenario: Every IaC stack has a row

- **WHEN** a Docker Compose stack exists under `bonneagar/stacks/<name>/`
- **THEN** the stack SHALL have a corresponding row in `PACKAGE-VERSIONS.md` with the `pinned_ciancho` + `pinned_cianfhog` + `latest` + `drift` + `stage` columns populated

#### Scenario: Every Python dep has a row

- **WHEN** a Python package appears in `pyproject.toml` (in either repo)
- **THEN** the package SHALL have a corresponding row in `PACKAGE-VERSIONS.md` with the same columns populated

### Requirement: The runtime audit script

The system SHALL provide a Python script at `scripts/audit/audit_package_versions.py` that:

- Queries the latest version of every package in the canonical table via 3 source APIs (PyPI JSON API + Docker Hub Registry API + GitHub Releases API)
- Computes the drift per package (aligned / behind-1-minor / behind-N-minor / behind-major / unknown)
- Supports 3 CLI modes: default (print drift table), `--json` (emit JSON for CI), `--strict` (exit 1 if drift > 1 minor)

#### Scenario: Default mode prints a drift table

- **WHEN** `python3 scripts/audit/audit_package_versions.py` is run
- **THEN** it SHALL print a human-readable drift table with all 4 columns (PINNED ciancho, PINNED cianfhog, LATEST, DRIFT) and a summary line (aligned / behind-1-minor / behind-N-minor / unknown counts)

#### Scenario: JSON mode emits structured output

- **WHEN** `python3 scripts/audit_package_versions.py --json` is run
- **THEN** it SHALL emit a JSON object with `audit_timestamp` + `results` (each result is a `DriftResult` dataclass with `name`, `kind`, `pinned_ciancho`, `pinned_cianfhog`, `latest`, `drift_status`, `policy`, `stage`, `note`)

#### Scenario: Strict mode fails on drift

- **WHEN** `python3 scripts/audit_package_versions.py --strict` is run
- **AND** any package has `drift_status` of `behind-2-minor` or worse
- **THEN** the script SHALL exit with status 1

### Requirement: The canonical skill

The system SHALL provide a skill at `.agents/skills/package-version-drift/SKILL.md` that documents:

- When to load the skill (adding a new package, bumping an existing one, auditing drift)
- How to add a new package to the canonical table
- How to bump an existing package (the openspec change workflow)
- How to run the audit script
- The 7-stage saga timeline

#### Scenario: Skill has canonical frontmatter

- **WHEN** a user inspects the skill metadata
- **THEN** the `SKILL.md` SHALL have `name:` + `description:` + `when_to_use:` fields in the canonical frontmatter (per `.agents/skills/_template/SKILL.md`)

### Requirement: The version policy

The system SHALL document the canonical version policy in `docs/VERSION-DRIFT-POLICY.md` (NEW 2026-09-26 in Stage 7). The policy SHALL specify:

- **IaC stack Docker images**: `==X.Y.Z` (exact)
- **Python BIEP data platform deps**: `>=X.Y,<X+1.0` (caret)
- **Dev tooling** (mise `[tools]`): `latest`

#### Scenario: Policy is published

- **WHEN** a user asks "what's the version policy?"
- **THEN** `docs/VERSION-DRIFT-POLICY.md` SHALL be the canonical source

### Requirement: The 7-stage saga timeline

The system SHALL plan a 7-stage sequential improvement saga to refactor every opensource package to latest, in dependency order:

| Stage | Scope |
|---|---|
| 1 | Foundation audit (THIS change) |
| 2a | Pangolin + Newt + Gerbil |
| 2b | Litellm + Langfuse + Komodo + OpenChamber image |
| 2c | Crawl4AI + Garage + Infisical |
| 3 | Python BIEP data platform deps |
| 4 | OpenChamber major refactor (1.0 → 1.22) |
| 5 | LanceDB major refactor (Lance v1 → Lance v2 in-place) |
| 6 | Skill version-header refresh |
| 7 | Continuous version drift monitoring |

#### Scenario: Saga timeline is documented

- **WHEN** a user asks "what's the upgrade plan?"
- **THEN** `bonneagar/stacks/PACKAGE-VERSIONS.md` SHALL document the 7-stage saga timeline + the per-stage openspec change IDs

## MODIFIED Requirements

None — this is a new capability.

## REMOVED Requirements

None.

## Cross-references

- `cianchosaint-pipeline` (the umbrella capability spec) — this spec extends the umbrella
- `openspec/AGENTS.md` (the openspec workflow)
- `.agents/skills/_template/SKILL.md` (the canonical skill template)
