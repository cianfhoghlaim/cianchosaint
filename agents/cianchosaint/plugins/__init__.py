# CIANCHOSAINT — plugins package (canonical BasePlugin + PanelPlugin).
#
# Per `openspec/changes/cianchosaint-plugin-v1/specs/cianchosaint-plugin/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's `monstertix/agent/concert/panel.py`:
# - `BasePlugin` (canonical subclass with before/after_tool_callback hooks)
# - `PanelPlugin` (canonical narrator that POSTs to the control panel)
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.plugins — canonical BasePlugin + PanelPlugin.

Re-exports:
- `BasePlugin` — canonical subclass with before/after_tool_callback hooks
- `PanelPlugin` — canonical narrator that POSTs to the control panel
"""

from __future__ import annotations

from .base_plugin import BasePlugin
from .panel_plugin import PanelPlugin

__all__ = ["BasePlugin", "PanelPlugin"]
