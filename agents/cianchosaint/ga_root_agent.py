# CIANCHOSAINT — An Garda Síochána (GA) root agent.
#
# NEW-BUILD code (not wholesale-copied). Authored per the
# `cianchosaint-per-constituency-agents-v1` change.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
GA Root Agent — An Garda Síochána (Ireland's national police).

Orchestrates 5 specialist agents:
- crime_statistics_agent (CSO Ireland crime & justice statistics)
- traffic_law_agent (non-emergency traffic violation reports)
- foia_requests_agent (ROI FOI Act requests)
- irish_statute_book_agent (irishstatutebook.ie search)
- courts_ie_agent (courts.ie forms + judgements)
"""

import datetime

from google.adk.agents import LlmAgent

from ._base import CianchosaintAgentBase, DEFAULT_MODEL
from .ga_specialists.courts_ie_agent import courts_ie_agent
from .ga_specialists.crime_statistics_agent import ga_crime_statistics_agent
from .ga_specialists.foia_requests_agent import ga_foia_requests_agent
from .ga_specialists.irish_statute_book_agent import irish_statute_book_agent
from .ga_specialists.traffic_law_agent import ga_traffic_law_agent


class GARootAgent(CianchosaintAgentBase):
    """An Garda Síochána root agent — orchestrates 5 GA specialists."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)

        self.root_agent = LlmAgent(
            name="ga_root_agent",
            model=self.get_active_model() or DEFAULT_MODEL,
            description=(
                "An Garda Síochána root — Ireland's national police. "
                "Routes queries to crime stats, traffic law, FOI, "
                "statute book, and courts specialists."
            ),
            instruction=f"""
            You are the GA Root Agent for An Garda Síochána
            (Ireland's national police service).

            **YOUR ROLE:**
            Route queries to the appropriate GA specialist agent and
            synthesize responses. Maintain a factual, public-record
            tone appropriate for a police liaison.

            **SPECIALIST AGENTS:**
            1. crime_statistics_agent — CSO Ireland crime & justice
            2. traffic_law_agent — Non-emergency traffic violation reports
            3. foia_requests_agent — ROI Freedom of Information Act
            4. irish_statute_book_agent — irishstatutebook.ie search
            5. courts_ie_agent — Courts Service forms + judgements

            **JURISDICTION:** Republic of Ireland only.
            **OSINT GATE:** All external sources must be on the
            cianchosaint OSINT allowlist.

            Current date: {datetime.datetime.now().strftime("%Y-%m-%d")}
            """,
            sub_agents=[
                ga_crime_statistics_agent,
                ga_traffic_law_agent,
                ga_foia_requests_agent,
                irish_statute_book_agent,
                courts_ie_agent,
            ],
            output_key="ga_response",
        )


ga_root_agent = GARootAgent().root_agent


__all__ = ["GARootAgent", "ga_root_agent"]
