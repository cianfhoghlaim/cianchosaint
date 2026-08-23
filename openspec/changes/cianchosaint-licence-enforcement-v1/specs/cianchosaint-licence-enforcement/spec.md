# Spec Delta: cianchosaint-licence-enforcement

This delta is applied by the openspec change
[`cianchosaint-licence-enforcement-v1`](../proposal.md). It describes
the ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-licence-enforcement/spec.md`](../../../../specs/cianchosaint-licence-enforcement/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: The Dagster sensor that monitors public sources for evidence of unauthorised use

The system SHALL provide a Dagster sensor at
`orchestration/defs/licence_enforcement_sensor.py` named
`licence_enforcement_sensor` that:

1. Runs daily (`minimum_interval_seconds=86400`).
2. Queries the 3 signal sources for evidence patterns matching the
   `LICENSE.md` §Warrant to enforce trigger conditions:
   - **Langfuse observability** — the
     `licence_violation_attempt` log stream (already emitted by the
     Hono API gateway + the 8 per-persona web apps).
   - **change-detection.io monitors** — the monitor webhooks that
     fire when a monitored page (e.g. a foreign intelligence
     agency's job page) changes.
   - **Structured logging** — the `cianchosaint.licence` log stream
     that the platform emits whenever a request crosses a licence
     boundary.
3. Emits a `RunRequest` for the `licence_enforcement_job` Dagster
   job when a signal matches a trigger condition.
4. Returns `None` (no-op) when no signals are detected.

The sensor SHALL be registered with Dagster via the existing
`orchestration/definitions.py` entry point.

#### Scenario: The sensor runs daily

- **WHEN** Dagster evaluates the sensor
- **THEN** the sensor SHALL NOT run more frequently than once per
  24 hours (the `minimum_interval_seconds=86400` configuration)

#### Scenario: The sensor queries the 3 signal sources

- **WHEN** Dagster evaluates the sensor
- **THEN** the sensor SHALL query the Langfuse observability stream
- **AND** SHALL query the change-detection.io monitor webhooks
- **AND** SHALL query the structured logging stream

#### Scenario: The sensor emits a RunRequest when a signal matches

- **WHEN** the sensor detects a signal matching the trigger condition
  (A) — foreign entity's job advertisement / press release / etc.
- **THEN** the sensor SHALL emit a `RunRequest` for the
  `licence_enforcement_job`
- **AND** SHALL include the signal's source URL + matched pattern in
  the RunRequest's `tags` (for downstream alerting)

#### Scenario: The sensor returns a no-op when no signals are detected

- **WHEN** the sensor evaluates and detects no matching signals
- **THEN** the sensor SHALL return `None`
- **AND** Dagster SHALL NOT trigger the `licence_enforcement_job`

### Requirement: The conservative posture (sensor returns a no-op until the operator wires in the live signal sources)

The system SHALL enforce the conservative posture until the operator
wires in the live signal sources (per the follow-up
`cianchosaint-licence-enforcement-signal-sources-v1` change):

1. The sensor SHALL return `None` (no-op) by default.
2. The sensor SHALL NOT query any third-party service until the
   operator has explicitly configured the Infisical + Locket secret
   refs.
3. The sensor SHALL log `checking_licence_enforcement_signals` on
   every evaluation (so operators can verify the sensor is running
   without triggering any signals).

#### Scenario: The sensor returns a no-op until wired in

- **WHEN** the operator inspects
  `orchestration/defs/licence_enforcement_sensor.py`
- **THEN** the sensor function SHALL return `None` as its default
  behaviour
- **AND** SHALL NOT query Langfuse, change-detection.io, or any
  structured logging stream until the follow-up change wires in
  the live signal sources

#### Scenario: The sensor logs every evaluation

- **WHEN** Dagster evaluates the sensor
- **THEN** the sensor SHALL emit a `checking_licence_enforcement_signals`
  log line at `INFO` level
- **AND** the log line SHALL be emitted to the `cianchosaint.licence`
  log stream

#### Scenario: The sensor is conservative about false positives

- **WHEN** the sensor evaluates and detects an ambiguous signal
  (e.g. a job advertisement mentioning "OSINT" without naming
  cianchosaint explicitly)
- **THEN** the sensor SHALL NOT emit a `RunRequest`
- **AND** SHALL log a `licence_signal_ambiguous` warning with the
  signal's source URL for operator review
