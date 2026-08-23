# Spec Delta: cianchosaint-citizen-use-grant

This delta is applied by the openspec change
[`cianchosaint-citizen-use-grant-v1`](../proposal.md). It describes
the ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-citizen-use-grant/spec.md`](../../../../specs/cianchosaint-citizen-use-grant/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: The Natural Person Citizen Grant amendment to LICENSE.md

The system SHALL extend `LICENSE.md` with a new "NATURAL PERSON
CITIZEN GRANT" section (placed immediately before the "**Change
Date:**" section) that grants natural persons of the British Isles
who are not affiliated with the bodies in (a), (b), or (c) of the
Additional Use Grant the right to use the Licensed Work for
non-commercial personal purposes, including self-hosted deployment.

The grant SHALL cover:
1. Self-hosted deployment on a natural person's own machine (per the
   `cianchosaint-self-hosted-citizen` spec).
2. Personal OSINT investigation (subject to the OSINT allowlist
   ceiling).
3. Personal study, learning, and experimentation.

The grant SHALL NOT cover:
1. Public-facing deployment of any kind.
2. Commercial monetisation of any kind.
3. Use by any foreign entity (foreign intelligence agencies remain
   explicitly banned).

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
   is preserved (the citizen MAY NOT charge for the use of the
   Licensed Work or any derivative work).
4. No public-facing deployment (the citizen's instance is private —
   no `*.cianchosaint.ie` subdomains are issued to natural-person
   citizens).

#### Scenario: The grant excludes commercial monetisation

- **WHEN** the operator inspects the new "NATURAL PERSON CITIZEN
  GRANT" section
- **THEN** the section SHALL state that the grant does NOT cover
  commercial monetisation of any kind
- **AND** SHALL NOT introduce any new exception to (1) of `LICENSE.md`

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
  (per the Pocket ID attribute check)
