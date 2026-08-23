# cianchosaint-cloudflare-deploy Capability

## Purpose

`cianchosaint-cloudflare-deploy` is the capability that deploys the
**8 per-persona web apps + the Hono API gateway** to Cloudflare
Workers + Containers under the `cianchosaint.ie` zone. The
deployment is declared in a consolidated `wrangler.toml` at
`web/apps/ciafagent-api/wrangler.toml`.

The 9 routes (per environment) are:

1. `ga.cianchosaint.ie/*` (ciafagent-ga-public)
2. `ga-internal.cianchosaint.ie/*` (ciafagent-ga-internal)
3. `met.cianchosaint.ie/*` (ciafagent-met-public)
4. `met-internal.cianchosaint.ie/*` (ciafagent-met-internal)
5. `psni.cianchosaint.ie/*` (ciafagent-psni-public)
6. `psni-internal.cianchosaint.ie/*` (ciafagent-psni-internal)
7. `reform-uk-pilot.cianchosaint.ie/*` (ciafagent-reform-uk-pilot)
8. `self-host.cianchosaint.ie/*` (ciafagent-self-host)
9. `api.cianchosaint.ie/*` (ciafagent-api — Hono gateway)

The 3 Cloudflare environments (dev / staging / production) deploy
to the corresponding `*.cianchosaint.ie` subdomains.

## Background

Per the locked plan, the 8 per-persona web apps + the Hono API
gateway share a common canonical Cloudflare Workers + Containers
deployment. Before this capability was added, only the Hono API
gateway was deployed (per the existing
`web/apps/ciafagent-api/wrangler.toml`). This capability fixes the
gap by extending the `wrangler.toml` to declare all 9 services.

## Requirements

### Requirement: The consolidated wrangler.toml for the 8 web apps + the Hono API gateway

The system SHALL provide a consolidated `wrangler.toml` at
`web/apps/ciafagent-api/wrangler.toml` that declares all 8 web apps +
the Hono API gateway under the `cianchosaint.ie` Cloudflare zone.

The `wrangler.toml` SHALL declare at minimum the 9 routes under
`[env.production]` and SHALL be valid TOML.

#### Scenario: The wrangler.toml declares all 9 routes

- **WHEN** the operator runs
  `python3 -c "import tomllib; data = tomllib.loads(open('web/apps/ciafagent-api/wrangler.toml','rb').read()); print(len(data['env']['production']['routes']))"`
- **THEN** the output SHALL be `9`

#### Scenario: The wrangler.toml is valid TOML

- **WHEN** the operator runs
  `python3 -c "import tomllib; tomllib.loads(open('web/apps/ciafagent-api/wrangler.toml','rb').read())"`
- **THEN** the script SHALL exit with code 0

#### Scenario: All 9 routes use the cianchosaint.ie zone

- **WHEN** the operator inspects
  `web/apps/ciafagent-api/wrangler.toml`
- **THEN** every route SHALL declare `zone_name = "cianchosaint.ie"`

#### Scenario: The wrangler.toml declares the production environment

- **WHEN** the operator runs `wrangler deploy --env production`
- **THEN** Cloudflare SHALL deploy all 9 routes to the
  `cianchosaint.ie` zone

### Requirement: Per-environment Cloudflare Workers config (dev | staging | prod)

The system SHALL declare 3 Cloudflare environments under
`web/apps/ciafagent-api/wrangler.toml`: `[env.dev]`, `[env.staging]`,
and `[env.production]`. Each environment SHALL declare its own
routes, vars, and bindings. The production environment SHALL be the
only environment exposed at the public `*.cianchosaint.ie` domain.

#### Scenario: The dev environment uses the dev zone

- **WHEN** the operator runs `wrangler deploy --env dev`
- **THEN** Cloudflare SHALL deploy all 9 routes to the
  `dev.cianchosaint.ie` zone

#### Scenario: The staging environment uses the staging zone

- **WHEN** the operator runs `wrangler deploy --env staging`
- **THEN** Cloudflare SHALL deploy all 9 routes to the
  `staging.cianchosaint.ie` zone

#### Scenario: The production environment uses the production zone

- **WHEN** the operator runs `wrangler deploy --env production`
- **THEN** Cloudflare SHALL deploy all 9 routes to the
  `cianchosaint.ie` zone

#### Scenario: The 3 environments have separate vars

- **WHEN** the operator inspects
  `web/apps/ciafagent-api/wrangler.toml`
- **THEN** each environment SHALL declare its own `vars` block
- **AND** the production vars SHALL be the canonical production
  values

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document (BUSL-1.1 v2)
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../cianchosaint-deployment/spec.md`](../cianchosaint-deployment/spec.md) — the deployment umbrella
- [`../cianchosaint-pangolin-ingress/spec.md`](../cianchosaint-pangolin-ingress/spec.md) — the upstream ingress layer
- [`../cianchosaint-per-constituency-agents/spec.md`](../cianchosaint-per-constituency-agents/spec.md) — the per-persona apps deployed
