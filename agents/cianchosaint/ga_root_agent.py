# CIANCHOSAINT — An Garda Síochána (GA) root agent.
#
# Per `cianchosaint-per-constituency-agents-v1` + the
# `cianchosaint-agent-factory-v1` refactor.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""GA Root Agent — An Garda Síochána (Ireland's national police).

Orchestrates 5 specialist agents:
- ga_crime_statistics_agent (CSO Ireland crime & justice statistics)
- ga_traffic_law_agent (non-emergency traffic violation reports)
- ga_foia_requests_agent (ROI FOI Act requests)
- irish_statute_book_agent (irishstatutebook.ie search)
- courts_ie_agent (courts.ie forms + judgements)
"""

from agents.cianchosaint._factory import (
    AGENT_FACTORY_REGISTRY,
    make_cianchosaint_agent,
)
from agents.cianchosaint._base import CianchosaintAgentBase
from agents.cianchosaint.ga_specialists.courts_ie_agent import courts_ie_agent
from agents.cianchosaint.ga_specialists.crime_statistics_agent import ga_crime_statistics_agent
from agents.cianchosaint.ga_specialists.foia_requests_agent import ga_foia_requests_agent
from agents.cianchosaint.ga_specialists.irish_statute_book_agent import irish_statute_book_agent
from agents.cianchosaint.ga_specialists.traffic_law_agent import ga_traffic_law_agent


class GARootAgent(CianchosaintAgentBase):
    """An Garda Síochána root agent — orchestrates 5 GA specialists."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)
        self.root_agent = ga_root_agent


ga_root_agent = make_cianchosaint_agent(
    name="ga_root_agent",
    description=AGENT_FACTORY_REGISTRY["ga_root_agent"].description,
    instruction=AGENT_FACTORY_REGISTRY["ga_root_agent"].instruction,
    sub_agents=[
        ga_crime_statistics_agent,
        ga_traffic_law_agent,
        ga_foia_requests_agent,
        irish_statute_book_agent,
        courts_ie_agent,
    ],
    output_key="ga_response",
)
