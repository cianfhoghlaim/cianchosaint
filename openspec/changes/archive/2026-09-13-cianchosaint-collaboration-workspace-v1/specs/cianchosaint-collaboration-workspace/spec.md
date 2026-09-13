## ADDED Requirements

### Requirement: The CollaborationWorkspaceManager class

The system SHALL provide a `CollaborationWorkspaceManager` class at `agents/cianchosaint/tools/collaboration_workspace.py`.

#### Scenario: Workspace creation + membership + dossier sharing

- **WHEN** the operator invokes `create_workspace(workspace_id, name, created_by)`
- **THEN** the workspace SHALL be created

- **WHEN** the operator invokes `add_member(...)`
- **THEN** the member SHALL be added

- **WHEN** the operator invokes `add_dossier(...)`
- **THEN** the dossier SHALL be shared

#### Scenario: Per-tenant data isolation

- **WHEN** `actor_email` is NOT a member
- **THEN** `list_dossiers()` SHALL raise `PermissionError`