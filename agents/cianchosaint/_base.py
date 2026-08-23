# CIANCHOSAINT — per-constituency Google ADK agent fleet.
#
# This is NEW-BUILD code (not wholesale-copied). Authored per the
# `cianchosaint-per-constituency-agents-v1` change, drawing on the
# Cianfhoghlaim PATTERN files at `agents/adk/tuatha_root_agent.py`,
# `agents/adk/celtic_tutor_agent.py`, `agents/adk/curriculum_comparison_agent.py`,
# and `agents/adk/litellm_agent.py`.
#
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Part of the cianchosaint Google ADK agent framework. The
# `CianchosaintAgentBase` is the common base class for all 24
# cianchosaint agents — 3 root agents (GA / MET / PSNI) + 15
# specialists (5 per jurisdiction) + 7 tools (form fillers +
# cross-jurisdiction lookups).

"""
Common base class for all cianchosaint per-constituency agents.

Provides:
- `CianchosaintAgentBase` — the parent class that all GA / MET / PSNI
  agents inherit from. Holds the optional `provider_router` parameter
  and exposes `check_osint_source()` + `get_active_model()` helpers
  for the 4-tier ModelProviderRouter.
- `read_osint_allowlist()` — reads
  `dlt_sources/cianchosaint/common/osint_allowlist.yaml` (the canonical
  allowlist of OSINT domains the agents are permitted to consult).
- `DEFAULT_MODEL` — the canonical default model alias
  (`"minimax-m3"`).
- `OSINT_ALLOWLIST_PATH` — the on-disk path to the allowlist YAML.

The OSINT allowlist is the security boundary for the cianchosaint
platform — agents MUST consult `check_osint_source()` before reading
from any external URL, and MUST refuse to proceed if the source is
not on the allowlist.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

DEFAULT_MODEL = "minimax-m3"

OSINT_ALLOWLIST_PATH = Path(
    "dlt_sources/cianchosaint/common/osint_allowlist.yaml"
)


def read_osint_allowlist() -> dict[str, Any]:
    """Read the cianchosaint OSINT allowlist from disk.

    Returns:
        A dict with shape `{"domains": [...], "version": str,
        "last_updated": str}`. Returns an empty allowlist if the
        file is missing or malformed (fail-closed: agents will
        refuse to consult any external source).

    Reference:
        dlt_sources/cianchosaint/common/osint_allowlist.yaml
    """
    try:
        with OSINT_ALLOWLIST_PATH.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
            if not isinstance(data, dict):
                return {"domains": [], "version": "0.0.0"}
            data.setdefault("domains", [])
            return data
    except (FileNotFoundError, yaml.YAMLError):
        return {"domains": [], "version": "0.0.0"}


class CianchosaintAgentBase:
    """The common base class for all cianchosaint per-constituency agents.

    Subclasses (the 3 root agents + the 15 specialists) inherit from
    this class to gain:
    - The optional `provider_router` parameter (the 4-tier
      ModelProviderRouter; injected via the constructor).
    - The `check_osint_source()` helper (the security gate).
    - The `get_active_model()` helper (resolves the active model
      via the provider router or falls back to `DEFAULT_MODEL`).

    Args:
        provider_router: Optional 4-tier ModelProviderRouter instance.
            When `None`, the agent uses `DEFAULT_MODEL` directly. When
            provided, `get_active_model()` queries the router's
            `resolve()` method to pick the active model.

    Reference:
        openspec/changes/cianchosaint-per-constituency-agents-v1
    """

    def __init__(self, provider_router: Any | None = None) -> None:
        self.provider_router = provider_router
        self.osint_allowlist = read_osint_allowlist()

    def check_osint_source(self, url: str) -> bool:
        """Check whether `url` is on the OSINT allowlist.

        Args:
            url: The URL the agent wants to consult.

        Returns:
            True if the URL's domain is on the allowlist; False
            otherwise. Fail-closed: returns False if the allowlist
            cannot be read.

        Usage:
            >>> agent.check_osint_source("https://www.irishstatutebook.ie/eli/2024/act/1")
            True
            >>> agent.check_osint_source("https://example.com/secret")
            False
        """
        domains = self.osint_allowlist.get("domains", [])
        if not domains:
            return False
        for allowed in domains:
            if allowed in url:
                return True
        return False

    def get_active_model(self) -> str:
        """Return the active model for this agent.

        Resolves through the `provider_router` if one was injected
        at construction time. Falls back to `DEFAULT_MODEL` if no
        router is present or the router raises.

        Returns:
            The active model alias (e.g. `"minimax-m3"`).
        """
        if self.provider_router is None:
            return DEFAULT_MODEL
        try:
            return self.provider_router.resolve()
        except Exception:
            return DEFAULT_MODEL


__all__ = [
    "CianchosaintAgentBase",
    "DEFAULT_MODEL",
    "OSINT_ALLOWLIST_PATH",
    "read_osint_allowlist",
]
