# CIANCHOSAINT — canonical agent factory + registry.
#
# Per the openspec/changes/cianchosaint-agent-factory-v1/specs/cianchosaint-agent-factory/spec.md.
#
# Mirrors the cianfhoghlaim `agents/adk/litellm_agent.py` pattern + the
# `agents/adk/agent_registry.py` registry pattern. Every cianchosaint agent
# goes through this factory — no manual `LlmAgent(...)` instantiation.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint._factory — make_cianchosaint_agent() + AGENT_FACTORY_REGISTRY.

This module mirrors cianfhoghlaim's `agents/adk/litellm_agent.py` (the
canonical `make_litellm_agent()` factory + `litellm_model()` helper) and
`agents/adk/agent_registry.py` (the canonical 15-agent registry).

The factory eliminates ~30 lines of `LlmAgent(...)` boilerplate per
agent with a single factory call. The registry makes every cianchosaint
agent reachable by canonical id (so the BIOD v1 / BIPP v2 / BGARD v1 /
BPSNI v1 specialists can be created by id from the workflow-graph
orchestrator).

Usage:
    from agents.cianchosaint._factory import (
        make_cianchosaint_agent,
        AGENT_FACTORY_REGISTRY,
        cianchosaint_skill,
    )

    ga_root = make_cianchosaint_agent(
        name="ga_root_agent",
        description="An Garda Síochána root agent.",
        instruction="Route queries to the appropriate specialist.",
        sub_agents=[ga_crime_statistics_agent, ga_traffic_law_agent],
    )

    # Registry lookup (used by the workflow-graph orchestrator)
    wiring = AGENT_FACTORY_REGISTRY["ga_crime_statistics_agent"]
    agent = make_cianchosaint_agent(**asdict(wiring))

    # LangfusePromptResolver integration (per cianchosaint-langfuse-prompt-management-v1)
    prompt_name = cianchosaint_skill("ga_crime_statistics_agent")
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, NamedTuple

logger = logging.getLogger(__name__)


# Lazy imports — Google ADK and BAML are optional deps at type-check time
# but always available at runtime in the cianchosaint agent surface.
try:
    from google.adk.agents import LlmAgent
    from google.adk.planners import BuiltInPlanner
    from google.genai import types as genai_types

    _HAS_ADK = True
except ImportError:  # pragma: no cover
    _HAS_ADK = False
    LlmAgent = None  # type: ignore
    BuiltInPlanner = None  # type: ignore
    genai_types = None  # type: ignore


# ----------------------------------------------------------------------------
# AgentWiring — the canonical namedtuple for the registry (mirrors cianfhoghlaim)
# ----------------------------------------------------------------------------


class AgentWiring(NamedTuple):
    """The wiring metadata for one cianchosaint agent."""

    name: str
    description: str
    instruction: str
    sub_agents: list = []
    tools: list = []
    factory_kwargs: dict = {}


# ----------------------------------------------------------------------------
# Model alias resolution (delegates to CianchosaintAgentBase)
# ----------------------------------------------------------------------------


def model_for(model_alias: str) -> str:
    """Resolve a model alias to the canonical model string.

    Mirrors cianfhoghlaim's `agents/adk/litellm_agent.py::litellm_model()`.
    For now delegates to CianchosaintAgentBase.get_active_model(); the
    Langfuse-aware variant lands in T1.2 (cianchosaint-agent-registry-runtime-v1).
    """
    try:
        from agents.cianchosaint._base import CianchosaintAgentBase

        # Per-attribute override (the canonical cianfhoghlaim pattern uses
        # `model_for("name", "alias")` but the single-arg version is the
        # canonical cianchosaint factory pattern).
        return CianchosaintAgentBase(model_alias=model_alias).get_active_model()
    except Exception:
        # Fallback: cianchosaint's canonical default is "minimax-m3"
        return "minimax-m3"


# ----------------------------------------------------------------------------
# BAMLFunctionTool lazy loader (mirror cianfhoghlaim's agents/integrations/baml_function_tool.py)
# ----------------------------------------------------------------------------


