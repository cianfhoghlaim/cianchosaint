# cianchosaint-agentic-interaction Capability

## Purpose

`cianchosaint-agentic-interaction` is the umbrella capability for the
agentic interaction layer of the `cianchosaint` platform. It enables
British Isles public-sector bodies (An Garda Síochána, MET Police,
PSNI, the 4 Welsh forces, the devolved administrations, the Crown
Dependencies) AND members of the public (via the self-hosted citizen
option — see `cianchosaint-self-hosted-citizen` spec) to interact
conversationally with Cian — the open-source agentic assistant that
mediates access to official British Isles OSINT sources (irishstatutebook.ie,
courts.ie, data.police.uk, psni.police.uk, met.police.uk, gov.uk, etc.).

The umbrella subsumes three flagship interaction surfaces:

- **GA** — An Garda Síochána + Irish Defence Forces + the other Irish
  governmental bodies (per the `LICENSE.md` Additional Use Grant)
- **MET** — Metropolitan Police + the 43 UK territorial forces
- **PSNI** — Police Service of Northern Ireland + the NI Policing Board

The agentic layer is built on **Google ADK** (per the user's Gemini
hackathon experience — Cianfhoghlaim already has 12 agents built on
Google ADK at `agents/adk/`) and routes every LLM call through the
**4-tier ModelProviderRouter** (Unsloth Studio → LiteLLM → MiniMax
Token Plan → Gemini API) plus a **BrowserToolRouter** that dispatches
to Crawl4AI / Stagehand / Firecrawl / BrowserBase for browser
automation.

## Background

Cianfhoghlaim (the sibling education platform) has already built:
- A Google ADK root agent (`agents/adk/tuatha_root_agent.py`)
- 8 NCCA subject specialist agents (chem, engl, hist, etc.)
- The 4-tier ModelProviderRouter contract (per the
  `cianchosaint-repo-foundation-v1` openspec change)
- The 12-tool FirecrawlMCPClient wrapper
  (`agents/meaisinfhoghlaim/firecrawl_mcp/client.py`)
- AG-UI + CopilotKit per-subject web surfaces
  (`web/apps/cianfhoghlaim-leaving-cert/`)

Cianchosaint lateralises these patterns to the defence / policing /
intelligence-oversight domain. The agentic interaction layer is the
user-facing surface that turns the data pipeline (the
`cianchosaint-pipeline` umbrella) into actionable insights.
## Requirements
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

### Requirement: 7 per-persona web surfaces

The system SHALL provide 7 per-persona web surfaces that connect the
24 Google ADK agents (per `cianchosaint-per-constituency-agents`
spec) to the end users (British Isles public-sector analysts AND
members of the public). Each surface is a TanStack Start + Convex +
AG-UI + CopilotKit app.

#### Scenario: 7 per-persona surfaces ship from this change

- **WHEN** the operator runs `ls web/apps/`
- **THEN** the list SHALL include 7 surfaces:
  - `ciafagent-ga-public/` — An Garda Síochána public-facing AG-UI chat
  - `ciafagent-ga-internal/` — GA internal-facing (PULSE cross-ref + circulars)
  - `ciafagent-met-public/` — Metropolitan Police public-facing AG-UI chat
  - `ciafagent-met-internal/` — MET internal-facing
  - `ciafagent-psni-public/` — PSNI public-facing AG-UI chat
  - `ciafagent-psni-internal/` — PSNI internal-facing (NI Policing Board)
  - `ciafagent-self-host/` — the self-hosted citizen Docker entry point
- **AND** each SHALL adopt the combined template (per Q23 synthesis)
  from BOTH `web/apps/cianfhoghlaim-leaving-cert/` AND
  `web/apps/cianfhoghlaim-web/`
- **AND** each SHALL pass `mise run lint:web`

#### Scenario: Combined template (Q23 synthesis)

- **WHEN** the operator creates a new per-persona web app
- **THEN** the app SHALL adopt the per-app `packages/` structure
  (`auth`, `db`, `i18n`, `ui`, `convex`, `config`) from
  Cianfhoghlaim-leaving-cert
