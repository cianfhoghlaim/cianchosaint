# CIANCHOSAINT — Metropolitan Police + 43 UK forces root agent.
#
# Per `cianchosaint-per-constituency-agents-v1` + the
# `cianchosaint-agent-factory-v1` refactor.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""MET Root Agent — Metropolitan Police + 43 UK forces.

Orchestrates 5 specialist agents:
- met_crime_statistics_agent (data.police.uk crime stats)
- met_stop_and_search_agent (data.police.uk stop & search)
- met_press_releases_agent (met.police.uk press releases)
- met_public_contact_agent (MET non-emergency form filler)
- met_crime_prevention_agent (NPCC crime prevention advice)
"""

from agents.cianchosaint._factory import (
    AGENT_FACTORY_REGISTRY,
    make_cianchosaint_agent,
)
from agents.cianchosaint._base import CianchosaintAgentBase
from agents.cianchosaint.met_specialists.crime_prevention_agent import met_crime_prevention_agent
from agents.cianchosaint.met_specialists.crime_statistics_agent import met_crime_statistics_agent
from agents.cianchosaint.met_specialists.met_press_releases_agent import met_press_releases_agent
from agents.cianchosaint.met_specialists.met_public_contact_agent import met_public_contact_agent
from agents.cianchosaint.met_specialists.stop_and_search_agent import met_stop_and_search_agent


class METRootAgent(CianchosaintAgentBase):
    """Metropolitan Police + 43 UK forces root agent."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)
        self.root_agent = met_root_agent


met_root_agent = make_cianchosaint_agent(
    name="met_root_agent",
    description=AGENT_FACTORY_REGISTRY["met_root_agent"].description,
    instruction=AGENT_FACTORY_REGISTRY["met_root_agent"].instruction,
    sub_agents=[
        met_crime_statistics_agent,
        met_stop_and_search_agent,
        met_press_releases_agent,
        met_public_contact_agent,
        met_crime_prevention_agent,
    ],
    output_key="met_response",
)