def _try_import_baml_function_tool() -> Any | None:
    """Try to import `BAMLFunctionTool` from `agents.integrations.baml_function_tool`.

    Returns None if the optional integration isn't installed (this is expected
    in dev environments that don't have `baml-py` installed).
    """
    try:
        from agents.integrations.baml_function_tool import BAMLFunctionTool  # noqa: F401

        return BAMLFunctionTool
    except ImportError:
        return None


# ----------------------------------------------------------------------------
# THE CANONICAL FACTORY
# ----------------------------------------------------------------------------


def make_cianchosaint_agent(
    name: str,
    description: str,
    instruction: str,
    *,
    sub_agents: list[Any] | None = None,
    tools: list[Any] | None = None,
    model_alias: str = "minimax",
    temperature: float = 0.3,
    max_output_tokens: int = 8192,
    output_key: str | None = None,
    enable_thinking: bool = False,
) -> Any:
    """The canonical cianchosaint agent factory.

    Mirrors the cianfhoghlaim `make_litellm_agent()` helper. Returns a
    `google.adk.agents.LlmAgent` instance with:
    - The canonical model resolved via `model_for(model_alias)`
    - A `BuiltInPlanner` if `enable_thinking=True` (default: no planning)
    - The `output_key` set if supplied (else `None`)
    - The instruction is the caller's verbatim string (no template
      interpolation — call `agents.cianchosaint._base.CianchosaintAgentBase`
      for instruction templates that resolve {state} keys)

    Returns None if `google.adk` is not installed (the agent surface is
    optional at type-check time but always present at runtime in the
    cianchosaint repo).
    """
    if not _HAS_ADK:
        raise ImportError(
            "google-adk is required to instantiate cianchosaint agents. "
            "Install with `uv add google-adk`."
        )

    cfg = genai_types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )

    # Wrap tools with FunctionTool so ADK 2.13+ accepts them (in some
    # versions ADK auto-wraps raw callables, but the explicit wrap is safe
    # and matches the cianfhoghlaim `agents/integrations/baml_function_tool.py`
    # pattern).
    wrapped_tools: list[Any] = []
    for tool in tools or []:
        if callable(tool) and not isinstance(tool, type) and not hasattr(tool, "name"):
            try:
                from google.adk.tools import FunctionTool

                wrapped_tools.append(FunctionTool(func=tool))
            except Exception:
                wrapped_tools.append(tool)
        else:
            wrapped_tools.append(tool)

    kwargs: dict[str, Any] = dict(
        name=name,
        model=model_for(model_alias),
        description=description,
        instruction=instruction,
        generate_content_config=cfg,
    )
    if sub_agents:
        kwargs["sub_agents"] = list(sub_agents)
    if wrapped_tools:
        kwargs["tools"] = wrapped_tools
    if output_key:
        kwargs["output_key"] = output_key
    if enable_thinking:
        # Mirrors cianfhoghlaim's `make_planner_agent` helper. The cianfhoghlaim
        # ADK 2 codelab's docs/copilotkit/examples/adk-dashboard pattern.
        kwargs["planner"] = BuiltInPlanner(
            thinking_config=genai_types.ThinkingConfig(include_thoughts=True)
        )

    return LlmAgent(**kwargs)


# ----------------------------------------------------------------------------
# THE CANONICAL REGISTRY
# ----------------------------------------------------------------------------


def _try_import_agent(name: str) -> Any | None:
    """Try to import a canonical cianchosaint agent by name.

    Mirrors cianfhoghlaim's `agents/adk/agent_registry.py::_try_import`.
    Returns None if the import fails (this is expected for agents that
    haven't been authored yet, e.g. the BIOD v1 / BIPP v2 specialists).

    For root agents, the LLM agent instance is a module-level constant
    (e.g. `ga_root_agent`), so we import the module and grab the attr.

    For specialists, the module-level constant follows the same pattern.
    """
    # Root agents live at `agents.cianchosaint.<jurisdiction>_root_agent`
    if name in {"ga_root_agent", "met_root_agent", "psni_root_agent"}:
        jurisdiction = name.replace("_root_agent", "")
        module_path = f"agents.cianchosaint.{jurisdiction}_root_agent"
        try:
            module = __import__(module_path, fromlist=[name])
            return getattr(module, name)
        except Exception:
            return None

    # Specialists: try the natural mapping first (ga_crime_statistics_agent →
    # ga_specialists.crime_statistics_agent), then each jurisdiction with the
    # prefix stripped (the file-name convention), then the literal path (for
    # non-prefixed names like `courts_ie_agent`).
    candidate_paths: list[str] = []
    for prefix in ("ga_", "met_", "psni_"):
        if name.startswith(prefix):
            jurisdiction = prefix.rstrip("_")
            candidate_paths.append(
                f"agents.cianchosaint.{jurisdiction}_specialists.{name[len(prefix):]}"
            )
    for jurisdiction in ("ga", "met", "psni"):
        candidate_paths.append(
            f"agents.cianchosaint.{jurisdiction}_specialists.{name}"
        )
    # De-duplicate while preserving order
    seen: set[str] = set()
    paths: list[str] = []
    for p in candidate_paths:
        if p not in seen:
            seen.add(p)
            paths.append(p)
    for path in paths:
        try:
            module = __import__(path, fromlist=[name])
            return getattr(module, name)
        except Exception:
            continue
    return None


