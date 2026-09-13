# Cross-Repo Sync: cianchosaint-politician-schema-v1

This change touches ONLY the `cianchosaint/cianchosaint` repo. Cianfhoghlaim + leabharlann remain completely unchanged (the 87 politics PDFs are read-only context).

## Order of Operations

```
[1] cianchosaint → openspec/changes/cianchosaint-politician-schema-v1/
                   (proposal + tasks + cross-repo-sync + 5 spec deltas)
                   Adds: ~30 NEW files (5 DLT source trees + 4 FunctionTools + 2 scripts + 1 BAML file)
                   Modifies: 4 files (political_graph_store.py + osint_allowlist.yaml + mise.toml + __init__.py)
                   Pushed to main.
                        ↓
[2] operator    → cd cianchosaint && openspec validate cianchosaint-politician-schema-v1 --strict
                   → cd cianchosaint && openspec validate --all --strict
                   → All validations pass
                        ↓
[3] operator    → openspec archive cianchosaint-politician-schema-v1 --yes
                        ↓
[4] follow-ups  → The 2 follow-up changes may begin:
                   1. cianchosaint-bipp-v2-cocoindex-v2-v1 (the 7 politician CocoIndex flows)
                   2. cianchosaint-bipp-v2-orchestration-v2-v1 (the Dagster defs + milestone gates)
                   3. cianchosaint-ragas-eval-pipeline-v2-v1 (the politician extraction RAGAS eval)
                   4. cianchosaint-adjacent-cocoindex-v1 (the 4 adjacent CocoIndex flows)
```

## Repo 1: cianchosaint (sole)

**Files to commit** (under `openspec/changes/cianchosaint-politician-schema-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-baml-schemas/spec.md` (the BAML extraction delta)
- `specs/cianchosaint-bipp-v2/spec.md` (the BIPP v2 cohort cross-reference delta)
- `specs/cianchosaint-political-graph/spec.md` (the political graph entity-type delta)
- `specs/cianchosaint-dlt-sources-carveout/spec.md` (the 5 new DLT source-tree deltas)
- `specs/cianchosaint-agents-sync/spec.md` (the agent-fleet registry delta)

**New files in the cianchosaint repo (under `baml_src/`, `dlt_sources/`, `agents/`, `scripts/`)**:

- `baml_src/cianchosaint/politics/politician_extraction.baml`
- `dlt_sources/cianchosaint/politicians/__init__.py` + `_base.py` + `_registry.py`
- `dlt_sources/cianchosaint/politicians/uk/nigel_farage.py`
- `dlt_sources/cianchosaint/politicians/uk/zack_polanski.py`
- `dlt_sources/cianchosaint/politicians/ni/john_o_dowd.py`
- `dlt_sources/cianchosaint/politicians/ni/gordon_lyons.py`
- `dlt_sources/cianchosaint/politicians/ni/paul_givan.py`
- `dlt_sources/cianchosaint/politicians/ni/gavin_robinson.py`
- `dlt_sources/cianchosaint/politicians/scotland/lara_bird.py`
- `dlt_sources/cianchosaint/advisors/__init__.py` + `_base.py` + `_registry.py` + 4 source modules
- `dlt_sources/cianchosaint/funders/__init__.py` + `_base.py` + `_registry.py` + 9 source modules
- `dlt_sources/cianchosaint/historical_associations/__init__.py` + `_base.py` + `_registry.py` + 6 source modules
- `dlt_sources/cianchosaint/wikipedia_archives/__init__.py` + `_base.py` + `_registry.py` + 5 source modules
- `dlt_sources/official_media_cianchosaint/platforms.py`
- `agents/cianchosaint/tools/politician_account_resolver.py`
- `agents/cianchosaint/tools/adjacent_context_resolver.py`
- `agents/cianchosaint/tools/funder_network_graph.py`
- `agents/cianchosaint/tools/wikipedia_bridge.py`
- `scripts/harvest_politicians_from_leabharlann.py`
- `scripts/lint_politician_schema.py`

**Modified files**:

- `agents/cianchosaint/tools/political_graph_store.py` (+4 entity types, +4 relationship types)
- `dlt_sources/cianchosaint/common/osint_allowlist.yaml` (+34 entries)
- `mise.toml` (+7 tasks)
- `agents/cianchosaint/tools/__init__.py` (export the 4 new FunctionTools)
- `dlt_sources/cianchosaint/__init__.py` (export the 5 new DLT source trees)

## Repo 2: cianfhoghlaim (unchanged)

No changes. The education-platform repo is not affected by this change.

## Repo 3: leabharlann (unchanged)

No changes. The 87 politics PDFs are read-only context.
