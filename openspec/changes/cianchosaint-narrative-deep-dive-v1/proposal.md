# Change: cianchosaint-narrative-deep-dive-v1

## Why

Cianfhoghlaim's `docs/google_examples/adk-examples/agent-valley-archive` shows the canonical `NarrativeContext` pattern: every dossier gets a narrative context (Vesper's "fairy lights in your antlers" / "I keep the tower where the valley writes everything down") + a `season` (the bounded window of conversations) + the canonical `FILING["allowed_topics"]` governance.

Per the archive's `archive.py::agent.py`:

> "Why this file carries the lesson: what should NOT be remembered is not something you resist writing into a prompt. It is something the topics make impossible to extract."

The cianchosaint politician pipeline (per `cianchosaint-politician-schema-v1`) currently has raw BAML extraction + 4 FunctionTools + 3 workflow graphs, but no **narrative deep-dive** that gives the dossier a canonical story arc. There's no `season_search` (vector-search the canonical BIPP v2 dossier corpus) or `season_known_issue` (graph-walk the canonical dossier knowledge graph).

This change lands the canonical NarrativeContext + `season_search` + `season_known_issue` pattern for cianchosaint.

## What changes

- **NEW file** `agents/cianchosaint/narrative/__init__.py` (~20 LOC) — package marker
- **NEW file** `agents/cianchosaint/narrative/context.py` (~120 LOC) — the canonical `NarrativeContext` class (mirrors `agent-valley-archive/archive/topics.py`)
- **NEW file** `agents/cianchosaint/narrative/season.py` (~150 LOC) — the canonical `season_search` function (per `archive/season.py::season_search` — uses VECTOR_SEARCH over the canonical BIPP v2 dossier corpus)
- **NEW file** `agents/cianchosaint/narrative/dossier.py` (~120 LOC) — the canonical `season_known_issue` function (per `archive/season.py::season_known_issue` — uses GRAPH_TABLE over the canonical dossier knowledge graph)
- **NEW file** `baml_src/cianchosaint/politics/bipp_v2_narrative.baml` (~80 LOC) — the `NarrativeContext` BAML extraction function
- **NEW file** `tests/agents/cianchosaint/test_narrative_deep_dive.py` (~120 LOC) — the smoke test
- **NEW spec delta** `openspec/changes/cianchosaint-narrative-deep-dive-v1/specs/cianchosaint-narrative-deep-dive/spec.md`

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-narrative-deep-dive`)
- Affected code/config: 6 NEW files
- Estimated LOC: ~600 LOC added

## Out of scope (follow-up changes)

- The BIEP v2 dossier knowledge graph (the table for `season_known_issue` to walk) — separate change
- The CocoIndex VECTOR_SEARCH setup (the index for `season_search` to query) — separate change

## Dependencies

`Blocked by: cianchosaint-workflow-graph-v1` (the dossier corpus is produced by the workflow graphs)
`Affected repos: cianchosaint only.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `docs/google_examples/adk-examples/agent-valley-archive` remains the upstream reference.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-narrative-deep-dive-v1 --strict

# 2. run the smoke test
PYTHONPATH=. python3 tests/agents/cianchosaint/test_narrative_deep_dive.py

# 3. regression: existing tests still pass
PYTHONPATH=. python3 tests/agents/cianchosaint/test_agent_factory.py
PYTHONPATH=. python3 tests/agents/integrations/test_agent_registry_runtime.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_long_running_tools.py
PYTHONPATH=. python3 tests/cocoindex_flows/test_shared_lifespan.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_workflow_graphs.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_memory_bank.py
PYTHONPATH=. python3 tests/evals/politician/walk.py
PYTHONPATH=. python3 tests/orchestration/test_dagster_orchestration.py
PYTHONPATH=. python3 tests/openspec/test_sister_mirrors.py

# 4. lint_license
mise run lint:license
```
