# Change: cianchosaint-collaboration-workspace-v1

## Why

Two problems converged on 2026-08-24:

1. **The user explicitly requested multi-tenant collaboration**: *"collaborate share resources using our data engineering and agentic and web stack for such"*. This requires a multi-tenant collaboration workspace where multiple British-Isles public-sector bodies (An Garda Síochána + PSNI + UK Home Office + NCA + etc.) can share dossiers.

2. **The 8 per-persona web apps** (`ciafagent-ga-public` + `ciafagent-ga-internal` + `ciafagent-met-public` + `ciafagent-met-internal` + `ciafagent-psni-public` + `ciafagent-psni-internal` + `ciafagent-self-host` + `ciafagent-api`) are single-tenant. There's no shared workspace where multiple agencies can collaborate.

## What changes

- **NEW module** at `agents/cianchosaint/tools/collaboration_workspace.py` (~280 LOC) — the `CollaborationWorkspaceManager` class
  - `create_workspace(workspace_id, name, created_by)` — creates a workspace
  - `add_member(workspace_id, email, role, organisation, added_by)` — adds a member
  - `add_dossier(workspace_id, dossier_id, cohort, source, added_by)` — shares a dossier
  - `list_dossiers(workspace_id, actor_email)` — lists the dossiers (gated by membership)
  - `get_workspace(workspace_id)` — gets the workspace record
  - `list_workspaces()` — lists all workspaces
  - The `WorkspaceAuditEntry` log (every action is logged per the warrant-to-enforce)

## Impact

- Affected specs: **1 NEW spec** (`cianchosaint-collaboration-workspace`)
- Affected code/config: 1 NEW file (`agents/cianchosaint/tools/collaboration_workspace.py`)

## Out of scope (follow-up changes)

- The full Convex schema for the workspaces — follow-up `cianchosaint-convex-collaboration-v1`
- The web UI for the workspaces — follow-up `ciafagent-collaboration-web-v1`

## Dependencies

`Blocked by: cianchosaint-cognee-graphiti-political-v1` (the graph data is shared via the collaboration workspace).
`Blocked by: cianchosaint-bipp-v2-baml-v1` (the shared dossiers are the BIPP v2 composite dossiers).
`Affected repos: cianchosaint.`

## Cross-repo sync

This change touches ONLY the `cianchosaint` repo.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec validate cianchosaint-collaboration-workspace-v1 --strict
# Expected: pass

python3 -c "
import sys
sys.path.insert(0, 'agents/cianchosaint/tools')
import collaboration_workspace as cw

mgr = cw.CollaborationWorkspaceManager()
ws = mgr.create_workspace(workspace_id='ws-ga-psni-001', name='GA + PSNI', created_by='analyst.a@garda.ie')
mgr.add_member(ws.workspace_id, 'analyst.b@psni.police.uk', role='analyst', organisation='PSNI', added_by='analyst.a@garda.ie')
mgr.add_dossier(ws.workspace_id, 'pilot-qub-rvh', cohort='bipp_v2_reform_uk_accountability', source='https://www.psni.police.uk/', added_by='analyst.a@garda.ie')
dossiers = mgr.list_dossiers(ws.workspace_id, 'analyst.b@psni.police.uk')
print(f'Dossiers: {len(dossiers)}')
print(f'Audit log: {len(ws.audit_log)}')
"
# Expected: Dossiers: 1, Audit log: 3
```