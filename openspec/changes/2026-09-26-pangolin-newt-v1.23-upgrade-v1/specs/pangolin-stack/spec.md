# cianchosaint-pangolin-stack — Capability Spec

> **Spec ID:** `pangolin-stack`
> **Capability umbrella:** `cianchosaint-pipeline` (the broader British Isles defence / policing / intelligence-oversight pipeline)
> **Status:** PROPOSED (post-`2026-09-26-pangolin-newt-v1.23-upgrade-v1` archive)
> **Last updated:** 2026-09-26

## Purpose

Canonical surface for the Pangolin identity-aware reverse proxy stack — including the Pangolin server + Gerbil WireGuard controller + Newt/Pangolin Site tunnel client. Covers the version pinning, the rename migration (Newt → Pangolin Site per v1.23), and the backward-compat pattern for existing deployments.

## ADDED Requirements

### Requirement: Pangolin server pinned to v1.23.0

The system SHALL pin the Pangolin server container in `bonneagar/stacks/pangolin/compose.yaml` to `fosrl/pangolin:ee-1.23.0` (exact pin, not `latest`).

#### Scenario: Pangolin server uses pinned v1.23.0 image

- **WHEN** the Pangolin container starts
- **THEN** the container SHALL be running `fosrl/pangolin:ee-1.23.0` (the canonical v1.23.0 release)
- **AND** the `ee-latest` placeholder SHALL NOT appear in the compose file

### Requirement: Gerbil pinned to v1.5.1

The system SHALL pin the Gerbil WireGuard controller container in `bonneagar/stacks/pangolin/compose.yaml` to `fosrl/gerbil:1.5.1` (exact pin, not `latest`).

#### Scenario: Gerbil uses pinned v1.5.1 image

- **WHEN** the Gerbil container starts
- **THEN** the container SHALL be running `fosrl/gerbil:1.5.1`
- **AND** the `latest` placeholder SHALL NOT appear in the compose file

### Requirement: New pangolin-site/ directory (the v1.23 pattern)

The system SHALL provide a new `bonneagar/stacks/pangolin-site/` directory containing the canonical new-deployment pattern using `fosrl/pangolin-cli` (the v1.23 CLI that supersedes the standalone Newt binary).

The directory SHALL contain:
- `compose.yaml` — the new `pangolin-site` container using `fosrl/pangolin-cli:latest`
- `secrets.env` — the credentials template (SITE_ID + SITE_SECRET)
- `sidecar.yaml` — Locket secret injection
- `README.md` — the migration guide from `newt.yaml` → `pangolin-site.yaml`

#### Scenario: New site deploys use pangolin-cli

- **WHEN** a new site is created in the Pangolin dashboard (per the v1.23 wizard)
- **THEN** the recommended deployment SHALL use `pangolin-site/compose.yaml` (not `newt.yaml`)
- **AND** the CLI command SHALL be `pangolin up site --id <id> --secret <secret> --endpoint https://pangolin.cianchosaint.ie`

### Requirement: Existing newt.yaml kept for backward compat

The system SHALL keep `bonneagar/stacks/pangolin/newt.yaml` working for existing deployments, per the v1.23 docs: *"Existing Newt deployments keep working. Leave them as they are, or switch to the CLI when you want to. Newt will continue to be provided in all of its current forms for the foreseeable future."*

The `newt.yaml` file SHALL have a header comment indicating: *"NEW: use pangolin-site.yaml per Pangolin v1.23; this file is kept for backward compat"*.

#### Scenario: Existing Newt deployments continue working

- **WHEN** an existing site uses the standalone Newt binary
- **THEN** the Pangolin server SHALL accept the connection (backward compat)
- **AND** the dashboard SHALL display "Pangolin Site" as the canonical name but recognise the legacy Newt binary

## MODIFIED Requirements

None — this is a pure version bump that doesn't change the functional behaviour.

## REMOVED Requirements

None.

## Cross-references

- `infrastructure-stacks` (the umbrella spec) — this spec extends the umbrella
- `package-version-drift` (the Stage 1 spec) — this spec implements Stage 2a of the saga
- [Pangolin 1.23 release notes](https://github.com/fosrl/pangolin/releases/tag/1.23.0)
- [Pangolin 1.23 blog post](https://pangolin.net/news/1-23-release)
- `bonneagar/stacks/PACKAGE-VERSIONS.md` — the canonical version pinning table
