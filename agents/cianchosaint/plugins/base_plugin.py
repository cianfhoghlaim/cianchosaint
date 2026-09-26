# CIANCHOSAINT — plugins.base_plugin (canonical BasePlugin).
#
# Per `openspec/changes/cianchosaint-plugin-v1/specs/cianchosaint-plugin/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's `monstertix/agent/concert/panel.py::PanelPlugin`
# base behaviour + `docs/google_examples/adk-examples/support-memory-lab/_shared/iris_tools.py::refresh_before_purchase`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.plugins.base_plugin — canonical BasePlugin.

Mirrors cianfhoghlaim's `monstertix/agent/concert/panel.py::PanelPlugin` base behaviour:
- `before_tool_callback` + `after_tool_callback` hooks (no-ops by default)
- Preserves the existing `refresh_before_purchase` signature compatibility (per T1.3)
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


# Lazy imports — the ADK plugin surface is optional at type-check time
try:
    from google.adk.plugins.base_plugin import BasePlugin as _ADKBasePlugin  # type: ignore
    from google.adk.tools import BaseTool, ToolContext  # type: ignore

    _HAS_ADK_PLUGINS = True
except ImportError:  # pragma: no cover
    _HAS_ADK_PLUGINS = False
    _ADKBasePlugin = object  # type: ignore
    BaseTool = None  # type: ignore
    ToolContext = None  # type: ignore


class BasePlugin(_ADKBasePlugin if _HAS_ADK_PLUGINS else object):
    """The canonical BasePlugin for cianchosaint.

    Mirrors cianfhoghlaim's `monstertix/agent/concert/panel.py::PanelPlugin` base behaviour:
    - `before_tool_callback(tool, args, tool_context)` — no-op by default
    - `after_tool_callback(tool, args, tool_context, result)` — no-op by default

    Subclasses override these hooks to add behavior (e.g., the PanelPlugin
    narrates tool calls to the control panel).
    """

    name: str = "cianchosaint_base_plugin"

    async def before_tool_callback(
        self,
        tool: Any,
        args: dict[str, Any],
        tool_context: Any,
    ) -> dict[str, Any] | None:
        """No-op hook (override in subclasses)."""
        return None

    async def after_tool_callback(
        self,
        tool: Any,
        args: dict[str, Any],
        tool_context: Any,
        result: Any,
    ) -> None:
        """No-op hook (override in subclasses)."""
        return None


__all__ = ["BasePlugin"]
