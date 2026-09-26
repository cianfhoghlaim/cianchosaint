# cianchosaint-ragas-eval-dataset Capability

## Purpose

`cianchosaint-ragas-eval-dataset` provides the canonical RAGAS eval dataset + adversarial judges for the 7 case-study politicians. Mirrors cianfhoghlaim's `loop-lab-table/03_optimize`:

- A **deterministic honest judge** (`every_politician_account_collected`) — Python only, no LLM, walks every fact category
- A **gameable judge** (`star_rating`) — returns random rating, never reads context
- The gold-standard Q/A pairs (`train.evalset.json` + `val.evalset.json`)
- The canonical `world.py` analogue that defines the 7 politicians + 5 fact categories
- The `walk.py` analogue that runs every assertion as a sentence against the real agent

## Background

Cianfhoghlaim's `loop-lab-table/03_optimize` shows the canonical RAGAS pattern with adversarial judges:

- A **deterministic judge** (`everyone_ate`) — Python only, no LLM, walks the table seat-by-seat
- A **gameable judge** (`rating_score`) — just returns star rating, never reads the party
- An eval config that registers BOTH metrics into ADK's `MetricEvaluatorRegistry`
- A reward-hacking study — 4 measured runs showing the same coach pointed at different judges produces different scores

Cianchosaint has the spec for a RAGAS pipeline (per `openspec/changes/cianchosaint-ragas-eval-pipeline-v1/`) but no gold-standard Q/A pairs + no canonical judge functions. The politician BAML extraction has no measured quality.

This change lands the canonical dataset + judges + walk.py, all modelled on `loop-lab-table/03_optimize`.

## ADDED Requirements

### Requirement: The 7 politicians + 5 fact categories

The system SHALL provide a `world.py` analogue at `tests/evals/politician/world.py` with the 7 case-study politicians and 5 fact categories.

#### Scenario: Every politician has the canonical 5 fact categories

- **WHEN** the operator imports `from tests.evals.politician.world import POLITICIANS, FACT_CATEGORIES`
- **THEN** `POLITICIANS` SHALL contain 7 entries: Nigel Farage, Zack Polanski, John O'Dowd, Gordon Lyons, Paul Givan, Gavin Robinson, Lara Bird
- **AND** `FACT_CATEGORIES` SHALL contain 5 entries: canonical_name, party_id, jurisdiction, social_handles, public_metrics

### Requirement: The deterministic honest judge

The system SHALL provide `every_politician_account_collected(actual_politician, expected_politician)` in `world.py` that walks every fact category and checks correctness.

#### Scenario: The honest judge returns the correct score

- **WHEN** the operator runs `every_politician_account_collected(actual, expected)`
- **THEN** the judge SHALL return a score between 0.0 and 1.0
- **AND** the score SHALL be the fraction of fact categories that match
- **AND** the function SHALL be deterministic (no randomness, no LLM)

#### Scenario: The honest judge is verified deterministic

- **WHEN** the operator runs `is_deterministic(every_politician_account_collected)` (per `loop-lab-table/03_optimize/metrics/__init__.py`)
- **THEN** the function SHALL return True (verifying that this judge cannot be gamed by randomness)

### Requirement: The gameable judge

The system SHALL provide `star_rating(actual_politician, expected_politician)` in `world.py` that returns a random star rating WITHOUT reading the context.

#### Scenario: The gameable judge returns a random rating

- **WHEN** the operator runs `star_rating(actual, expected)`
- **THEN** the function SHALL return a float between 0.0 and 1.0 (the rating / 5.0)
- **AND** the result SHALL NOT correlate with `expected` (it's just a random rating)
- **AND** this demonstrates the reward-hacking principle from `loop-lab-table/04_reward_hacking`

### Requirement: The gold-standard Q/A pairs

The system SHALL provide `train.evalset.json` + `val.evalset.json` with gold-standard Q/A pairs for the 7 politicians.

#### Scenario: The training split has canonical Q/A pairs

- **WHEN** the operator opens `tests/evals/politician/train.evalset.json`
- **THEN** the file SHALL contain ≥7 Q/A pairs (one per politician)
- **AND** every Q/A pair SHALL have `input.politician_name` + `expected_output` matching the canonical schema

#### Scenario: The validation split has canonical Q/A pairs

- **WHEN** the operator opens `tests/evals/politician/val.evalset.json`
- **THEN** the file SHALL contain ≥3 Q/A pairs (held-out for validation)
- **AND** the validation pairs SHALL be disjoint from the training pairs

### Requirement: The canonical walk.py

The system SHALL provide a `walk.py` at `tests/evals/politician/walk.py` that runs every assertion as a sentence against the real agent.

#### Scenario: The walk runs every assertion

- **WHEN** the operator runs `python3 tests/evals/politician/walk.py`
- **THEN** every assertion in the lab SHALL be checked
- **AND** a failure SHALL mean the prose is wrong, not just the code

### Requirement: The MetricEvaluatorRegistry helpers

The system SHALL provide `metrics.py` at `tests/evals/politician/metrics.py` with the canonical `politician_metrics` + `register_metrics` helpers.

#### Scenario: The metrics are registered

- **WHEN** the operator runs `register_metrics()` (the canonical `loop-lab-table/03_optimize/metrics/__init__.py` pattern)
- **THEN** both metrics (`every_politician_account_collected` + `star_rating`) SHALL be registered with ADK's `MetricEvaluatorRegistry`
- **AND** the registry SHALL be importable by `adk eval` for use in `eval_config.json`

## Cross-references

- [`../../../tests/evals/politician/world.py`](../../../tests/evals/politician/world.py) — the deterministic world
- [`../../../tests/evals/politician/metrics.py`](../../../tests/evals/politician/metrics.py) — the MetricEvaluatorRegistry helpers
- [`../../../tests/evals/politician/walk.py`](../../../tests/evals/politician/walk.py) — runs every assertion
- cianfhoghlaim `loop-lab-table/03_optimize` — upstream reference
- cianfhoghlaim `loop-lab-table/04_reward_hacking` — the reward-hacking study pattern
- cianfhoghlaim `loop-lab-table/06_refuel` — the production-deployment pattern
