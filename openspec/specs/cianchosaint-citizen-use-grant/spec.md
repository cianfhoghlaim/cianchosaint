# cianchosaint-citizen-use-grant Capability

## Purpose

`cianchosaint-citizen-use-grant` is the capability that extends
`LICENSE.md` with the **Natural Person Citizen Grant** — a legal
amendment that grants natural persons of the British Isles who are
not affiliated with the bodies in (a), (b), or (c) of the
Additional Use Grant the right to use the Licensed Work for
non-commercial personal purposes, including self-hosted deployment.

The grant is conditioned on:

1. The citizen is a natural person of the British Isles.
2. The use is for non-commercial personal purposes only.
3. The prohibition on commercial monetisation in (1) of `LICENSE.md`
   is preserved.
4. No public-facing deployment.
5. No foreign use (foreign entities are still explicitly banned).

The grant is the legal counterpart to the existing
`cianchosaint-self-hosted-citizen` technical capability (Docker
Compose bundle + Locket sidecar + private Pangolin resource +
per-tenant Infisical read-only token).

## Background

`LICENSE.md` §Additional Use Grant covers production use by
British Isles public-sector bodies (Ireland / UK / Crown Dependencies).
Members of the public using cianchosaint for personal interaction
with their own government's services do NOT fall under the
Additional Use Grant as drafted. Before this capability was added,
the self-hosted citizen option was **experimental** and licensed
under the same grant as the rest of the platform.

This capability fixes the gap by amending the licence.

## Requirements

### Requirement: The Natural Person Citizen Grant amendment to LICENSE.md

The system SHALL extend `LICENSE.md` with a new "NATURAL PERSON
CITIZEN GRANT" section that grants natural persons of the British
Isles the right to use the Licensed Work for non-commercial
personal purposes, including self-hosted deployment.

#### Scenario: The grant appears in LICENSE.md

- **WHEN** the operator inspects `LICENSE.md`
- **THEN** the file SHALL contain the heading "NATURAL PERSON
  CITIZEN GRANT" placed before the "**Change Date:**" section

#### Scenario: The grant preserves the existing BUSL-1.1 v2 grant structure

- **WHEN** the operator inspects `LICENSE.md`
- **THEN** the file SHALL preserve the Additional Use Grant (Ireland
  / UK / Crown Dependencies) verbatim
- **AND** SHALL preserve the Conditional foreign use (the 3-step
  gate) verbatim
- **AND** SHALL preserve the Warrant to enforce clause verbatim
- **AND** SHALL preserve the Change Date + Change License verbatim

#### Scenario: The grant explicitly excludes foreign use

- **WHEN** the operator inspects the new "NATURAL PERSON CITIZEN
  GRANT" section
- **THEN** the section SHALL state that the grant does NOT cover use
  by any foreign entity
- **AND** SHALL state that foreign intelligence agencies remain
  explicitly banned

### Requirement: The grant preserves the prohibition on commercial monetisation + foreign use + public-facing deployment

The system SHALL enforce the 4 binding constraints on the Natural
Person Citizen Grant:

1. The citizen is a natural person of the British Isles.
2. The use is for non-commercial personal purposes only.
3. The prohibition on commercial monetisation in (1) of `LICENSE.md`
   is preserved.
4. No public-facing deployment.

#### Scenario: The grant excludes commercial monetisation

- **WHEN** the operator inspects the new "NATURAL PERSON CITIZEN
  GRANT" section
- **THEN** the section SHALL state that the grant does NOT cover
  commercial monetisation of any kind

#### Scenario: The grant excludes public-facing deployment

- **WHEN** a natural-person citizen attempts to deploy the
  self-hosted citizen Docker Compose bundle with a public-facing
  Pangolin resource
- **THEN** the deployment SHALL fail validation
- **AND** SHALL log a `citizen_public_facing_deployment_blocked`
  warning to the Langfuse observability stack

#### Scenario: The grant is verified by Pocket ID organisation membership

- **WHEN** a natural-person citizen signs in to
  `self-host.cianchosaint.ie` via Pocket ID
- **THEN** Pocket ID SHALL verify the citizen's membership in the
  `cianchosaint-citizens` organisation
- **AND** SHALL reject access for non-British-Isles natural persons

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document (BUSL-1.1 v2 + the citizen grant amendment)
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../cianchosaint-self-hosted-citizen/spec.md`](../cianchosaint-self-hosted-citizen/spec.md) — the technical counterpart
- [`../cianchosaint-repo-foundation/spec.md`](../cianchosaint-repo-foundation/spec.md) — the upstream licence posture
