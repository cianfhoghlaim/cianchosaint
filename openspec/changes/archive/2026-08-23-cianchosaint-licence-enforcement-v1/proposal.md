# Change: cianchosaint-licence-enforcement-v1

## Why

`LICENSE.md` §Warrant to enforce grants the British Isles
public-sector bodies (and the Licensor) the right to enforce the
licence terms against any entity making production use of the
Licensed Work in breach of the Additional Use Grant, the
Foreign-Use Gate, or any other term.

Per the licence, the warrant triggers on either of:

(A) **Publicly observable evidence** that a non-British-Isles body is
    making production use of the Licensed Work in breach — including
    job advertisements, press releases, derivative works, or
    copy-pasted source code in closed products.

(B) **A credible written complaint** submitted to the enforcing body.

The Licensor cannot practically police every foreign use of the
Licensed Work. The platform needs an automated operational layer that
monitors public sources (Langfuse observability + change-detection.io
monitors + structured logging) for evidence patterns matching the
trigger conditions.

This change ships:

1. A Dagster sensor at `orchestration/defs/licence_enforcement_sensor.py`
   that monitors public sources for evidence patterns matching the
   trigger conditions, runs daily, and emits a RunRequest when a
   signal is detected.
2. The openspec capability spec (`cianchosaint-licence-enforcement`)
   that documents the sensor, its inputs, its outputs, and the
   conservative posture (sensor returns a no-op until the operator
   wires in the live signal sources).

## What changes

- **1 NEW canonical spec**: `cianchosaint-licence-enforcement` with 2
  ADDED Requirements:
  - Requirement: The Dagster sensor that monitors public sources for
    evidence of unauthorised use by foreign entities
  - Requirement: The conservative posture (sensor returns a no-op
    until the operator wires in the live signal sources)

- **1 NEW Python module** at
  `orchestration/defs/licence_enforcement_sensor.py` — the canonical
  Dagster sensor.

## Impact

- Affected specs: 1 NEW spec (`cianchosaint-licence-enforcement/`).
- Affected code/config: 1 NEW Python module at
  `orchestration/defs/licence_enforcement_sensor.py` (~60 LOC).
- No secret values are written to disk: all keys resolve via
  `infisical://dev-baile/cianchosaint/...` template refs hydrated by
  mise + Locket.
- No runtime behaviour changes — the sensor is registered but returns
  a no-op (the live signal sources are wired in a follow-up change).

## Out of scope

- The live signal sources (Langfuse observability queries +
  change-detection.io monitor webhooks + structured log queries).
  Out of scope — covered by the follow-up
  `cianchosaint-licence-enforcement-signal-sources-v1` change.
- The warrant enforcement action itself (sending a cease-and-desist
  letter, filing an injunction, etc.). Out of scope — the sensor
  surfaces signals, the Licensor + the British Isles enforcing
  bodies decide the action.
- The licence_amendment for the natural-person citizen grant.
  Covered by the next change (`cianchosaint-citizen-use-grant-v1`).

## Validation criteria

1. `openspec validate cianchosaint-licence-enforcement-v1 --strict`
   passes (exit code 0).
2. `openspec validate cianchosaint-licence-enforcement --strict` passes
   (exit code 0).
3. `python3 -c "import ast; ast.parse(open('orchestration/defs/licence_enforcement_sensor.py').read())"`
   passes (valid Python).
4. The sensor function returns `None` (the conservative no-op).

## Dependencies

`Blocked by: none`
`Blocked by (soft): cianchosaint-repo-foundation-v1` (extends; the
  upstream licence posture)
`Affected repos: cianchosaint.` (Cianfhoghlaim + leabharlann remain
  completely unchanged.)

## Cross-repo sync

This change touches **ONLY the `cianchosaint` repo**. See
`cross-repo-sync.md` for the full commit plan.