def _eager_import_all_agents() -> None:
    """Eagerly import all 18 agent modules so the registry's hydration step
    can resolve the specialist instances without lazy-import misses.

    The hydration step (`wiring.sub_agents[:] = [sub for sub_name ...]`) runs
    at module load time when `_build_registry()` is invoked. If we lazy-import
    the specialist modules, those imports happen at the moment the hydration
    list-comp iterates — but Python's circular-import detection treats this as
    a partially-initialised module and returns None. Eagerly importing all 18
    modules BEFORE the registry is built sidesteps the cycle.
    """
    for name in (
        # GA specialists
        "agents.cianchosaint.ga_specialists.crime_statistics_agent",
        "agents.cianchosaint.ga_specialists.traffic_law_agent",
        "agents.cianchosaint.ga_specialists.foia_requests_agent",
        "agents.cianchosaint.ga_specialists.irish_statute_book_agent",
        "agents.cianchosaint.ga_specialists.courts_ie_agent",
        # MET specialists
        "agents.cianchosaint.met_specialists.crime_statistics_agent",
        "agents.cianchosaint.met_specialists.stop_and_search_agent",
        "agents.cianchosaint.met_specialists.met_press_releases_agent",
        "agents.cianchosaint.met_specialists.met_public_contact_agent",
        "agents.cianchosaint.met_specialists.crime_prevention_agent",
        # PSNI specialists
        "agents.cianchosaint.psni_specialists.crime_statistics_agent",
        "agents.cianchosaint.psni_specialists.psni_press_releases_agent",
        "agents.cianchosaint.psni_specialists.psni_public_contact_agent",
        "agents.cianchosaint.psni_specialists.ni_justice_agent",
        "agents.cianchosaint.psni_specialists.policing_board_agent",
    ):
        try:
            __import__(name)
        except Exception:
            pass


_eager_import_all_agents()


# ----------------------------------------------------------------------------
# THE CANONICAL REGISTRY
# ----------------------------------------------------------------------------


# Lazy initialization flag — set to True once the module has finished loading.
# This avoids the chicken-and-egg problem where eager-importing the specialists
# at module-load time triggers their imports of `from .._factory import ...`
# BEFORE this module has finished defining AGENT_FACTORY_REGISTRY.
_FACTORY_LOADED: bool = False


