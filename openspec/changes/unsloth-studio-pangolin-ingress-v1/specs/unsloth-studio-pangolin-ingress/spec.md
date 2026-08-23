# Spec Delta: unsloth-studio-pangolin-ingress

This delta is applied by the openspec change
[`unsloth-studio-pangolin-ingress-v1`](../proposal.md). It describes
the ADDED Requirements to the canonical
[`openspec/specs/unsloth-studio-pangolin-ingress/spec.md`](../../../../specs/unsloth-studio-pangolin-ingress/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: The Pangolin resource for Unsloth Studio at unsloth.cianchosaint.ie:8889

The system SHALL provide a Pangolin resource at
`bonneagar/pangolin/unsloth_studio_resource.yaml` that exposes the
Unsloth Studio local API at `unsloth.cianchosaint.ie` via a private
Pangolin resource.

The resource SHALL satisfy:

1. `name: unsloth.cianchosaint.ie` — the public-facing domain.
2. `type: api` — the resource type is an API gateway.
3. `target: unsloth-serve:8889` — the upstream target (the
   wholesale-copied Unsloth Studio container stack at
   `bonneagar/stacks/unsloth-serve/`).
4. `visibility: private` — the resource is NOT publicly exposed.
5. `auth: pocketid` — Pocket ID authentication is required.
6. `role: member` — the Pocket ID role required (Member of the
   `cianchosaint-ops` organisation).
7. `labels: {app: unsloth-studio, role: model-server, jurisdiction: ireland, environment: prod, constituency: ops}` — the 5 canonical
   labels (per the wholesale-copied Cianfhoghlaim pattern).

The YAML file SHALL be valid YAML parseable by `yaml.safe_load`.

#### Scenario: The YAML file is valid YAML

- **WHEN** the operator runs
  `python3 -c "import yaml; yaml.safe_load(open('bonneagar/pangolin/unsloth_studio_resource.yaml').read())"`
- **THEN** the script SHALL exit with code 0

#### Scenario: The resource declares 1 entry

- **WHEN** the operator runs
  `python3 -c "import yaml; print(len(yaml.safe_load(open('bonneagar/pangolin/unsloth_studio_resource.yaml').read())['resources']))"`
- **THEN** the output SHALL be `1`

#### Scenario: The resource points at unsloth-serve:8889

- **WHEN** the operator inspects
  `bonneagar/pangolin/unsloth_studio_resource.yaml`
- **THEN** the resource SHALL declare `target: unsloth-serve:8889`

#### Scenario: The resource is private (not public)

- **WHEN** the operator inspects
  `bonneagar/pangolin/unsloth_studio_resource.yaml`
- **THEN** the resource SHALL declare `visibility: private`
- **AND** SHALL NOT be publicly exposed (only authenticated Pocket
  ID members of `cianchosaint-ops` can access)

### Requirement: Pocket ID authentication + Member role enforcement

The Unsloth Studio resource SHALL satisfy:

1. `auth: pocketid` — the resource requires Pocket ID authentication.
2. `role: member` — the resource requires the Pocket ID `Member`
   role in the `cianchosaint-ops` organisation.
3. Every request to `unsloth.cianchosaint.ie` SHALL be logged to
   the `cianchosaint.unsloth` log stream (for observability).

#### Scenario: Unauthenticated requests are rejected

- **WHEN** an unauthenticated user navigates to
  `https://unsloth.cianchosaint.ie/v1/models`
- **THEN** Pangolin SHALL redirect the user to the Pocket ID login page
- **AND** SHALL reject unauthenticated requests with a 401 response

#### Scenario: Non-Member requests are rejected

- **WHEN** an authenticated Pocket ID user attempts to access
  `https://unsloth.cianchosaint.ie/v1/models` but is NOT a Member of
  the `cianchosaint-ops` organisation
- **THEN** Pangolin SHALL reject the request with a 403 Forbidden
  response

#### Scenario: Member requests are forwarded to the upstream

- **WHEN** a Pocket ID Member of `cianchosaint-ops` navigates to
  `https://unsloth.cianchosaint.ie/v1/models`
- **THEN** Pangolin SHALL forward the request to
  `unsloth-serve:8889`
- **AND** SHALL log the request to the `cianchosaint.unsloth` log
  stream with the requester's Pocket ID username
