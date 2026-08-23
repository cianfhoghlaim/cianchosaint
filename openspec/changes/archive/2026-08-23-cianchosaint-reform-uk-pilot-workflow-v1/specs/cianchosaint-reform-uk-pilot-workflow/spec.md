# Spec Delta: cianchosaint-reform-uk-pilot-workflow

This delta is applied by the openspec change
[`cianchosaint-reform-uk-pilot-workflow-v1`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-reform-uk-pilot-workflow/spec.md`](../../../../specs/cianchosaint-reform-uk-pilot-workflow/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: The Reform UK pilot FunctionTool

The system SHALL provide a `reform_uk_pilot_tool` FunctionTool at
`agents/cianchosaint/tools/reform_uk_pilot.py` that:

1. Invokes `dlt_sources.cianchosaint.political_parties.uk.reform_uk.reform_uk_source()`
   to ingest Reform UK press releases.
2. Cross-references the records with
   `dlt_sources.cianchosaint.uk.intelligence_oversight.investigatory_powers_bill_evidence`
   (the IPB evidence source).
3. Invokes the `ExtractReformUkDossier` BAML extraction function
   (per the next Requirement) to produce a structured `ReformUkDossier` dict.
4. Returns the dict for analyst review — NEVER directly submits to
   operational systems.

The FunctionTool SHALL accept 3 parameters:
- `target_entity` (default: `"Richard Tice"`)
- `focus` (default: `"2024 election debt fraud"`)
- `jurisdiction` (default: `"uk_hoc"`)

The FunctionTool SHALL return a dict conforming to the `ReformUkDossier`
schema (per the next Requirement), including the
`osint_ceiling_enforced: true` and `analyst_review_required: true`
flags at all times.

#### Scenario: The FunctionTool returns a structured dossier

- **WHEN** a per-persona agent (the `ciafagent-ga-public` web app)
  invokes `reform_uk_pilot_tool(target_entity="Richard Tice", focus="2024 election debt fraud")`
- **THEN** the FunctionTool SHALL return a `ReformUkDossier` dict with
  the 13 canonical fields (dossier_id, target_entity, focus,
  jurisdiction, mentions_entities, mentions_donors,
  mentions_companies_house, mentions_investigatory_powers,
  osint_ceiling_enforced, licence_posture, analyst_review_required,
  source_pdf_urls, created_at)
- **AND** `osint_ceiling_enforced` SHALL be `true`
- **AND** `analyst_review_required` SHALL be `true`
- **AND** `licence_posture` SHALL be `"BUSL-1.1 v2 (British-Isles-only)"`

#### Scenario: The FunctionTool respects the OSINT ceiling

- **WHEN** the FunctionTool attempts to ingest a record whose source URL
  is NOT in the OSINT allowlist
  (`dlt_sources/cianchosaint/common/osint_allowlist.yaml` +
  `dlt_sources/official_media_cianchosaint/fixtures/allowlist_parties.yaml`)
- **THEN** the FunctionTool SHALL skip the record (not include it in the
  dossier) and log a warning
- **AND** SHALL NOT bypass the allowlist check under any circumstances

### Requirement: The ExtractReformUkDossier BAML extraction function

The system SHALL provide an `ExtractReformUkDossier` BAML extraction
function at `baml_src/cianchosaint/politics/reform_uk_pilot_extraction.baml`
that:

1. Accepts a string input (the Reform UK press release text + IPB
   evidence cross-reference text).
2. Returns a `ReformUkDossier` record conforming to the schema defined
   in the same file.
3. Uses the existing 4-tier client chain from `baml_src/clients.baml`
   (`Primary` → `Fallback` → `Emergency` → `Gemini`).

The `ReformUkDossier` schema SHALL have the 13 canonical fields
listed in the previous Requirement's Scenario.

#### Scenario: The BAML function extracts a structured dossier

- **WHEN** the operator runs
  `python -c "from baml_client import b; print(b.ExtractReformUkDossier('Reform UK press release: Richard Tice announces...'))"`
- **THEN** the returned `ReformUkDossier` SHALL include the dossier_id,
  target_entity, focus, jurisdiction, mentions_entities, mentions_donors,
  mentions_companies_house, mentions_investigatory_powers, and the 3
  conservative flags (osint_ceiling_enforced, licence_posture,
  analyst_review_required)
- **AND** SHALL be validated by the BAML runtime against the schema

#### Scenario: The BAML function never invents new factual claims

- **WHEN** the operator invokes `ExtractReformUkDossier` with content
  that does NOT mention a specific entity
- **THEN** the returned `ReformUkDossier.mentions_entities` SHALL be
  empty (the function SHALL NOT invent entities that are not in the
  input)
- **AND** the function SHALL NOT cite any source PDF URL that is NOT
  in the 4 leabharlann PDFs declared in the proposal.md

### Requirement: The reform-uk-pilot case study document

The system SHALL provide a case study document at
`docs/case-study/reform-uk-pilot.md` (~2,000-3,000 words) that
explains:

1. **Why Reform UK** — why Reform UK is the canonical pilot case study
   (the user's verified use case from 2026-08-23; the political-party
   pipeline covers 24 parties but Reform UK is the FIRST pilot).
2. **Inputs to the workflow** — the 2 DLT sources (reform_uk.py + IPB
   evidence) + the 4 leabharlann PDFs (read-only context).
3. **Outputs** — the structured `ReformUkDossier` JSON (the 13 canonical
   fields).
4. **Pilot scope** — single entity (Richard Tice), single focus (2024
   election debt fraud), single source PDF.
5. **Validation criteria** — manual review by a public-sector analyst
   before any law-enforcement-grade action; the platform NEVER
   directly submits forms to operational systems.
6. **OSINT ceiling + licence posture** — BUSL-1.1 v2, British-Isles-
   only Additional Use Grant, 3-step foreign-use gate, warrant-to-
   enforce clause, OSINT allowlist.

#### Scenario: The case study document is the canonical narrative

- **WHEN** the operator opens `docs/case-study/reform-uk-pilot.md`
- **THEN** the file SHALL be 2,000-3,000 words
- **AND** SHALL cite the 4 leabharlann PDFs in the References section
- **AND** SHALL explicitly state the conservative posture (no direct
  submission to operational systems; analyst review required)
- **AND** SHALL reference the BUSL-1.1 v2 licence posture

#### Scenario: The case study document cross-references the per-persona web app

- **WHEN** the operator reads the case study document
- **THEN** the document SHALL reference
  `web/apps/ciafagent-ga-public/` as the per-persona web surface that
  invokes the `reform_uk_pilot_tool`
- **AND** SHALL reference `agents/cianchosaint/tools/reform_uk_pilot.py`
  as the FunctionTool that the per-persona agent invokes
