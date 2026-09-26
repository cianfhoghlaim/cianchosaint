# cianchosaint-garage-stack — Capability Spec

> **Spec ID:** `garage-stack`
> **Capability umbrella:** `cianchosaint-pipeline`
> **Status:** PROPOSED (post-`2026-09-26-loc-data-storage-stack-upgrade-v1` archive)
> **Last updated:** 2026-09-26

## Purpose

Canonical surface for the Garage S3-compatible object storage stack — the lakehouse blob layer. Covers version pinning + the no-breaking-changes migration policy from v2.3.

## ADDED Requirements

### Requirement: Garage pinned to v2.4.1

The system SHALL pin the Garage container in `bonnegar/stacks/lakehouse/compose.yaml` to `dxflrs/garage:v2.4.1` (the latest stable release).

#### Scenario: Garage uses pinned v2.4.1 image

- **WHEN** the Garage container starts
- **THEN** the container SHALL be running `dxflrs/garage:v2.4.1` (the latest stable release)
- **AND** the `:v2.3.0` placeholder SHALL NOT appear as the default

## MODIFIED Requirements

None — per the v2.4.0 release notes: *"There are no breaking changes when migrating from Garage v2.3.0."*

## REMOVED Requirements

None.

## Cross-references

- `infrastructure-stacks` (the umbrella spec)
- `package-version-drift` (the Stage 1 spec) — this spec implements Stage 2c
- [Garage v2.4.1 release](https://git.deuxfleurs.fr/Deuxfleurs/garage/releases/tag/v2.4.1)
