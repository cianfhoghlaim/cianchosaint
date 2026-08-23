# cianchosaint-licence-enforcement Capability

## Purpose

`cianchosaint-licence-enforcement` is the capability that
**operationalises the warrant-to-enforce clause** from `LICENSE.md`.
The Dagster sensor at
`orchestration/defs/licence_enforcement_sensor.py` runs daily and
queries 3 signal sources (Langfuse observability +
change-detection.io monitors + structured logging) for evidence of
unauthorised use by foreign entities.

The sensor is **conservative by design**:

1. Returns a no-op (`None`) until the operator wires in the live
   signal sources.
2. Emits a `RunRequest` for the `licence_enforcement_job` only when
   a signal matches the `LICENSE.md` §Warrant to enforce trigger
   conditions.
3. Logs `checking_licence_enforcement_signals` on every evaluation
   for observability.

The sensor does NOT take enforcement action — it surfaces signals,
and the Licensor + the British Isles enforcing bodies decide the
action (per the licence).

## Background

`LICENSE.md` §Warrant to enforce grants the British Isles
public-sector bodies (and the Licensor) the right to enforce the
licence terms against any entity making production use of the
Licensed Work in breach of the Additional Use Grant, the
Foreign-Use Gate, or any other term.

The warrant triggers on:

(A) **Publicly observable evidence** that a non-British-Isles body is
    making production use in breach — including job ads, press
    releases, derivative works, copy-pasted source code.

(B) **A credible written complaint** from a named source.

The Licensor cannot practically police every foreign use. This
capability automates the operational layer — the sensor surfaces
signals, the Licensor decides the action.

## Requirements

### Requirement: The Dagster sensor that monitors public sources for evidence of unauthorised use

The system SHALL provide a Dagster sensor at
`orchestration/defs/licence_enforcement_sensor.py` named
`licence_enforcement_sensor` that runs daily, queries the 3 signal
sources (Langfuse, change-detection.io, structured logging), and
emits a `RunRequest` for the `licence_enforcement_job` when a
signal matches a trigger condition.

#### Scenario: The sensor runs daily

- **WHEN** Dagster evaluates the sensor
- **THEN** the sensor SHALL NOT run more frequently than once per
  24 hours

#### Scenario: The sensor queries the 3 signal sources

- **WHEN** Dagster evaluates the sensor
- **THEN** the sensor SHALL query Langfuse, change-detection.io, and
  the structured logging stream

#### Scenario: The sensor emits a RunRequest when a signal matches

- **WHEN** the sensor detects a signal matching trigger condition (A)
- **THEN** the sensor SHALL emit a `RunRequest` for the
  `licence_enforcement_job`
- **AND** SHALL include the signal's source URL + matched pattern in
  the RunRequest's `tags`

#### Scenario: The sensor returns a no-op when no signals are detected

- **WHEN** the sensor evaluates and detects no matching signals
- **THEN** the sensor SHALL return `None`
- **AND** Dagster SHALL NOT trigger the `licence_enforcement_job`

### Requirement: The conservative posture (sensor returns a no-op until the operator wires in the live signal sources)

The system SHALL enforce the conservative posture: the sensor
returns `None` by default and SHALL NOT query any third-party
service until the operator wires in the live signal sources.

#### Scenario: The sensor returns a no-op until wired in

- **WHEN** the operator inspects
  `orchestration/defs/licence_enforcement_sensor.py`
- **THEN** the sensor function SHALL return `None` as its default
  behaviour

#### Scenario: The sensor logs every evaluation

- **WHEN** Dagster evaluates the sensor
- **THEN** the sensor SHALL emit a `checking_licence_enforcement_signals`
  log line at `INFO` level
- **AND** the log line SHALL be emitted to the `cianchosaint.licence`
  log stream

#### Scenario: The sensor is conservative about false positives

- **WHEN** the sensor evaluates and detects an ambiguous signal
- **THEN** the sensor SHALL NOT emit a `RunRequest`
- **AND** SHALL log a `licence_signal_ambiguous` warning for
  operator review

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document (BUSL-1.1 v2)
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../cianchosaint-repo-foundation/spec.md`](../cianchosaint-repo-foundation/spec.md) — the upstream licence posture
