# Spec Delta: cianchosaint-cloudflare-deploy

This delta is applied by the openspec change
[`cianchosaint-cloudflare-deploy-v1`](../proposal.md). It describes
the ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-cloudflare-deploy/spec.md`](../../../../specs/cianchosaint-cloudflare-deploy/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: The consolidated wrangler.toml for the 8 web apps + the Hono API gateway

The system SHALL provide a consolidated `wrangler.toml` at
`web/apps/ciafagent-api/wrangler.toml` that declares all 8 web apps +
the Hono API gateway under the `cianchosaint.ie` Cloudflare zone.

The `wrangler.toml` SHALL declare at minimum the following 9 routes
under `[env.production]`:

1. `ga.cianchosaint.ie/*` (ciafagent-ga-public)
2. `ga-internal.cianchosaint.ie/*` (ciafagent-ga-internal)
3. `met.cianchosaint.ie/*` (ciafagent-met-public)
4. `met-internal.cianchosaint.ie/*` (ciafagent-met-internal)
5. `psni.cianchosaint.ie/*` (ciafagent-psni-public)
6. `psni-internal.cianchosaint.ie/*` (ciafagent-psni-internal)
7. `reform-uk-pilot.cianchosaint.ie/*` (ciafagent-reform-uk-pilot)
8. `self-host.cianchosaint.ie/*` (ciafagent-self-host)
9. `api.cianchosaint.ie/*` (ciafagent-api — Hono gateway)

The `wrangler.toml` SHALL be valid TOML parseable by `tomllib.loads`.

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
`web/apps/ciafagent-api/wrangler.toml`:

1. `[env.dev]` — the development environment, deployed to
   `dev.cianchosaint.ie`.
2. `[env.staging]` — the staging environment, deployed to
   `staging.cianchosaint.ie`.
3. `[env.production]` — the production environment, deployed to
   `cianchosaint.ie`.

Each environment SHALL declare its own routes, vars, and bindings.
The production environment SHALL be the only environment exposed at
the public `*.cianchosaint.ie` domain. The dev + staging environments
SHALL be exposed at subdomains of `dev.cianchosaint.ie` +
`staging.cianchosaint.ie`.

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
- **AND** the deployment SHALL be the only environment exposed at
  the public `*.cianchosaint.ie` domain

#### Scenario: The 3 environments have separate vars

- **WHEN** the operator inspects
  `web/apps/ciafagent-api/wrangler.toml`
- **THEN** each environment SHALL declare its own `vars` block
  (e.g. `CONVEX_DEPLOYMENT`, `COPILOTKIT_RUNTIME_URL`)
- **AND** the production vars SHALL be the canonical production
  values (e.g. `CONVEX_DEPLOYMENT = "prod:conic-api"`)
