# Spec Delta: cianchosaint-pipeline

This delta is applied by the openspec change
[`cianchosaint-repo-foundation-v1`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-pipeline/spec.md`](../../../../specs/cianchosaint-pipeline/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: Repo skeleton + tightened licence

The system SHALL provide a new repo `cianfhoghlaim/cianchosaint` with
the canonical skeleton (AGENTS.md + README.md + pyproject.toml +
mise.toml + package.json + openspec/) and a `LICENSE.md` containing
the Business Source License 1.1 — CIANCHOSAINT edition with the
Additional Use Grant for British Isles public-sector bodies, the
3-step foreign-use gate, and the warrant-to-enforce clause for
licencees.

#### Scenario: Licence body contains the 3-step foreign-use gate

- **WHEN** the operator opens `LICENSE.md`
- **THEN** the document SHALL contain a section titled
  "Conditional foreign use — the 3-step gate"
- **AND** the gate SHALL list STEP 1 (EXPLAIN), STEP 2 (DO US A
  FAVOUR), and STEP 3 (MAYBE) in that order
- **AND** STEP 2 SHALL list the 4 EXHAUSTIVE exemplars (reciprocal
  OSINT access, treaty-level cooperation, diplomatic recognition,
  open-source contribution under AGPL v3.0)

#### Scenario: Licence body contains the warrant-to-enforce clause

- **WHEN** the operator opens `LICENSE.md`
- **THEN** the document SHALL contain a section titled
  "Warrant to enforce — granted to the licencees"
- **AND** the section SHALL grant to every British Isles body named
  in the Additional Use Grant (Ireland, UK, Crown Dependencies) the
  right to enforce the licence terms
- **AND** the section SHALL specify the trigger conditions in a
  separate "Trigger conditions for the warrant-to-enforce" section
  covering both publicly observable evidence (production deployment,
  derivative works, source copy-paste) AND credible written complaints

### Requirement: 4-tier model provider chain

The system SHALL provide a `ModelProviderRouter` module at
`baml_src/_shared/provider_router.py` that routes every LLM call
through a 4-tier fallback chain: (1) Unsloth Studio local API,
(2) LiteLLM Proxy, (3) MiniMax Token Plan, (4) Gemini API.

#### Scenario: Primary provider is Unsloth Studio

- **WHEN** a BAML extraction function requests an LLM completion
- **THEN** the `ModelProviderRouter` SHALL first attempt the call
  against Unsloth Studio at `http://unsloth-serve:8889/api/v1`
- **AND** the call SHALL have a 30-second timeout
- **AND** the response SHALL be logged in Langfuse with the
  `provider_used` span attribute set to `"unsloth_studio"`

#### Scenario: Fallback to LiteLLM after primary failure

- **WHEN** the Unsloth Studio request fails (HTTP 5xx or timeout)
- **AND** the circuit-breaker for Unsloth Studio is closed
- **THEN** the router SHALL record the failure against Unsloth
  Studio's circuit-breaker
- **AND** SHALL attempt the call against the LiteLLM Proxy at
  `https://litellm.cianfhoghlaim.ie`
- **AND** the response SHALL be logged in Langfuse with the
  `fallback_reason` attribute set to `"unsloth_5xx"` or
  `"unsloth_timeout"`

#### Scenario: Circuit breaker opens after 3 consecutive failures

- **WHEN** the Unsloth Studio provider fails 3 consecutive times
- **THEN** its circuit-breaker SHALL transition to the OPEN state
- **AND** SHALL remain open for a configurable reset window
  (default 60 seconds)
- **AND** subsequent calls SHALL skip the Unsloth Studio provider
  entirely until the circuit-breaker resets
- **AND** the circuit-breaker state SHALL be emitted as a Langfuse
  span attribute `circuit_breaker_state`

### Requirement: OSINT source URL allowlist

The system SHALL maintain a strict allowlist of source URLs at
`dlt_sources/cianchosaint/common/osint_allowlist.yaml` containing
every public official-government source that may be ingested.

#### Scenario: Source not in allowlist is rejected at scaffold time

- **GIVEN** a developer adds a new DLT source pointing at
  `https://example.gov.uk/feed`
- **AND** that URL is NOT in
  `dlt_sources/cianchosaint/common/osint_allowlist.yaml`
- **WHEN** the developer runs `mise run lint:license`
- **THEN** the lint SHALL exit with code 1
- **AND** SHALL emit a structlog error pointing at the offending URL

#### Scenario: Allowlist entry must reference a British Isles body

- **GIVEN** an entry in `osint_allowlist.yaml` with
  `body: "us_department_of_justice"`
- **WHEN** the developer runs `mise run lint:license`
- **THEN** the lint SHALL exit with code 1
- **AND** SHALL emit a structlog error stating that the body is
  outside the British Isles

### Requirement: Wholesale migration of 8 assets from Cianfhoghlaim

The system SHALL migrate wholesale 8 specific assets from the
Cianfhoghlaim repo:

1. `dlt_sources/official_media/hmgcc/rolling_window.py` → `dlt_sources/cianchosaint/hmgcc/rolling_window.py`
2. `dlt_sources/official_media/ggy/sources.py` → `dlt_sources/cianchosaint/ggy/sources.py`
3. `dlt_sources/official_media/sct/sources.py` → `dlt_sources/cianchosaint/sct/sources.py`
4. `dlt_sources/official_media/wls/sources.py` → `dlt_sources/cianchosaint/wls/sources.py`
5. `dlt_sources/official_media/iom/sources.py` → `dlt_sources/cianchosaint/iom/sources.py`
6. `dlt_sources/official_media/jsy/sources.py` → `dlt_sources/cianchosaint/jsy/sources.py`
7. `dlt_sources/official_media/allowlist.py` → `dlt_sources/cianchosaint/common/allowlist.py`
8. `baml_src/processing/official_media.baml` → `baml_src/cianchosaint/processing/official_media.baml`

#### Scenario: Each migrated asset gets the cianchosaint namespace

- **WHEN** the migration lands in cianchosaint
- **THEN** every migrated `.py` file SHALL have its imports rewritten
  from `from dlt_sources.official_media.X` to
  `from dlt_sources.cianchosaint.X`
- **AND** every migrated `.baml` file SHALL have its imports rewritten
  from `from baml_src.processing.X` to
  `from baml_src.cianchosaint.processing.X`

#### Scenario: Each migrated asset gets a LICENCE attribution header

- **WHEN** the migration lands in cianchosaint
- **THEN** every migrated file SHALL start with a comment block
  stating `Original: cianfhoghlaim/cianfhoghlaim @ <commit-sha>` and
  `Migrated to cianchosaint: <date>` and `Licence: BUSL-1.1 (per LICENSE.md)`

### Requirement: Per-spec AGENTS.md convention

Every `openspec/specs/<spec-name>/` directory SHALL ship with a
sibling `AGENTS.md` file (≤30 lines) following the canonical 6-section
outline (routing sentence, quick start, key sources, adjacent specs,
DO NOT, skill pointers).

#### Scenario: New spec without AGENTS.md fails validation

- **GIVEN** a developer creates
  `openspec/specs/<new-spec>/spec.md`
- **AND** does NOT create `openspec/specs/<new-spec>/AGENTS.md`
- **WHEN** the developer runs `openspec validate <new-spec> --strict`
- **THEN** the validation SHALL exit with code 1
- **AND** SHALL emit a structlog error pointing at the missing
  AGENTS.md file

#### Scenario: AGENTS.md longer than 30 lines fails validation

- **GIVEN** a developer's `openspec/specs/<spec-name>/AGENTS.md`
  exceeds 30 lines
- **WHEN** the developer runs `openspec validate <spec-name> --strict`
- **THEN** the validation SHALL exit with code 1
- **AND** SHALL emit a structlog error stating the line count

### Requirement: Cross-repo openspec sync documentation

The system SHALL require every openspec change touching >1 repo
(cianchosaint + cianfhoghlaim + leabharlann) to include a
`cross-repo-sync.md` file at `openspec/changes/<id>/cross-repo-sync.md`
listing:

1. The commit plan for each repo
2. The branch name + remote URL for each push target
3. The order of operations (which repo MUST be committed first)

#### Scenario: Cross-repo change omits cross-repo-sync.md fails validation

- **GIVEN** a developer creates `openspec/changes/<id>/` that
  declares `Affected repos: cianchosaint, cianfhoghlaim`
- **AND** does NOT include `cross-repo-sync.md`
- **WHEN** the developer runs `openspec validate <id> --strict`
- **THEN** the validation SHALL exit with code 1
- **AND** SHALL emit a structlog error pointing at the missing file

#### Scenario: Cross-repo-sync.md specifies the correct commit order

- **GIVEN** a change touches cianfhoghlaim + cianchosaint
- **WHEN** the developer runs `openspec validate <id> --strict`
- **THEN** the validator SHALL verify that the cross-repo-sync.md
  file specifies cianfhoghlaim commits BEFORE cianchosaint commits
- **AND** SHALL exit with code 0 if the order is correct

### Requirement: BIPP v1 sub-pipeline (British Isles Policing Pipeline)

The system SHALL provide the BIPP v1 sub-pipeline ingesting 53 forces
× 7 domains = ~371 cohorts. The 53 forces include the 43 UK
territorial forces (England + Wales + Scotland) plus the PSNI, the
Metropolitan Police, Police Scotland, the 4 Welsh forces, the British
Transport Police, and the Crown Dependencies police forces (States of
Jersey Police, Bailiwick of Guernsey Police, Isle of Man
Constabulary). The 7 domains are street-level crime, stop & search,
outcomes, anti-social behaviour, police workforce, FOI responses,
and press releases.

#### Scenario: BIPP v1 milestone gate m1 (Ireland ROI)

- **WHEN** the operator runs `mise run cianchosaint:bipp:v1:m1`
- **THEN** the An Garda Síochána sources SHALL be ingested (14
  cohorts: 7 domains × 2 jurisdictions: ROI + UK-wide)
- **AND** the `ireland_policing_documents_ingested_check` Dagster
  asset check SHALL pass (cohort count >= 14)
- **AND** the `ireland_policing_extractions_ragas_check` SHALL pass
  (RAGAS faithfulness score >= 0.70)
- **AND** the `ireland_policing_lance_chunks_check` SHALL pass
  (chunk count >= 14_000)

### Requirement: BIDP v1 sub-pipeline (British Isles Defence Pipeline)

The system SHALL provide the BIDP v1 sub-pipeline ingesting 4 UK
services + Irish DF + UK MoD + 2 doctrine series = 64 cohorts. The
2 doctrine series are the JSP (Joint Service Publications) and JDP
(Joint Doctrine Publications) collections.

#### Scenario: BIDP v1 milestone gate m1 (UK services)

- **WHEN** the operator runs `mise run cianchosaint:bidp:v1:m1`
- **THEN** the UK MoD, RAF, Royal Navy, and British Army sources
  SHALL be ingested (32 cohorts: 4 services × 8 doctrinal
  categories)
- **AND** the `uk_defence_documents_ingested_check` Dagster asset
  check SHALL pass (cohort count >= 32)
- **AND** the `uk_defence_extractions_ragas_check` SHALL pass
  (RAGAS faithfulness score >= 0.70)
- **AND** the `uk_defence_lance_chunks_check` SHALL pass (chunk
  count >= 32_000)

### Requirement: BIIP v1 sub-pipeline (British Isles Intelligence Oversight Pipeline)

The system SHALL provide the BIIP v1 sub-pipeline ingesting 6
oversight bodies × 8 document kinds = 48 cohorts. The 6 oversight
bodies are UK ISC, UK IPCO, UK IPT, NI Policing Board, ROI Policing
Authority, and Garda Inspectorate.

#### Scenario: BIIP v1 milestone gate m1 (UK oversight bodies)

- **WHEN** the operator runs `mise run cianchosaint:biip:v1:m1`
- **THEN** the UK ISC, UK IPCO, and UK IPT sources SHALL be ingested
  (24 cohorts: 3 bodies × 8 document kinds)
- **AND** the `uk_oversight_documents_ingested_check` Dagster asset
  check SHALL pass (cohort count >= 24)
- **AND** the `uk_oversight_extractions_ragas_check` SHALL pass
  (RAGAS faithfulness score >= 0.70)
- **AND** the `uk_oversight_lance_chunks_check` SHALL pass (chunk
  count >= 24_000)
