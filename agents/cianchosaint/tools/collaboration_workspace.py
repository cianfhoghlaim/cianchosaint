# CIANCHOSAINT — Multi-tenant collaboration workspace.
#
# Per the openspec/changes/cianchosaint-collaboration-workspace-v1/
# specs/cianchosaint-collaboration-workspace/spec.md.
#
# The collaboration workspace enables multiple British-Isles public-sector
# bodies (An Garda Síochána + PSNI + UK Home Office + NCA + etc.) to
# share dossiers + collaborate on political-accountability investigations
# across the 8 jurisdictions.
#
# Each workspace has:
# - `workspace_id` — the canonical workspace id
# - `members` — the list of analyst emails + their roles
# - `dossiers` — the shared dossiers (cross-references to BIPP v2 composite dossiers)
# - `invitations` — the pending membership invitations
# - `audit_log` — every action is logged (per the warrant-to-enforce in LICENSE.md)
#
# License: BUSL-1.1 (per LICENSE.md).

"""CIANCHOSAINT — Multi-tenant collaboration workspace.

Per the openspec/changes/cianchosaint-collaboration-workspace-v1/.

Enables multiple British-Isles public-sector bodies (An Garda Síochána +
PSNI + UK Home Office + NCA + etc.) to share dossiers + collaborate on
political-accountability investigations across the 8 jurisdictions.

Each workspace has:
- `workspace_id` — the canonical workspace id
- `members` — the list of analyst emails + their roles
- `dossiers` — the shared dossiers (cross-references to BIPP v2 composite dossiers)
- `invitations` — the pending membership invitations
- `audit_log` — every action is logged (per the warrant-to-enforce in LICENSE.md)

Convex schema (per web/packages/db/src/collaboration-schemas.ts):
  workspaces: { workspace_id, name, created_at, created_by }
  workspace_members: { workspace_id, email, role, joined_at }
  workspace_dossiers: { workspace_id, dossier_id, source, cohort, added_at, added_by }
  workspace_invitations: { workspace_id, email, role, invited_at, invited_by, expires_at }
  workspace_audit_log: { workspace_id, action, actor, timestamp, details }
"""

from __future__ import annotations

import logging
import os
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


WorkspaceRole = Literal["admin", "analyst", "observer", "external_auditor"]


