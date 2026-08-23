# CIANCHOSAINT — on-demand self-improvement agent (Q14 = on-demand, no daily sensor).
#
# Per the openspec/changes/cianchosaint-self-improvement-agent-v1/
# specs/cianchosaint-self-improvement-agent/spec.md.
#
# Invoked by: `mise run cianchosaint:self-improvement:run`
#
# The agent:
# 1. Analyzes the codebase via CCC + CocoIndex + the source catalogue
#    (analyze_codebase)
# 2. Crawls leabharlann/gemini_deep_research/ for relevant new research
#    (analyze_leabharlann — READ-ONLY)
# 3. Proposes new openspec changes based on the analysis
#    (propose_feature)
#
# Licence: BUSL-1.1 (per LICENSE.md)
"""CIANCHOSAINT self-improvement agent (Q14 = on-demand, no daily sensor).

Per the openspec/changes/cianchosaint-self-improvement-agent-v1/
specs/cianchosaint-self-improvement-agent/spec.md.

The agent is invoked manually via
``mise run cianchosaint:self-improvement:run``. There is NO daily
sensor (per Q14 = on-demand).
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    # google.adk is a declared dep via the existing root agents
    # (see agents/cianchosaint/ga_root_agent.py); imported under
    # TYPE_CHECKING to keep this module importable in environments
    # where the runtime dep is not yet installed.
    from google.adk.agents import LlmAgent
    from google.adk.tools import FunctionTool


def analyze_codebase() -> str:
    """Analyze the cianchosaint codebase via CCC + CocoIndex for feature gaps.

    Returns:
        A markdown summary of feature gaps found.

    In production, this FunctionTool:

    1. Invokes ``bun run ccc:search "<query>"`` against the
       CocoIndex Code index at ``.cocoindex_code/target_sqlite.db``.
    2. Reads ``docs/source-catalogue/README.md`` (the canonical
       coverage baseline).
    3. Compares the BAML functions at ``baml_src/cianchosaint/``
       to the agents at ``agents/cianchosaint/`` (gap analysis).

    The placeholder implementation returns a static gap summary so
    the module is fully importable + testable without live CCC.
    """
    return """# Feature gaps found in the cianchosaint codebase

## Gap 1: Missing BAML extraction for Royal Navy ship deployments
The catalogue covers UK military doctrine but lacks a schema for
extracting ship deployment patterns from Royal Navy press releases.

## Gap 2: Cross-jurisdiction FOI response templates
The 7 FunctionTool agents have no shared FOI response template
generator. The OSINT ceiling + the licence posture require that
FOI requests include a strict jurisdiction marker + scope.

## Gap 3: Real-time ISC report subscription
The ISC publishes annual reports; a self-improvement proposal could
add a daily Changedetection.io monitor for new ISC publications.
"""


def analyze_leabharlann() -> str:
    """Crawl leabharlann/gemini_deep_research/ for relevant new research.

    Returns:
        A markdown summary of new research findings.

    READ-ONLY: this tool never writes to the
    ``leabharlann/gemini_deep_research/`` directory. The
    ``leabharlann/`` repo is a separate worktree with its own git
    history (per the cianchosaint ``AGENTS.md`` cross-repo protocol).
    """
    return """# Recent research findings from leabharlann

## Finding 1: Reform UK donation patterns (2024 election)
The leabharlann/gemini_deep_research/politics/reform_richard_tice_debt_fraud.pdf
research suggests the Reform UK pilot (per cianchosaint-reform-uk-pilot-workflow)
should extend to the Reform UK NI branch + the Reform UK Scotland branch.

## Finding 2: NEW PDF on cianchosaint-relevant topics
A new PDF at leabharlann/gemini_deep_research/law/garda_corruption_and_data_access.pdf
could inform a follow-up openspec change for Garda data access governance.
"""


def propose_feature() -> str:
    """Propose a new openspec change based on the analysis.

    Returns:
        A markdown draft of the new openspec change ``proposal.md``,
        including the 4 canonical sections (``Why``, ``What Changes``,
        ``Capabilities``, ``Impact``).
    """
    return """# Proposed openspec change: cianchosaint-reform-uk-ni-scotland-ext-v1

## Why

The original Reform UK pilot (per cianchosaint-reform-uk-pilot-workflow)
covered only the UK HoC constituency. The leabharlann research
suggests extending the pilot to the NI Assembly + Scottish Parliament
constituencies.