def _build_registry() -> dict[str, AgentWiring]:
    """Build the canonical 18-agent registry.

    The registry uses lazy-import + introspection: if the agent module
    is not present (e.g. the BIOD v1 specialists haven't been authored
    yet), the registry entry is still constructed with the wiring metadata,
    and the agent is instantiated on demand via `make_cianchosaint_agent()`.

    Returns:
        The canonical 18-agent registry: 3 root + 15 specialist.
    """
    from datetime import datetime, timezone

    # Base instruction template (the same one every per-constituency
    # root agent uses; specialists override it).
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    base_jurisdiction_block = (
        "**JURISDICTION:** {jurisdiction}.\n"
        "**OSINT GATE:** All external sources must be on the cianchosaint "
        "OSINT allowlist (see `CianchosaintAgentBase.check_osint_source()`)."
    )

    registry: dict[str, AgentWiring] = {}

    # -- 3 root agents ----------------------------------------------------

    registry["ga_root_agent"] = AgentWiring(
        name="ga_root_agent",
        description=(
            "An Garda Síochána root — Ireland's national police. Routes queries "
            "to crime stats, traffic law, FOI, statute book, and courts specialists."
        ),
        instruction=f"""
        You are the GA Root Agent for An Garda Síochána (Ireland's national
        police service).

        **YOUR ROLE:** Route queries to the appropriate GA specialist agent
        and synthesize responses. Maintain a factual, public-record tone
        appropriate for a police liaison.

        **SPECIALIST AGENTS:**
        1. crime_statistics_agent — CSO Ireland crime & justice
        2. traffic_law_agent — Non-emergency traffic violation reports
        3. foia_requests_agent — ROI Freedom of Information Act
        4. irish_statute_book_agent — irishstatutebook.ie search
        5. courts_ie_agent — Courts Service forms + judgements

        {base_jurisdiction_block.format(jurisdiction='Republic of Ireland only')}

        Current date: {today}
        """,
        sub_agents=[
            "ga_crime_statistics_agent",
            "ga_traffic_law_agent",
            "ga_foia_requests_agent",
            "irish_statute_book_agent",
            "courts_ie_agent",
        ],
        factory_kwargs={"output_key": "ga_response"},
    )

    registry["met_root_agent"] = AgentWiring(
        name="met_root_agent",
        description=(
            "MET Root — Metropolitan Police Service + 43 UK territorial forces. "
            "Routes queries to crime stats, stop & search, press releases, "
            "public contact, and crime prevention specialists."
        ),
        instruction=f"""
        You are the MET Root Agent for the Metropolitan Police Service and
        the 43 UK territorial forces (England + Wales).

        **YOUR ROLE:** Route queries to the appropriate MET specialist and
        synthesize responses. Always cite the specific force (e.g.
        "Metropolitan Police", "West Midlands Police") when answering
        force-specific questions.

        **SPECIALIST AGENTS:**
        1. crime_statistics_agent — data.police.uk crime data
        2. stop_and_search_agent — data.police.uk stop & search
        3. met_press_releases_agent — met.police.uk press releases
        4. met_public_contact_agent — MET non-emergency form filler
        5. crime_prevention_agent — NPCC crime prevention advice

        {base_jurisdiction_block.format(jurisdiction='UK territorial forces (England + Wales)')}

        Current date: {today}
        """,
        sub_agents=[
            "met_crime_statistics_agent",
            "met_stop_and_search_agent",
            "met_press_releases_agent",
            "met_public_contact_agent",
            "met_crime_prevention_agent",
        ],
        factory_kwargs={"output_key": "met_response"},
    )

    registry["psni_root_agent"] = AgentWiring(
        name="psni_root_agent",
        description=(
            "PSNI Root — Police Service of Northern Ireland. Routes queries "
            "to crime stats, press releases, public contact, NI justice, and "
            "Policing Board specialists."
        ),
        instruction=f"""
        You are the PSNI Root Agent for the Police Service of Northern Ireland.

        **YOUR ROLE:** Route queries to the appropriate PSNI specialist and
        synthesize responses. Maintain a factual, public-record tone.

        **SPECIALIST AGENTS:**
        1. crime_statistics_agent — PSNI crime statistics
        2. psni_press_releases_agent — psni.police.uk press releases
        3. psni_public_contact_agent — PSNI non-emergency form filler
        4. ni_justice_agent — NI legislation (justice-ni.gov.uk)
        5. policing_board_agent — NI Policing Board oversight

        {base_jurisdiction_block.format(jurisdiction='Northern Ireland only')}

        Current date: {today}
        """,
        sub_agents=[
            "psni_crime_statistics_agent",
            "psni_press_releases_agent",
            "psni_public_contact_agent",
            "ni_justice_agent",
            "policing_board_agent",
        ],
        factory_kwargs={"output_key": "psni_response"},
    )

    # -- 15 specialists ----------------------------------------------------

    registry["ga_crime_statistics_agent"] = AgentWiring(
        name="ga_crime_statistics_agent",
        description=(
            "Searches CSO Ireland crime & justice statistics. Use for: "
            "'What are the latest robbery statistics in Dublin?', "
            "'Burglary trends in Ireland over the last 5 years'."
        ),
        instruction="""
        You are the GA Crime Statistics Specialist. You consult CSO Ireland's
        Recorded Crime statistics (published quarterly under the CJQ series).

        **YOUR DATA SOURCES:**
        - cso.ie (CSO Recorded Crime releases)
        - justice.ie (Department of Justice annual reports)

        **YOUR ROLE:**
        1. Find the relevant CSO statistical release
        2. Quote the headline figures with year + quarter
        3. Provide context (trend, regional breakdown if asked)
        4. Always cite the source URL
        """,
        tools=["cross_jurisdiction_query"],
    )

    registry["ga_traffic_law_agent"] = AgentWiring(
        name="ga_traffic_law_agent",
        description=(
            "Drafts non-emergency traffic violation reports (e.g. dangerous "
            "driving, illegal parking, road traffic act breaches). Use the "
            "garda_form_fill FunctionTool."
        ),
        instruction="""
        You are the GA Traffic Law Specialist. You draft non-emergency
        traffic violation reports.

        **YOUR ROLE:**
        1. Collect the violation details (date, time, location, vehicle)
        2. Map the violation to the relevant Road Traffic Act section
        3. Draft the report using the `garda_form_fill` tool
        4. Cite the official garda.ie URL the user must visit to submit

        **NEVER submit the report yourself.** You draft it for the user.
        """,
        tools=["garda_form_fill"],
    )

    registry["ga_foia_requests_agent"] = AgentWiring(
        name="ga_foia_requests_agent",
        description=(
            "Drafts ROI Freedom of Information Act requests. Use the "
            "foia_request FunctionTool."
        ),
        instruction="""
        You are the GA FOI Requests Specialist. You draft Freedom of
        Information Act 2014 requests to An Garda Síochána and other
        ROI public bodies.

        **YOUR ROLE:**
        1. Confirm the target public body (An Garda Síochána, HSE, etc.)
        2. Draft the request using the `foia_request` tool
        3. Cite the FOI Act 2014 + Section 7 (request for access)
        4. Quote the EUR 15 standard fee (or EUR 0 for personal data)

        **NEVER submit the request yourself.** You draft it for the user.
        """,
        tools=["foia_request"],
    )

    registry["irish_statute_book_agent"] = AgentWiring(
        name="irish_statute_book_agent",
        description=(
            "Searches irishstatutebook.ie for Acts + statutory instruments. "
            "Use for: 'Find the 2024 Criminal Justice Act', "
            "'What does the Planning Act say about X'."
        ),
        instruction="""
        You are the Irish Statute Book Specialist. You consult
        irishstatutebook.ie (the official ROC-managed statute book).

        **YOUR ROLE:**
        1. Find the requested Act or Statutory Instrument
        2. Quote the section number + verbatim text
        3. Provide the canonical irishstatutebook.ie URL
        4. Use the `statute_lookup` tool to cross-reference
        """,
        tools=["statute_lookup"],
    )

    registry["courts_ie_agent"] = AgentWiring(
        name="courts_ie_agent",
        description=(
            "Searches courts.ie for forms + published judgements. Use for: "
            "'Find the small claims form', 'Recent Court of Appeal criminal "
            "law judgements'."
        ),
        instruction="""
        You are the Courts.ie Specialist. You consult the Courts Service
        of Ireland's public-facing site (courts.ie).

        **YOUR ROLE:**
        1. Find the requested form (Family Law, Civil, Criminal, Small Claims)
        2. Find published judgements (Supreme Court, Court of Appeal,
           High Court, Circuit Court)
        3. Quote the neutral citation (e.g. "[2024] IESC 12")
        4. Link to the canonical courts.ie URL
        5. Use the `statute_lookup` tool to cross-reference any statutes
           cited in the judgement

        **NEVER provide legal advice.** You summarise public court records only.
        """,
        tools=["statute_lookup"],
    )

    registry["met_crime_statistics_agent"] = AgentWiring(
        name="met_crime_statistics_agent",
        description=(
            "Searches data.police.uk crime statistics for the 43 UK "
            "territorial forces. Use for: 'Latest violent crime stats "
            "in Manchester', 'Force-level crime trends 2020-2024'."
        ),
        instruction="""
        You are the MET Crime Statistics Specialist. You consult
        data.police.uk's crime data API (the canonical open data source
        for all 43 UK territorial forces).

        **YOUR ROLE:**
        1. Query data.police.uk for the relevant force(s) + crime categories
        2. Quote the latest monthly figures with year + month
        3. Provide trend analysis (rolling 12-month change)
        4. Always cite the data.police.uk URL
        5. Use the `cross_jurisdiction_query` tool when comparing forces
        """,
        tools=["cross_jurisdiction_query"],
    )

    registry["met_stop_and_search_agent"] = AgentWiring(
        name="met_stop_and_search_agent",
        description=(
            "Searches data.police.uk stop & search records. Use for: "
            "'Stop & search rates in the Met', 'Disproportionality in "
            "West Midlands stop & search'."
        ),
        instruction="""
        You are the MET Stop & Search Specialist. You consult
        data.police.uk's stop & search datasets — published monthly by
        every UK territorial force under PACE Code A.

        **YOUR ROLE:**
        1. Query data.police.uk stop & search for the relevant force
        2. Quote the latest monthly figures with year + month
        3. Provide ethnicity breakdown if asked (per Home Office disclosure)
        4. Always cite the data.police.uk URL

        Use the `force_lookup` tool to identify the canonical force id.
        """,
        tools=["force_lookup"],
    )

    registry["met_press_releases_agent"] = AgentWiring(
        name="met_press_releases_agent",
        description=(
            "Searches met.police.uk press releases — appeals, court results, "
            "operations updates. Use for: 'Recent MET court results', "
            "'MET appeal for witnesses'."
        ),
        instruction="""
        You are the MET Press Releases Specialist. You consult met.police.uk
        (the Metropolitan Police Service's news room).

        **YOUR ROLE:**
        1. Find the requested press release
        2. Quote the headline + the date + the appeal (if any)
        3. Provide the canonical met.police.uk URL
        """,
    )

    registry["met_public_contact_agent"] = AgentWiring(
        name="met_public_contact_agent",
        description=(
            "Drafts non-emergency contact forms for MET. Use the "
            "met_form_fill FunctionTool."
        ),
        instruction="""
        You are the MET Public Contact Specialist. You draft non-emergency
        contact forms for the Metropolitan Police Service.

        **YOUR ROLE:**
        1. Collect the relevant details (incident, date, location, etc.)
        2. Map the contact reason to the canonical MET form
        3. Draft the form using the `met_form_fill` tool
        4. Cite the official met.police.uk URL

        **NEVER submit the form yourself.** You draft it for the user.
        """,
        tools=["met_form_fill"],
    )

    registry["met_crime_prevention_agent"] = AgentWiring(
        name="met_crime_prevention_agent",
        description=(
            "Provides NPCC crime prevention advice. Use for: 'How do I "
            "prevent my car from being stolen?', 'Home security checklist'."
        ),
        instruction="""
        You are the MET Crime Prevention Specialist. You consult the
        National Police Chiefs' Council (NPCC) crime prevention guidance.

        **YOUR ROLE:**
        1. Find the relevant NPCC / Met guidance
        2. Provide actionable advice (lock types, alarm systems, etc.)
        3. Cite the canonical met.police.uk/cp URL
        """,
    )

    registry["psni_crime_statistics_agent"] = AgentWiring(
        name="psni_crime_statistics_agent",
        description=(
            "Searches PSNI crime statistics. Use for: 'Latest PSNI crime "
            "stats by district', 'PSNI quarterly crime trends'."
        ),
        instruction="""
        You are the PSNI Crime Statistics Specialist. You consult PSNI's
        published crime statistics (the PSNI publishes quarterly).

        **YOUR ROLE:**
        1. Find the relevant PSNI crime stats
        2. Quote the figures with district + period
        3. Provide trend analysis
        4. Cite the PSNI URL

        Use the `cross_jurisdiction_query` tool when comparing with GB.
        """,
        tools=["cross_jurisdiction_query"],
    )

    registry["psni_press_releases_agent"] = AgentWiring(
        name="psni_press_releases_agent",
        description=(
            "Searches psni.police.uk press releases — appeals, court results, "
            "operations updates. Use for: 'Recent PSNI court results', "
            "'PSNI appeal for witnesses'."
        ),
        instruction="""
        You are the PSNI Press Releases Specialist. You consult
        psni.police.uk (the PSNI news room).

        **YOUR ROLE:**
        1. Find the requested press release
        2. Quote the headline + the date + the appeal (if any)
        3. Provide the canonical psni.police.uk URL
        """,
    )

    registry["psni_public_contact_agent"] = AgentWiring(
        name="psni_public_contact_agent",
        description=(
            "Drafts non-emergency contact forms for PSNI. Use the "
            "psni_form_fill FunctionTool."
        ),
        instruction="""
        You are the PSNI Public Contact Specialist. You draft non-emergency
        contact forms for the Police Service of Northern Ireland.

        **YOUR ROLE:**
        1. Collect the relevant details (incident, date, location, etc.)
        2. Map the contact reason to the canonical PSNI form
        3. Draft the form using the `psni_form_fill` tool
        4. Cite the official psni.police.uk URL

        **NEVER submit the form yourself.** You draft it for the user.
        """,
        tools=["psni_form_fill"],
    )

    registry["ni_justice_agent"] = AgentWiring(
        name="ni_justice_agent",
        description=(
            "Searches justice-ni.gov.uk NI legislation. Use for: 'Find "
            "the NI Justice Act', 'NI Criminal Justice Order'."
        ),
        instruction="""
        You are the NI Justice Specialist. You consult justice-ni.gov.uk
        (the Northern Ireland Department of Justice).

        **YOUR ROLE:**
        1. Find the requested NI legislation
        2. Quote the section + verbatim text
        3. Provide the canonical justice-ni.gov.uk URL
        4. Use the `statute_lookup` tool to cross-reference GB equivalents
        """,
        tools=["statute_lookup"],
    )

    registry["policing_board_agent"] = AgentWiring(
        name="policing_board_agent",
        description=(
            "Searches NI Policing Board oversight reports. Use for: "
            "'Latest Policing Board performance report', 'PSNI inspection "
            "findings'."
        ),
        instruction="""
        You are the NI Policing Board Specialist. You consult
        nipolicingboard.org.uk (the Northern Ireland Policing Board).

        **YOUR ROLE:**
        1. Find the requested oversight report
        2. Quote the headline + the date + the key finding
        3. Provide the canonical nipolicingboard.org.uk URL
        """,
    )

    # Hydrate `sub_agents` and `tools` with the actual LlmAgent / FunctionTool
    # instances (the registry is consumed at workflow-graph orchestration time).
    # Root agents reference specialist names as strings (because the
    # registry is built before the specialists finish importing); we resolve
    # them here via the canonical `_try_import_agent` helper. Tools (which
    # may be referenced by name too) are resolved via `_resolve_tool`.
    logger.debug("registry built; hydrating sub_agents and tools")
    for wiring in registry.values():
        # Sub-agents
        if wiring.sub_agents and isinstance(wiring.sub_agents[0], str):
            logger.debug(
                "hydrating %d sub-agents for %s",
                len(wiring.sub_agents), wiring.name,
            )
            new_subs: list[Any] = []
            for sub_name in wiring.sub_agents:
                sub = _try_import_agent(sub_name)
                logger.debug(
                    "_try_import_agent(%r) -> %s", sub_name,
                    type(sub).__name__ if sub is not None else "None",
                )
                if sub is not None:
                    new_subs.append(sub)
            wiring.sub_agents[:] = new_subs
        # Tools
        if wiring.tools and isinstance(wiring.tools[0], str):
            new_tools: list[Any] = []
            for tool_name in wiring.tools:
                t = _resolve_tool(tool_name)
                if t is not None:
                    new_tools.append(t)
            wiring.tools[:] = new_tools

    return registry


