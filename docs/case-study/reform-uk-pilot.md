# Reform UK Pilot Case Study

> Per the openspec/changes/cianchosaint-reform-uk-pilot-workflow-v1/
> specs/cianchosaint-reform-uk-pilot-workflow/spec.md, this case study
> is the canonical narrative for the Reform UK pilot workflow.
>
> Per the locked plan **Q12 = B**, the pilot starts with a SINGLE entity
> (Richard Tice + 2024 election debt fraud PDF) and validates the
> workflow before expanding.

## Why Reform UK?

Reform UK is the canonical pilot case study for the cianchosaint
platform for three converging reasons: a verified user use case, a
well-defined OSINT allowlist, and a politically-accountable vertical
that exercises both the political-party and intelligence-oversight
pipelines end-to-end.

**The verified user use case.** On 2026-08-23 the user explicitly
clarified the platform's scope, stating: *"political party official
resources for use by the aforementioned intelligence agencies as a
source of information to help investigations of such example case
studies as reform uk corruption and similar topics"*. This statement
is load-bearing: it establishes that political party official
resources are a lawful OSINT input to the cianchosaint intelligence /
investigation workflows, AND that Reform UK corruption is the
canonical first case study. The platform's political-party pipeline
(`cianchosaint-political-party-pipeline`, archived 2026-08-23) covers
24 active parties across the British Isles — but Reform UK is the
**FIRST** pilot by design, not by accident. The user's verified use
case elevates it from one-of-24 to the canonical pilot.

**The OSINT allowlist.** Reform UK's official website
(`https://www.reformparty.uk/news`) is in the cianchosaint OSINT
allowlist at `dlt_sources/official_media_cianchosaint/fixtures/
allowlist_parties.yaml`. This is critical because the cianchosaint
licence posture — BUSL-1.1 v2 with the British-Isles-only Additional
Use Grant — explicitly forbids ingesting source URLs outside the
allowlist. Every DLT source URL must be auditable back to a
documented allowlist entry. Reform UK clears this bar cleanly.

**The politically-accountable vertical.** Reform UK exercises both
upstream pipelines that the cianchosaint platform offers for
political-accountability investigations:

1. The political-party DLT source at
   `dlt_sources/cianchosaint/political_parties/uk/reform_uk.py` (the
   Reform UK press releases).
2. The intelligence-oversight DLT source at
   `dlt_sources/cianchosaint/uk/intelligence_oversight/investigatory_powers_bill_evidence.py`
   (the Investigatory Powers Bill evidence submissions).

A pilot that exercises both pipelines validates the cross-reference
contract — the workflow that joins political-party outputs with
intelligence-oversight inputs. This is the architectural pattern the
platform needs to validate before any expansion to multi-entity or
cross-jurisdiction dossiers.

The OSINT ceiling posture is enforced at every layer: the source
URL allowlist at the DLT source layer, the schema validation at the
BAML extraction layer, the conservative flags at the FunctionTool
layer, and the per-persona UI at the web app layer. The pilot is
**not** a "search the entire web for Reform UK corruption" exercise
— it is a narrowly-scoped, allowlist-bounded, analyst-reviewed
investigation dossier.

The BUSL-1.1 v2 licence posture is similarly layered: the source
PDFs are read-only context (the pilot does not generate new factual
claims from the PDFs — only references them in the `source_pdf_urls`
field of the dossier); the FunctionTool output includes the
`osint_ceiling_enforced: true` and `analyst_review_required: true`
flags at all times; and the per-persona web app
(`web/apps/ciafagent-ga-public/`) renders the dossier for human
review ONLY.

## Inputs to the workflow

The Reform UK pilot workflow consumes three input layers, in order
of increasing breadth.

**Layer 1 — Reform UK press releases (the primary input).** The
political-party pipeline (`cianchosaint-political-party-pipeline`,
archived 2026-08-23) ships a dedicated DLT source at
`dlt_sources/cianchosaint/political_parties/uk/reform_uk.py`. This
source defines `ReformUKPipeline(PoliticalPartyPipelineBase)` with
the canonical attributes:

```python
PARTY_ID = "reform-uk"
PARTY_NAME = "Reform UK"
JURISDICTION = "uk_hoc"
SOURCE_BASE = "https://www.reformparty.uk/news"
ELECTORAL_COMMISSION_ID = "PP-12345"  # Reform UK's Electoral Commission ID (verify)
```

