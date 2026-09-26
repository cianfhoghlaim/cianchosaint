# CIANCHOSAINT — per-constituency Google ADK agent fleet registry.
#
# Per `cianchosaint-per-constituency-agents-v1` + the
# `cianchosaint-agent-factory-v1` refactor.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""The 24-agent cianchosaint per-constituency fleet.

The fleet is organised into 3 jurisdictions:
- An Garda Síochána (Ireland): 1 root + 5 specialists
- Metropolitan Police + 43 UK forces (England + Wales):
  1 root + 5 specialists
- Police Service of Northern Ireland: 1 root + 5 specialists

Plus 7 cross-cutting tools shared by all 3 root agents.
"""

from __future__ import annotations

# === 3 root agents ===
from .ga_root_agent import ga_root_agent
from .met_root_agent import met_root_agent
from .psni_root_agent import psni_root_agent

# === 5 GA specialists (built via the canonical make_cianchosaint_agent factory) ===
from .ga_specialists.courts_ie_agent import courts_ie_agent
from .ga_specialists.crime_statistics_agent import ga_crime_statistics_agent
from .ga_specialists.foia_requests_agent import ga_foia_requests_agent
from .ga_specialists.irish_statute_book_agent import irish_statute_book_agent
from .ga_specialists.traffic_law_agent import ga_traffic_law_agent

# === 5 MET specialists (built via the canonical make_cianchosaint_agent factory) ===
from .met_specialists.crime_prevention_agent import met_crime_prevention_agent
from .met_specialists.crime_statistics_agent import met_crime_statistics_agent
from .met_specialists.met_press_releases_agent import met_press_releases_agent
from .met_specialists.met_public_contact_agent import met_public_contact_agent
from .met_specialists.stop_and_search_agent import met_stop_and_search_agent

# === 5 PSNI specialists (built via the canonical make_cianchosaint_agent factory) ===
from .psni_specialists.crime_statistics_agent import psni_crime_statistics_agent
from .psni_specialists.ni_justice_agent import ni_justice_agent
from .psni_specialists.policing_board_agent import policing_board_agent
from .psni_specialists.psni_press_releases_agent import psni_press_releases_agent
from .psni_specialists.psni_public_contact_agent import psni_public_contact_agent

# === 4 memory_bank modules (canonical Memory Bank pattern per T2.3) ===
from .memory_bank import (
    APP_SCOPE_KEY as _MEMORY_APP_SCOPE_KEY,
    CianchosaintMemoryService,
    candidates_from_session,
)
from .memory_bank import state as memory_bank_state
from .memory_bank import topics as memory_bank_topics

# === 7 tools (the FunctionTool-wrapped helpers) ===
from .tools.cross_jurisdiction_query import (
    cross_jurisdiction_query,
    cross_jurisdiction_query_tool,
)
from .tools.foia_request import foia_request, foia_request_tool
from .tools.force_lookup import UK_FORCES, force_lookup, force_lookup_tool
from .tools.garda_form_fill import garda_form_fill, garda_form_fill_tool
from .tools.met_form_fill import met_form_fill, met_form_fill_tool
from .tools.psni_form_fill import psni_form_fill, psni_form_fill_tool
from .tools.statute_lookup import statute_lookup, statute_lookup_tool


# The 18-agent fleet tuple. Total count: 3 root + 15 specialists.
CIANCHOSAINT_AGENT_FLEET: tuple = (
    # 3 root agents
    ga_root_agent,
    met_root_agent,
    psni_root_agent,
    # 5 GA specialists
    ga_crime_statistics_agent,
    ga_traffic_law_agent,
    ga_foia_requests_agent,
    irish_statute_book_agent,
    courts_ie_agent,
    # 5 MET specialists
    met_crime_statistics_agent,
    met_stop_and_search_agent,
    met_press_releases_agent,
    met_public_contact_agent,
    met_crime_prevention_agent,
    # 5 PSNI specialists
    psni_crime_statistics_agent,
    psni_press_releases_agent,
    psni_public_contact_agent,
    ni_justice_agent,
    policing_board_agent,
)


CIANCHOSAINT_AGENT_FLEET_SIZE = len(CIANCHOSAINT_AGENT_FLEET)


# Hydrate the AGENT_FACTORY_REGISTRY's `sub_agents` + `tools` strings into
# actual LlmAgent + FunctionTool instances. Runs AFTER all 18 specialist
# modules have loaded their canonical agent instances.
from ._factory import _post_load_hydration  # noqa: E402

_post_load_hydration()


__all__ = [
    # 3 root agents
    "ga_root_agent",
    "met_root_agent",
    "psni_root_agent",
    # 5 GA specialists (instances only — the *ClassName* exports are dropped
    # in the factory refactor; the agent instances are the canonical surface)
    "ga_crime_statistics_agent",
    "ga_traffic_law_agent",
    "ga_foia_requests_agent",
    "irish_statute_book_agent",
    "courts_ie_agent",
    # 5 MET specialists
    "met_crime_statistics_agent",
    "met_stop_and_search_agent",
    "met_press_releases_agent",
    "met_public_contact_agent",
    "met_crime_prevention_agent",
    # 5 PSNI specialists
    "psni_crime_statistics_agent",
    "psni_press_releases_agent",
    "psni_public_contact_agent",
    "ni_justice_agent",
    "policing_board_agent",
    # 7 tools
    "cross_jurisdiction_query",
    "cross_jurisdiction_query_tool",
    "foia_request",
    "foia_request_tool",
    "force_lookup",
    "force_lookup_tool",
    "UK_FORCES",
    "garda_form_fill",
    "garda_form_fill_tool",
    "met_form_fill",
    "met_form_fill_tool",
    "psni_form_fill",
    "psni_form_fill_tool",
    "statute_lookup",
    "statute_lookup_tool",
    # Fleet
    "CIANCHOSAINT_AGENT_FLEET",
    "CIANCHOSAINT_AGENT_FLEET_SIZE",
]
