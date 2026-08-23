# Change: cianchosaint-reform-uk-pilot-workflow-v1

## Why

The `cianchosaint-political-party-pipeline-v1` change (archived) shipped
the 24 per-political-party DLT sources, including the canonical Reform UK
source at `dlt_sources/cianchosaint/political_parties/uk/reform_uk.py`.
The `cianchosaint-intelligence-agency-pipeline-v1` change (archived)
shipped the 5 UK intelligence agency DLT sources, including the
Investigatory Powers Bill evidence source at
`dlt_sources/cianchosaint/uk/intelligence_oversight/investigatory_powers_bill_evidence.py`.

These two pipelines provide the canonical input layer for **political-
accountability investigations** — but there is no workflow that
**cross-references** them, no BAML extraction that produces a
**structured investigation dossier**, and no FunctionTool that a
per-persona agent (the `ciafagent-ga-public` web app) can invoke.

Per the locked plan **Q12 = B**, the pilot starts with a SINGLE entity
(Richard Tice + the 2024 election debt fraud PDF in
`leabharlann/gemini_deep_research/politics/reform_richard_tice_debt_fraud.pdf`)
and validates the workflow before expanding to multi-entity or
cross-jurisdiction dossiers.

The pilot is conservative by design:
- It NEVER directly submits forms to operational systems.
- It generates the dossier for **analyst review ONLY**.
- The OSINT ceiling + the BUSL-1.1 v2 licence posture apply at every
  layer (the source URL allowlist, the BAML extraction, the FunctionTool
  output, and the per-persona UI).

## What changes

- **1 NEW canonical spec**: `cianchosaint-reform-uk-pilot-workflow` with
  3 ADDED Requirements:
  - Requirement: The Reform UK pilot FunctionTool
    (`agents/cianchosaint/tools/reform_uk_pilot.py`) that cross-references
    the political-party DLT source + the IPB evidence source
  - Requirement: The `ExtractReformUkDossier` BAML extraction function
    + the `ReformUkDossier` schema in
    `baml_src/cianchosaint/politics/reform_uk_pilot_extraction.baml`
  - Requirement: The reform-uk-pilot case study document at
    `docs/case-study/reform-uk-pilot.md` (the canonical narrative for
    the pilot scope + validation criteria + licence posture)

- **1 NEW FunctionTool** at
  `agents/cianchosaint/tools/reform_uk_pilot.py` — the
  `reform_uk_pilot_tool = FunctionTool(func=reform_uk_pilot)` that
  consumes both DLT sources + the BAML extraction function and returns a
  structured `ReformUkDossier` dict.

- **1 NEW BAML file** at
  `baml_src/cianchosaint/politics/reform_uk_pilot_extraction.baml` —
  the `ReformUkDossier` schema + the `ExtractReformUkDossier` extraction
  function (uses the existing 4-tier client chain from `baml_src/clients.baml`).

- **1 NEW case study document** at `docs/case-study/reform-uk-pilot.md` —
  the canonical narrative (~2,000-3,000 words) explaining why Reform UK
  is the canonical pilot, the workflow inputs + outputs, the pilot scope,
  the validation criteria, the OSINT ceiling + BUSL-1.1 v2 licence
  posture, and references to the 4 leabharlann source PDFs.

## Pilot scope (per Q12 = B)

- **SINGLE entity**: Richard Tice (the Reform UK chairman / former co-
  chairman). NOT every Reform UK politician, donor, or staffer.
- **SINGLE focus**: the 2024 election debt fraud allegation.
- **SINGLE source PDF**:
  `leabharlann/gemini_deep_research/politics/reform_richard_tice_debt_fraud.pdf`.
- **Companion cross-reference PDFs** (read-only context):
  - `leabharlann/gemini_deep_research/politics/reform_corruption.pdf`
  - `leabharlann/gemini_deep_research/politics/clacton_farage_reform_refusal.pdf`
  - `leabharlann/gemini_deep_research/politics/farage_20reform_20uk_20crypto_20oversight.pdf`

