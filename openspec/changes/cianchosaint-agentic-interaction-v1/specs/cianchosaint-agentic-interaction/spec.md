# Spec Delta: cianchosaint-agentic-interaction

This delta is applied by the openspec change
[`cianchosaint-agentic-interaction-v1`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-agentic-interaction/spec.md`](../../../../specs/cianchosaint-agentic-interaction/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: Agentic interaction layer (Google ADK + 4-tier provider chain)

The system SHALL provide an agentic interaction layer built on
**Google ADK** that routes every LLM call through the existing
4-tier `ModelProviderRouter` (Unsloth Studio → LiteLLM → MiniMax Token
Plan → Gemini API) and exposes users (public-sector analysts AND
members of the public) to conversational access to British Isles
official OSINT sources via an AG-UI + CopilotKit web surface.

#### Scenario: ADK agent routes through Unsloth Studio first

- **GIVEN** a public-sector analyst at An Garda Síochána types
  "find every 2024 Act related to PULSE modernisation" into the
  Cian chat interface
- **WHEN** the Cian chat interface dispatches the query to the
  `ga_root_agent` Google ADK agent
- **THEN** the `ga_root_agent` SHALL first attempt to satisfy the
  query by routing the LLM call through Unsloth Studio at
  `http://unsloth-serve:8889/api/v1`
- **AND** the response SHALL be logged in Langfuse with the
  `provider_used` span attribute set to `"unsloth_studio"`
- **AND** the response SHALL cite the source URL for every BAML
  extraction result (e.g. `https://www.irishstatutebook.ie/eli/2024/act/12/enacted/en/xml`)

#### Scenario: ADK agent falls back to LiteLLM after Unsloth timeout

- **GIVEN** the Unsloth Studio request times out (>30 seconds) or
  returns HTTP 5xx
- **WHEN** the `ga_root_agent` retries the call
- **THEN** the `ModelProviderRouter` SHALL record the failure
  against Unsloth Studio's circuit-breaker
- **AND** SHALL fall back to the LiteLLM Proxy at
  `https://litellm.cianfhoghlaim.ie`
- **AND** the response SHALL be logged in Langfuse with the
  `fallback_reason` attribute set to `"unsloth_timeout"` or
  `"unsloth_5xx"`

#### Scenario: ADK agent uses the BrowserToolRouter for OSINT lookups

- **WHEN** the `ga_root_agent` needs to fetch a public statute page
  (e.g. `https://www.irishstatutebook.ie/eli/2024/act/12/enacted/en/xml`)
- **THEN** the agent SHALL dispatch the fetch through the
  `BrowserToolRouter` module
- **AND** the `BrowserToolRouter` SHALL first attempt to satisfy the
  fetch via Crawl4AI (open-source)
- **AND** SHALL fall back to Firecrawl `/scrape` if Crawl4AI fails
- **AND** SHALL fall back to Stagehand + headless Chrome if both
  Crawl4AI and Firecrawl fail

### Requirement: Form-filling agents (Google ADK FunctionTool)

The system SHALL provide Google ADK `FunctionTool` agents that help
members of the public fill out non-emergency forms on official British
Isles websites (Garda traffic violation reports, MET non-emergency
contact forms, PSNI non-emergency contact forms) via conversation.
The agents MUST NOT directly submit forms to operational systems
(PULSE, crime-recording databases); they MUST generate the form
contents for the user to copy / paste into the official website.

#### Scenario: GA traffic violation form filler

- **GIVEN** a member of the public opens the Cian chat interface
- **AND** types "I need to report a non-emergency traffic violation
  that happened on the M50 yesterday"
- **WHEN** the Cian chat interface dispatches to the `ga_tutor_agent`
- **THEN** the `ga_tutor_agent` SHALL ask the user clarifying
  questions (location, time, vehicle registration, brief description)
- **AND** the agent SHALL generate the form contents in a structured
  format compatible with the official garda.ie traffic violation form
- **AND** the agent SHALL include a clear disclaimer that the user
  must copy the form contents and submit them on garda.ie themselves
- **AND** the agent SHALL NOT attempt to submit the form directly to
  PULSE or any operational system

#### Scenario: MET non-emergency contact form filler

- **GIVEN** a member of the public opens the Cian chat interface
  and selects "I want to report a non-emergency matter to the MET"
- **WHEN** the `met_tutor_agent` is invoked
- **THEN** the agent SHALL use the same form-filling pattern as the
  GA agent, adapted to met.police.uk's form schema
- **AND** the agent SHALL cite the met.police.uk URL the user should
  visit to submit the form

### Requirement: Lateralised GA + irishstatutebook.ie + courts.ie pipelines

The system SHALL lateralise the existing Cianfhoghlaim legal data
pipelines (DLT sources + BAML schemas + CocoIndex flows) to power
the GA agentic interaction layer. Specifically:

- **Irish Statute Book DLT source**
  (`dlt_sources/british_isles/ireland/law/irish_statute_book.py`)
  → re-used as the canonical source for irishstatutebook.ie
- **Courts.ie DLT source** (`dlt_sources/british_isles/ireland/law/courts_ie.py`)
  → re-used for courts.ie forms + judgements + fees + rules
- **5 Ireland-law BAML files**
  (`baml_src/british_isles/ireland/education/law/`) → re-used as the
  BAML extraction schemas for the GA agent
- **Ireland legal CocoIndex embedding**
  (`cocoindex_flows/british_isles/ireland/ireland_legal_embedding.py`)
  → re-used for the LanceDB namespace

The cross-repo mirror (not migration) is documented in
`cross-repo-sync.md`.

#### Scenario: GA agent queries irishstatutebook.ie via lateralised pipeline

- **WHEN** the `ga_root_agent` receives a query about an Irish
  statute (e.g. "what does section 15 of the Criminal Justice (Theft
  & Fraud Offences) Act 2001 say?")
- **THEN** the agent SHALL route the query through the
  `BrowserToolRouter` to fetch the canonical statute page from
  `irishstatutebook.ie`
- **AND** the agent SHALL extract the structured statute reference
  using the BAML `ExtractStatuteReference` schema from
  `baml_src/british_isles/ireland/education/law/shared_legal_enums.baml`
- **AND** the response SHALL include the canonical citation (e.g.
  "[2001] Act No. 50/2001, Section 15") and the source URL

#### Scenario: GA agent lateralises courts.ie judgements pipeline

- **WHEN** the `ga_root_agent` receives a query about a recent Irish
  court judgment (e.g. "what did the Supreme Court decide in
  [2025] IESC 12?")
- **THEN** the agent SHALL query the lateralised courts.ie DLT
  source via `md:cianchosaint.courts_ie.judgements`
- **AND** SHALL extract the judgment text using the BAML
  `ExtractJudgement` schema from
  `baml_src/british_isles/ireland/education/law/judgements.baml`

### Requirement: MET + PSNI new pipelines

The system SHALL provide new DLT sources + BAML schemas for MET
(London) + PSNI (Northern Ireland) police force OSINT. These are
NEW builds (not lateralised from Cianfhoghlaim — Cianfhoghlaim does
not have these pipelines).

- **MET DLT source**: `dlt_sources/cianchosaint/uk/met_police/data_police_uk.py`
  (43 UK forces via `data.police.uk` API)
- **PSNI DLT source**: `dlt_sources/cianchosaint/ni/psni/press_releases.py`
  + `justice_ni.py`
- **MET BAML schema**: `baml_src/cianchosaint/processing/met_police.baml`
- **PSNI BAML schema**: `baml_src/cianchosaint/processing/psni.baml`

#### Scenario: MET agent queries data.police.uk

- **WHEN** the `met_root_agent` receives a query about a specific UK
  police force (e.g. "what was the crime rate in Manchester last
  month?")
- **THEN** the agent SHALL query the lateralised MET DLT source via
  `md:cianchosaint.met_police.crime_statistics`
- **AND** SHALL extract the structured crime statistics using the
  BAML `ExtractCrimeStatistics` schema

#### Scenario: PSNI agent queries psni.police.uk press releases

- **WHEN** the `psni_root_agent` receives a query about recent PSNI
  announcements (e.g. "what has PSNI said about cross-border
  policing in the last 30 days?")
- **THEN** the agent SHALL query the PSNI DLT source via
  `md:cianchosaint.psni.press_releases`
- **AND** SHALL extract the structured press releases using the
  BAML `ExtractPSNIPressRelease` schema

### Requirement: Lateralised AG-UI + CopilotKit web surface

The system SHALL provide per-constituency web surfaces built on
TanStack Start + Convex + AG-UI + CopilotKit, lateralising the
existing Cianfhoghlaim patterns at
`web/apps/cianfhoghlaim-leaving-cert/packages/i18n/`.

- **GA public-facing**: `web/apps/cianchosaint-ga-public/`
- **GA internal-facing**: `web/apps/cianchosaint-ga-internal/`
- **MET public-facing**: `web/apps/cianchosaint-met-public/`
- **MET internal-facing**: `web/apps/cianchosaint-met-internal/`
- **PSNI public-facing**: `web/apps/cianchosaint-psni-public/`
- **PSNI internal-facing**: `web/apps/cianchosaint-psni-internal/`
- **Self-hosted citizen**: `web/apps/cianchosaint-self-host/`

#### Scenario: GA public-facing web surface connects to GA agent

- **WHEN** a member of the public visits `ga.cianchosaint.ie`
- **THEN** the web surface SHALL display the AG-UI chat interface
  connected to the `ga_root_agent` Google ADK agent
- **AND** the interface SHALL display the active provider tier
  (e.g. "powered by Unsloth Studio; LiteLLM fallback")
- **AND** the interface SHALL include a privacy disclaimer that the
  user is interacting with an AI assistant, not a Garda officer

#### Scenario: GA internal-facing web surface for Garda members

- **WHEN** an authenticated Garda member visits
  `ga-internal.cianchosaint.ie`
- **THEN** the web surface SHALL display additional capabilities
  NOT available to the public: cross-reference to PULSE schema,
  internal circulars, training materials
- **AND** authentication SHALL be via PocketID + BetterAuth (per
  the existing Cianfhoghlaim pattern)

### Requirement: Self-hosted citizen Docker image

The system SHALL provide a self-hosted citizen Docker image at
`docker/cianchosaint-citizen/` that allows a member of the public to
run Cian on their own machine, using Crawl4AI + Stagehand +
Unsloth Studio + LiteLLM as the open-source stack (no SaaS
dependency). The Docker image SHALL include a Locket sidecar for
secret injection and a private Pangolin resource pattern for
optional secure remote access.

#### Scenario: Citizen runs self-hosted Docker image

- **GIVEN** a member of the public downloads the
  `docker/cianchosaint-citizen/` Docker Compose bundle
- **WHEN** they run `docker compose up -d`
- **THEN** the bundle SHALL start: (1) the Cian AG-UI web
  interface on `http://localhost:7777`, (2) the Locket sidecar for
  secret injection, (3) the Unsloth Studio local API on
  `http://localhost:8889`, (4) the LiteLLM Proxy on
  `http://localhost:4000`, (5) the Crawl4AI worker on
  `http://localhost:11235`
- **AND** the citizen SHALL be able to chat with Cian about British
  Isles official OSINT sources (irishstatutebook.ie, courts.ie,
  data.police.uk, etc.) without sending any data to a SaaS

#### Scenario: Self-hosted citizen uses MiniMax Token Plan as fallback

- **GIVEN** the citizen's local Unsloth Studio is unavailable
  (hardware too old, container crashed, etc.)
- **WHEN** the citizen's `deployment-choice.yaml` has
  `provider_chain: [unsloth_studio, litellm, minimax_token_plan, gemini_api]`
- **THEN** the `ModelProviderRouter` SHALL fall back to MiniMax
  Token Plan via the citizen's own MiniMax API key
- **AND** SHALL fall back to Gemini API if MiniMax Token Plan is
  also unavailable
