# cianchosaint-openchamber-major — Capability Spec

> **Spec ID:** `openchamber-major`
> **Capability umbrella:** `cianchosaint-pipeline`
> **Status:** PROPOSED (post-`2026-09-26-openchamber-v1.22-major-upgrade-v1` archive)
> **Last updated:** 2026-09-26

## Purpose

Canonical surface for the OpenChamber major refactor (1.0 → 1.22) — covering the image bump + the OpenCode 2.x prerequisite + the v1.22 features documentation + the v2.0 hot reload prep.

## ADDED Requirements

### Requirement: OpenChamber image pinned to v1.22.2

The system SHALL pin the OpenChamber container in `bonnegar/stacks/openchamber/compose.yaml` to `ghcr.io/openchamber/openchamber:1.22.2`.

#### Scenario: OpenChamber uses pinned v1.22.2 image

- **WHEN** the OpenChamber container starts
- **THEN** the container SHALL be running `ghcr.io/openchamber/openchamber:1.22.2` (the canonical latest release)
- **AND** the `1.0.0@sha256:21fda...` placeholder SHALL NOT appear in the compose file

### Requirement: OpenCode 2.x prerequisite documented

The system SHALL document the OpenCode 2.x prerequisite in the OpenChamber README: OpenChamber v1.22+ requires the OpenCode server to be on version 2.x (per the v1.22 release notes: *"Startup: connecting to an OpenCode 1.x server shows a clear 'update OpenCode to 2.x' screen."*).

#### Scenario: Operator upgrades OpenCode before deploying

- **WHEN** the operator pulls the OpenChamber v1.22.2 image
- **THEN** the operator MUST also upgrade OpenCode to 2.x (via `mise install opencode@2.0.0`)

### Requirement: OpenChamber README documents the v1.22 release

The system SHALL document the OpenChamber v1.22 release in the canonical README at `bonnegar/stacks/openchamber/README.md` — including the new features (browser panel, queue retry, status refresh, VS Code comments, OpenCode Go integration) + the OpenCode 2.x prerequisite + the v2.0 hot reload prep roadmap.

#### Scenario: Operator reads the OpenChamber README

- **WHEN** the operator inspects `bonnegar/stacks/openchamber/README.md`
- **THEN** the README SHALL include a "What's new in OpenChamber 1.22" section + the OpenCode 2.x prerequisite note + the v2.0 hot reload prep roadmap

## MODIFIED Requirements

None — this is a documentation + verification change. The image bump itself was shipped in Stage 2b.3.

## REMOVED Requirements

None.

## Cross-references

- `infrastructure-stacks` (the umbrella spec)
- `package-version-drift` (the Stage 1 spec) — this spec implements Stage 4
- `openchamber-image` (the Stage 2b.3 spec) — the image-only bump
- [OpenChamber v1.22 changelog](https://openchamber.dev/changelog/)
- [OpenChamber 2.0 blog post](https://openchamber.dev/blog/opencode-v2/)
