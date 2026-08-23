# cianchosaint-deployment Capability

## Purpose

`cianchosaint-deployment` is the capability that provides the
**canonical, operator-facing deployment runbook** for the cianchosaint
platform. The runbook documents the 13 Docker Compose stacks, the 8
per-persona web apps, the 24 per-constituency Google ADK agents, the
4-tier `ModelProviderRouter`, the CCC indexing setup, the OSINT
allowlist, the smoke tests, the health checks, and the rollback
plan — all in a single canonical artefact at `docs/DEPLOYMENT.md`.

This capability is the load-bearing companion to the wholesale-copy
umbrella (`cianchosaint-bootstrap-v2`), the per-constituency agents
(`cianchosaint-per-constituency-agents`), the data pipeline
(`cianchosaint-pipeline`), and the self-host citizen
(`cianchosaint-self-hosted-citizen`).

## Background

On a fresh machine, an operator previously had to read:

1. `AGENTS.md` (top-level routing)
2. `mise.toml` (32 tasks without context)
3. `bonneagar/AGENTS.md` (the IaC inventory)
4. `LICENSE.md` (the licence)
5. The 8+ openspec specs (the contracts)
6. Per-stack `README.md` files (the bring-up commands)

to understand how to deploy the platform. The knowledge was scattered
across 6+ documents and the operator had to mentally re-assemble it.

The `cianchosaint-deployment-runbook-v1` change collapses all of that
into a single canonical runbook at `docs/DEPLOYMENT.md` (~3,000-5,000
words, 13 sections).

## Requirements

### Requirement: The 13-stacks deployment catalogue

The system SHALL provide a canonical deployment runbook that documents
every one of the 13 Docker Compose stacks in `bonneagar/stacks/` with
its port, purpose, env vars, dependencies, smoke test, and rollback
procedure.

#### Scenario: All 13 stacks documented

- **WHEN** the operator reads `docs/DEPLOYMENT.md` §2
- **THEN** the table SHALL include all 13 stacks: `infisical`,
  `motherduck`, `lakehouse`, `litellm`, `unsloth-serve`, `langfuse`,
  `crawl4ai`, `stagehand`, `changedetection`, `komodo`, `pangolin`,
  `locket`, `openchamber`
- **AND** each row SHALL include the stack's primary port, purpose,
  env vars, and dependencies

#### Scenario: Per-stack deployment section present

- **WHEN** the operator reads `docs/DEPLOYMENT.md` §4
- **THEN** for each of the 13 stacks there SHALL be a sub-section
  with the env vars, the deploy commands, the smoke test, and the
  rollback procedure

### Requirement: The stack lifecycle ordering

The system SHALL document the canonical stack ordering — which stack
to start first when bringing up the platform from cold — in
`docs/DEPLOYMENT.md` §3.

#### Scenario: 8-tier lifecycle documented

- **WHEN** the operator reads `docs/DEPLOYMENT.md` §3
- **THEN** the lifecycle SHALL be:
  1. secrets (infisical)
  2. storage (motherduck + lakehouse)
  3. LLM (litellm + unsloth-serve)
  4. observability (langfuse)
  5. browser (crawl4ai + stagehand)
  6. monitoring (changedetection)
  7. governance (komodo + pangolin + locket)
  8. UI (openchamber)
