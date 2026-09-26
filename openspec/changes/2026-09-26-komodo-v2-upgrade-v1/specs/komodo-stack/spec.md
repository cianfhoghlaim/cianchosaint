# cianchosaint-komodo-stack — Capability Spec

> **Spec ID:** `komodo-stack`
> **Capability umbrella:** `cianchosaint-pipeline`
> **Status:** PROPOSED (post-`2026-09-26-komodo-v2-upgrade-v1` archive)
> **Last updated:** 2026-09-26

## Purpose

Canonical surface for the Komodo GitOps orchestrator stack — the Docker container management + resource-sync + procedure + build system. Covers version pinning + the FerretDB v2 requirement + the PKI authentication model introduced in v2.

## ADDED Requirements

### Requirement: Komodo Core + Periphery pinned to v2

The system SHALL pin the Komodo containers to:
- `ghcr.io/moghtech/komodo-core:${KOMODO_IMAGE_TAG:-2}` (Core)
- `ghcr.io/moghtech/komodo-periphery:${KOMODO_IMAGE_TAG:-2-dev}` (Periphery)

`KOMODO_IMAGE_TAG` SHALL default to `2` in `.env.example`.

#### Scenario: Komodo Core + Periphery run v2

- **WHEN** the Komodo Core + Periphery containers start
- **THEN** Core SHALL be running `ghcr.io/moghtech/komodo-core:2` (the canonical v2 GA release)
- **AND** Periphery SHALL be running `ghcr.io/moghtech/komodo-periphery:2-dev` (the v2 dev tag for the Periphery variant)
- **AND** the `init: true` flag SHALL be set on both services (per the v2 upgrade docs)

### Requirement: FerretDB v2 (the load-bearing dependency)

The system SHALL use FerretDB v2 (`ferretdb:2`) + `postgres-documentdb:17` as the database backend for Komodo.

Per the Komodo v1.18.0+ requirement: *"Komodo 1.18.0 requires FerretDB v2 · SQLite and PostgreSQL via FerretDB v1 are no longer supported."*

#### Scenario: FerretDB v2 is the database backend

- **WHEN** the Komodo Core container starts
- **THEN** the database connection SHALL point at a FerretDB v2 instance (not v1)
- **AND** the compose.yaml SHALL use `ferretdb:2` (not `ferretdb:1`)

### Requirement: Core ↔ Periphery PKI authentication

The system SHALL use the v2 PKI authentication model between Core + Periphery (per the v2 release notes: *"PKI authentication: Core and Periphery now authenticate with auto-generated keys"*).

#### Scenario: PKI keys are auto-generated

- **WHEN** the Komodo Core container starts for the first time
- **THEN** Core SHALL auto-generate the PKI keys for Periphery authentication
- **AND** the keys SHALL be persisted to the `keys:` volume (the canonical key store)

## MODIFIED Requirements

None — this is a version verification (the v2 bump was already in place).

## REMOVED Requirements

None.

## Cross-references

- `infrastructure-stacks` (the umbrella spec)
- `package-version-drift` (the Stage 1 spec) — this spec implements Stage 2b.2
- [Komodo v2.0.0 upgrade docs](https://komo.do/docs/releases/v2.0.0) — the upstream upgrade guide
- [Komodo FerretDB v1 → v2 migration](https://github.com/community-scripts/ProxmoxVE/discussions/5689)
