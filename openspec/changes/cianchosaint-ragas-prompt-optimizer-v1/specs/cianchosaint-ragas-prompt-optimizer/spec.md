# cianchosaint-ragas-prompt-optimizer Capability

## Purpose

`cianchosaint-ragas-prompt-optimizer` provides the canonical RAGAS-driven prompt optimization + reward-hacking study + production-traffic loop for the politician BAML extraction. Mirrors cianfhoghlaim's `loop-lab-table/{03_optimize, 04_reward_hacking, 06_refuel}`:

- **`adk optimize` (GEPA)** rewrites the agent's instruction from its own scored failures
- **`reflection_minibatch_size=3`** drives the reflection loop
- **`max_metric_calls=100`** caps the total cost
- The **reward-hacking study** shows that the same coach pointed at honest vs gameable judges produces different scores
- The **production-traffic loop** mints real failures into the eval set

## Background

Cianfhoghlaim's `loop-lab-table/03_optimize` shows the canonical pattern:

> The one rule to carry through all six levels: *the loop is neutral machinery — it pushes up whatever number you hand it. Everything here is about which number you hand it.*

The politician BAML extraction has no measured quality — no gold-standard Q/A pairs + no canonical judges + no GEPA optimization + no reward-hacking study + no production-traffic loop.

This change lands the canonical optimizer + study + traffic loop, all modelled on `loop-lab-table/{03_optimize, 04_reward_hacking, 06_refuel}`.

## ADDED Requirements

### Requirement: The canonical GEPA optimization runner

The system SHALL provide a `run_optimization(...)` function at `scripts/politician_optimize.py`.

#### Scenario: The runner invokes `adk optimize` (GEPA) on the canonical eval dataset

- **WHEN** the operator runs `python3 scripts/politician_optimize.py`
- **THEN** the runner SHALL invoke `adk optimize` (or its equivalent) with the `train.evalset.json` + `eval_config.json` + `optimizer_config.json`
- **AND** the resulting `instruction_after.txt` SHALL be persisted to `scripts/politician_gepa_run_winner.txt`

#### Scenario: The runner respects the max_metric_calls budget

- **WHEN** `optimizer_config.json` specifies `max_metric_calls=100`
- **THEN** the runner SHALL cap the total calls at 100
- **AND** SHALL emit a log line every 10 calls so the cost is observable

### Requirement: The canonical reward-hacking study

The system SHALL provide a `run_study(num_runs=4)` function at `scripts/politician_reward_hacking_study.py`.

#### Scenario: The study shows that the same coach produces different scores under different judges

- **WHEN** the operator runs `python3 scripts/politician_reward_hacking_study.py`
- **THEN** the runner SHALL invoke the same coach pointed at the honest + gameable judges in `num_runs` rounds
- **AND** the runner SHALL emit a table showing the score divergence (per cianfhoghlaim's `04_reward_hacking/hack_2sec.py`)

### Requirement: The canonical production-traffic runner

The system SHALL provide a `send_traffic(num_parties=8, num_seeds=5)` function at `scripts/politician_send_traffic.py`.

#### Scenario: The runner sends the canonical 13 conversations

- **WHEN** the operator runs `python3 scripts/politician_send_traffic.py`
- **THEN** the runner SHALL send 8 holdout + 5 seed conversations (matching cianfhoghlaim's `06_refuel/send_traffic.py`)
- **AND** SHALL record every conversation for downstream harvesting

### Requirement: The canonical harvest runner

The system SHALL provide a `harvest_failures()` function at `scripts/politician_harvest.py`.

#### Scenario: The runner grades real dinners offline

- **WHEN** the operator runs `python3 scripts/politician_harvest.py`
- **THEN** the runner SHALL re-grade every harvested conversation with the canonical `every_politician_account_collected` honest judge
- **AND** SHALL mint every failure into `train.evalset.json` (or a sibling) for the next round's GEPA training

### Requirement: The pre-baked candidates

The system SHALL ship 3 pre-baked candidate instructions (mirroring `loop-lab-table/03_optimize/prebaked/`):

- `politician_gepa_run_draft.txt` — the day-one draft
- `politician_gepa_run_winner.txt` — the GEPA winner
- `politician_gepa_run_hacked.txt` — the ratings-hack version

#### Scenario: The candidates ship in the canonical location

- **WHEN** the operator inspects `scripts/`
- **THEN** the 3 files SHALL be present
- **AND** each SHALL be a non-empty politician-resolution instruction

### Requirement: The conservative-posture guard

The system SHALL preserve the OSINT allowlist gate on every optimization + harvest run.

#### Scenario: OSINT allowlist is checked during optimization

- **WHEN** the GEPA runner generates candidate instructions
- **THEN** the runner SHALL verify every URL reference against `dlt_sources/cianchosaint/common/osint_allowlist.yaml`
- **AND** SHALL reject any candidate that violates the gate

## Cross-references

- [`../../scripts/politician_optimize.py`](../../scripts/politician_optimize.py) — the GEPA runner
- [`../../scripts/politician_reward_hacking_study.py`](../../scripts/politician_reward_hacking_study.py) — the reward-hacking study
- [`../../scripts/politician_send_traffic.py`](../../scripts/politician_send_traffic.py) — the production-traffic runner
- [`../../scripts/politician_harvest.py`](../../scripts/politician_harvest.py) — the harvest runner
- [`../../tests/evals/politician/world.py`](../../tests/evals/politician/world.py) — the deterministic world
- cianfhoghlaim `loop-lab-table/03_optimize` — upstream reference
- cianfhoghlaim `loop-lab-table/04_reward_hacking` — the reward-hacking study pattern
- cianfhoghlaim `loop-lab-table/06_refuel` — the production-deployment pattern
