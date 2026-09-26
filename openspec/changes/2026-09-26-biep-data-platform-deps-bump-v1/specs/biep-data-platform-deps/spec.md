# cianchosaint-biep-data-platform-deps — Capability Spec

> **Spec ID:** `biep-data-platform-deps`
> **Capability umbrella:** `cianchosaint-pipeline`
> **Status:** PROPOSED (post-`2026-09-26-biep-data-platform-deps-bump-v1` archive)
> **Last updated:** 2026-09-26

## Purpose

Canonical surface for the Python BIEP data platform deps — the load-bearing deps that run the Dagster + CocoIndex + DLT + DuckDB + LanceDB + MotherDuck + Langfuse + Litellm + Google ADK + BAML stack. Covers version pinning policy + per-dep carets.

## ADDED Requirements

### Requirement: Python BIEP data platform deps pinned per the policy

The system SHALL pin the 12 canonical Python BIEP data platform deps in `pyproject.toml` (both repos) per the version policy (`>=X.Y,<X+1.0` caret, or `==X.Y.Z` exact for security-critical deps):

| Package | Pinned (caret range) | Rationale |
|---|---|---|
| dagster | `>=1.13,<2.0` | Bugfixes auto-flow within v1.x |
| dagster-dlt | `>=0.29,<1.0` | New releases follow the 0.x cadence |
| dagster-dbt | `>=0.29,<1.0` | New releases follow the 0.x cadence |
| cocoindex | `>=1.0.20,<2.0` | Bugfixes auto-flow within v1.x |
| baml-py | `>=0.223,<1.0` | Tracks the BAML language v0.x cadence |
| dlt | `>=1.30,<2.0` | Bugfixes auto-flow within v1.x |
| duckdb | `>=1.5.5,<1.6.0` | MotherDuck CLI minimum; v1.5.5 LTS |
| motherduck | `>=0.10,<1.0` | New releases follow the 0.x cadence |
| lancedb | `>=0.39,<1.0` | New releases follow the 0.x cadence |
| google-adk | `>=2.9.0,<3.0` | Bugfixes auto-flow within v2.x |
| langfuse | `>=4.7.0,<5.0` | Python SDK ≥4.7.0 for real-time ingestion |
| litellm | `>=1.102,<2.0` | LiteLLM rolling-window: 4 most recent minor lines |

#### Scenario: All 12 deps resolve at uv sync

- **WHEN** `uv sync` is run in either repo
- **THEN** all 12 deps SHALL resolve at the latest compatible version within their pinned range
- **AND** `python3 scripts/audit/audit_package_versions.py` SHALL show all 12 deps as `aligned`

## MODIFIED Requirements

None — this is a version bump that doesn't change the functional behaviour of any dep.

## REMOVED Requirements

None.

## Cross-references

- `infrastructure-stacks` (the umbrella spec)
- `package-version-drift` (the Stage 1 spec) — this spec implements Stage 3
- [Dagster releases](https://github.com/dagster-io/dagster/releases)
- [CocoIndex releases](https://pypi.org/project/cocoindex/)
- [DLT releases](https://github.com/dlt-hub/dlt/releases)
- [LanceDB releases](https://github.com/lancedb/lancedb/releases)
- [Google ADK releases](https://github.com/google/adk-python/releases)
- [BAML releases](https://boundaryml.com/blog)
- [DuckDB version lifecycle](https://motherduck.com/docs/troubleshooting/version-lifecycle-schedules/) — MotherDuck CLI minimum 1.5.5
- [LiteLLM version-support policy](https://docs.litellm.ai/blog/version-support) — 4 most recent minor lines
- [Langfuse v4 docs](https://langfuse.com/docs/compatibility) — Python SDK ≥4.7.0
