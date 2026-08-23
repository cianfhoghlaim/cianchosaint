# Spec Delta: cianchosaint-agentic-interaction

This delta is applied by the openspec change
[`cianchosaint-per-persona-app-bundles-v1`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-agentic-interaction/spec.md`](../../../../specs/cianchosaint-agentic-interaction/spec.md)
that this change adds.

## ADDED Requirements

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
