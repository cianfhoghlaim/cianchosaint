# CIANCHOSAINT — canonical BAMLFunctionTool wrapper.
#
# Wholesale-adapted from cianfhoghlaim's
# `agents/integrations/baml_function_tool.py`.
#
# Per `openspec/changes/cianchosaint-agent-registry-runtime-v1/specs/cianchosaint-agent-registry-runtime/spec.md`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.integrations.baml_function_tool — BAML → ADK FunctionTool.

Wraps any `async def` BAML function as a Google ADK `FunctionTool`. The
helper auto-detects the BAML function from `baml_client.async_client.b`
and exposes it as a tool with the right schema (parameter names, types,
descriptions).

Mirrors cianfhoghlaim's `agents/integrations/baml_function_tool.py`:
- `BAMLFunctionTool(baml_function_name)` looks up the function by name
  in the canonical `baml_client.async_client.b`
- Returns a Google ADK `FunctionTool` with the right schema

Usage::

    from agents.integrations.baml_function_tool import BAMLFunctionTool

    tool = BAMLFunctionTool("ExtractPoliticianFromWebPage")
    agent = LlmAgent(
        name="politician_resolver",
        model="minimax-m3",
        tools=[tool],
    )
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


# Lazy imports — baml-py is an optional dep at type-check time
try:
    from baml_client.baml_client import b  # type: ignore

    _HAS_BAML = True
except ImportError:  # pragma: no cover
    _HAS_BAML = False
    b = None  # type: ignore

try:
    from google.adk.tools import FunctionTool

    _HAS_ADK_TOOLS = True
except ImportError:  # pragma: no cover
    _HAS_ADK_TOOLS = False
    FunctionTool = None  # type: ignore


class BAMLFunctionTool:
    """The canonical wrapper that turns a BAML function into an ADK FunctionTool.

    Looks up the function by name in `baml_client.async_client.b` (the canonical
    BAML client). Returns a `google.adk.tools.FunctionTool` instance with the
    function name, docstring, and parameter schema auto-detected.
    """

    def __init__(self, function_name: str, **kwargs: Any) -> Any:
        self.function_name = function_name
        self._fn = None
        self._tool = None
        if _HAS_BAML:
            self._fn = getattr(b, function_name, None)
            if self._fn is None:
                logger.warning(
                    "BAMLFunctionTool(%s): function not found in baml_client.b",
                    function_name,
                )
            elif _HAS_ADK_TOOLS:
                try:
                    self._tool = FunctionTool(func=self._fn)
                except Exception as exc:  # noqa: BLE001
                    logger.warning(
                        "BAMLFunctionTool(%s): FunctionTool construction failed: %s",
                        function_name,
                        exc,
                    )
        else:
            logger.debug(
                "BAMLFunctionTool(%s): baml_client not available; "
                "tool is a stub",
                function_name,
            )

    @property
    def name(self) -> str:
        if self._tool is not None and hasattr(self._tool, "name"):
            return self._tool.name
        return self.function_name

    @property
    def description(self) -> str:
        if self._fn is not None and getattr(self._fn, "__doc__", None):
            return self._fn.__doc__
        if self._tool is not None and hasattr(self._tool, "description"):
            return self._tool.description
        return ""

    def __getattr__(self, name: str) -> Any:
        # Proxy to the wrapped FunctionTool so callers can use the wrapper
        # interchangeably with the ADK tool (e.g. `tool.run_async(...)`)
        return getattr(self._tool, name)

    def __repr__(self) -> str:
        status = "wrapped" if self._tool is not None else "stub"
        return f"<BAMLFunctionTool {self.function_name!r} ({status})>"


__all__ = ["BAMLFunctionTool"]
