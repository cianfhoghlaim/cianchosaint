# Cross-Repo Sync: cianchosaint-ragas-eval-dataset-v1

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `loop-lab-table/03_optimize` remains the upstream reference. No changes to the cianfhoghlaim or leabharlann repos are needed.

## Order of Operations

```
[1] cianchosaint → openspec/changes/cianchosaint-ragas-eval-dataset-v1/
                   (proposal + tasks + cross-repo-sync + spec)
                   Adds: tests/evals/politician/{__init__,world,metrics}.py
                   Adds: tests/evals/politician/{eval_config,optimizer_config,train,val}.{json,jsonl}
                   Adds: tests/evals/politician/walk.py
                   Pushed to main.
                       ↓
[2] operator    → cd cianchosaint && openspec validate cianchosaint-ragas-eval-dataset-v1 --strict
                  → openspec validate --all --strict
                  → All validations pass
                       ↓
[3] operator    → openspec archive cianchosaint-ragas-eval-dataset-v1 --yes
```

## Repo 1: cianchosaint (sole)

**Files to commit** (under `openspec/changes/cianchosaint-ragas-eval-dataset-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-ragas-eval-dataset/spec.md` (the canonical spec)

**New files**:
- `tests/evals/politician/__init__.py` (~20 LOC)
- `tests/evals/politician/world.py` (~300 LOC) — 7 politicians + 5 fact categories + 2 judges
- `tests/evals/politician/metrics.py` (~150 LOC) — MetricEvaluatorRegistry helpers
- `tests/evals/politician/eval_config.json` (~40 LOC)
- `tests/evals/politician/optimizer_config.json` (~20 LOC)
- `tests/evals/politician/train.evalset.json` (~150 LOC) — the training split
- `tests/evals/politician/val.evalset.json` (~50 LOC) — the validation split
- `tests/evals/politician/walk.py` (~120 LOC) — runs every assertion as a sentence

## Repo 2: cianfhoghlaim (unchanged)

The upstream `loop-lab-table/03_optimize` remains unchanged. We wholesale-adapt the pattern in this change.

## Repo 3: leabharlann (unchanged)

The 87 politics PDFs in `leabharlann/gemini_deep_research/politics/` are read-only context for the politician pipeline (which T2.4 doesn't touch). No changes.
