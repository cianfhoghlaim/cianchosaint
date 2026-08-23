# unsloth-studio-pangolin-ingress Capability

## Purpose

`unsloth-studio-pangolin-ingress` is the capability that exposes the
**Unsloth Studio local API** at `unsloth.cianchosaint.ie` via a
Pangolin private resource. Unsloth Studio is the local-model
serving layer that powers the 4-tier provider chain (Primary /
Fallback / Emergency / Gemini — per `baml_src/clients.baml`).

The resource is private (not public) — only authenticated Pocket ID
members of the `cianchosaint-ops` organisation can access the API.
The BUSL-1.1 v2 licence posture is preserved (foreign entities
remain explicitly banned).

## Background

The cianchosaint platform has a wholesale-copied Unsloth Studio
container stack at `bonneagar/stacks/unsloth-serve/` (per the
wholesale-copied Cianfhoghlaim pattern). The Unsloth Studio local
API listens on port 8889 inside the `unsloth-serve` Docker network.
Before this capability was added, no Pangolin resource exposed the
API at `*.cianchosaint.ie` — the 8 per-persona web apps + the Hono
API gateway had to invoke the API directly from inside the Docker
network.

This capability fixes the gap by exposing the API at
`unsloth.cianchosaint.ie` via a private Pangolin resource with
Pocket ID authentication + Member role enforcement.

## Requirements

### Requirement: The Pangolin resource for Unsloth Studio at unsloth.cianchosaint.ie:8889

The system SHALL provide a Pangolin resource at
`bonneagar/pangolin/unsloth_studio_resource.yaml` that exposes the
Unsloth Studio local API at `unsloth.cianchosaint.ie` via a private
Pangolin resource. The resource SHALL satisfy the 7 fields declared
in the spec delta (name, type, target, visibility, auth, role,
labels).

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

### Requirement: Pocket ID authentication + Member role enforcement

The Unsloth Studio resource SHALL satisfy:

1. `auth: pocketid` — Pocket ID authentication is required.
2. `role: member` — the Pocket ID `Member` role in the
   `cianchosaint-ops` organisation is required.
3. Every request to `unsloth.cianchosaint.ie` SHALL be logged to
   the `cianchosaint.unsloth` log stream.

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
  stream

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document (BUSL-1.1 v2)
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../cianchosaint-pangolin-ingress/spec.md`](../cianchosaint-pangolin-ingress/spec.md) — the upstream 8-web-app + Hono API gateway ingress pattern
- [`../../bonneagar/stacks/unsloth-serve/`](../../bonneagar/stacks/unsloth-serve/) — the wholesale-copied Unsloth Studio container stack
