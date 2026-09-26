# Tasks: cianchosaint-dagster-orchestration-v1

## 0. Pre-flight

- [x] Verify openspec CLI 1.11+ installed
- [x] Verify `orchestration/defs/2_materials/` exists (per cianfhoghlaim's 5-layer structure)

## 1. Author the canonical base class

- [x] Write `orchestration/defs/2_materials/_base/__init__.py` (~20 LOC) — the _base package marker
- [x] Write `orchestration/defs/2_materials/_base/jurisdiction_assets_base.py` (~250 LOC) with:
  - `JurisdictionAssetsBase` abstract class
  - `jurisdiction_name: ClassVar[str]` — required subclass attribute
  - `pipeline_factory: ClassVar[Callable]` — required subclass attribute
  - `asset_name: ClassVar[str]` — defaults to f"{jurisdiction_name}_documents_ingested"
  - `group_name: ClassVar[str]` — defaults to the jurisdiction name
  - `build_asset()` class method that returns the canonical Dagster `@asset`

## 2. Author the canonical Garda politician-pipeline assets

- [x] Write `orchestration/defs/2_materials/_ga/ga_politician_pipeline_assets.py` (~100 LOC) with:
  - `class GAPoliticianPipelineAssets(JurisdictionAssetsBase)`
  - `jurisdiction_name = "ireland"` (the Garda is the ROI jurisdiction)
  - `pipeline_factory = make_cianchosaint_politician_pipeline_factory` (per T2.2)
  - `asset_name = "ga_politician_pipeline_documents_ingested"`
  - `group_name = "ireland_politician_pipeline"`

## 3. Author the spec

- [x] Write `openspec/changes/cianchosaint-dagster-orchestration-v1/specs/cianchosaint-dagster-orchestration/spec.md` — the canonical spec (Requirement: JurisdictionAssetsBase contract; Scenario: every per-jurisdiction asset subclasses this + saves ~330 LOC per jurisdiction)
- [x] Write `openspec/changes/cianchosaint-dagster-orchestration-v1/cross-repo-sync.md` — sole repo cianchosaint
- [x] Write `openspec/changes/cianchosaint-dagster-orchestration-v1/tasks.md` — the task breakdown

## 4. CI gate

- [x] Run `openspec validate cianchosaint-dagster-orchestration-v1 --strict`
- [x] Run regression tests for T1.1 + T1.2 + T1.3 + T2.1 + T2.2 + T2.3 + T2.4 + T3.1 + T3.2
- [x] Run `mise run lint:license`

## 5. Commit + archive

- [x] `git add openspec/changes/cianchosaint-dagster-orchestration-v1/ orchestration/defs/2_materials/_base/ orchestration/defs/2_materials/_ga/`
- [x] `git commit -m "feat(cianchosaint): add Dagster JurisdictionAssetsBase + canonical Garda politician-pipeline assets"`
- [x] `openspec archive cianchosaint-dagster-orchestration-v1 --yes`

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
