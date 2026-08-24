# cianchosaint-bipp-v2 Capability

## Purpose

`cianchosaint-bipp-v2` is the **British Isles Political Accountability Pipeline (BIPP v2)** — the fourth flagship sub-pipeline of cianchosaint (parallel to BIPP v1 / BIDP v1 / BIIP v1 / BIPP v2).

BIPP v2 ingests from the **87 Gemini Deep Research PDFs** in `leabharlann/gemini_deep_research/politics/` (read-only context) and from **6 sub-national official source families** across the 8 British Isles jurisdictions, structured into **7 thematic cohorts**:

| # | Cohort | Sub-cohort themes | Primary leabharlann PDFs |
|--:|---|---|---|
| 1 | **Reform UK accountability** | Single-entity pilot (Richard Tice + Reform UK press releases + Electoral Commission returns + Companies House) | `reform_richard_tice_debt_fraud.pdf` + `reform_corruption.pdf` + `clacton_farage_reform_refusal.pdf` + `farage_20reform_20uk_20crypto_20oversight.pdf` + `farage_s_failed_political_history_research_plan.pdf` |
| 2 | **Reform UK devolved branches** (NI + Scotland) | Reform UK NI + Reform UK Scotland devolved branches | `farage_clacton_opposition_research_blueprint.md` + the devolved-branch press releases |
| 3 | **Northern Ireland political accountability** | Sinn Féin funding + DUP + NI Assembly + Arlene Foster + Burnham/Streeting + whistleblower investigations | `sinn_f_in_data_funding_and_foreign_influence.pdf` + `sinn_f_in_history_and_funding_inquiry.pdf` + `burnham_streeting_compromised_assets.pdf` + `arlene_foster_research_plan_generation.pdf` + `whistleblower_investigates_scottish_officials.pdf` |
| 4 | **Scottish political accountability** | Sturgeon + SNP + Scottish Labour + Scottish Conservatives + Russell Group whistleblowers + Russell Group donor networks | `sturgeon_political_history_research_plan.pdf` + `russell_group_whistleblower_protocol_inquiry.pdf` + `whistleblower_investigates_scottish_officials.pdf` |
| 5 | **Welsh + London political accountability** | London boroughs + Plaid Cymru + Kneecap investigation + Kneecap band + Veolia outsourcing | `london_boroughs_funding_and_cleanliness_investigation.pdf` + `veolia_outsourcing_and_neglect_investigation.pdf` + `kneecap_band_business_and_youth_concerns.pdf` + `kneecap_deep_dive_investigation.pdf` + `royal_family_kneecap_and_irish_cities.pdf` |
| 6 | **ROI political accountability** | Fine Gael coalition + Sinn Féin ROI + Varadkar controversy + Galway by-election + Irish political strategy | `farrell_sinn_f_in_and_united_ireland_rhetoric.pdf` + `fine_gael_coalition_strategy_analysis.pdf` + `irish_political_strategy_and_performance_analysis.pdf` + `varadkar_controversies_and_political_future.pdf` + `galway_by_election_media_analysis.pdf` + `galway_west_election_candidate_analysis.pdf` |
| 7 | **Cross-cutting intelligence / cybersecurity** | Intelligence agency job cycles + propaganda + Russian/US cyber + Russian influence + radicalization prevention + crypto group investigation + cyber defence | `intelligence_disinformation_and_geopolitics.pdf` + `intelligence_agency_software_job_cycles.pdf` + `propaganda_language_and_intelligence_agencies.pdf` + `russia_us_cyber_influence_comparison.pdf` + `cybersecurity_strategy_for_british_isles.pdf` + `british_isles_cyber_defense_strategy.pdf` + `crypto_group_investigation_and_takedown.pdf` + `investigating_radicalization_and_venues.pdf` + `radicalization_manipulation_and_prevention_strategies.pdf` + `uk_intelligence_jobs_belfast_vs_london.pdf` + `uk_security_job_eligibility_research.pdf` |

**Total cohorts: 7 × 6-8 jurisdictions = ~50 BIPP v2 cohorts.**

## Background

Per the user's request on 2026-08-24:
> "using those output documents to show via cianchosaint how gardai can selfhost develop prompts take advantage of langfuse evals type agentic ai analytics of the official sources based on themese and utilising the gemini_deep_research/politics topics"

