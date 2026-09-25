# CIANCHOSAINT — Police Service of Northern Ireland (PSNI) root agent.
#
# Per `cianchosaint-per-constituency-agents-v1` + the
# `cianchosaint-agent-factory-v1` refactor.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""PSNI Root Agent — Police Service of Northern Ireland.

Orchestrates 5 specialist agents:
- psni_crime_statistics_agent (PSNI crime statistics)
- psni_press_releases_agent (psni.police.uk press releases)
- psni_public_contact_agent (PSNI non-emergency form filler)
- ni_justice_agent (justice-ni.gov.uk NI legislation)
- policing_board_agent (NI Policing Board oversight reports)
"""

from agents.cianchosaint._factory import (
    AGENT_FACTORY_REGISTRY,
    make_cianchosaint_agent,
)
from agents.cianchosaint._base import CianchosaintAgentBase
from agents.cianchosaint.psni_specialists.crime_statistics_agent import psni_crime_statistics_agent
from agents.cianchosaint.psni_specialists.ni_justice_agent import ni_justice_agent
from agents.cianchosaint.psni_specialists.policing_board_agent import policing_board_agent
from agents.cianchosaint.psni_specialists.psni_press_releases_agent import psni_press_releases_agent
from agents.cianchosaint.psni_specialists.psni_public_contact_agent import psni_public_contact_agent


class PSNIRootAgent(CianchosaintAgentBase):
    """Police Service of Northern Ireland root agent."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)
        self.root_agent = psni_root_agent


psni_root_agent = make_cianchosaint_agent(
    name="psni_root_agent",
    description=AGENT_FACTORY_REGISTRY["psni_root_agent"].description,
    instruction=AGENT_FACTORY_REGISTRY["psni_root_agent"].instruction,
    sub_agents=[
        psni_crime_statistics_agent,
        psni_press_releases_agent,
        psni_public_contact_agent,
        ni_justice_agent,
        policing_board_agent,
    ],
    output_key="psni_response",
)


__all__ = ["PSNIRootAgent", "psni_root_agent"]
