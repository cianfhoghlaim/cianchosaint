# cianchosaint-political-graph — Agent Routing

| Spec | Path |
|:--|:--|
| spec.md | [./spec.md](./spec.md) |

## Quick orientation

`cianchosaint-political-graph` is the canonical political-accountability graph store. It extends the existing Cognee + Graphiti stores.

## Routing table

| I want to... | Look at... |
|:--|:--|
| Add a political-accountability entity | `agents/cianchosaint/tools/political_graph_store.py:PoliticalGraphStore.add_entity()` |
| Add a political-accountability relationship | `PoliticalGraphStore.add_relationship()` |
| Query the dossier | `PoliticalGraphStore.query_dossier()` |