The pilot validates the workflow end-to-end before any expansion. A
follow-up `cianchosaint-reform-uk-pilot-workflow-v2` change would
expand to multi-entity dossiers, cross-jurisdiction linking (e.g.
NI ↔ ROI), or Companies House bulk data cross-referencing — but only
after the v1 pilot has been validated by a public-sector analyst.

## Impact

- Affected specs: 1 NEW spec (`cianchosaint-reform-uk-pilot-workflow/`).
- Affected code/config: 3 NEW files (1 FunctionTool + 1 BAML + 1 case
  study). ~250-400 LOC of new code.
- No secret values are written to disk: all keys resolve via
  `infisical://dev-baile/cianchosaint/...` template refs hydrated by
  mise + Locket.
- No DLT source is created (the 2 input sources already exist in
  `dlt_sources/cianchosaint/political_parties/uk/reform_uk.py` and
  `dlt_sources/cianchosaint/uk/intelligence_oversight/investigatory_powers_bill_evidence.py`).
- No BAML client is created (the `ExtractReformUkDossier` function uses
  the existing 4-tier client chain — `Primary` / `Fallback` / `Emergency` /
  `Gemini` — declared in `baml_src/clients.baml`).
- No new openspec specs are added beyond the 1 NEW spec above.

## Out of scope

- Multi-entity dossiers (e.g. all 7 Reform UK politicians). Covered by
  follow-up `cianchosaint-reform-uk-pilot-workflow-v2`.
- Companies House bulk data cross-referencing. Covered by follow-up
  `cianchosaint-companies-house-bulk-pipeline-v1`.
- Cross-jurisdiction linking (NI ↔ ROI). Covered by follow-up
  `cianchosaint-per-constituency-agents-v2`.
- Direct submission to operational systems (e.g. Companies House
  webhook, ICO complaint form). Explicitly FORBIDDEN per the BUSL-1.1
  licence posture — the pilot NEVER directly submits forms.
- The 3 remaining leabharlann PDFs (`intelligence_disinformation_and_geopolitics.pdf`,
  `garda_corruption_and_data_access.pdf`, `regulating_big_tech_in_british_isles.pdf`)
  are read for context but NOT used as inputs to the pilot dossier.

## Validation criteria (manual review)

Per the OSINT ceiling + the BUSL-1.1 v2 licence posture, the pilot is
NOT valid for law-enforcement-grade action. The pilot generates a
structured dossier for **manual review by a public-sector analyst**
who verifies:

1. The Reform UK press releases cited in the dossier are from the
   canonical Reform UK source URL (https://www.reformparty.uk/news) and
   the source URL is in the OSINT allowlist.
2. The Companies House filings cited (if any) are from the canonical
   Companies House bulk data endpoint and the entity names + officer
   names match the Reform UK donor/affiliate registry.
3. The Investigatory Powers Bill evidence submissions cited (if any) are
   from the canonical `bills.parliament.uk/bills/2687` source URL.
4. The leabharlann source PDFs cited are read-only context (the pilot
   does NOT generate new factual claims from the PDFs — only references
   them in the `source_pdf_urls` field of the dossier).
5. The dossier's `analyst_review_required = true` flag is respected — no
   automated downstream action is taken without human sign-off.

## Dependencies

`Blocked by: cianchosaint-political-party-pipeline-v1` (must archive
first; it has — archived 2026-08-23).
`Blocked by: cianchosaint-intelligence-agency-pipeline-v1` (must
archive first; it has — archived 2026-08-23).
`Blocked by (soft): cianchosaint-per-constituency-dlt-sources-v1`
(extends but doesn't block; archived 2026-08-23).
`Affected repos: cianchosaint.` (Cianfhoghlaim + leabharlann are
unchanged — the leabharlann PDFs are read-only context.)

## Cross-repo sync

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) and leabharlann
(`/Users/cianmacandeisigh/dev/kings_college_galway/leabharlann/` — a
separate repo per the cianfhoghlaim AGENTS.md) remain **completely
unchanged**.