The source crawls `https://www.reformparty.uk/news` (max 50 pages,
max depth 3) and yields a `reform_uk_press_releases` resource (merge
write disposition, `natural_key` primary key). Each record carries
the `party_id`, `party_name`, `jurisdiction`, and
`electoral_commission_id` fields, which downstream BAML extraction
uses to enrich the dossier.

**Layer 2 — Investigatory Powers Bill evidence submissions (the
cross-reference input).** The intelligence-oversight pipeline
(`cianchosaint-intelligence-agency-pipeline`, archived 2026-08-23)
ships a DLT source at
`dlt_sources/cianchosaint/uk/intelligence_oversight/investigatory_powers_bill_evidence.py`.
This source crawls `https://bills.parliament.uk/bills/2687` (the IP
Bill page on bills.parliament.uk) and yields written evidence
submissions from civil society, industry, and agencies. The cross-
reference with the Reform UK press releases is conservative: the
FunctionTool only cites IPB evidence submissions that explicitly
mention Reform UK or a Reform UK politician. Unrelated IPB evidence
submissions are skipped, not hallucinated into the dossier.

**Layer 3 — The 4 leabharlann source PDFs (read-only context).**
The pilot cross-references four source PDFs from the leabharlann
corpus at `/Users/cianmacandeisigh/dev/kings_college_galway/leabharlann/
gemini_deep_research/politics/`. These PDFs are stored in a SEPARATE
git repo (leabharlann, per the cianfhoghlaim AGENTS.md hard rule)
and are read-only context for the pilot — the pilot does NOT
generate new factual claims from the PDFs, only references them in
the `source_pdf_urls` field of the dossier.

The 4 PDFs are:

1. **`reform_richard_tice_debt_fraud.pdf`** — the primary case-study
   PDF, the 2024 election debt fraud allegation against Richard Tice.
   This is the SINGLE source PDF for the pilot (per Q12 = B).
2. **`reform_corruption.pdf`** — broader Reform UK corruption
   context. Read-only reference for the `mentions_entities` field.
3. **`clacton_farage_reform_refusal.pdf`** — the Clacton / Farage
   lens. Read-only reference for the constituency dimension of the
   dossier.
4. **`farage_20reform_20uk_20crypto_20oversight.pdf`** — Farage +
   Reform UK + crypto oversight. Read-only reference for the
   crypto-policy dimension of the dossier.

The pilot does NOT use the 3 broader leabharlann PDFs (`intelligence_disinformation_and_geopolitics.pdf`,
`garda_corruption_and_data_access.pdf`, `regulating_big_tech_in_british_isles.pdf`)
as inputs — they are read for context but are NOT in the
`source_pdf_urls` field of the dossier.

## Outputs

The pilot output is a single structured `ReformUkDossier` dict
returned by the `reform_uk_pilot_tool` FunctionTool. The dict has 13
canonical fields, defined in the BAML schema at
`baml_src/cianchosaint/politics/reform_uk_pilot_extraction.baml`:

| Field | Type | Description |
|:--|:--|:--|
| `dossier_id` | `string` | Auto-generated unique ID (e.g. `"reform-uk-pilot-richard-tice"`) |
| `target_entity` | `string` | The entity being investigated (default: `"Richard Tice"`) |
| `focus` | `string` | The investigation focus (default: `"2024 election debt fraud"`) |
| `jurisdiction` | `enum` | The constituency — `UK_HOC` / `ROI_DAIL` / `NI_ASSEMBLY` / `SENEDD` / `HOLYROOD` |
| `mentions_entities` | `string[]` | Entities mentioned in the cross-referenced input |
| `mentions_donors` | `string[]` | Donors mentioned in the cross-referenced input |
| `mentions_companies_house` | `string[]` | Companies House entity numbers / names mentioned in the input |
| `mentions_investigatory_powers` | `string[]` | IPB evidence submission IDs / titles mentioned in the input |
| `osint_ceiling_enforced` | `bool` | ALWAYS `true` (the conservative posture) |
| `licence_posture` | `string` | ALWAYS `"BUSL-1.1 v2 (British-Isles-only)"` |
| `analyst_review_required` | `bool` | ALWAYS `true` (no automated downstream action) |
| `source_pdf_urls` | `string[]` | The 4 leabharlann PDFs (read-only context) |
| `created_at` | `string` | ISO 8601 timestamp of the dossier creation |

The dict is rendered by the per-persona web app at
`web/apps/ciafagent-ga-public/` for analyst review. The per-persona
agent invokes the FunctionTool with the 3 default parameters
(`target_entity="Richard Tice"`, `focus="2024 election debt fraud"`,
`jurisdiction="uk_hoc"`) and the dossier is returned as JSON for
the analyst to inspect.