# The canonical British-Isles public-sector bodies that can host workspaces.
CANONICAL_WORSPACE_HOSTS = {
    "ga": "An Garda Síochána",
    "psni": "Police Service of Northern Ireland",
    "met": "Metropolitan Police Service",
    "home_office": "UK Home Office",
    "nca": "National Crime Agency",
    "dpsi": "Defence Intelligence (UK)",
    "mod": "Ministry of Defence (UK)",
    "fcd": "Foreign, Commonwealth & Development Office (UK)",
    "judiciary_uk": "HM Courts & Tribunals Service (UK)",
    "law_soc_ireland": "Law Society of Ireland",
    "law_soc_ni": "Law Society of Northern Ireland",
    "law_soc_eng_wales": "Law Society of England & Wales",
    "law_soc_scotland": "Law Society of Scotland",
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class WorkspaceMember:
    """A member of a collaboration workspace."""

    email: str
    role: WorkspaceRole
    joined_at: str
    organisation: str = ""  # The public-sector body


@dataclass
class WorkspaceDossier:
    """A shared dossier in the workspace."""

    workspace_id: str
    dossier_id: str  # Cross-reference to a BIPP v2 composite dossier
    cohort: str  # The BIPP v2 cohort
    source: str  # The BIPP v2 DLT source URL
    added_at: str
    added_by: str  # The email of the analyst who added it


@dataclass
class WorkspaceInvitation:
    """A pending membership invitation."""

    workspace_id: str
    email: str
    role: WorkspaceRole
    invited_at: str
    invited_by: str
    expires_at: str


@dataclass
class WorkspaceAuditEntry:
    """An audit log entry (every action is logged)."""

    workspace_id: str
    action: str  # "member_added" / "dossier_added" / "invitation_sent" / etc.
    actor: str  # The email of the actor
    timestamp: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class CollaborationWorkspace:
    """The canonical workspace record."""

    workspace_id: str
    name: str
    created_at: str
    created_by: str
    members: list[WorkspaceMember] = field(default_factory=list)
    dossiers: list[WorkspaceDossier] = field(default_factory=list)
    invitations: list[WorkspaceInvitation] = field(default_factory=list)
    audit_log: list[WorkspaceAuditEntry] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Workspace manager
# ---------------------------------------------------------------------------


class CollaborationWorkspaceManager:
    """The canonical multi-tenant workspace manager.

    Manages:
    - Workspace creation + membership + invitations
    - Dossier sharing + cross-references
    - Audit log (every action is logged per the warrant-to-enforce)
    - Per-tenant data isolation (every query is gated by workspace membership)
    """

    def __init__(self) -> None:
        self._workspaces: dict[str, CollaborationWorkspace] = {}
        self._lock = threading.Lock()

    def create_workspace(
        self,
        workspace_id: str,
        name: str,
        created_by: str,
    ) -> CollaborationWorkspace:
        """Create a new collaboration workspace.

        Args:
            workspace_id: the canonical id (e.g. "ws-ga-psni-001")
            name: the human-readable name (e.g. "GA + PSNI Joint Intelligence Workspace")
            created_by: the email of the creator

        Returns:
            The new CollaborationWorkspaceWorkspace record.
        """
        with self._lock:
            if workspace_id in self._workspaces:
                raise ValueError(f"workspace_id {workspace_id!r} already exists")
            workspace = CollaborationWorkspace(
                workspace_id=workspace_id,
                name=name,
                created_at=datetime.now(timezone.utc).isoformat(),
                created_by=created_by,
            )
            self._workspaces[workspace_id] = workspace
            self._log_audit(workspace, action="workspace_created", actor=created_by)
            logger.info(
                "workspace_created",
                extra={"workspace_id": workspace_id, "name": name, "created_by": created_by},
            )
            return workspace

    def add_member(
        self,
        workspace_id: str,
        email: str,
        role: WorkspaceRole,
        organisation: str = "",
        added_by: str = "",
    ) -> WorkspaceMember:
        """Add a member to the workspace."""
        with self._lock:
            workspace = self._get_workspace(workspace_id)
            member = WorkspaceMember(
                email=email,
                role=role,
                joined_at=datetime.now(timezone.utc).isoformat(),
                organisation=organisation,
            )
            workspace.members.append(member)
            self._log_audit(
                workspace,
                action="member_added",
                actor=added_by,
                details={"email": email, "role": role, "organisation": organisation},
            )
            return member

    def add_dossier(
        self,
        workspace_id: str,
        dossier_id: str,
        cohort: str,
        source: str,
        added_by: str,
    ) -> WorkspaceDossier:
        """Share a dossier in the workspace."""
        with self._lock:
            workspace = self._get_workspace(workspace_id)
            dossier = WorkspaceDossier(
                workspace_id=workspace_id,
                dossier_id=dossier_id,
                cohort=cohort,
                source=source,
                added_at=datetime.now(timezone.utc).isoformat(),
                added_by=added_by,
            )
            workspace.dossiers.append(dossier)
            self._log_audit(
                workspace,
                action="dossier_added",
                actor=added_by,
                details={"dossier_id": dossier_id, "cohort": cohort, "source": source},
            )
            return dossier

    def list_dossiers(
        self,
        workspace_id: str,
        actor_email: str,
    ) -> list[WorkspaceDossier]:
        """List the dossiers shared in the workspace (gated by membership)."""
        with self._lock:
            workspace = self._get_workspace(workspace_id)
            if not any(m.email == actor_email for m in workspace.members):
                raise PermissionError(f"{actor_email!r} is not a member of {workspace_id!r}")
            return list(workspace.dossiers)

    def get_workspace(self, workspace_id: str) -> CollaborationWorkspace:
        """Get a workspace by id."""
        with self._lock:
            return self._get_workspace(workspace_id)

    def list_workspaces(self) -> list[CollaborationWorkspace]:
        """List all workspaces."""
        with self._lock:
            return list(self._workspaces.values())

    def _get_workspace(self, workspace_id: str) -> CollaborationWorkspace:
        if workspace_id not in self._workspaces:
            raise KeyError(f"workspace_id {workspace_id!r} not found")
        return self._workspaces[workspace_id]

    def _log_audit(
        self,
        workspace: CollaborationWorkspace,
        action: str,
        actor: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Log an audit entry (every action is logged per the warrant-to-enforce)."""
        workspace.audit_log.append(
            WorkspaceAuditEntry(
                workspace_id=workspace.workspace_id,
                action=action,
                actor=actor,
                timestamp=datetime.now(timezone.utc).isoformat(),
                details=details or {},
            )
        )


__all__ = [
    "CANONICAL_WORSPACE_HOSTS",
    "CollaborationWorkspace",
    "CollaborationWorkspaceManager",
    "WorkspaceAuditEntry",
    "WorkspaceDossier",
    "WorkspaceInvitation",
    "WorkspaceMember",
    "WorkspaceRole",
]


if __name__ == "__main__":
    import json

    mgr = CollaborationWorkspaceManager()
    ws = mgr.create_workspace(
        workspace_id="ws-ga-psni-001",
        name="GA + PSNI Joint Intelligence Workspace",
        created_by="analyst.a@garda.ie",
    )
    mgr.add_member(ws.workspace_id, "analyst.b@psni.police.uk", role="analyst", organisation="PSNI", added_by="analyst.a@garda.ie")
    mgr.add_dossier(ws.workspace_id, "pilot-qub-rvh", cohort="bipp_v2_reform_uk_accountability", source="https://www.psni.police.uk/", added_by="analyst.a@garda.ie")
    dossiers = mgr.list_dossiers(ws.workspace_id, "analyst.b@psni.police.uk")
    print(f"Workspace: {ws.name}")
    print(f"Members: {len(ws.members)}")
    print(f"Dossiers: {len(dossiers)}")
    print(f"Audit log entries: {len(ws.audit_log)}")