- **AND** each tier SHALL explain WHY it precedes the next
  (e.g. "infisical must start first because all other stacks depend
  on its `infisical://dev-baile/...` secret references")

### Requirement: The 4-tier ModelProviderRouter contract

The system SHALL document the 4-tier `ModelProviderRouter` (Unsloth
Studio → LiteLLM → MiniMax → Gemini) in `docs/DEPLOYMENT.md` §5, with
the failover semantics and the env-var contract.

#### Scenario: The 4-tier chain explains each tier

- **WHEN** the operator reads `docs/DEPLOYMENT.md` §5
- **THEN** the runbook SHALL explain each tier's role:
  - Tier 1 (Unsloth Studio): local-first, default; LLM gateway at
    `http://localhost:8889`
  - Tier 2 (LiteLLM, our gateway): fallback #1; routes the 76-entry
    MODEL_REGISTRY at `:4000`
  - Tier 3 (MiniMax Token Plan): fallback #2; hosted at
    `https://api.minimax.chat/v1`
  - Tier 4 (Gemini API): fallback #3; last-resort via
    `GOOGLE_API_KEY`
- **AND** SHALL document the failover algorithm (try tier 1, if
  timeout/error try tier 2, etc.)

### Requirement: The 8 per-persona web apps

The system SHALL document the 8 per-persona web apps in
`docs/DEPLOYMENT.md` §6, with the URL, the route, and the backing
agent.

#### Scenario: All 8 apps documented

- **WHEN** the operator reads `docs/DEPLOYMENT.md` §6
- **THEN** the table SHALL include all 8 apps:
  `ciafagent-ga-public`, `ciafagent-ga-internal`, `ciafagent-met-public`,
  `ciafagent-met-internal`, `ciafagent-psni-public`,
  `ciafagent-psni-internal`, `ciafagent-self-host`, `ciafagent-api`
- **AND** each row SHALL include the URL, the route, and the backing
  agent (root agent from `agents/cianchosaint/`)

### Requirement: The 24 per-constituency agents

The system SHALL document the 24 per-constituency Google ADK agents
in `docs/DEPLOYMENT.md` §7, with the constituency, the sub-domain, and
the backing BAML.

#### Scenario: All 24 agents documented

- **WHEN** the operator reads `docs/DEPLOYMENT.md` §7
- **THEN** the table SHALL include all 24 agents: 3 root + 15 specialists
  + 6 FunctionTool wrappers
- **AND** each row SHALL include the constituency (An Garda Síochána /
  Met Police / PSNI / cross-constituency), the sub-domain
  (crime_statistics / stop_and_search / press_releases / etc.), and
  the backing BAML extraction function

#### Scenario: The 3 root agents are highlighted

- **WHEN** the operator reads `docs/DEPLOYMENT.md` §7
- **THEN** the runbook SHALL highlight the 3 root agents
  (`ga_root_agent`, `met_root_agent`, `psni_root_agent`) as the
  orchestrators that dispatch to their 5 specialists each

### Requirement: Per-deployment-target procedures

The system SHALL document deployment procedures for all 3 deployment
targets in `docs/DEPLOYMENT.md` §8-§10: `arm1-oci`, `bunchloch`
(MacBook M4 local-dev), and self-host citizen Docker bundle.

#### Scenario: arm1-oci procedure documented

- **WHEN** the operator reads `docs/DEPLOYMENT.md` §8
- **THEN** the runbook SHALL include the arm1-oci procedure: SSH +
  pull + `komodo deploy stack <name>` + smoke test + Pangolin ingress
  validation

#### Scenario: bunchloch procedure documented

- **WHEN** the operator reads `docs/DEPLOYMENT.md` §9
- **THEN** the runbook SHALL include the bunchloch procedure: local
  `docker compose` + Locket sidecar + smoke test

#### Scenario: self-host citizen procedure documented

- **WHEN** the operator reads `docs/DEPLOYMENT.md` §10
- **THEN** the runbook SHALL include the self-host citizen procedure:
  `cd docker/ciafagent-self-host && docker compose up -d` + per-tenant
  Infisical provisioning + private Pangolin resource enablement

### Requirement: Smoke tests + health checks + rollback plan

The system SHALL document the smoke tests, health checks, and rollback
plan in `docs/DEPLOYMENT.md` §11-§13.

#### Scenario: Per-stack smoke tests documented

- **WHEN** the operator reads `docs/DEPLOYMENT.md` §11
- **THEN** the table SHALL include a smoke test command for each of
  the 13 stacks (e.g. for `litellm`:
  `curl -s -H "Authorization: Bearer $LITELLM_MASTER_KEY"
  http://localhost:4000/v1/models`)

#### Scenario: Health checks documented

- **WHEN** the operator reads `docs/DEPLOYMENT.md` §12
- **THEN** the runbook SHALL document the 3 health check mise tasks:
  - `mise run cianchosaint:provider:health-check` (the 4-tier router)
  - `mise run cianchosaint:browser-tool:health-check` (crawl4ai + stagehand)
  - `mise run cianchosaint:osint:health-check` (the OSINT allowlist integrity)

#### Scenario: Per-stack rollback procedures documented

- **WHEN** the operator reads `docs/DEPLOYMENT.md` §13
- **THEN** the runbook SHALL include a rollback procedure for each of
  the 13 stacks (the `docker compose down` or `komodo rollback` command,
  plus the secret-revocation ritual)

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../../docs/DEPLOYMENT.md`](../../docs/DEPLOYMENT.md) — the canonical runbook
- [`../cianchosaint-pipeline/spec.md`](../cianchosaint-pipeline/spec.md) — the data pipeline umbrella
- [`../cianchosaint-bootstrap-v2/spec.md`](../cianchosaint-bootstrap-v2/spec.md) — the wholesale-copy umbrella (13 stacks + 7 apps + 24 agents)
- [`../cianchosaint-per-constituency-agents/spec.md`](../cianchosaint-per-constituency-agents/spec.md) — the per-constituency agents
- [`../cianchosaint-self-hosted-citizen/spec.md`](../cianchosaint-self-hosted-citizen/spec.md) — the self-host citizen Docker bundle
