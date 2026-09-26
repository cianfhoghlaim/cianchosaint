# cianchosaint-litellm-stack — Capability Spec

> **Spec ID:** `litellm-stack`
> **Capability umbrella:** `cianchosaint-pipeline`
> **Status:** PROPOSED (post-`2026-09-26-litellm-langfuse-upgrade-v1` archive)
> **Last updated:** 2026-09-26

## Purpose

Canonical surface for the Litellm LLM gateway stack — the OpenAI-compatible proxy that fronts the 4-tier provider chain (Unsloth Studio → Litellm → MiniMax → Gemini). Covers version pinning + the rolling-window policy.

## ADDED Requirements

### Requirement: Litellm pinned to v1.102.0

The system SHALL pin the Litellm proxy container in `bonnegar/stacks/litellm/compose.yaml` to `ghcr.io/berriai/litellm-database:v1.102.0` (exact pin).

#### Scenario: Litellm proxy uses pinned v1.102.0 image

- **WHEN** the Litellm proxy container starts
- **THEN** the container SHALL be running `ghcr.io/berriai/litellm-database:v1.102.0` (the canonical latest release)
- **AND** the `v1.97.0` placeholder SHALL NOT appear in the compose file

### Requirement: Litellm rolling-window policy documented

The system SHALL document the Litellm release-support policy in the canonical Litellm skill: *"LiteLLM will only actively support the four most recent stable minor lines."*

#### Scenario: User checks whether a Litellm version is supported

- **WHEN** a user asks "is Litellm v1.97 still supported?"
- **THEN** the Litellm skill SHALL reference the rolling-window policy and indicate that v1.97 is approaching EOL (4 lines behind the current latest)

## MODIFIED Requirements

None.

## REMOVED Requirements

None.

## Cross-references

- `infrastructure-stacks` (the umbrella spec) — this spec extends the umbrella
- `package-version-drift` (the Stage 1 spec) — this spec implements Stage 2b.1
- [LiteLLM version-support policy](https://docs.litellm.ai/blog/version-support)
- [LiteLLM v1.102.0 release notes](https://docs.litellm.ai/release_notes/v1.102.0/v1-102-0)