The BAML extraction function (`ExtractReformUkDossier`) is invoked
against the cross-referenced input (the Reform UK press releases
plus the IPB evidence submissions that mention Reform UK). The
function uses the 4-tier client chain from `baml_src/clients.baml`:
`Primary` (Unsloth Studio) → `Fallback` (LiteLLM) → `Emergency`
(MiniMax Token Plan) → `Gemini`. The router dynamically picks the
active provider based on circuit-breaker state, latency, and
per-deployment config (`deployment-choice.yaml`).

## Pilot scope

Per the locked plan **Q12 = B**, the pilot is intentionally
narrow:

- **SINGLE entity**: Richard Tice (the Reform UK chairman / former
  co-chairman). The pilot does NOT investigate every Reform UK
  politician, donor, or staffer.
- **SINGLE focus**: the 2024 election debt fraud allegation. The
  pilot does NOT investigate every Reform UK corruption topic.
- **SINGLE source PDF**:
  `leabharlann/gemini_deep_research/politics/reform_richard_tice_debt_fraud.pdf`.
  The 3 other leabharlann PDFs are read-only context.
- **SINGLE jurisdiction**: `uk_hoc` (UK House of Commons). The
  pilot does NOT cross-reference with NI Assembly, ROI Dáil, or
  Scottish Parliament records.

The pilot validates the workflow end-to-end BEFORE any expansion.
The 5-step validation chain is:

1. The FunctionTool returns a valid `ReformUkDossier` dict (Python
   type-check + BAML schema validation).
2. The 3 conservative flags are present and correctly set
   (`osint_ceiling_enforced: true`, `licence_posture` matches the
   literal, `analyst_review_required: true`).
3. The `source_pdf_urls` field is exactly the 4 leabharlann PDFs
   declared in the proposal.md — no other URLs.
4. The dossier is rendered by the per-persona web app for analyst
   review.
5. The analyst manually verifies the dossier against the 5
   validation criteria below.

A follow-up `cianchosaint-reform-uk-pilot-workflow-v2` change would
expand to multi-entity dossiers, cross-jurisdiction linking (e.g.
NI ↔ ROI), or Companies House bulk data cross-referencing — but only
after the v1 pilot has been validated by a public-sector analyst.

## Validation criteria

Per the OSINT ceiling + the BUSL-1.1 v2 licence posture, the pilot
is **NOT valid for law-enforcement-grade action**. The pilot
generates a structured dossier for **manual review by a public-
sector analyst** who verifies:

1. **Source URL provenance.** The Reform UK press releases cited in
   the dossier are from the canonical Reform UK source URL
   (`https://www.reformparty.uk/news`) and the source URL is in the
   OSINT allowlist at
   `dlt_sources/official_media_cianchosaint/fixtures/allowlist_parties.yaml`.
   The analyst cross-references each cited URL with the allowlist
   entry.

2. **Companies House filings.** Any Companies House filings cited
   in the dossier are from the canonical Companies House bulk data
   endpoint, and the entity names + officer names match the Reform
   UK donor/affiliate registry. Companies House filings that do not
   match are removed from the dossier.

3. **IPB evidence submissions.** Any IPB evidence submissions cited
   in the dossier are from the canonical
   `bills.parliament.uk/bills/2687` source URL. Unrelated IPB
   evidence submissions are removed.

4. **Leabharlann PDFs as read-only context.** The leabharlann
   source PDFs cited in the `source_pdf_urls` field are
   read-only context. The pilot does NOT generate new factual claims
   from the PDFs — only references them. If the analyst identifies
   factual claims that are not in the input, the dossier is
   rejected.

5. **Conservative flag compliance.** The dossier's
   `analyst_review_required = true` flag is respected — no
   automated downstream action is taken without human sign-off. The
   `osint_ceiling_enforced = true` flag is respected — no source URL
   outside the allowlist is included.

If any of the 5 validation criteria fail, the dossier is rejected
and the analyst logs the failure to the cianchosaint audit trail.
The pilot does NOT auto-retry, auto-correct, or auto-submit — the
analyst's manual sign-off is the terminal step.

## OSINT ceiling + licence posture

The cianchosaint platform operates under the **BUSL-1.1 v2 licence**
with the **British-Isles-only Additional Use Grant** (per
`LICENSE.md`). This licence posture has 4 components that govern
the Reform UK pilot:

