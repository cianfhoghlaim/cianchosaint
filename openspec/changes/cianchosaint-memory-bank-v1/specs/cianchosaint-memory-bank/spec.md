# cianchosaint-memory-bank Capability

## Purpose

`cianchosaint-memory-bank` provides the canonical `CianchosaintMemoryService` for cross-session learning. Mirrors cianfhoghlaim's `docs/google_examples/adk-examples/agent-valley-archive`:

- 4 canonical key prefixes: `(none)` (this visit), `user:` (this analyst, forever), `app:` (everyone, forever), `temp:` (this turn only)
- `FILING["allowed_topics"]` governance at write time (what topics may be filed for each entity class)
- `CianchosaintMemoryService(BaseMemoryService)` with `app:` prefix scope (per the user's selection)

## Background

Cianfhoghlaim's `agent-valley-archive` shows the canonical Memory Bank pattern:

- The `state.py` defines 3 key prefixes: `(none)` / `user:` / `app:`
- The `topics.py` defines `FILING["allowed_topics"]` — governance at write time
- The `memory.py` defines `MarkdownMemoryService(BaseMemoryService)` — a custom memory service whose `add_session_to_memory(session)` + `search_memory(...)` work over a Markdown file

The user selected the `app:` prefix scope (per the prior conversation): every cianchosaint web app + every BIPP/BIDP/BIIP worker + every cross-cutting workflow shares Farage investigations across all 8 surfaces.

Cianchosaint has `cognee_store` + `graphiti_store` (general-purpose knowledge graphs) but no notion of `user:` / `app:` scoped memory. Every conversation is independent; no cross-session learning.

## ADDED Requirements

### Requirement: The CianchosaintMemoryService class

The system SHALL provide a `CianchosaintMemoryService(BaseMemoryService)` class at `agents/cianchosaint/memory_bank/service.py`.

#### Scenario: The service subclasses BaseMemoryService

- **WHEN** the operator imports `CianchosaintMemoryService` from `agents.cianchosaint.memory_bank.service`
- **THEN** the class SHALL be a subclass of `google.adk.memory.BaseMemoryService`
- **AND** the class SHALL implement `add_session_to_memory(session)` + `search_memory(...)`

#### Scenario: The service persists across process boundaries

- **WHEN** the service stores a memory under `app:` prefix
- **AND** the process restarts
- **THEN** the next `search_memory(...)` call SHALL return the stored memory
- **AND** the persistence SHALL use the existing cianchosaint storage stack (cognee_store + graphiti_store)

### Requirement: The `app:` prefix scope (per the user's selection)

The system SHALL store all memories under the `app:` prefix by default (not `user:`).

#### Scenario: The `app:` scope is the default

- **WHEN** the operator invokes `add_session_to_memory(session)` without specifying a scope
- **THEN** the memory SHALL be stored under `("cianchosaint", "app")` scope
- **AND** every cianchosaint surface (8 web apps + BIPP/BIDP/BIIP workers + workflow graphs) SHALL share the same scope

#### Scenario: Cross-session recall works

- **WHEN** agent A stores "Nigel Farage led UKIP from 2006-2016" under `app:` scope
- **AND** agent B queries `search_memory(query="UKIP leadership")` in a different session
- **THEN** agent B SHALL receive "Nigel Farage led UKIP from 2006-2016" as a memory fact
- **AND** the recall SHALL NOT cross scopes (no leakage to non-cianchosaint agents)

### Requirement: The `FILING["allowed_topics"]` governance

The system SHALL enforce topic-level governance on every `add_session_to_memory` call.

#### Scenario: Disallowed topics are rejected

- **WHEN** the operator invokes `add_session_to_memory(session)` with a candidate whose topic is NOT in `FILING["allowed_topics"]`
- **THEN** the service SHALL reject the candidate (no persistence)
- **AND** SHALL emit a `governance_rejected` log event with the disallowed topic name

#### Scenario: Allowed topics are persisted

- **WHEN** the operator invokes `add_session_to_memory(session)` with a candidate whose topic IS in `FILING["allowed_topics"]`
- **THEN** the candidate SHALL be persisted under the `app:` scope
- **AND** SHALL be retrievable via `search_memory(query=<topic>)`

### Requirement: The 4 canonical key prefixes

The system SHALL support 4 key prefixes (mirroring cianfhoghlaim's state.py):

| Prefix | Scope | Survives process? |
|---|---|---|
| `(none)` | this visit only | no |
| `user:` | this analyst, forever | yes |
| `app:` | everyone, forever | yes |
| `temp:` | this turn only | no |

#### Scenario: The prefixes are documented and exported

- **WHEN** the operator imports `from agents.cianchosaint.memory_bank import *`
- **THEN** the 4 prefix constants SHALL be exported
- **AND** the constants SHALL be the canonical cianfhoghlaim-style names

### Requirement: The conservative-posture guard

The system SHALL enforce the OSINT allowlist gate on every memory write (per `cianchosaint-per-constituency-agents` spec + `cianchosaint-baml-schemas` spec).

#### Scenario: Disallowed URLs are not persisted

- **WHEN** `add_session_to_memory(session)` extracts a candidate containing a URL NOT on the cianchosaint OSINT allowlist
- **THEN** the candidate SHALL be rejected
- **AND** the rejection SHALL be logged with the disallowed URL

## Cross-references

- [`../../agents/cianchosaint/memory_bank/service.py`](../../agents/cianchosaint/memory_bank/service.py) — the canonical service
- [`../../agents/cianchosaint/memory_bank/state.py`](../../agents/cianchosaint/memory_bank/state.py) — the key prefixes
- [`../../agents/cianchosaint/memory_bank/topics.py`](../../agents/cianchosaint/memory_bank/topics.py) — the `FILING["allowed_topics"]` governance
- [`../../agents/cianchosaint/_base.py`](../../agents/cianchosaint/_base.py) — the canonical `CianchosaintAgentBase`
- cianfhoghlaim `docs/google_examples/adk-examples/agent-valley-archive/archive/` — upstream reference
