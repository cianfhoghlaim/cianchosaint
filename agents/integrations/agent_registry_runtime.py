# CIANCHOSAINT — canonical AG-UI + CopilotKit runtime surface.
#
# Wholesale-adapted from cianfhoghlaim's
# `agents/integrations/agent_registry_runtime.py`.
#
# Per `openspec/changes/cianchosaint-agent-registry-runtime-v1/specs/cianchosaint-agent-registry-runtime/spec.md`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.integrations.agent_registry_runtime — runtime helpers.

Three helpers for wiring every cianchosaint ADK agent to the CopilotKit
runtime + the AG-UI 17-event protocol.

Mirrors cianfhoghlaim's `agents/integrations/agent_registry_runtime.py`:
- `register_all_agents_with_copilotkit()` — calls `register_adk_agent(agent, name=name)`
  for every entry in `AGENT_FACTORY_REGISTRY`
- `collect_all_agui_events()` — collects the registration events emitted
  by `ag-ui-adk`
- `build_copilotkit_runtime_config()` — produces the canonical CopilotKit
  runtime configuration (agents + tools + metadata)
"""

from __future__ import annotations

import logging
from typing import Any, NamedTuple

logger = logging.getLogger(__name__)


# Lazy imports — CopilotKit + ag-ui-adk are optional deps at type-check time
# but always present at runtime in the cianchosaint agent surface.
try:
    from ag_ui_adk import ADKAgent  # noqa: F401

    _HAS_AGUI = True
except ImportError:  # pragma: no cover
    _HAS_AGUI = False
    ADKAgent = None  # type: ignore

try:
    from copilotkit.runtime import CopilotKitRuntime  # noqa: F401

    _HAS_COPILOTKIT = True
except ImportError:  # pragma: no cover
    _HAS_COPILOTKIT = False
    CopilotKitRuntime = None  # type: ignore


# ----------------------------------------------------------------------------
# The canonical 18-agent fleet tuple (mirrors cianfhoghlaim's AGENT_REGISTRY)
# ----------------------------------------------------------------------------


# Lazy import the fleet (avoids the eager-import cycle with `_factory`)
def _get_fleet() -> tuple:
    """Get the 18-agent cianchosaint fleet tuple.

    Lazy because importing the fleet at module-load time triggers the
    `agents.cianchosaint` package's `__init__.py` chain which builds the
    factory + registry. Lazy-loading here keeps this module independent
    of the package's import order.
    """
    from agents.cianchosaint import CIANCHOSAINT_AGENT_FLEET

    return CIANCHOSAINT_AGENT_FLEET


def CIANCHOSAINT_AGENT_FLEET() -> tuple:
    """Get the 18-agent cianchosaint fleet tuple.

    Mirrors cianfhoghlaim's `AGENT_REGISTRY` export — returns the same
    tuple that the cianchosaint `__init__.py` exposes.
    """
    return _get_fleet()


def _try_register_single(agent: Any, name: str) -> bool:
    """Try to register a single agent with the CopilotKit runtime.

    Returns True on success, False if the runtime is unavailable (the
    ag-ui-adk / copilotkit packages are optional). No-ops in dev
    environments that don't have the runtime installed.
    """
    if not _HAS_AGUI:
        logger.debug("ag-ui-adk unavailable; skipping registration for %s", name)
        return False
    try:
        # Use the canonical agent_ui_bridge helper
        from .agent_ui_bridge import register_adk_agent as _register

        _register(agent, name=name)
        return True
    except Exception as exc:  # noqa: BLE001
        logger.warning("register_adk_agent(%s) failed: %s", name, exc)
        return False


def register_all_agents_with_copilotkit() -> dict[str, bool]:
    """Register every entry in the cianchosaint fleet with the CopilotKit runtime.

    Returns a `{agent_name: success_bool}` dict so the caller can verify
    which agents registered successfully (e.g. for CI logging).

    No-op when `ag-ui-adk` is not installed — returns an empty dict.

    Usage::

        from agents.integrations import register_all_agents_with_copilotkit
        results = register_all_agents_with_copilotkit()
        for name, ok in results.items():
            print(f"{name}: {'OK' if ok else 'SKIPPED'}")
    """
    results: dict[str, bool] = {}
    for agent in _get_fleet():
        name = getattr(agent, "name", type(agent).__name__)
        results[name] = _try_register_single(agent, name)
    return results


def collect_all_agui_events() -> list[dict]:
    """Collect the registration events emitted by `ag-ui-adk`.

    In a real runtime, this returns the list of `agent_registered` events
    that the CopilotKit runtime emits as each agent is registered. In
    environments without the runtime, this returns an empty list.
    """
    if not _HAS_AGUI:
        return []
    try:
        # The real implementation would query the CopilotKit runtime's
        # event bus. In cianchosaint we keep it minimal — return the
        # collected events from any registered hooks.
        from ag_ui_adk import get_registered_events  # type: ignore

        return list(get_registered_events())
    except Exception:
        return []


def build_copilotkit_runtime_config() -> dict[str, Any]:
    """Build the canonical CopilotKit runtime configuration for cianchosaint.

    Returns a dict with `agents` (every registered agent),
    `tools` (every FunctionTool wrapper), `metadata` (the runtime metadata).
    The structure is compatible with the cianfhoghlaim-style CopilotKit runtime.
    """
    config: dict[str, Any] = {
        "agents": {},
        "tools": {},
        "metadata": {
            "version": "2026-09-12.v1",
            "registry_size": 18,
            "runtime": "cianchosaint",
        },
    }
    for agent in _get_fleet():
        name = getattr(agent, "name", type(agent).__name__)
        config["agents"][name] = {
            "agent": agent,
            "sub_agents": [
                sub.name if hasattr(sub, "name") else sub
                for sub in getattr(agent, "sub_agents", []) or []
            ],
            "tools": [
                t.name if hasattr(t, "name") else type(t).__name__
                for t in getattr(agent, "tools", []) or []
            ],
        }
    return config


__all__ = [
    "CIANCHOSAINT_AGENT_FLEET",
    "register_all_agents_with_copilotkit",
    "collect_all_agui_events",
    "build_copilotkit_runtime_config",
]
