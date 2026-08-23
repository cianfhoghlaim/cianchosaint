# cianchosaint-reform-uk-pilot-workflow Capability

## Purpose

`cianchosaint-reform-uk-pilot-workflow` is the capability that
provides the **Reform UK pilot investigation dossier** — the FIRST
case-study pilot in the cianchosaint platform (per the locked plan
**Q12 = B** + the verified user use case from 2026-08-23:
*"political party official resources for use by the aforementioned
intelligence agencies as a source of information to help investigations
of such example case studies as reform uk corruption and similar topics"*).

The pilot cross-references:

1. The Reform UK political-party DLT source
   (`dlt_sources/cianchosaint/political_parties/uk/reform_uk.py` —
   shipped by `cianchosaint-political-party-pipeline-v1`).
2. The Investigatory Powers Bill evidence DLT source
   (`dlt_sources/cianchosaint/uk/intelligence_oversight/investigatory_powers_bill_evidence.py` —
   shipped by `cianchosaint-intelligence-agency-pipeline-v1`).
3. The 4 leabharlann source PDFs (read-only context):
   - `leabharlann/gemini_deep_research/politics/reform_richard_tice_debt_fraud.pdf`
     (the primary case-study PDF — Richard Tice + 2024 election debt fraud)
   - `leabharlann/gemini_deep_research/politics/reform_corruption.pdf`
     (Reform UK corruption — broader context)
   - `leabharlann/gemini_deep_research/politics/clacton_farage_reform_refusal.pdf`
     (Clacton / Farage — the constituency lens)
   - `leabharlann/gemini_deep_research/politics/farage_20reform_20uk_20crypto_20oversight.pdf`
     (Farage + Reform UK + crypto oversight — the crypto-policy lens)

The pilot is **conservative by design**:
- The FunctionTool NEVER directly submits forms to operational systems.
- The dossier is generated for **manual review by a public-sector
  analyst** ONLY.
- The OSINT ceiling + the BUSL-1.1 v2 licence posture apply at every
  layer.

## Background

The user explicitly verified (2026-08-23) that political party
official resources are a lawful OSINT input to the cianchosaint
intelligence / investigation workflows — and Reform UK is the FIRST
case-study pilot (per the locked plan Q12 = B).

The pilot validates the workflow end-to-end before any expansion.
A follow-up `cianchosaint-reform-uk-pilot-workflow-v2` change would
expand to multi-entity dossiers, cross-jurisdiction linking (e.g.
NI ↔ ROI), or Companies House bulk data cross-referencing — but only
after the v1 pilot has been validated by a public-sector analyst.

## Requirements

### Requirement: The Reform UK pilot FunctionTool

The system SHALL provide a `reform_uk_pilot_tool` FunctionTool at
`agents/cianchosaint/tools/reform_uk_pilot.py` that cross-references
the political-party DLT source + the IPB evidence source + the BAML
extraction function, and returns a structured `ReformUkDossier` dict
for analyst review.

#### Scenario: The FunctionTool returns a structured dossier

- **WHEN** a per-persona agent (the `ciafagent-ga-public` web app)
  invokes `reform_uk_pilot_tool(target_entity="Richard Tice", focus="2024 election debt fraud")`
- **THEN** the FunctionTool SHALL return a `ReformUkDossier` dict with
  the 13 canonical fields
- **AND** `osint_ceiling_enforced` SHALL be `true`
- **AND** `analyst_review_required` SHALL be `true`

#### Scenario: The FunctionTool respects the OSINT ceiling

- **WHEN** the FunctionTool encounters a record whose source URL is
  NOT in the OSINT allowlist
- **THEN** the FunctionTool SHALL skip the record and log a warning

### Requirement: The ExtractReformUkDossier BAML extraction function

The system SHALL provide an `ExtractReformUkDossier` BAML extraction
function at `baml_src/cianchosaint/politics/reform_uk_pilot_extraction.baml`
that accepts a string input and returns a `ReformUkDossier` record
conforming to the 13-field schema in the same file.

#### Scenario: The BAML function extracts a structured dossier

- **WHEN** the operator invokes `ExtractReformUkDossier` with Reform UK
  press release text
- **THEN** the returned `ReformUkDossier` SHALL include the dossier_id,
  target_entity, focus, jurisdiction, mentions_entities,
  mentions_donors, mentions_companies_house,
  mentions_investigatory_powers, and the 3 conservative flags

#### Scenario: The BAML function never invents new factual claims

- **WHEN** the operator invokes `ExtractReformUkDossier` with content
  that does NOT mention a specific entity
- **THEN** the returned `ReformUkDossier.mentions_entities` SHALL be
  empty (the function SHALL NOT invent entities)

### Requirement: The reform-uk-pilot case study document

The system SHALL provide a case study document at
`docs/case-study/reform-uk-pilot.md` (~2,000-3,000 words) that
explains the pilot scope, inputs, outputs, validation criteria, and
licence posture.

#### Scenario: The case study document is the canonical narrative

- **WHEN** the operator opens `docs/case-study/reform-uk-pilot.md`
- **THEN** the file SHALL be 2,000-3,000 words
- **AND** SHALL cite the 4 leabharlann PDFs in the References section
- **AND** SHALL explicitly state the conservative posture

#### Scenario: The case study document cross-references the per-persona web app

- **WHEN** the operator reads the case study document
- **THEN** the document SHALL reference `web/apps/ciafagent-ga-public/`
  as the per-persona web surface that invokes the FunctionTool

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document (BUSL-1.1 v2)
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../cianchosaint-pipeline/spec.md`](../cianchosaint-pipeline/spec.md) — the data pipeline umbrella
- [`../cianchosaint-political-party-pipeline/spec.md`](../cianchosaint-political-party-pipeline/spec.md) — the upstream political-party pipeline
- [`../cianchosaint-intelligence-agency-pipeline/spec.md`](../cianchosaint-intelligence-agency-pipeline/spec.md) — the upstream intelligence agency pipeline
- [`../cianchosaint-per-constituency-dlt-sources/spec.md`](../cianchosaint-per-constituency-dlt-sources/spec.md) — the per-constituency DLT sources (companion)