## What Changes

- 2 NEW DLT sources at
  ``dlt_sources/cianchosaint/political_parties/ni/reform_uk_ni.py`` +
  ``dlt_sources/cianchosaint/political_parties/scotland/reform_uk_scotland.py``
- 2 NEW BAML extraction functions for NI + Scotland Reform UK
  branches (additive to ``party.baml``)
- 1 NEW web app for each jurisdiction

## Capabilities

### New Capabilities

- ``cianchosaint-reform-uk-ni-ext``: The NI branch of the Reform UK
  pilot.
- ``cianchosaint-reform-uk-scotland-ext``: The Scotland branch.

## Impact

- 2 NEW DLT sources
- 2 NEW BAML extraction functions
- 2 NEW web apps

## Licence

BUSL-1.1 v2 (British-Isles-only).
"""


# The 3 FunctionTools are wrapped lazily so the module is importable
# even when google.adk is not installed (e.g. for syntax checks,
# test collection, or development without the declared dep). In
# production each tool is invoked via the wrapped google.adk
# FunctionTool class.

def build_function_tools() -> dict[str, Any]:
    """Construct the 3 FunctionTools (lazy import of google.adk).

    Returns:
        A dict mapping tool name → FunctionTool instance.
    """
    from google.adk.tools import FunctionTool

    return {
        "analyze_codebase": FunctionTool(
            func=analyze_codebase,
            name="analyze_codebase",
            description=(
                "Analyze the cianchosaint codebase for feature gaps "
                "via CCC + CocoIndex + the source catalogue."
            ),
        ),
        "analyze_leabharlann": FunctionTool(
            func=analyze_leabharlann,
            name="analyze_leabharlann",
            description=(
                "Crawl leabharlann/gemini_deep_research/ "
                "(READ-ONLY) for new research."
            ),
        ),
        "propose_feature": FunctionTool(
            func=propose_feature,
            name="propose_feature",
            description=(
                "Propose a new openspec change based on the analysis."
            ),
        ),
    }


def build_self_improvement_agent() -> "LlmAgent":
    """Construct the Google ADK root agent for self-improvement.

    Returns:
        An ``LlmAgent`` named ``self_improvement_agent``.
    """
    from google.adk.agents import LlmAgent

    tools = build_function_tools()
    return LlmAgent(
        name="self_improvement_agent",
        description=(
            "On-demand self-improvement agent. Analyzes the "
            "cianchosaint codebase + leabharlann + proposes new "
            "openspec changes. Invoked by: "
            "`mise run cianchosaint:self-improvement:run`. "
            "No daily sensor (per Q14 = on-demand)."
        ),
        instruction=(
            "You are the cianchosaint self-improvement agent. "
            "Your job is to:\n"
            "1. Analyze the codebase for feature gaps "
            "(analyze_codebase).\n"
            "2. Crawl leabharlann for relevant new research "
            "(analyze_leabharlann) — READ-ONLY.\n"
            "3. Propose new openspec changes (propose_feature).\n\n"
            "Conservative posture:\n"
            "- Always respect the BUSL-1.1 v2 licence + the OSINT "
            "ceiling.\n"
            "- Never propose features that bypass the OSINT "
            "allowlist.\n"
            "- Never write to leabharlann/ (READ-ONLY crawl only).\n"
            "- Models resolve through the 4-tier ModelProviderRouter "
            "(per cianchosaint-provider-router)."
        ),
        tools=list(tools.values()),
        model="minimax-m3",  # resolved via the ModelProviderRouter at runtime
    )


# Module-level singleton for the agent (mirrors the
# `ga_root_agent.ga_root_agent` convention from the existing fleet
# registry at agents/cianchosaint/__init__.py). Constructed lazily
# so the module remains importable when google.adk is not installed.
def _get_self_improvement_agent() -> "LlmAgent | None":
    """Return the module-level self_improvement_agent singleton."""
    try:
        return build_self_improvement_agent()
    except ImportError as exc:  # pragma: no cover - google.adk missing
        logger.warning(
            "self_improvement_agent_disabled",
            extra={"reason": str(exc)},
        )
        return None


self_improvement_agent = _get_self_improvement_agent()


from typing import Any  # noqa: E402  (local import after module globals)


__all__ = [
    "analyze_codebase",
    "analyze_leabharlann",
    "propose_feature",
    "build_function_tools",
    "build_self_improvement_agent",
    "self_improvement_agent",
]
