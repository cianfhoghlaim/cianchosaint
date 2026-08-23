# cianchosaint-source-catalogue Capability

## Purpose

`cianchosaint-source-catalogue` is the capability that provides the
**canonical, operator-facing catalogue of British Isles public-sector
bodies** that cianchosaint ingests from or COULD ingest from. The
catalogue is a 11-file multi-file artefact at `docs/source-catalogue/`
(1 README + 10 topical files) that documents every body (intelligence
agency, police force, military, government department, court, political
party, audit body, etc.) with a uniform per-body schema (URL + DLT
source linkage + OSINT allowlist flag + coverage + update cadence +
notes).

This catalogue is the load-bearing companion to the allowlist
(`dlt_sources/cianchosaint/common/osint_allowlist.yaml`), the per-
constituency cohort registry
(`dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`),
and the per-political-party registry
(`dlt_sources/cianchosaint/political_parties/_registry.py`).

## Background

On a fresh deployment, an operator previously had to read:

1. The OSINT allowlist (URL list, no bodies)
2. The per-constituency cohort registry (technical, no body descriptions)
3. The political-party registry (technical, no body descriptions)
4. The intelligence-agency DLT source files (5 files, each only
   documenting itself)
5. The UK / NI / ROI policing DLT source files (5 files, each only
   documenting itself)

to understand the FULL scope of "what British Isles public-sector
bodies does cianchosaint cover?". The knowledge was scattered across
~15 files and the operator had to mentally re-assemble it.

The `cianchosaint-british-isles-source-catalogue-v1` change collapses
all of that into a single canonical multi-file artefact at
`docs/source-catalogue/` (11 files, ~8,000-12,000 words).

## Requirements

### Requirement: The multi-file catalogue format

The system SHALL provide a canonical multi-file catalogue at
`docs/source-catalogue/` that enumerates every British Isles
public-sector body that cianchosaint ingests from or COULD ingest
from, organised into 10 topical files + 1 README.

#### Scenario: 11 catalogue files present

- **WHEN** the operator runs `ls docs/source-catalogue/`
- **THEN** the directory SHALL contain 11 markdown files:
  `README.md`, `01-intelligence-agencies.md`,
  `02-police-forces-uk.md`, `03-police-forces-ireland.md`,
  `04-police-forces-crown-dependencies.md`, `05-armed-forces-uk.md`,
  `06-armed-forces-ireland.md`, `07-key-government-departments.md`,
  `08-courts-and-tribunals.md`, `09-political-parties.md`,
  `10-other-bodies.md`

#### Scenario: The README is the master catalogue

- **WHEN** the operator reads `docs/source-catalogue/README.md`
- **THEN** the README SHALL provide the overview of the catalogue
- **AND** SHALL explain how to use it (the per-body schema; the gap
  inventory)
- **AND** SHALL cross-link to all 10 topic files

### Requirement: The per-body schema

The system SHALL document every British Isles public-sector body in
the catalogue using a uniform per-body schema (URL, DLT source linkage,
OSINT allowlist flag, coverage description, update cadence, notes).

#### Scenario: Every body uses the per-body schema

- **WHEN** the operator reads any topic file in
  `docs/source-catalogue/`
- **THEN** every body SHALL be documented under a `### <Body Name>`
  heading
- **AND** SHALL include the 6 schema fields:
  - `**URL**` (the body's canonical website)
  - `**DLT source**` (the path to the DLT source file, or
    `NOT YET WIRED`)
  - `**OSINT allowlist**` (`yes` / `no`)
  - `**Coverage**` (what the source provides)
  - `**Update cadence**` (`daily` / `weekly` / `monthly` /
    `on-publication`)
  - `**Notes**` (any caveats)

#### Scenario: The catalogue numbers match ground truth

- **WHEN** the operator runs `mise run lint:drift-docs`
- **THEN** the linter SHALL verify the catalogue's number claims:
  - 12 UK intelligence + oversight bodies in `01-intelligence-agencies.md`
  - 45 UK police forces in `02-police-forces-uk.md` (43 territorial +
    BTP + MDP)
  - 2 ROI police forces in `03-police-forces-ireland.md`
  - 3 Crown Dependencies police forces in
    `04-police-forces-crown-dependencies.md`
  - 24 political parties in `09-political-parties.md`
- **AND** SHALL fail with exit code 1 if any number is wrong

### Requirement: The gap inventory

The system SHALL maintain a `## Gaps` section in every topic file in
`docs/source-catalogue/` that enumerates what is NOT yet covered
(bodies without a DLT source, sources without an OSINT allowlist entry,
etc.).

#### Scenario: Every topic file has a Gaps section

- **WHEN** the operator reads any topic file in
  `docs/source-catalogue/`
- **THEN** the file SHALL have a `## Gaps` section
- **AND** the section SHALL list every body that is documented but
  NOT yet wired (marked `**DLT source**: NOT YET WIRED`)
- **AND** SHALL list every body whose URL is NOT yet in the OSINT
  allowlist

#### Scenario: The gap inventory feeds the follow-up change pipeline

- **WHEN** the operator runs
  `mise run cianchosaint:osint:health-check`
- **THEN** the health check SHALL cross-reference the gap inventory
- **AND** SHALL suggest which follow-up openspec change would close
  each gap (e.g. "NAO is NOT YET WIRED → follow-up
  `cianchosaint-nao-pipeline-v1` would close this gap")

### Requirement: The licence attribution + British Isles scope

The system SHALL enforce the licence ceiling (BUSL-1.1 — British Isles
public-sector bodies only) across the catalogue, with every documented
body being a verified British Isles public-sector body.

#### Scenario: Every body is a British Isles public-sector body

- **WHEN** the operator reads any topic file in
  `docs/source-catalogue/`
- **THEN** every documented body SHALL be a British Isles public-sector
  body (per `LICENSE.md` § Additional Use Grant)
- **AND** the body's URL SHALL be the official `.gov.uk` /
  `.gov.ie` / `.police.uk` / `.judiciary.uk` / Crown Dependency
  equivalent

#### Scenario: No foreign bodies in the catalogue

- **WHEN** the operator runs `mise run lint:license`
- **THEN** the linter SHALL verify no foreign body (e.g. FBI / CIA /
  BND) appears in the catalogue
- **AND** SHALL fail with exit code 1 if any foreign body is found
  (the licence explicitly bans them)

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../../docs/source-catalogue/README.md`](../../docs/source-catalogue/README.md) — the master catalogue
- [`../../dlt_sources/cianchosaint/common/osint_allowlist.yaml`](../../dlt_sources/cianchosaint/common/osint_allowlist.yaml) — the OSINT allowlist
- [`../../dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`](../../dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py) — the per-constituency cohort registry
- [`../../dlt_sources/cianchosaint/political_parties/_registry.py`](../../dlt_sources/cianchosaint/political_parties/_registry.py) — the per-political-party registry
- [`../cianchosaint-pipeline/spec.md`](../cianchosaint-pipeline/spec.md) — the data pipeline umbrella
- [`../cianchosaint-per-constituency-dlt-sources/spec.md`](../cianchosaint-per-constituency-dlt-sources/spec.md) — the per-constituency DLT sources
- [`../cianchosaint-intelligence-agency-pipeline/spec.md`](../cianchosaint-intelligence-agency-pipeline/spec.md) — the intelligence agency pipeline
- [`../cianchosaint-political-party-pipeline/spec.md`](../cianchosaint-political-party-pipeline/spec.md) — the political party pipeline
