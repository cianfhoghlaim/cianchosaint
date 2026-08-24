# cianchosaint-collaboration-workspace Capability

## Purpose

`cianchosaint-collaboration-workspace` is the canonical multi-tenant collaboration workspace for cianchosaint. It enables multiple British-Isles public-sector bodies (An Garda Síochána + PSNI + UK Home Office + NCA + etc.) to share dossiers + collaborate on political-accountability investigations.

## Background

Per the user's request: *"collaborate share resources using our data engineering and agentic and web stack for such"*.

## Requirements

### Requirement: The CollaborationWorkspaceManager class

The system SHALL provide a `CollaborationWorkspaceManager` class at `agents/cianchosaint/tools/collaboration_workspace.py`.

#### Scenario: Workspace creation + membership + dossier sharing

- **WHEN** the operator invokes `CollaborationWorkspaceManager().create_workspace(workspace_id, name, created_by)`
- **THEN** the workspace SHALL be created with an audit log entry

- **WHEN** the operator invokes `add_member(workspace_id, email, role, organisation, added_by)`
- **THEN** the member SHALL be added + an audit log entry SHALL be created

- **WHEN** the operator invokes `add_dossier(workspace_id, dossier_id, cohort, source, added_by)`
- **THEN** the dossier SHALL be shared + an audit log entry SHALL be created

#### Scenario: Per-tenant data isolation

- **WHEN** the operator invokes `list_dossiers(workspace_id, actor_email)`
- **AND** `actor_email` is NOT a member
- **THEN** the method SHALL raise `PermissionError`

## Cross-references

- [`../../agents/cianchosaint/tools/collaboration_workspace.py`](../../agents/cianchosaint/tools/collaboration_workspace.py) — the canonical manager
- [`../../openspec/specs/cianchosaint-bipp-v2/spec.md`](../../openspec/specs/cianchosaint-bipp-v2/spec.md) — the BIPP v2 vertical (the shared dossiers)
- [`../../openspec/specs/cianchosaint-political-graph/spec.md`](../../openspec/specs/cianchosaint-political-graph/spec.md) — the political graph
- [`../../LICENSE.md`](../../LICENSE.md) — the warrant-to-enforce clause