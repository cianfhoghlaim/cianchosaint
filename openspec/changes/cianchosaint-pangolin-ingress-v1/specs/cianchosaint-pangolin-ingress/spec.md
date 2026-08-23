# Spec Delta: cianchosaint-pangolin-ingress

This delta is applied by the openspec change
[`cianchosaint-pangolin-ingress-v1`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-pangolin-ingress/spec.md`](../../../../specs/cianchosaint-pangolin-ingress/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: The 8 web apps + Hono API gateway exposed at *.cianchosaint.ie via Pangolin

The system SHALL expose the 8 per-persona web apps + the Hono API
gateway at `*.cianchosaint.ie` via Pangolin private + public
resources declared in
`bonneagar/pangolin/cianchosaint_resources.yaml`. The 9 resources
SHALL be:

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

The YAML file SHALL conform to the Pangolin resource schema
(version: 1) and SHALL be valid YAML parseable by `yaml.safe_load`.

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
  (the public-facing apps still require authentication per the
  Pocket ID pattern)

#### Scenario: Private resources serve the internal-facing apps

- **WHEN** the operator navigates to
  `https://ga-internal.cianchosaint.ie` in a browser
- **THEN** the An Garda Síochána internal-facing app SHALL be served
  via the private Pangolin resource
- **AND** the user SHALL be required to authenticate via Pocket ID
  AND be a member of the `ga-internal` Pocket ID organisation

### Requirement: Pocket ID authentication + 6-label pattern on every private resource

Every private resource SHALL satisfy:

1. `auth: pocketid` — the resource requires Pocket ID authentication.
2. The 6 canonical labels:
   - `constituency` — the British Isles sub-nation (ga | met | psni |
     reform_uk | self_host | api)
   - `app` — the per-persona app name (ciafagent-ga-public |
     ciafagent-ga-internal | ciafagent-met-public |
     ciafagent-met-internal | ciafagent-psni-public |
     ciafagent-psni-internal | ciafagent-reform-uk-pilot |
     ciafagent-self-host | ciafagent-api)
   - `persona` — the audience (public | internal | pilot | citizen)
   - `role` — the resource role (web | api)
   - `jurisdiction` — the British Isles sub-nation (ireland | uk | ni
     | scotland | wales | jersey | guernsey | iom)
   - `environment` — the deployment environment (dev | staging | prod)

Every public resource SHALL satisfy the same 6-label pattern (the
labels are required for the per-resource metrics + alerting).

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
