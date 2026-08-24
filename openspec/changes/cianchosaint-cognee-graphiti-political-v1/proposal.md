# Change: cianchosaint-cognee-graphiti-political-v1

## Why

Two problems converged on 2026-08-24:

1. **The cianchosaint platform has Cognee + Graphiti graph stores** (per `agents/meaisinfhoghlaim/firecrawl_mcp/memory/{cognee_store,graphiti_store}.py`) but no political-accountability-specific graph extensions. The 7 BIPP v2 BAML extraction schemas (per `cianchosaint-bipp-v2-baml-v1`) extract entities + relationships that need a canonical graph store.

2. **The user explicitly requested the cross-source dossier composition**: *"improve the agentic pipelines and generative ui and copilotkit features to further enable them intelligence agencies and other possible users of the cianchosaint repo to inform themselves of the topic and do deeper research and populate our lakehouse and collaborate share resources using our data engineering and agentic and web stack for such"*.

## What changes

- **NEW module** at `agents/cianchosaint/tools/political_graph_store.py` (~200 LOC) — the `PoliticalGraphStore` class
  - 13 entity types (politician, donor, company, agency, court, event, media_outlet, trade_union, think_tank, lobbyist, regulator, publication, source_pdf)
  - 13 relationship types (donates_to, employed_by, owns, regulates, sued_by, sues, investigates, investigated_by, reports_on, member_of, sp_legates_to, employs, linked_to)
  - `add_entity()` + `add_relationship()` methods
  - `query_dossier(target_entity, cohort, depth)` method — the cross-source BFS query that composes the dossier

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-political-graph`)
- Affected code/config: 1 NEW file (`agents/cianchosaint/tools/political_graph_store.py`)

## Out of scope (follow-up changes)

- The full Cognee cognify flow over the 87 leabharlann politics PDFs — follow-up `cianchosaint-cognee-flow-political-v1`
- The Graphiti bi-temporal knowledge graph over the per-cohort BAML extraction outputs — follow-up `cianchosaint-graphiti-flow-political-v1`
- The cross-source dossier composition web surface (the `ciafagent-bipp-v2` web app) — follow-up `ciafagent-bipp-v2-web-v1`

## Dependencies

`Blocked by: cianchosaint-bipp-v2-baml-v1` (the 7 BAML extraction schemas are the source of the graph data).
`Blocked by: cianchosaint-generative-ui-kit-v1` (the `TopicGraph` component consumes the graph data).
`Affected repos: cianchosaint.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec validate cianchosaint-cognee-graphiti-political-v1 --strict
# Expected: pass

python3 -c "
import sys, asyncio
sys.path.insert(0, 'agents/cianchosaint/tools')
import political_graph_store as pgs

async def test():
    store = pgs.PoliticalGraphStore()
    await store.add_entity(pgs.PoliticalGraphEntity(
        entity_id='richard_tice', name='Richard Tice', type='politician',
        cohort='bipp_v2_reform_uk_accountability', jurisdiction='uk',
    ))
    result = await store.query_dossier('richard_tice', 'bipp_v2_reform_uk_accountability')
    print(f'Entities: {len(result.entities)}')
asyncio.run(test())
"
# Expected: Entities: 1
```