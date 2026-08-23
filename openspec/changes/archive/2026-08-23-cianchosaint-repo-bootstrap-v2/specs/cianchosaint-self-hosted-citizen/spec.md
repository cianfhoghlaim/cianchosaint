# Spec Delta: cianchosaint-self-hosted-citizen

This delta is applied by the openspec change
[`cianchosaint-repo-bootstrap-v2`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-self-hosted-citizen/spec.md`](../../../../specs/cianchosaint-self-hosted-citizen/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: Stagehand + Locket new stacks

The system SHALL provide 2 new-build Docker Compose stacks at
`bonneagar/stacks/stagehand/` + `bonneagar/stacks/locket/` that are
NOT in Cianfhoghlaim.

#### Scenario: Stagehand + Locket stacks present

- **WHEN** the operator runs `ls bonneagar/stacks/`
- **THEN** `stagehand/` SHALL exist with the open-source Stagehand +
  headless Chrome stack (compose.yaml + Dockerfile + Pangolin
  resource pattern + blueprint.yaml + .env.example + README.md)
- **AND** `locket/` SHALL exist with the secret-injection sidecar
  stack (compose.yaml + Pangolin resource pattern + blueprint.yaml +
  .env.example + README.md)

### Requirement: Self-hosted citizen uses Stagehand instead of BrowserBase

The system SHALL default the self-hosted citizen Docker Compose
bundle to use the open-source Stagehand + headless Chrome stack
(rather than the commercial BrowserBase SaaS), so citizens don't
need a SaaS subscription.

#### Scenario: Self-hosted citizen runs Stagehand in their container

- **GIVEN** a member of the public runs the
  `docker/cianchosaint-citizen/` Docker Compose bundle
- **WHEN** the bundle starts
- **THEN** the Stagehand container SHALL start in the bundle
- **AND** the citizen SHALL be able to interact with Cian about
  British Isles official OSINT sources without any SaaS dependency
