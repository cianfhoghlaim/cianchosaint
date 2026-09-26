# cianchosaint-infisical-stack — Capability Spec

> **Spec ID:** `infisical-stack`
> **Capability umbrella:** `cianchosaint-pipeline`
> **Status:** PROPOSED (post-`2026-09-26-loc-data-storage-stack-upgrade-v1` archive)
> **Last updated:** 2026-09-26

## Purpose

Canonical surface for the Infisical secrets management stack — the source of truth for the `dev-baile` vault. Covers version pinning + the weekly release cadence policy.

## ADDED Requirements

### Requirement: Infisical pinned to v0.165.15

The system SHALL pin the Infisical container in `bonnegar/stacks/infisical/compose.yaml` to `infisical/infisical:v0.165.15` (the latest stable release).

#### Scenario: Infisical uses pinned v0.165.15 image

- **WHEN** the Infisical container starts
- **THEN** the container SHALL be running `infisical/infisical:v0.165.15` (the latest stable release)
- **AND** the `:v0.161.12` placeholder SHALL NOT appear as the default

## MODIFIED Requirements

None — per the Infisical upgrade guide, the upgrade is *"easy: pull the new version. During startup, the application will automatically compare the current database schema with the updated schema in the code."*

## REMOVED Requirements

None.

## Cross-references

- `infrastructure-stacks` (the umbrella spec)
- `package-version-drift` (the Stage 1 spec) — this spec implements Stage 2c
- [Infisical releases](https://github.com/Infisical/infisical/releases) — weekly cadence
- [Infisical upgrade guide](https://infisical.com/docs/self-hosting/guides/upgrading-infisical)
