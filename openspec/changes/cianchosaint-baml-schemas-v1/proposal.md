# Change: cianchosaint-baml-schemas-v1

## Why

The `cianchosaint-bootstrap-v2` spec (archived) wholesale-copied the
Cianfhoghlaim BAML extraction framework into cianchosaint, but the
**per-vertical BAML extraction functions** for the seven Q3 verticals
have not been authored yet:

1. Irish law (`baml_src/cianchosaint/processing/irish_legal_extraction.baml`)
2. UK 43 police forces via data.police.uk (`met_police_extraction.baml`)
3. PSNI + NI Justice + NI Policing Board (`psni_extraction.baml`)
4. UK military doctrine (`uk_military_extraction.baml`)
5. Defence Forces of Ireland (`ireland_defence_forces_extraction.baml`)
6. Intelligence oversight: ISC + IPCO + IPT + IPB (`intelligence_oversight_extraction.baml`)
7. Shared political-party extraction (`political_party_extraction.baml`)
8. Reform UK pilot dossier refinement (`reform_uk_dossier_extraction.baml`)

The wholesale-copied `baml_src/clients.baml` already declares the 4-tier
client chain (`Primary` → `Fallback` → `Emergency` → `LastResort`)
per the `cianchosaint-bootstrap-v2` spec, plus 7 placeholder
extraction functions (`ExtractDefencePublication`, `ExtractCourtJudgment`,
`ExtractStatuteReference`, `ExtractPoliceCrimeStatistics`,
`ExtractStopAndSearchRecord`, `ExtractIntelligenceOversightReport`,
`ExtractCrossJurisdictionFinding`). The wholesale-copied wholesale
copies at `baml_src/cianchosaint/processing/party.baml` +
`baml_src/cianchosaint/politics/reform_uk_pilot_extraction.baml`
already define the shared party schema + the Reform UK dossier
schema as placeholders.

This change authorises the per-vertical extraction functions,
refines the two wholesale-copied placeholders to the canonical
schema, and enforces the BUSL-1.1 v2 licence + OSINT ceiling on
every extraction.

## What Changes

- **1 NEW canonical spec**: `cianchosaint-baml-schemas` with 4 ADDED
  Requirements (per-vertical extraction contract + per-jurisdiction
  enum + conservative-posture guard + BAML runtime validation gate).
- **8 NEW BAML files** under `baml_src/cianchosaint/processing/` +
  `baml_src/cianchosaint/politics/`:
  - `irish_legal_extraction.baml` — `ExtractCourtJudgment` +
    `ExtractStatuteReference` + `ExtractFOIARequest`
  - `met_police_extraction.baml` — `ExtractMETPressRelease` +
    `ExtractStopAndSearchRecord` + `ExtractCrimeStatistics`
  - `psni_extraction.baml` — `ExtractPSNIPressRelease` + `ExtractNIJustice` +
    `ExtractPolicingBoardReport`
  - `uk_military_extraction.baml` — `ExtractMODPressRelease` +
    `ExtractRAFDoctrine` + `ExtractRoyalNavyDoctrine` +
    `ExtractBritishArmyDoctrine` + `ExtractJSPDoctrine` + `ExtractJDPDoctrine`
  - `ireland_defence_forces_extraction.baml` — `ExtractIDFPressRelease` +
    `ExtractIDFWhitePaper`
  - `intelligence_oversight_extraction.baml` — `ExtractISCReport` +
    `ExtractIPCOReport` + `ExtractIPTDecision` + `ExtractInvestigatoryPowersBillEvidence`
  - `political_party_extraction.baml` — `ExtractPartyPressRelease`
    (the SHARED schema, supersedes the wholesale-copied
    `baml_src/cianchosaint/processing/party.baml`)
  - `reform_uk_dossier_extraction.baml` — `ExtractReformUkDossier`
    (refines the wholesale-copied
    `baml_src/cianchosaint/politics/reform_uk_pilot_extraction.baml`)

## Capabilities

### New Capabilities
- `cianchosaint-baml-schemas`: The 12+ BAML extraction functions for
  the per-constituency verticals — Irish law, UK 43 forces via
  data.police.uk, PSNI + NI Justice + NI Policing Board, UK military
  doctrine, Defence Forces of Ireland, intelligence oversight, shared
  political-party extraction, Reform UK pilot dossier.

### Modified Capabilities
- `cianchosaint-pipeline` — the per-vertical extraction functions are
  the input layer for the pipeline.

## Impact

- 8 NEW BAML files under `baml_src/cianchosaint/processing/` +
  `baml_src/cianchosaint/politics/`
- 1 NEW canonical spec at `openspec/specs/cianchosaint-baml-schemas/`
- 8 functions per the wholesale-copied `baml_src/clients.baml` are
  reused (this change does NOT modify the 4-tier client chain)
- DAG: depends on `cianchosaint-bootstrap-v2` (archived) for the
  wholesale-copied client infrastructure

## Dependencies

- `Blocked by: cianchosaint-repo-bootstrap-v2` (archived) — the
  wholesale-copied 4-tier client chain at `baml_src/clients.baml`
  must exist before this change can author the extraction functions.
- `Affected repos: cianchosaint` (Cianfhoghlaim is NOT touched).

## Cross-references

- [`baml_src/clients.baml`](../../../baml_src/clients.baml) — the
  4-tier client chain (wholesale-copied from Cianfhoghlaim)
- [`openspec/specs/cianchosaint-bootstrap-v2/spec.md`](../../specs/cianchosaint-bootstrap-v2/spec.md) —
  the wholesale-copy umbrella spec
- [`openspec/specs/cianchosaint-pipeline/spec.md`](../../specs/cianchosaint-pipeline/spec.md) —
  the data pipeline umbrella
- [`LICENSE.md`](../../../LICENSE.md) — the BUSL-1.1 v2 licence
  posture
