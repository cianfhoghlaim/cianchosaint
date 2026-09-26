# CIANCHOSAINT — plugins.panel_plugin (canonical PanelPlugin).
#
# Per `openspec/changes/cianchosaint-plugin-v1/specs/cianchosaint-plugin/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's `monstertix/agent/concert/panel.py::PanelPlugin`.
#
# Mirrors the canonical panel narration:
# - `before_tool_callback` → POSTs an `agent` event to the venue control panel
# - `after_tool_callback` → POSTs a `returned` event (or `error` event)
# - Both fire-and-forget (the narrator NEVER blocks the tool call)
#
# Per the cianfhoghlaim pattern:
# "The PanelPlugin narrates tool calls to the venue control panel. A blank
# projector loses the room."
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.plugins.panel_plugin — canonical PanelPlugin.

Mirrors `monstertix/agent/concert/panel.py::PanelPlugin` exactly:
- Posts every agent tool call to the venue control panel
- Uses httpx fire-and-forget (the narrator NEVER blocks the tool call)
- Tags the panel endpoint from the `CIANCHOSAINT_PANEL_URL` env var
"""

from __future__ import annotations

import logging
import os
from typing import Any

from .base_plugin import BasePlugin

logger = logging.getLogger(__name__)


# Lazy imports — httpx is optional at type-check time
try:
    import httpx

    _HAS_HTTPX = True
except ImportError:  # pragma: no cover
    _HAS_HTTPX = False
    httpx = None  # type: ignore


#: The canonical panel endpoint (per cianfhoghlaim's monstertix pattern)
DEFAULT_PANEL_URL: str = os.environ.get(
    "CIANCHOSAINT_PANEL_URL",
    "http://localhost:8080/admin/agent-event",
)


def _short_args(args: dict[str, Any]) -> dict[str, Any]:
    """Return a shortened args dict for the panel (per cianfhoghlaim's `_short`)."""
    return {k: (str(v)[:60]) for k, v in list(args.items())[:4]}


def _emit(endpoint: str, kind: str, message: str, detail: dict[str, Any] | None = None) -> None:
    """Fire-and-forget POST to the panel endpoint."""
    if not _HAS_HTTPX:
        logger.debug("httpx unavailable; PanelPlugin cannot emit")
        return
    try:
        httpx.post(
            endpoint,
            json={"kind": kind, "message": message, "detail": detail or {}},
            timeout=2,
        )
    except httpx.HTTPError as exc:
        logger.debug("PanelPlugin emit failed: %s", exc)


class PanelPlugin(BasePlugin):
    """The canonical cianchosaint PanelPlugin.

    Mirrors `monstertix/agent/concert/panel.py::PanelPlugin` exactly:
- Narrates every tool call to the venue control panel
- Fire-and-forget (the narrator NEVER blocks the tool call)
- Tags the endpoint from `CIANCHOSAINT_PANEL_URL` env var
"""

    name: str = "cianchosaint_panel_plugin"

    def __init__(self, endpoint: str | None = None) -> None:
        self.endpoint = endpoint or DEFAULT_PANEL_URL

    async def before_tool_callback(
        self,
        tool: Any,
        args: dict[str, Any],
        tool_context: Any,
    ) -> dict[str, Any] | None:
        """Narrate the tool call to the panel."""
        tool_name = getattr(tool, "name", type(tool).__name__)
        _emit(
            self.endpoint,
            "agent",
            f"calling {tool_name}",
            {"args": _short_args(args)},
        )
        return None

    async def after_tool_callback(
        self,
        tool: Any,
        args: dict[str, Any],
        tool_context: Any,
        result: Any,
    ) -> None:
        """Narrate the tool result to the panel."""
        tool_name = getattr(tool, "name", type(tool).__name__)
        if isinstance(result, dict) and result.get("error"):
            _emit(
                self.endpoint,
                "error",
                f"{tool_name} failed: {result.get('message', '')[:80]}",
            )
        else:
            _emit(
                self.endpoint,
                "agent",
                f"{tool_name} returned",
            )
        return None


__all__ = ["PanelPlugin"]