1. **British-Isles-only scope.** The platform is strictly
   restricted to public-sector bodies of the Republic of Ireland,
   the United Kingdom of Great Britain and Northern Ireland, the
   Crown Dependencies (Jersey, Guernsey, Isle of Man), and their
   respective defence, security, intelligence, and policing bodies.

2. **3-step foreign-use gate.** Foreign use of the platform
   requires satisfaction of the 3-step gate: **Explain** (the
   foreign user explains their use case) → **Do us a favour** (the
   foreign user provides reciprocal access to their own OSINT
   sources) → **Maybe** (the licencees named in `LICENSE.md §
   Additional Use Grant` evaluate and either grant or deny). This
   gate is enforced at the per-persona UI layer.

3. **Warrant-to-enforce clause.** The warrant-to-enforce is held
   by every licencee named in `LICENSE.md § Additional Use Grant`.
   This means that any breach of the licence terms (e.g. attempting
   to use the platform for foreign intelligence, attempting to
   ingest source URLs outside the OSINT allowlist, attempting to
   bypass the analyst-review gate) can be enforced by the
   licencees.

4. **OSINT allowlist.** Every DLT source URL must be in the OSINT
   allowlist at
   `dlt_sources/official_media_cianchosaint/fixtures/allowlist_parties.yaml`
   (political parties) +
   `dlt_sources/cianchosaint/common/osint_allowlist.yaml` (broader
   British Isles official sources). The pilot's 2 input DLT sources
   (Reform UK + IPB evidence) are already in the allowlist. No new
   source URLs are added by this change.

The Reform UK pilot workflow respects all 4 components at every
layer:

- The DLT source layer respects component 4 (the OSINT allowlist).
- The BAML extraction layer respects components 1, 2, and 4 (the
  function never invents new factual claims that would extend the
  scope beyond the British Isles).
- The FunctionTool layer respects component 3 (the FunctionTool
  never directly submits to operational systems — the analyst's
  manual sign-off is the terminal step).
- The per-persona UI layer respects components 1, 2, and 3 (the UI
  renders the dossier for analyst review, not for automated
  downstream action).

The pilot is the **first** end-to-end demonstration of these 4
components working in concert. If the pilot validates successfully,
the pattern extends to multi-entity dossiers (v2), cross-
jurisdiction linking (v2), and Companies House bulk data cross-
referencing (v3) — each gated by its own follow-up openspec change.

## References

- The openspec spec:
  `openspec/specs/cianchosaint-reform-uk-pilot-workflow/spec.md`
- The openspec change:
  `openspec/changes/cianchosaint-reform-uk-pilot-workflow-v1/`
- The per-spec AGENTS.md:
  `openspec/specs/cianchosaint-reform-uk-pilot-workflow/AGENTS.md`
- The FunctionTool:
  `agents/cianchosaint/tools/reform_uk_pilot.py`
- The BAML extraction:
  `baml_src/cianchosaint/politics/reform_uk_pilot_extraction.baml`
- The political party pipeline (upstream, Change 4):
  `openspec/specs/cianchosaint-political-party-pipeline/spec.md`
- The intelligence agency pipeline (upstream, Change 3):
  `openspec/specs/cianchosaint-intelligence-agency-pipeline/spec.md`
- The per-constituency DLT sources (companion, Change 3):
  `openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md`
- The per-constituency agents (downstream consumer):
  `openspec/specs/cianchosaint-per-constituency-agents/spec.md`
- The data pipeline umbrella:
  `openspec/specs/cianchosaint-pipeline/spec.md`
- The Reform UK DLT source:
  `dlt_sources/cianchosaint/political_parties/uk/reform_uk.py`
- The IPB evidence DLT source:
  `dlt_sources/cianchosaint/uk/intelligence_oversight/investigatory_powers_bill_evidence.py`
- The 4 leabharlann source PDFs:
  - `leabharlann/gemini_deep_research/politics/reform_richard_tice_debt_fraud.pdf`
  - `leabharlann/gemini_deep_research/politics/reform_corruption.pdf`
  - `leabharlann/gemini_deep_research/politics/clacton_farage_reform_refusal.pdf`
  - `leabharlann/gemini_deep_research/politics/farage_20reform_20uk_20crypto_20oversight.pdf`
- The cianchosaint root agent routing:
  `AGENTS.md`
- The cianchosaint licence posture:
  `LICENSE.md`
- The cianchosaint openspec routing:
  `openspec/AGENTS.md`
