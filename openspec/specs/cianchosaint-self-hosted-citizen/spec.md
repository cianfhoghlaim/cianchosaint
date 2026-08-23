# cianchosaint-self-hosted-citizen Capability

## Purpose

`cianchosaint-self-hosted-citizen` is the capability that enables
members of the British Isles public to run Cian — the open-source
agentic assistant — on their own machine (Docker container + Locket
sidecar + private Pangolin resource) without sending any data to a
SaaS. The self-hosted citizen option is the consumer-side
counterpart to the public-sector-facing per-constituency agent
surfaces (see `cianchosaint-per-constituency-agents`).

## Background

The `LICENSE.md` Additional Use Grant covers use by British Isles
public-sector bodies. Members of the public using cianchosaint for
personal interaction with their own government's services are now
covered by the **Natural Person Citizen Grant** (per the
`cianchosaint-citizen-use-grant` spec, archived 2026-08-23), which
extends the licence to grant citizen self-host use, conditioned on:
(i) the citizen is a natural person of the British Isles, (ii) the
citizen's own machine, (iii) no commercial monetisation, (iv) no
public-facing deployment, (v) no foreign use.

The self-hosted citizen option is now **production-ready** for
natural persons of the British Isles, subject to the 5 binding
constraints in the Natural Person Citizen Grant.

## Requirements

### Requirement: Self-hosted Docker Compose bundle

The system SHALL provide a Docker Compose bundle at
`docker/cianchosaint-citizen/` that includes:
- The Cian AG-UI web interface
- A Locket sidecar for secret injection
- The Unsloth Studio local API
- The LiteLLM Proxy
- The Crawl4AI worker
- The Stagehand + headless Chrome worker (when BrowserBase is
  disabled; when BrowserBase is enabled, Stagehand connects to the
  cloud)
- The MotherDuck / DuckLake reader (read-only token)

#### Scenario: Citizen runs the Docker Compose bundle

- **GIVEN** a member of the public downloads the
  `docker/cianchosaint-citizen/` Docker Compose bundle
- **WHEN** they run `docker compose up -d`
- **THEN** the bundle SHALL start all 7 containers
- **AND** the Cian AG-UI interface SHALL be accessible at
  `http://localhost:7777`
- **AND** the citizen SHALL be able to chat with Cian about British
  Isles official OSINT sources without sending any data to a SaaS

#### Scenario: Self-hosted citizen uses MiniMax Token Plan as fallback

- **GIVEN** the citizen's Unsloth Studio is unavailable
- **WHEN** the citizen's `deployment-choice.yaml` lists
  `minimax_token_plan` as the fallback
- **THEN** the `ModelProviderRouter` SHALL fall back to the
  citizen's own MiniMax API key (BYOK)
- **AND** SHALL emit a Langfuse span attribute `fallback_reason:
  "unsloth_unavailable"` so the citizen can see what happened

### Requirement: Locket sidecar for secret injection

The system SHALL include a Locket sidecar in the self-hosted citizen
Docker Compose bundle that hydrates the runtime environment from a
Pangolin-issued secret, mirroring the existing Cianfhoghlaim Locket
pattern.

#### Scenario: Locket sidecar injects Infisical secret at runtime

- **WHEN** the citizen starts the Docker Compose bundle
- **THEN** the Locket sidecar SHALL fetch the secret from the
  Pangolin-issued token
- **AND** SHALL inject the secret into the runtime environment of
  the Cian AG-UI container, the Unsloth Studio container, and the
  LiteLLM Proxy container

### Requirement: Private Pangolin resource pattern

The system SHALL provide a private Pangolin resource configuration at
`docker/cianchosaint-citizen/pangolin.yaml` that exposes the
self-hosted Cian instance to the citizen's own private network (e.g.
their home network, a VPN).

#### Scenario: Pangolin resource exposes Cian to citizen's VPN

- **WHEN** the citizen enables the Pangolin resource (via
  `docker/cianchosaint-citizen/pangolin.yaml`)
- **THEN** the citizen SHALL be able to access the Cian AG-UI
  interface from any device on their Pangolin-issued VPN
- **AND** the Pangolin resource SHALL be private (not publicly
  exposed)

### Requirement: Per-tenant Infisical read-only token

The system SHALL provision the citizen's Infisical folder
(`dev-baile/cianchosaint/citizen/<citizen-id>/`) with a read-only
token, mirroring the existing Cianfhoghlaim Infisical pattern.

#### Scenario: Citizen has read-only Infisical access

- **GIVEN** a citizen signs up for self-host access
- **WHEN** the operator (or the Cianchosaint Licence Enforcement
  body) provisions the citizen's Infisical folder
- **THEN** the citizen SHALL receive a read-only Infisical token
  scoped to their own folder
- **AND** the citizen SHALL NOT have admin scope on any Infisical
  folder
- **AND** the citizen SHALL NOT have write access to any
  Cianchosaint configuration

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../cianchosaint-agentic-interaction/spec.md`](../cianchosaint-agentic-interaction/spec.md) — the umbrella capability
- [`../cianchosaint-pipeline/spec.md`](../cianchosaint-pipeline/spec.md) — the data pipeline umbrella
