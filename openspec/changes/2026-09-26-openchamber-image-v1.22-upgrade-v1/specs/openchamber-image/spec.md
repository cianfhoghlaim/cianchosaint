# cianchosaint-openchamber-image — Capability Spec

> **Spec ID:** `openchamber-image`
> **Capability umbrella:** `cianchosaint-pipeline`
> **Status:** PROPOSED (post-`2026-09-26-openchamber-image-v1.22-upgrade-v1` archive)
> **Last updated:** 2026-09-26

## Purpose

Canonical surface for the OpenChamber UI container — the browser-based OpenCode UI built on Bun + React. Covers the v1.0 → v1.22 image bump + the OpenCode 2.x prerequisite.

## ADDED Requirements

### Requirement: OpenChamber pinned to v1.22.2

The system SHALL pin the OpenChamber container in `bonnegar/stacks/openchamber/compose.yaml` to `ghcr.io/openchamber/openchamber:1.22.2` (exact pin, dropping the legacy SHA digest).

#### Scenario: OpenChamber uses pinned v1.22.2 image

- **WHEN** the OpenChamber container starts
- **THEN** the container SHALL be running `ghcr.io/openchamber/openchamber:1.22.2` (the canonical latest release)
- **AND** the `1.0.0@sha256:21fda...` placeholder SHALL NOT appear in the compose file

### Requirement: OpenCode 2.x prerequisite

The system SHALL document the OpenCode 2.x prerequisite: OpenChamber v1.22+ requires the OpenCode server to be on version 2.x (per the v1.22 release notes: *"Startup: connecting to an OpenCode 1.x server shows a clear 'update OpenCode to 2.x' screen."*).

#### Scenario: Operator upgrades OpenCode before deploying

- **WHEN** the operator pulls the OpenChamber v1.22.2 image
- **THEN** the operator MUST also upgrade OpenCode to 2.x (via `mise install opencode@2.0.0`)

## MODIFIED Requirements

None — this is an image-only bump. The full OpenChamber major refactor (Stage 4) will handle the opencode.json updates + the skill rewrite + any UI breaking changes.

## REMOVED Requirements

None.

## Cross-references

- `infrastructure-stacks` (the umbrella spec)
- `package-version-drift` (the Stage 1 spec) — this spec implements Stage 2b.3
- [OpenChamber changelog](https://openchamber.dev/changelog/) — the v1.22 features detail