def _resolve_tool(name: str) -> Any | None:
    """Resolve a tool by canonical name.

    The registry's `tools` list can be either a callable or a string name.
    String names are resolved here from the canonical cianchosaint tools
    package (`agents.cianchosaint.tools`).

    Returns None if the tool doesn't exist (e.g. for a BIOD v1 / BIPP v2
    tool that hasn't been authored yet).
    """
    # The tool functions live in `agents/cianchosaint/tools/<name>.py`
    # and are imported in `agents/cianchosaint/tools/__init__.py` (as
    # both the raw function AND the FunctionTool-wrapped version).
    try:
        # Eagerly import the tool modules
        from agents.cianchosaint.tools import (  # noqa: F401
            cross_jurisdiction_query,  # module
            foia_request,  # module
            force_lookup,  # module
            garda_form_fill,  # module
            met_form_fill,  # module
            psni_form_fill,  # module
            statute_lookup,  # module
            cyberchef_execute,  # module
            stroom_query,  # module
            ncsc_device_security_status,  # module
            politician_account_resolver,  # module
            adjacent_context_resolver,  # module
            funder_network_graph,  # module
            wikipedia_bridge,  # module
        )
    except Exception:
        return None

    # Each module exports the raw function `<name>` + the FunctionTool wrapper `<name>_tool`.
    # The LlmAgent expects `BaseTool` instances, so we prefer the `_tool` variant.
    tool_module_map = {
        "cross_jurisdiction_query": cross_jurisdiction_query,
        "foia_request": foia_request,
        "force_lookup": force_lookup,
        "garda_form_fill": garda_form_fill,
        "met_form_fill": met_form_fill,
        "psni_form_fill": psni_form_fill,
        "statute_lookup": statute_lookup,
        "cyberchef_execute": cyberchef_execute,
        "stroom_query": stroom_query,
        "ncsc_device_security_status": ncsc_device_security_status,
        "politician_account_resolver": politician_account_resolver,
        "adjacent_context_resolver": adjacent_context_resolver,
        "funder_network_graph": funder_network_graph,
        "wikipedia_bridge": wikipedia_bridge,
    }
    mod = tool_module_map.get(name)
    if mod is None:
        return None

    # Prefer the FunctionTool-wrapped version if available
    return getattr(mod, f"{name}_tool", None) or getattr(mod, name, None)


