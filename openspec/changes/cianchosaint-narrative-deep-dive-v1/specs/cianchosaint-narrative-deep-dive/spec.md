# cianchosaint-narrative-deep-dive Capability

## Purpose

`cianchosaint-narrative-deep-dive` provides the canonical `NarrativeContext` + `season_search` + `season_known_issue` for the BIOD v1 dossier deep-dive. Mirrors cianfhoghlaim's `docs/google_examples/adk-examples/agent-valley-archive`:

- `NarrativeContext` — the canonical narrative-arc class (per `agent-valley-archive/archive/topics.py::LANTERN_CONTEXT`)
- `season_search(query)` — VECTOR_SEARCH over the canonical BIPP v2 dossier corpus (per `agent-valley-archive/archive/season.py::season_search`)
- `season_known_issue(mark)` — GRAPH_TABLE walk over the canonical dossier knowledge graph (per `agent-valley-archive/archive/season.py::season_known_issue`)

## Background

Cianfhoghlaim's `agent-valley-archive` shows the canonical pattern:

> "Why this file carries the lesson: what should NOT be remembered is not something you resist writing into a prompt. It is something the topics make impossible to extract."

The cianchosaint politician pipeline (per `cianchosaint-politician-schema-v1`) currently has raw BAML extraction + 4 FunctionTools + 3 workflow graphs, but no **narrative deep-dive** that gives the dossier a canonical story arc + no `season_search` (vector-search the canonical BIPP v2 dossier corpus) + no `season_known_issue` (graph-walk the canonical dossier knowledge graph).

This change lands the canonical NarrativeContext + `season_search` + `season_known_issue` pattern for cianchosaint.

## ADDED Requirements

### Requirement: The NarrativeContext class

The system SHALL provide a `NarrativeContext` class at `agents/cianchosaint/narrative/context.py`.

#### Scenario: The NarrativeContext has the canonical narrative-arc fields

- **WHEN** the operator imports `from agents.cianchosaint.narrative.context import NarrativeContext`
- **THEN** the class SHALL have the canonical narrative-arc fields: `subject_name`, `narrative_summary`, `opening_question`, `constraints`, `closed_topics`
- **AND` SHALL mirror `LANTERN_CONTEXT` from cianfhoghlaim's `agent-valley-archive/archive/topics.py`

### Requirement: The season_search function

The system SHALL provide `season_search(query: str)` at `agents/cianchosaint/narrative/season.py`.

#### Scenario: season_search returns relevant matches

- **WHEN** the operator calls `season_search("UKIP leadership")`
- **THEN` the function SHALL return a list of match dicts (with `who`, `mark`, `distance`)
- `AND` the matches SHALL be sorted by distance (closest first)
- `AND` the function SHALL fall back to empty list when no dossier corpus is available

### Requirement: The season_known_issue function

The system SHALL provide `season_known_issue(mark: str)` at `agents/cianchosaint/narrative/dossier.py`.

#### Scenario: season_known_issue walks the dossier graph

- **WHEN** the operator calls `season_known_issue("q7")`
- **THEN` the function SHALL return a dict with `count`, `who`, `said`, `known_issue`, `found_by`, `walked`, `path`
- `AND` SHALL fall back gracefully when no dossier graph is available

### Requirement: The NarrativeContext BAML extraction

The system SHALL provide a BAML function `ExtractNarrativeContext` in `baml_src/cianchosaint/politics/bipp_v2_narrative.baml`.

#### Scenario: The BAML function extracts the canonical narrative arc

- **WHEN` the operator calls `b.ExtractNarrativeContext(input=dossier)`
- `THEN` the function SHALL return a `NarrativeContext` record
- `AND` the function SHALL use the Langfuse prompt resolver per `cianchosaint-langfuse-prompt-management-v1`

### Requirement: Conservative-posture guard

The system SHALL preserve the OSINT allowlist gate on every narrative operation.

#### Scenario: OSINT allowlist is preserved

- `WHEN` the operator runs any narrative operation
- `THEN` the function SHALL verify every URL against `dlt_sources/cianchosaint/common/osint_allowlist.yaml`
- `AND` SHALL NOT proceed if any URL is not allowlisted

## Cross-references

- [`../../../agents/cianchosaint/narrative/context.py`](../../../agents/cianchosaint/narrative/context.py) — the canonical NarrativeContext
- [`../../../agents/cianchosaint/narrative/season.py`](../../../agents/cianchosaint/narrative/season.py) — the canonical season_search
- [`../../../agents/cianchosaint/narrative/dossier.py`](../../../agents/cianchosaint/narrative/dossier.py) — the canonical season_known_issue
- cianfhoghlaim `docs/google_examples/adk-examples/agent-valley-archive/` — upstream reference
- cianfhoghlaim `agent-valley-archive/archive/topics.py::LANTERN_CONTEXT` — upstream narrative context
- cianfhoghlaim `agent-valley-archive/archive/season.py` — upstream season implementation
