# CIANCHOSAINT — integrations package (canonical AG-UI runtime + BAMLFunctionTool).
#
# Per `openspec/changes/cianchosaint-agent-registry-runtime-v1/specs/cianchosaint-agent-registry-runtime/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's `agents/integrations/` package:
# - agent_registry_runtime.py — 3-helper surface for wiring agents to the
#   CopilotKit runtime + the AG-UI 17-event protocol
# - agent_ui_bridge.py — the canonical `register_adk_agent()` helper that
#   uses `ag-ui-adk.ADKAgent` + `CopilotKitRuntime`
# - baml_function_tool.py — wraps any `async def` BAML function as a
#   Google ADK `FunctionTool`
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.integrations — the canonical runtime + tooling surface.

Re-exports the 3 helpers from cianchosaint's `agents.integrations` package:
- `register_all_agents_with_copilotkit()` — wires every `AGENT_FACTORY_REGISTRY`
  entry to the CopilotKit runtime
- `collect_all_agui_events()` — collects the registration events for the
  AG-UI 17-event protocol
- `build_copilotkit_runtime_config()` — produces the canonical runtime config
- `BAMLFunctionTool` — wraps any BAML function as an ADK `FunctionTool`
"""

from __future__ import annotations

from .agent_registry_runtime import (
    CIANCHOSAINT_AGENT_FLEET,
    register_all_agents_with_copilotkit,
    collect_all_agui_events,
    build_copilotkit_runtime_config,
)
from .agent_ui_bridge import register_adk_agent, make_planner_agent
from .baml_function_tool import BAMLFunctionTool

__all__ = [
    "CIANCHOSAINT_AGENT_FLEET",
    "register_all_agents_with_copilotkit",
    "collect_all_agui_events",
    "build_copilotkit_runtime_config",
    "register_adk_agent",
    "make_planner_agent",
    "BAMLFunctionTool",
]