The 87 PDFs in `leabharlann/gemini_deep_research/politics/` are the canonical source-of-truth for every BIPP v2 thematic cohort. They are **read-only context** for the BAML extraction functions (per the canonical cianchosaint OSINT ceiling).

The previous cianchosaint pipeline (BIPP v1 / BIDP v1 / BIIP v1 / BIPP v2) covered:
- BIPP v1 — British Isles Policing Pipeline (53 forces × 7 domains = ~371 cohorts)
- BIDP v1 — British Isles Defence Pipeline (4 UK services + Irish DF + doctrine series = 64 cohorts)
- BIIP v1 — British Isles Intelligence Oversight Pipeline (6 oversight bodies × 8 document kinds = 48 cohorts)
- BIPP v2 — British Isles Political Party Pipeline (24 parties × 6 jurisdictions = 24 cohorts)

BIPP v2 (this spec) is **distinct from** the existing `cianchosaint-political-party-pipeline`. The existing political-party pipeline covers the 24 active parties' press releases. BIPP v2 (this spec) covers the **political-accountability investigations** of those parties + the cross-cutting intelligence / cybersecurity vertical.

The composite-pilot pattern follows `cianchosaint-reform-uk-pilot-workflow` (per `openspec/changes/archive/2026-08-23-cianchosaint-reform-uk-pilot-workflow-v1/specs/cianchosaint-reform-uk-pilot-workflow/spec.md`). The Reform UK accountability cohort (#1 above) extends the existing Reform UK pilot to multi-party + multi-jurisdiction dossiers.

The Langfuse prompt management foundation (per `openspec/specs/cianchosaint-langfuse-prompt-management/spec.md`) provides the load-bearing infrastructure for all 7 BIPP v2 BAML extraction functions. Every BIPP v2 BAML function uses the `LangfusePromptResolver` pattern.

## Requirements

### Requirement: The 7 thematic cohorts

The system SHALL provide the 7 BIPP v2 thematic cohorts per the cohort matrix in §Purpose.

#### Scenario: Each cohort has a canonical cohort_id

- **WHEN** the operator inspects the BIPP v2 cohort registry at `dlt_sources/cianchosaint/bipp_v2/_registry.py`
- **THEN** the registry SHALL enumerate all 7 cohorts with `cohort_id`, `cohort_name`, `source_pdfs`, `primary_sources`, `secondary_sources`, `milestone_gate`

### Requirement: The 50 cohort DLT sources

The system SHALL provide the 50 cohort DLT source modules (~7 cohorts × 6-8 jurisdictions).

#### Scenario: Each DLT source is in the OSINT allowlist

- **WHEN** the operator runs `mise run lint:license`
- **THEN** the CI gate SHALL pass (every URL is on `dlt_sources/cianchosaint/common/osint_allowlist.yaml`)

### Requirement: The 7 BAML extraction schemas

The system SHALL provide the 7 BIPP v2 BAML extraction functions (one per cohort), each using the `LangfusePromptResolver` pattern.

#### Scenario: Every BAML function uses the LangfusePromptResolver

- **WHEN** the operator inspects any `.baml` file in `baml_src/cianchosaint/politics/bipp_v2/`
- **THEN** the file SHALL declare `resolver "langfuse"` + `resolver_args { prompt_name "<canonical>" }` for every function

### Requirement: The 7 CocoIndex flows

The system SHALL provide the 7 BIPP v2 CocoIndex flows (one per cohort) that embed the leabharlann PDFs (read-only context) + the per-cohort DLT sources.

#### Scenario: Each flow mounts a LanceDB table keyed on (cohort, jurisdiction)

- **WHEN** the operator runs `mise run ciandchosaint:bipp:v2:m1`
- **THEN** the Dagster defs SHALL materialize the LanceDB tables for the Ireland cohorts
- **AND** the RAGAS faithfulness score SHALL be >= 0.70

### Requirement: The 3 milestone gates (m1 / m2 / m3 / ga)

The system SHALL provide the 3 BIPP v2 milestone gates.

#### Scenario: m1 — Republic of Ireland

- **WHEN** the operator runs `mise run cianchosaint:bipp:v2:m1`
- **THEN** the Ireland sources SHALL be ingested (7 cohorts × 1 jurisdiction = 7 cohorts minimum)
- **AND** the `ireland_political_accountability_documents_ingested_check` Dagster asset check SHALL pass

#### Scenario: m2 — United Kingdom

- **WHEN** the operator runs `mise run cianchosaint:bipp:v2:m2`
- **THEN** the NI + Scotland + Wales + England sources SHALL be ingested (7 cohorts × 4 jurisdictions = 28 cohorts)

#### Scenario: m3 — Crown Dependencies + v1 GA

- **WHEN** the operator runs `mise run cianchosaint:bipp:v2:m3`
- **THEN** the Jersey + Guernsey + Isle of Man sources SHALL be ingested (7 cohorts × 3 jurisdictions = 21 cohorts)

- **WHEN** the operator runs `mise run cianchosaint:bipp:v2:ga`
- **THEN** all 6-8 jurisdictions SHALL be ingested (~50 cohorts)
- **AND** the `all_british_isles_political_accountability_documents_ingested_check` SHALL pass

### Requirement: The BIPP v2 → BIPP v1 cross-reference

The system SHALL cross-reference every BIPP v2 cohort with the existing BIPP v1 political-party cohort (per the `cianchosaint-political-party-pipeline` spec).

#### Scenario: Every BIPP v2 cohort cites the relevant BIPP v1 political party

- **WHEN** the operator inspects a BIPP v2 dossier
- **THEN** the dossier SHALL include a `related_political_parties` field referencing the relevant BIPP v1 parties
- **AND** the cross-reference SHALL be populated by the per-persona agent (not auto-generated)

### Requirement: The composite pilot extension

The system SHALL extend the existing `reform_uk_pilot` (per `cianchosaint-reform-uk-pilot-workflow-v1`) to a 7-entity composite pilot.

#### Scenario: The composite pilot covers 7 entities

- **WHEN** the operator invokes the `composite_political_accountability_pilot` FunctionTool
- **THEN** the tool SHALL return 7 dossiers (one per BIPP v2 cohort)
- **AND** each dossier SHALL include the `source_pdf_urls` field referencing the corresponding leabharlann PDFs
- **AND** the `osint_ceiling_enforced` + `analyst_review_required` flags SHALL be True

### Requirement: The OSINT allowlist extension

The system SHALL extend `dlt_sources/cianchosaint/common/osint_allowlist.yaml` with the new BIPP v2 URLs.

#### Scenario: Every BIPP v2 URL is on the allowlist

- **WHEN** the operator runs `mise run lint:license`
- **THEN** the CI gate SHALL pass

### Requirement: The cross-cutting intelligence cohort

The system SHALL provide the 7th cohort (`cross_cutting_intelligence_cybersecurity`) covering intelligence agency job cycles + propaganda + Russian/US cyber + radicalization prevention.

#### Scenario: The 7th cohort has 11 leabharlann PDFs

- **WHEN** the operator inspects `baml_src/cianchosaint/politics/bipp_v2/extract_intelligence_cybersecurity_dossier.baml`
- **THEN** the file SHALL cite the 11 PDFs listed in §Purpose cohort 7
- **AND** the BAML function SHALL extract entity relationships + propaganda patterns + cyber indicators

## Cross-references

- [`../../../openspec/changes/cianchosaint-bipp-v2-spec-v1/proposal.md`](../../../openspec/changes/cianchosaint-bipp-v2-spec-v1/proposal.md) — the change proposal
- [`../../../openspec/changes/cianchosaint-bipp-v2-spec-v1/tasks.md`](../../../openspec/changes/cianchosaint-bipp-v2-spec-v1/tasks.md) — the change tasks
- [`../../../openspec/changes/cianchosaint-bipp-v2-spec-v1/specs/cianchosaint-bipp-v2/spec.md`](../../../openspec/changes/cianchosaint-bipp-v2-spec-v1/specs/cianchosaint-bipp-v2/spec.md) — the spec delta
- [`../../../openspec/specs/cianchosaint-pipeline/spec.md`](../../../openspec/specs/cianchosaint-pipeline/spec.md) — the umbrella pipeline spec
- [`../../../openspec/specs/cianchosaint-political-party-pipeline/spec.md`](../../../openspec/specs/cianchosaint-political-party-pipeline/spec.md) — the existing political-party pipeline spec
- [`../../../openspec/specs/cianchosaint-langfuse-prompt-management/spec.md`](../../../openspec/specs/cianchosaint-langfuse-prompt-management/spec.md) — the Langfuse prompt management spec
- [`../../../openspec/specs/cianchosaint-political-graph/spec.md`](../../../openspec/specs/cianchosaint-political-graph/spec.md) — the Cognee+Graphiti graph spec (planned)