# cianchosaint-collaboration-workspace — Agent Routing

| Spec | Path |
|:--|:--|
| spec.md | [./spec.md](./spec.md) |

## Quick orientation

`cianchosaint-collaboration-workspace` is the canonical multi-tenant collaboration workspace. Enables An Garda Síochána + PSNI + UK Home Office + NCA + etc. to share dossiers.

## Routing table

| I want to... | Look at... |
|:--|:--|
| Create a workspace | `agents/cianchosaint/tools/collaboration_workspace.py:CollaborationWorkspaceManager.create_workspace()` |
| Add a member | `add_member()` |
| Share a dossier | `add_dossier()` |
| List shared dossiers | `list_dossiers()` (gated by membership) |