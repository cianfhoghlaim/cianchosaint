# cianchosaint-pangolin-ingress Capability

## Purpose

`cianchosaint-pangolin-ingress` is the capability that exposes the
**8 per-persona web apps + the Hono API gateway** at `*.cianchosaint.ie`
via Pangolin private + public resources. Pangolin is the reverse proxy
+ WireGuard tunnel layer (wholesale-copied from Cianfhoghlaim's
`bonneagar/pangolin/`).

The 9 resources are:

| Resource name | Target | Visibility | Auth |
|:--|:--|:--|:--|
| `ga.cianchosaint.ie` | `ciafagent-ga-public:7777` | public | pocketid |
| `ga-internal.cianchosaint.ie` | `ciafagent-ga-internal:7777` | private | pocketid |
| `met.cianchosaint.ie` | `ciafagent-met-public:7777` | public | pocketid |
| `met-internal.cianchosaint.ie` | `ciafagent-met-internal:7777` | private | pocketid |
| `psni.cianchosaint.ie` | `ciafagent-psni-public:7777` | public | pocketid |
| `psni-internal.cianchosaint.ie` | `ciafagent-psni-internal:7777` | private | pocketid |
| `reform-uk-pilot.cianchosaint.ie` | `ciafagent-reform-uk-pilot:7777` | private | pocketid |
| `self-host.cianchosaint.ie` | `ciafagent-self-host:7777` | private | pocketid |
| `api.cianchosaint.ie` | `ciafagent-api:8787` | private | pocketid |

Every private resource requires Pocket ID authentication + organisation
membership, and carries the 6 canonical labels (constituency, app,
persona, role, jurisdiction, environment).

## Background

Per the locked plan, the 8 per-persona web apps + the Hono API
gateway share a common canonical Pangolin ingress pattern. Before
this capability was added, no Pangolin resource definitions existed
for cianchosaint — the `bonneagar/pangolin/` directory was empty.
This capability fixes the gap by declaring all 9 resources.

## Requirements

### Requirement: The 8 web apps + Hono API gateway exposed at *.cianchosaint.ie via Pangolin

The system SHALL expose the 8 per-persona web apps + the Hono API
gateway at `*.cianchosaint.ie` via Pangolin private + public
resources declared in
`bonneagar/pangolin/cianchosaint_resources.yaml`.

#### Scenario: All 9 resources are declared in the YAML file

- **WHEN** the operator runs
  `python3.13 -c "import yaml; print(len(yaml.safe_load(open('bonneagar/pangolin/cianchosaint_resources.yaml').read())['resources']))"`
- **THEN** the output SHALL be `9`

#### Scenario: The YAML file is valid YAML

- **WHEN** the operator runs
  `python3.13 -c "import yaml; yaml.safe_load(open('bonneagar/pangolin/cianchosaint_resources.yaml').read())"`
- **THEN** the script SHALL exit with code 0

#### Scenario: Public resources serve the public-facing per-persona apps

- **WHEN** the operator navigates to `https://ga.cianchosaint.ie` in
  a browser
- **THEN** the An Garda Síochána public-facing app SHALL be served
- **AND** the user SHALL be prompted to authenticate via Pocket ID

#### Scenario: Private resources serve the internal-facing apps

- **WHEN** the operator navigates to
  `https://ga-internal.cianchosaint.ie` in a browser
- **THEN** the An Garda Síochána internal-facing app SHALL be served
  via the private Pangolin resource
- **AND** the user SHALL be required to authenticate via Pocket ID
  AND be a member of the `ga-internal` Pocket ID organisation

### Requirement: Pocket ID authentication + 6-label pattern on every private resource

Every private resource SHALL satisfy Pocket ID authentication + the
6 canonical labels (constituency, app, persona, role, jurisdiction,
environment). Every public resource SHALL also satisfy the 6-label
pattern (the labels are required for per-resource metrics).

#### Scenario: Private resources require Pocket ID authentication

- **WHEN** the operator navigates to `https://ga-internal.cianchosaint.ie`
  WITHOUT a Pocket ID session
- **THEN** Pangolin SHALL redirect the user to the Pocket ID login page
- **AND** SHALL reject unauthenticated requests with a 401 response

#### Scenario: Private resources enforce Pocket ID organisation membership

- **WHEN** an authenticated Pocket ID user attempts to access
  `https://ga-internal.cianchosaint.ie` but is NOT a member of the
  `ga-internal` Pocket ID organisation
- **THEN** Pangolin SHALL reject the request with a 403 Forbidden
  response
- **AND** SHALL log an `unauthorised_resource_access` warning to
  the Langfuse observability stack

#### Scenario: The 6-label pattern is enforced on every private resource

- **WHEN** the operator inspects
  `bonneagar/pangolin/cianchosaint_resources.yaml`
- **THEN** every resource SHALL declare all 6 labels
  (constituency, app, persona, role, jurisdiction, environment)
- **AND** no resource SHALL omit any label

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document (BUSL-1.1 v2)
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../cianchosaint-deployment/spec.md`](../cianchosaint-deployment/spec.md) — the deployment umbrella
- [`../cianchosaint-per-constituency-agents/spec.md`](../cianchosaint-per-constituency-agents/spec.md) — the per-persona apps exposed by the resources
- [`../cianchosaint-reform-uk-pilot-workflow/spec.md`](../cianchosaint-reform-uk-pilot-workflow/spec.md) — the reform-uk-pilot consumer of `reform-uk-pilot.cianchosaint.ie`
- [`../cianchosaint-self-hosted-citizen/spec.md`](../cianchosaint-self-hosted-citizen/spec.md) — the self-host consumer of `self-host.cianchosaint.ie`
