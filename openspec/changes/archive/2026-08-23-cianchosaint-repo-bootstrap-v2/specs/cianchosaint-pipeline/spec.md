# Spec Delta: cianchosaint-pipeline

This delta is applied by the openspec change
[`cianchosaint-repo-bootstrap-v2`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-pipeline/spec.md`](../../../../specs/cianchosaint-pipeline/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: Data platform wholesale-copy contract (DLT + BAML + CocoIndex)

The system SHALL wholesale-copy the relevant Cianfhoghlaim data
platform assets into cianchosaint under the `cianchosaint`
namespace, with the renamed destinations factory
(`destinations_cianchosaint.py` with `DEFAULT_NAMESPACE =
"cianchosaint"` and `LAKEHOUSE_DUCKDB = "md:cianchosaint"`), the
renamed CocoIndex shared lifespan (`_lifespan.py` with
`CIANCHOSAINT_*` env vars), and the per-jurisdiction wholesale-copied
DLT sources (Irish Statute Book + Courts.ie + 6 sibling Irish law
sources + 8 official_media assets) + the 5 BAML files + the 3
CocoIndex flows + the 28 DLT common helpers.

#### Scenario: Wholesale-copied destinations factory uses cianchosaint namespace

- **WHEN** the operator imports
  `from dlt_sources.common.destinations_cianchosaint import get_dlt_destination, LAKEHOUSE_DUCKDB`
- **THEN** the factory SHALL be reachable via the
  `cianchosaint` namespace
- **AND** `LAKEHOUSE_DUCKDB` SHALL equal `"md:cianchosaint"`
- **AND** `get_dlt_destination(mode="local")` SHALL return a local
  DuckDB destination at `./data/cianchosaint.duckdb`

### Requirement: 11 wholesale-copied IaC stacks + 2 new builds

The system SHALL provide 13 Docker Compose stacks under
`bonneagar/stacks/`: 11 wholesale-copied from Cianfhoghlaim
(`litellm/`, `langfuse/`, `motherduck/`, `lakehouse/`,
`unsloth-serve/`, `openchamber/`, `crawl4ai/`, `changedetection/`,
`komodo/`, `pangolin/`, `infisical/`) + 2 built from scratch
(`stagehand/`, `locket/`).

#### Scenario: All 13 stacks validated against the 6-file GOLD_STANDARD pattern

- **WHEN** the operator runs `mise run devops:validate-stacks`
- **THEN** the linter SHALL pass for all 13 stacks
- **AND** each stack SHALL have the 6-file GOLD_STANDARD pattern
  (`compose.yaml`, `sidecar.yaml`, `secrets.env`, `pangolin.yaml`,
  `blueprint.yaml`, `.env.example`)
