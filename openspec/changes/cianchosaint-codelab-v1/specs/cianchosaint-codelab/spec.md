# cianchosaint-codelab Capability

## Purpose

`cianchosaint-codelab` provides the canonical markdown walkthrough + Colab-style notebook builder + assertion runner for the politician pipeline. Mirrors cianfhoghlaim's codelab convention (`loop-lab-table/codelab/` + `support-memory-lab/codelab/` + `monstertix/codelab/`):

> "Every codelab follows the same convention: `codelab/<name>.md` is the markdown walkthrough, `notebooks/<name>.ipynb` is the buildable notebook, `solutions/` has the finished code, `scripts/walk.py` runs every assertion as a sentence."

## Background

Cianfhoghlaim's codelabs are extensive:
- `loop-lab-table/codelab/loop-lab-table.md` — 6-rung marathon coach codelab (per `codelab/loop-lab-table.md`)
- `loop-lab-table/notebooks/build.py` — builds the Colab notebook from the runnable modules
- `support-memory-lab/codelab/` + `notebooks/` — the 5-rung memory codelab
- `monstertix/codelab/` — the long-running agent codelab

Cianchosaint has NO codelabs. The existing `openspec/changes/cianchosaint-politician-schema-v1/` change shipped the 7 case-study politicians + the BAML extraction + the 4 FunctionTools, but there's no narrative walkthrough that ties them together for a new analyst.

This change lands the canonical codelab for the cianchosaint politician pipeline.

## ADDED Requirements

### Requirement: The codelab markdown walkthrough

The system SHALL provide a `codelab/politician-pipeline.md` that walks a new analyst through the full pipeline:

- Setup (clone + venv + .env + the canonical 5 mise tasks)
- The 7 case-study politicians
- The BAML `ExtractPoliticianFromWebPage` function (per `cianchosaint-politician-schema-v1`)
- The 4 FunctionTools (`politician_account_resolver`, `adjacent_context_resolver`, `funder_network_graph`, `wikipedia_bridge`)
- The 3 workflow graphs (`politician_resolver_graph`, `funder_network_graph`, `wikipedia_bridge_graph`)
- The RAGAS eval + GEPA optimizer (per `cianchosaint-ragas-eval-dataset-v1` + `cianchosaint-ragas-prompt-optimizer-v1`)

#### Scenario: The codelab is the canonical narrative

- **WHEN** the operator opens `codelab/politician-pipeline.md`
- **THEN** the codelab SHALL have a Setup → 5 runnable levels → Exercises structure
- **AND** each level SHALL have a sentence-form assertion (mirrors `loop-lab-table/codelab/loop-lab-table.md`)

### Requirement: The Colab-style notebook builder

The system SHALL provide a `notebooks/build.py` that builds `notebooks/politician_pipeline.ipynb` from the runnable modules.

#### Scenario: The notebook is buildable

- **WHEN** the operator runs `python3 notebooks/build.py`
- **THEN** the script SHALL write `notebooks/politician_pipeline.ipynb` with the canonical Colab schema
- **AND** every cell SHALL have a stable `metadata.id` so the codelab can deep-link via `#scrollTo=<id>`

### Requirement: The canonical walk.py

The system SHALL provide a `scripts/walk.py` that runs every assertion as a sentence against the real pipeline.

#### Scenario: The walk runs every assertion

- **WHEN** the operator runs `python3 scripts/walk.py`
- **THEN** every assertion in the codelab SHALL be checked
- **AND** a failure SHALL mean the prose is wrong, not just the code

### Requirement: The conservative-posture guard

The system SHALL preserve the OSINT allowlist gate on every codelab exercise.

#### Scenario: OSINT allowlist is checked in every exercise

- **WHEN** the analyst completes an exercise that introduces a new URL
- **THEN** the codelab SHALL instruct them to verify the URL against `dlt_sources/cianchosaint/common/osint_allowlist.yaml`
- **AND** SHALL NOT proceed if the URL is not allowlisted

## Cross-references

- [`../../../openspec/changes/cianchosaint-codelab-v1/codelab/politician-pipeline.md`](../../../openspec/changes/cianchosaint-codelab-v1/codelab/politician-pipeline.md) — the canonical walkthrough
- [`../../../openspec/changes/cianchosaint-codelab-v1/notebooks/build.py`](../../../openspec/changes/cianchosaint-codelab-v1/notebooks/build.py) — the Colab-style notebook builder
- [`../../../openspec/changes/cianchosaint-codelab-v1/scripts/walk.py`](../../../openspec/changes/cianchosaint-codelab-v1/scripts/walk.py) — the assertion runner
- cianfhoghlaim `loop-lab-table/codelab/loop-lab-table.md` — upstream reference
- cianfhoghlaim `loop-lab-table/notebooks/build.py` — upstream reference
- cianfhoghlaim `loop-lab-table/scripts/walk.py` — upstream reference
