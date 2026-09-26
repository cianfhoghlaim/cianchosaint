# Change: cianchosaint-dagster-orchestration-v1

## Why

Cianfhoghlaim's `orchestration/defs/2_materials/_base/jurisdiction_assets_base.py` shows the canonical `JurisdictionAssetsBase` pattern. The cianfhoghlaim Wave 2 vertical pipelines refactored 10 per-jurisdiction `*_assets.py` files of ~378 LOC each (england, ireland, scotland, wales, ni, scot_wales_ni, crown_dependencies, isle_of_man, jersey, guernsey) into thin subclasses of ~50 LOC each — a net savings of ~3,300 LOC.

Cianchosaint has the 5-layer `orchestration/defs/` folder structure (`1_ingestion`, `2_materials`, `3_model_lifecycle`, `4_asset_generation`, `5_agent_ops`) but no `_base/jurisdiction_assets_base.py`. Each jurisdiction's per-vertical asset is hand-rolled.

This change lands the canonical `JurisdictionAssetsBase` for cianchosaint + converts 1 jurisdiction (the Garda — per the user's selection) as the canonical example.

## What changes

- **NEW file** `orchestration/defs/2_materials/_base/__init__.py` (~20 LOC) — the _base package marker
- **NEW file** `orchestration/defs/2_materials/_base/jurisdiction_assets_base.py` (~250 LOC) — the canonical `JurisdictionAssetsBase` class (per cianfhoghlaim)
- **NEW file** `orchestration/defs/2_materials/_ga/ga_politician_pipeline_assets.py` (~100 LOC) — the canonical Garda politician-pipeline assets subclass
- **NEW spec delta** `openspec/changes/cianchosaint-dagster-orchestration-v1/specs/cianchosaint-dagster-orchestration/spec.md`

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-dagster-orchestration`)
- Affected code/config: 3 NEW files
- Estimated LOC: ~400 LOC added

## Out of scope (follow-up changes)

- Converting the remaining 9 jurisdictions (england, ireland, scotland, wales, ni, scot_wales_ni, crown_dependencies, isle_of_man, jersey, guernsey) — separate per-jurisdiction changes
- The Dagster sensor for licence enforcement (separate change)

## Dependencies

`Blocked by: cianchosaint-cocoindex-shared-lifespan-v1` (the lifespan is required by the assets)
`Affected repos: cianchosaint only.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `orchestration/defs/2_materials/_base/jurisdiction_assets_base.py` remains the upstream reference.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-dagster-orchestration-v1 --strict

# 2. regression: existing tests still pass
PYTHONPATH=. python3 tests/agents/cianchosaint/test_agent_factory.py
PYTHONPATH=. python3 tests/agents/integrations/test_agent_registry_runtime.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_long_running_tools.py
PYTHONPATH=. python3 tests/cocoindex_flows/test_shared_lifespan.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_workflow_graphs.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_memory_bank.py
PYTHONPATH=. python3 tests/evals/politician/walk.py

# 3. lint_license
mise run lint:license
```
