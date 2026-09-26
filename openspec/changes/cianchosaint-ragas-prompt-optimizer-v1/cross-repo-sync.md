# Cross-Repo Sync: cianchosaint-ragas-prompt-optimizer-v1

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `loop-lab-table/{03_optimize, 04_reward_hacking, 06_refuel}` remain the upstream reference. No changes to the cianfhoghlaim or leabharlann repos are needed.

## Order of Operations

```
[1] cianchosaint → openspec/changes/cianchosaint-ragas-prompt-optimizer-v1/
                   (proposal + tasks + cross-repo-sync + spec)
                   Adds: scripts/politician_{optimize,reward_hacking_study,send_traffic,harvest}.py
                   Adds: scripts/politician_gepa_run_{draft,winner,hacked}.txt
                   Pushed to main.
                       ↓
[2] operator    → cd cianchosaint && openspec validate cianchosaint-ragas-prompt-optimizer-v1 --strict
                  → openspec validate --all --strict
                  → All validations pass
                       ↓
[3] operator    → openspec archive cianchosaint-ragas-prompt-optimizer-v1 --yes
```

## Repo 1: cianchosaint (sole)

**Files to commit** (under `openspec/changes/cianchosaint-ragas-prompt-optimizer-v1/`):

- `proposal.md` (DONE)
- `tasks.md` (DONE)
- `cross-repo-sync.md` (this file)
- `specs/cianchosaint-ragas-prompt-optimizer/spec.md` (the canonical spec)

**New files**:
- `scripts/politician_optimize.py` (~200 LOC) — the GEPA runner
- `scripts/politician_reward_hacking_study.py` (~150 LOC) — the reward-hacking study
- `scripts/politician_send_traffic.py` (~120 LOC) — the production-traffic runner
- `scripts/politician_harvest.py` (~120 LOC) — the harvest runner
- `scripts/politician_gepa_run_draft.txt` — the day-one draft
- `scripts/politician_gepa_run_winner.txt` — the GEPA winner
- `scripts/politician_gepa_run_hacked.txt` — the ratings-hack version

## Repo 2: cianfhoghlaim (unchanged)

The upstream `loop-lab-table/{03_optimize, 04_reward_hacking, 06_refuel}` remain unchanged. We wholesale-adapt the patterns in this change.

## Repo 3: leabharlann (unchanged)

The 87 politics PDFs in `leabharlann/gemini_deep_research/politics/` are read-only context for the politician pipeline (which T3.1 doesn't touch). No changes.
