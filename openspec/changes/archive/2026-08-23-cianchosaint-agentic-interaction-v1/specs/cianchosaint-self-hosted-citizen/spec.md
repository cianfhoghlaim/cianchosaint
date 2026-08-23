# Spec Delta: cianchosaint-self-hosted-citizen

This delta is applied by the openspec change
[`cianchosaint-agentic-interaction-v1`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-self-hosted-citizen/spec.md`](../../../../specs/cianchosaint-self-hosted-citizen/spec.md)
that this change adds.

## ADDED Requirements

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
