# cianchosaint-langfuse-stack — Capability Spec

> **Spec ID:** `langfuse-stack`
> **Capability umbrella:** `cianchosaint-pipeline`
> **Status:** PROPOSED (post-`2026-09-26-litellm-langfuse-upgrade-v1` archive)
> **Last updated:** 2026-09-26

## Purpose

Canonical surface for the Langfuse observability stack — the LLM tracing + prompt management + cost tracking layer. Covers version pinning + the Python SDK ≥4.7.0 requirement for real-time ingestion.

## ADDED Requirements

### Requirement: Langfuse Docker image pinned to v4.7.0

The system SHALL pin the Langfuse containers in `bonnegar/stacks/langfuse/compose.yaml` to `langfuse/langfuse:4.7.0` + `langfuse/langfuse-worker:4.7.0` (exact pins).

#### Scenario: Langfuse server uses pinned v4.7.0 image

- **WHEN** the Langfuse server + worker containers start
- **THEN** both containers SHALL be running `langfuse/langfuse:4.7.0` + `langfuse/langfuse-worker:4.7.0`
- **AND** the `:4` (major-only) placeholder SHALL NOT appear in the compose file

### Requirement: Langfuse Python SDK pinned to ≥4.7.0

The system SHALL pin the Langfuse Python SDK in `pyproject.toml` (cianchosaint) to `langfuse>=4.7.0,<5.0` (the lower bound is the real-time ingestion requirement; the upper bound is the v4 cycle).

#### Scenario: Real-time ingestion works

- **WHEN** a Langfuse trace is sent via the Python SDK
- **AND** the SDK version is ≥4.7.0
- **THEN** the trace SHALL appear in the Langfuse UI without the 15-minute delay that data from <4.7.0 SDKs experiences

## MODIFIED Requirements

None.

## REMOVED Requirements

None.

## Cross-references

- `infrastructure-stacks` (the umbrella spec)
- `package-version-drift` (the Stage 1 spec) — this spec implements Stage 2b.1
- [Langfuse v4 docs](https://langfuse.com/docs/compatibility) — Python SDK ≥4.7.0 requirement
