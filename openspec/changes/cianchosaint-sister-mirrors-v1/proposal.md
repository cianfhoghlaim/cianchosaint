# Change: cianchosaint-sister-mirrors-v1

## Why

Cianfhoghlaim's `bonneagar-mirror` (the sister-side mirror) wholesale-copies specific assets between sister repos (`bonneagar/` files, sibling repos' manifests). Per cianfhoghlaim's `openspec/changes/2026-09-01-bonneagar-sister-umbrella-mirror-v1/`, the canonical pattern is:

- Create a `mirror_destination/` directory in the receiving repo
- Bulk-copy from the source repo's `openspec/changes/<name>/` to the receiving repo
- Update the receiving repo's manifests (sub_app_manifest.yaml) to register the new flows
- Run the canonical `pc_consolidation` / `pc_web_consolidation` mise tasks

Cianchosaint has 8 web apps (`ciafagent-{api,cyberchef,ga-internal,ga-public,met-internal,met-public,psni-internal,psni-public,self-host}`) that are individually configured with their own manifests, route tables, and deployment pipelines. Consolidating them into a unified `ciafagent-nua` (per the cianfhoghlaim `web_consolidation` pattern) is a 2-week effort that depends on the 7-tier mise task stack.

This change lands the canonical "sister-mirror" mechanism for cianchosaint + provides the consolidation manifest as a starting point for the full T3.4 work.

## What changes

- **NEW file** `openspec/changes/cianchosaint-sister-mirrors-v1/manifest.yaml` (~100 lines) — the canonical consolidation manifest for the 8 web apps
- **NEW file** `openspec/changes/cianchosaint-sister-mirrors-v1/mirror.py` (~80 lines) — the canonical mirror script that bulk-copies assets
- **NEW file** `openspec/changes/cianchosaint-sister-mirrors-v1/specs/cianchosaint-sister-mirrors/spec.md`

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-sister-mirrors`)
- Affected code/config: 3 NEW files
- Estimated LOC: ~200 LOC added

## Out of scope (follow-up changes)

- The full web app consolidation (ciafagent-nua) — separate change
- The Hono / Convex backend consolidation — separate change
- The CopilotKit GenUI kit consolidation — separate change

## Dependencies

`Blocked by: cianchosaint-agent-factory-v1` (the agents are the canonical surface)
`Affected repos: cianchosaint only.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo. Cianfhoghlaim's `bonneagar-mirror` pattern remains the upstream reference.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# 1. openspec validation
openspec validate cianchosaint-sister-mirrors-v1 --strict

# 2. run the mirror script in dry-run mode
PYTHONPATH=. python3 openspec/changes/cianchosaint-sister-mirrors-v1/mirror.py --dry-run

# 3. regression: existing tests still pass
PYTHONPATH=. python3 tests/agents/cianchosaint/test_agent_factory.py
PYTHONPATH=. python3 tests/agents/integrations/test_agent_registry_runtime.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_long_running_tools.py
PYTHONPATH=. python3 tests/cocoindex_flows/test_shared_lifespan.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_workflow_graphs.py
PYTHONPATH=. python3 tests/agents/cianchosaint/test_memory_bank.py
PYTHONPATH=. python3 tests/evals/politician/walk.py
PYTHONPATH=. python3 tests/orchestration/test_dagster_orchestration.py

# 4. lint_license
mise run lint:license
```