- **AND** SHALL adopt the per-app `baml_src/` for the BAML client
- **AND** SHALL adopt the AG-UI + CopilotKit integration pattern
- **AND** SHALL adopt the simple `apps/web` + `apps/api` + `convex`
  + `packages` layout from cianfhoghlaim-web
- **AND** SHALL use Turbo monorepo + Biome + Bun workspace
- **AND** SHALL use Convex v1.40+ + Zod v4 dependency pins
- **AND** SHALL NOT include the LC subject catalog (education-specific)
- **AND** SHALL NOT include the education i18n translations
- **AND** SHALL NOT include the LC subject BAML client

#### Scenario: Public vs internal surface separation

- **WHEN** the operator runs the public-facing surface
  (e.g. `ciafagent-ga-public/`)
- **THEN** the surface SHALL display a privacy disclaimer that the
  user is interacting with an AI assistant, NOT a Garda officer
- **AND** SHALL NOT attempt to submit forms directly to PULSE
- **AND** SHALL cite the official garda.ie URL the user must visit

- **WHEN** the operator runs the internal-facing surface
  (e.g. `ciafagent-ga-internal/`)
- **THEN** the surface SHALL require authentication via BetterAuth
  + PocketID + TinyAuth proxy
- **AND** SHALL display additional capabilities NOT available to the
  public: cross-reference to PULSE schema, internal circulars, training
  materials

#### Scenario: Self-hosted citizen surface

- **WHEN** the citizen runs `docker/ciafagent-self-host/`
- **THEN** the self-hosted surface SHALL display the AG-UI chat for
  Cian on `http://localhost:7777`
- **AND** SHALL route every LLM call through the 4-tier
  `ModelProviderRouter`
- **AND** SHALL NOT send any user data to a SaaS by default

### Requirement: 1 Hono API gateway (ciafagent-api)

The system SHALL provide a Hono API gateway that serves as the AG-UI
event source for all 7 per-persona apps. The gateway routes every
request to the appropriate Google ADK agent (per the
`cianchosaint-per-constituency-agents` spec).

#### Scenario: API gateway routes to the correct agent

- **WHEN** a per-persona app sends a request to `/api/agent/<root>`
  (where `<root>` ∈ `{ga, met, psni}`)
- **THEN** the gateway SHALL route the request to the corresponding
  root agent (`ga_root_agent`, `met_root_agent`, `psni_root_agent`)
- **AND** SHALL stream the AG-UI events back to the per-persona app
  via Server-Sent Events

#### Scenario: API gateway uses the 4-tier provider chain

- **WHEN** the gateway invokes any of the 24 Google ADK agents
- **THEN** the gateway SHALL route every LLM call through the
  4-tier `ModelProviderRouter` (Unsloth Studio primary → LiteLLM →
  MiniMax Token Plan → Gemini API)
- **AND** SHALL emit Langfuse span attributes `provider_used` +
  `fallback_reason` + `circuit_breaker_state` for observability

#### Scenario: API gateway authenticates via BetterAuth

- **WHEN** a per-persona internal-facing app sends a request to the
  gateway
- **THEN** the gateway SHALL validate the BetterAuth JWT token in
  the `Authorization: Bearer <token>` header
- **AND** SHALL reject the request with HTTP 401 if the token is
  invalid or expired
- **AND** SHALL log the rejection via structlog

#### Scenario: API gateway rate-limits per-agent

- **WHEN** a per-persona app sends > 100 requests/minute for a
  single agent
- **THEN** the gateway SHALL return HTTP 429 with a `Retry-After`
  header
- **AND** SHALL emit a Langfuse span attribute `rate_limited: true`
  so operators can spot abuse

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../cianchosaint-pipeline/spec.md`](../cianchosaint-pipeline/spec.md) — the data pipeline umbrella
- [`../cianchosaint-self-hosted-citizen/spec.md`](../cianchosaint-self-hosted-citizen/spec.md) — self-hosted deployment pattern
- [`../cianchosaint-per-constituency-agents/spec.md`](../cianchosaint-per-constituency-agents/spec.md) — per-constituency agents