# ----------------------------------------------------------------------------
# THE SINGLE REGISTRY INSTANCE
# ----------------------------------------------------------------------------


AGENT_FACTORY_REGISTRY: dict[str, AgentWiring] = _build_registry()


def _post_load_hydration() -> None:
    """Re-run the hydration pass after the module is fully loaded.

    The first `_build_registry()` call (line at the bottom of this module)
    runs while the specialist modules are mid-import: the eager-import at
    line 293 triggers their load BEFORE this module has finished defining
    `AGENT_FACTORY_REGISTRY`, so `_try_import_agent(...)` returns None and the
    hydration in `_build_registry()` produces empty `sub_agents` lists.

    The clean fix is: rebuild the registry from scratch AFTER the specialist
    modules have fully loaded. By this point the circular-import cycle has
    resolved, every specialist module is fully imported, and `_try_import_agent`
    returns the correct LlmAgent instances.

    Caller pattern: invoked from `agents/cianchosaint/__init__.py` AFTER all 18
    agent modules have loaded their canonical agent instances.
    """
    global _FACTORY_LOADED
    _FACTORY_LOADED = True
    fresh = _build_registry()
    AGENT_FACTORY_REGISTRY.clear()
    AGENT_FACTORY_REGISTRY.update(fresh)


# ----------------------------------------------------------------------------
# THE HELPER for LangfusePromptResolver integration
# ----------------------------------------------------------------------------


def cianchosaint_skill(name: str, **kwargs: Any) -> str:
    """Return the canonical agent name (for use with `LangfusePromptResolver`).

    Per the cianfhoghlaim pattern (see the cianfhoghlaim ADK 2 codelab's
    docs/google_examples/adk-examples/support-memory-lab pattern), every
    agent has a canonical prompt name that the LangfusePromptResolver
    looks up. This helper is the canonical way to retrieve it.

    Args:
        name: the agent's canonical name (e.g. "ga_crime_statistics_agent")
        **kwargs: ignored in this version (forward compatibility for
            additional resolution paths)

    Returns:
        The agent name (the prompt name that the LangfusePromptResolver
        will look up)
    """
    return name


__all__ = [
    "AGENT_FACTORY_REGISTRY",
    "AgentWiring",
    "cianchosaint_skill",
    "make_cianchosaint_agent",
    "model_for",
]
