# CIANCHOSAINT — per-constituency Google ADK agent fleet registry.
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Exports `CIANCHOSAINT_AGENT_FLEET` — a tuple of all 24 agents:
# 3 root + 15 specialists + 6 FunctionTool wrappers
# (the 7 tool modules expose 7 tool callables, one of which
# is `cross_jurisdiction_query` shared across specialists).

"""
The 24-agent cianchosaint per-constituency fleet.

The fleet is organised into 3 jurisdictions:
- An Garda Síochána (Ireland): 1 root + 5 specialists
- Metropolitan Police + 43 UK forces (England + Wales):
  1 root + 5 specialists
- Police Service of Northern Ireland: 1 root + 5 specialists

Plus 7 cross-cutting tools shared by all 3 root agents.
"""

from __future__ import annotations

# === 3 root agents ===
from .ga_root_agent import GARootAgent, ga_root_agent
from .met_root_agent import METRootAgent, met_root_agent
from .psni_root_agent import PSNIRootAgent, psni_root_agent

# === 5 GA specialists ===
from .ga_specialists.courts_ie_agent import CourtsIeAgent, courts_ie_agent
from .ga_specialists.crime_statistics_agent import (
    GACrimeStatisticsAgent,
    ga_crime_statistics_agent,
)
from .ga_specialists.foia_requests_agent import (
    GAFOIARequestsAgent,
    ga_foia_requests_agent,
)
from .ga_specialists.irish_statute_book_agent import (
    IrishStatuteBookAgent,
    irish_statute_book_agent,
)
from .ga_specialists.traffic_law_agent import (
    GATrafficLawAgent,
    ga_traffic_law_agent,
)

# === 5 MET specialists ===
from .met_specialists.crime_prevention_agent import (
    METCrimePreventionAgent,
    met_crime_prevention_agent,
)
from .met_specialists.crime_statistics_agent import (
    METCrimeStatisticsAgent,
    met_crime_statistics_agent,
)
from .met_specialists.met_press_releases_agent import (
    METPressReleasesAgent,
    met_press_releases_agent,
)
from .met_specialists.met_public_contact_agent import (
    METPublicContactAgent,
    met_public_contact_agent,
)
from .met_specialists.stop_and_search_agent import (
    METStopAndSearchAgent,
    met_stop_and_search_agent,
)

# === 5 PSNI specialists ===
from .psni_specialists.crime_statistics_agent import (
    PSNICrimeStatisticsAgent,
    psni_crime_statistics_agent,
)
from .psni_specialists.ni_justice_agent import NIJusticeAgent, ni_justice_agent
from .psni_specialists.policing_board_agent import (
    PolicingBoardAgent,
    policing_board_agent,
)
from .psni_specialists.psni_press_releases_agent import (
    PSNIPressReleasesAgent,
    psni_press_releases_agent,
)
from .psni_specialists.psni_public_contact_agent import (
    PSNIPublicContactAgent,
    psni_public_contact_agent,
)

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


# The 24-agent fleet tuple. Total count: 3 root + 15 specialists + 6 tool
# callables exposed (one tool, `cross_jurisdiction_query`, is shared by
# multiple specialists and counted once here).
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
    # 6 tool callables (one is shared)
    garda_form_fill,
    met_form_fill,
    psni_form_fill,
    statute_lookup,
    force_lookup,
    foia_request,
    cross_jurisdiction_query,
)


CIANCHOSAINT_AGENT_FLEET_SIZE = len(CIANCHOSAINT_AGENT_FLEET)


__all__ = [
    # 3 root agents
    "GARootAgent",
    "METRootAgent",
    "PSNIRootAgent",
    "ga_root_agent",
    "met_root_agent",
    "psni_root_agent",
    # 5 GA specialists
    "GACrimeStatisticsAgent",
    "GATrafficLawAgent",
    "GAFOIARequestsAgent",
    "IrishStatuteBookAgent",
    "CourtsIeAgent",
    "ga_crime_statistics_agent",
    "ga_traffic_law_agent",
    "ga_foia_requests_agent",
    "irish_statute_book_agent",
    "courts_ie_agent",
    # 5 MET specialists
    "METCrimeStatisticsAgent",
    "METStopAndSearchAgent",
    "METPressReleasesAgent",
    "METPublicContactAgent",
    "METCrimePreventionAgent",
    "met_crime_statistics_agent",
    "met_stop_and_search_agent",
    "met_press_releases_agent",
    "met_public_contact_agent",
    "met_crime_prevention_agent",
    # 5 PSNI specialists
    "PSNICrimeStatisticsAgent",
    "PSNIPressReleasesAgent",
    "PSNIPublicContactAgent",
    "NIJusticeAgent",
    "PolicingBoardAgent",
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
