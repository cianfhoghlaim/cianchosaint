# cianchosaint-baml-schemas Capability

## Purpose

`cianchosaint-baml-schemas` captures the contract for the 12+ BAML
extraction functions that author the per-constituency vertical
extraction layer. The wholesale-copied 4-tier client chain at
`baml_src/clients.baml` (per `cianchosaint-bootstrap-v2`) is the
canonical transport; this spec captures the
**per-vertical extraction contract** + the per-jurisdiction enum +
the conservative-posture guard + the BAML runtime validation gate.

## Background

Cianchosaint has 7 per-constituency verticals (Irish law, UK 43
forces, PSNI + NI Justice, UK military, Defence Forces of Ireland,
intelligence oversight, shared political-party). Each vertical
needs a BAML extraction function that takes raw press-release /
statute / doctrine HTML/Markdown and returns a typed Pydantic /
BAML class.

The wholesale-copied `baml_src/clients.baml` already declares the
4-tier client chain. This spec authors the per-vertical classes +
the `Extract<X>` functions + the conservative-posture enforcement
+ the BAML runtime validation gate.

## Requirements

### Requirement: The 7 per-vertical BAML extraction schemas

The system SHALL provide 7 per-vertical BAML extraction schemas at
`baml_src/cianchosaint/processing/` (or `baml_src/cianchosaint/politics/`
for the political-party + Reform UK dossiers):

1. **Irish law** (`irish_legal_extraction.baml`) — `ExtractCourtJudgment` +
   `ExtractStatuteReference` + `ExtractFOIARequest`
2. **UK 43 police forces via data.police.uk** (`met_police_extraction.baml`) —
   `ExtractMETPressRelease` + `ExtractStopAndSearchRecord` +
   `ExtractCrimeStatistics`
3. **PSNI + NI Justice + NI Policing Board** (`psni_extraction.baml`) —
   `ExtractPSNIPressRelease` + `ExtractNIJustice` + `ExtractPolicingBoardReport`
4. **UK military doctrine** (`uk_military_extraction.baml`) —
   `ExtractMODPressRelease` + `ExtractRAFDoctrine` +
   `ExtractRoyalNavyDoctrine` + `ExtractBritishArmyDoctrine` +
   `ExtractJSPDoctrine` + `ExtractJDPDoctrine`
5. **Defence Forces of Ireland** (`ireland_defence_forces_extraction.baml`) —
   `ExtractIDFPressRelease` + `ExtractIDFWhitePaper`
6. **Intelligence oversight** (`intelligence_oversight_extraction.baml`) —
   `ExtractISCReport` + `ExtractIPCOReport` + `ExtractIPTDecision` +
   `ExtractInvestigatoryPowersBillEvidence`
7. **Shared political-party** (`political_party_extraction.baml`) —
   `ExtractPartyPressRelease` (the SHARED schema for all 24 parties)
8. **Reform UK pilot dossier** (`reform_uk_dossier_extraction.baml`) —
   `ExtractReformUkDossier` (refines the wholesale-copied pilot)

#### Scenario: Every BAML extraction function uses the 4-tier client chain

- **WHEN** the operator inspects any of the 8 NEW BAML files
- **THEN** every function SHALL declare `client Primary` (or a named
  variant of the 4-tier chain from `baml_src/clients.baml`)
- **AND** SHALL NOT declare a new client (the 4-tier chain is the
  canonical source of truth)

#### Scenario: Every BAML extraction function declares the conservative posture

- **WHEN** the operator inspects any of the 8 NEW BAML files
- **THEN** every class SHALL include the conservative-posture fields
  (`osint_ceiling_enforced: bool`, `licence_posture: string`,
  `analyst_review_required: bool`) with sensible defaults
- **AND** every function prompt SHALL explicitly forbid inventing new
  factual claims

### Requirement: The per-jurisdiction enum + per-vertical BranchType

The system SHALL define consistent jurisdiction enums (`UK`, `IRELAND`,
`NI`, `SCOTLAND`, `WALES`, `JERSEY`, `GUERNSEY`, `IOM`) and BranchType
enums (`MetropolitanPolice`, `PSNI`, `AnGarda`, `UKMoD`, `DefenceForcesOfIreland`)
across the 8 NEW BAML files, ensuring downstream CocoIndex flows can
filter by jurisdiction + branch type.

#### Scenario: Per-jurisdiction enum covers all 8 British Isles jurisdictions

- **WHEN** the operator inspects the per-vertical BAML classes
- **THEN** every class that records jurisdiction SHALL use the canonical
  8-value British Isles enum
- **AND** SHALL NOT introduce new jurisdiction enums for non-British
  Isles geographies

### Requirement: Conservative-posture guard on every extraction

The system SHALL enforce the conservative-posture contract
(per `LICENSE.md` + the `cianchosaint-bootstrap-v2` spec) on every
BAML extraction function:

- `osint_ceiling_enforced` SHALL be `true` by default
- `licence_posture` SHALL be `"BUSL-1.1 v2 (British-Isles-only)"`
- `analyst_review_required` SHALL be `true` by default
- Functions SHALL NOT invent new factual claims that are not in the
  input; lists SHALL be left empty rather than hallucinated

#### Scenario: The extraction never invents new factual claims

- **WHEN** a per-persona agent invokes a BAML extraction function with
  content that does NOT mention a specific entity
- **THEN** the returned class's `mentions_entities` (or equivalent list
  field) SHALL be empty
- **AND** the function SHALL NOT cite any source URL that is NOT on
  the OSINT allowlist at
  `dlt_sources/cianchosaint/common/osint_allowlist.yaml`

### Requirement: BAML runtime validation gate

The system SHALL provide a BAML runtime validation gate that:

1. Validates every BAML file under `baml_src/` against the BAML
   schema (when `baml-cli` is available)
2. Validates that every function's `client` references one of the
   4 named clients in `baml_src/clients.baml` (`Primary`,
   `Fallback`, `Emergency`, `LastResort`)
3. Validates that every class includes the conservative-posture
   fields

#### Scenario: The BAML runtime validates every extraction

- **WHEN** the operator runs `baml-cli validate baml_src/cianchosaint/`
- **THEN** the BAML runtime SHALL validate every class + function
  against the BAML schema
- **AND** SHALL exit with code 0 if all extractions are well-formed

#### Scenario: The conservative-posture gate fires on missing fields

- **WHEN** a developer adds a NEW BAML class without the
  conservative-posture fields
- **THEN** the BAML runtime (when wired to the `mise run
  baml:lint-extractions` task) SHALL raise a
  `ConservativePostureViolation`
- **AND** SHALL exit with code 1

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../cianchosaint-bootstrap-v2/spec.md`](../cianchosaint-bootstrap-v2/spec.md) —
  the wholesale-copy umbrella spec (source of the 4-tier client chain)
- [`../cianchosaint-pipeline/spec.md`](../cianchosaint-pipeline/spec.md) —
  the data pipeline umbrella
- [`../cianchosaint-source-catalogue/spec.md`](../cianchosaint-source-catalogue/spec.md) —
  the 17-domain British Isles source catalogue
- [`../cianchosaint-reform-uk-pilot-workflow/spec.md`](../cianchosaint-reform-uk-pilot-workflow/spec.md) —
  the Reform UK pilot (uses `ExtractReformUkDossier`)
