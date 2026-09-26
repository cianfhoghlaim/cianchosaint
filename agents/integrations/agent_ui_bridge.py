# CIANCHOSAINT — canonical ADK ↔ CopilotKit bridge.
#
# Wholesale-adapted from cianfhoghlaim's
# `agents/integrations/agent_ui_bridge.py`.
#
# Per `openspec/changes/cianchosaint-agent-registry-runtime-v1/specs/cianchosaint-agent-registry-runtime/spec.md`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.integrations.agent_ui_bridge — ADK ↔ CopilotKit bridge.

The canonical `register_adk_agent(agent, name=name)` helper that wraps an
`LlmAgent` as an `ag-ui-adk.ADKAgent` and registers it with the CopilotKit
runtime. Mirrors cianfhoghlaim's `agents/integrations/agent_ui_bridge.py`.

Usage::

    from agents.integrations.agent_ui_bridge import register_adk_agent

    for name, wiring in AGENT_FACTORY_REGISTRY.items():
        register_adk_agent(wiring, name=name)
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


# Lazy imports — ag-ui-adk is an optional dep at type-check time
try:
    from ag_ui_adk import ADKAgent

    _HAS_AGUI = True
except ImportError:  # pragma: no cover
    _HAS_AGUI = False
    ADKAgent = None  # type: ignore


def register_adk_agent(
    agent: Any,
    *,
    name: str,
    description: str | None = None,
) -> Any | None:
    """Wrap an LlmAgent (or AgentWiring) as an `ag-ui-adk.ADKAgent`.

    Returns the `ADKAgent` wrapper, or `None` if `ag-ui-adk` is not installed.

    Mirrors cianfhoghlaim's `agents/integrations/agent_ui_bridge.py`:
    - `description` overrides the agent's default description
    - The wrapper uses `agent_ui_adk.ADKAgent` which translates ADK
      streaming events into the AG-UI 17-event protocol

    Usage::

        from agents.cianchosaint._factory import AGENT_FACTORY_REGISTRY
        from agents.integrations.agent_ui_bridge import register_adk_agent

        for name, wiring in AGENT_FACTORY_REGISTRY.items():
            wrapper = register_adk_agent(
                wiring,
                name=name,
                description=f"Cianchosaint {name} via the agent factory.",
            )
    """
    if not _HAS_AGUI:
        logger.warning(
            "register_adk_agent(%s): ag-ui-adk not installed; returning None",
            name,
        )
        return None
    try:
        # The agent may be an LlmAgent instance OR an AgentWiring namedtuple;
        # ADKAgent expects an LlmAgent. Resolve from the wiring if needed.
        actual_agent = _resolve_agent(agent)
        wrapper = ADKAgent(
            agent=actual_agent,
            name=name,
            description=description or getattr(actual_agent, "description", ""),
        )
        return wrapper
    except Exception as exc:  # noqa: BLE001
        logger.warning("register_adk_agent(%s) failed: %s", name, exc)
        return None


def _resolve_agent(agent: Any) -> Any:
    """Resolve an agent to an LlmAgent instance.

    AgentWiring namedtuples are NOT LlmAgents — they're wiring metadata.
    The canonical cianchosaint factory exposes them as `AGENT_FACTORY_REGISTRY[name]`
    which is the wiring, NOT the agent. The runtime caller is expected
    to use the wiring's `factory_kwargs` to instantiate the agent via
    `make_cianchosaint_agent(**wiring.factory_kwargs)`.

    If `agent` already looks like an LlmAgent (has `name`, `sub_agents`, `tools`),
    return it as-is.
    """
    from google.adk.agents import LlmAgent

    if isinstance(agent, LlmAgent):
        return agent
    # Fall back: import the instance from the module that defined it
    try:
        name = getattr(agent, "name", None)
        if name:
            # Map `name` back to the module-level instance
            import importlib
            # Try the canonical mapping (specialists + root agents)
            module_map = {
                "ga_root_agent": "agents.cianchosaint.ga_root_agent",
                "met_root_agent": "agents.cianchosaint.met_root_agent",
                "psni_root_agent": "agents.cianchosaint.psni_root_agent",
                "ga_crime_statistics_agent": "agents.cianchosaint.ga_specialists.crime_statistics_agent",
                "ga_traffic_law_agent": "agents.cianchosaint.ga_specialists.traffic_law_agent",
                "ga_foia_requests_agent": "agents.cianchosaint.ga_specialists.foia_requests_agent",
                "irish_statute_book_agent": "agents.cianchosaint.ga_specialists.irish_statute_book_agent",
                "courts_ie_agent": "agents.cianchosaint.ga_specialists.courts_ie_agent",
                "met_crime_statistics_agent": "agents.cianchosaint.met_specialists.crime_statistics_agent",
                "met_stop_and_search_agent": "agents.cianchosaint.met_specialists.stop_and_search_agent",
                "met_press_releases_agent": "agents.cianchosaint.met_specialists.met_press_releases_agent",
                "met_public_contact_agent": "agents.cianchosaint.met_specialists.met_public_contact_agent",
                "met_crime_prevention_agent": "agents.cianchosaint.met_specialists.crime_prevention_agent",
                "psni_crime_statistics_agent": "agents.cianchosaint.psni_specialists.crime_statistics_agent",
                "psni_press_releases_agent": "agents.cianchosaint.psni_specialists.psni_press_releases_agent",
                "psni_public_contact_agent": "agents.cianchosaint.psni_specialists.psni_public_contact_agent",
                "ni_justice_agent": "agents.cianchosaint.psni_specialists.ni_justice_agent",
                "policing_board_agent": "agents.cianchosaint.psni_specialists.policing_board_agent",
            }
            mod_path = module_map.get(name)
            if mod_path:
                mod = importlib.import_module(mod_path)
                return getattr(mod, name, agent)
    except Exception as exc:  # noqa: BLE001
        logger.debug("_resolve_agent fallback failed: %s", exc)
    return agent


def make_planner_agent(
    name: str,
    description: str,
    *,
    model_alias: str = "minimax",
    temperature: float = 0.3,
    max_output_tokens: int = 8192,
    instruction: str = "",
    tools: list | None = None,
) -> Any:
    """Create a planner-enabled LlmAgent using the canonical BuiltInPlanner helper.

    Mirrors cianfhoghlaim's `make_planner_agent()` helper (per the ADK 2
    codelab's `docs/copilotkit/examples/adk-dashboard` pattern).
    """
    from agents.cianchosaint._factory import make_cianchosaint_agent

    return make_cianchosaint_agent(
        name=name,
        description=description,
        instruction=instruction or f"You are {name}.",
        tools=tools,
        model_alias=model_alias,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        enable_thinking=True,
    )


__all__ = [
    "register_adk_agent",
    "make_planner_agent",
]
