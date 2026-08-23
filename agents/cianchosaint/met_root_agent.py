# CIANCHOSAINT — Metropolitan Police + 43 UK forces root agent.
#
# NEW-BUILD code (not wholesale-copied). Authored per the
# `cianchosaint-per-constituency-agents-v1` change.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
MET Root Agent — Metropolitan Police + 43 UK forces.

Orchestrates 5 specialist agents:
- crime_statistics_agent (data.police.uk crime stats)
- stop_and_search_agent (data.police.uk stop & search)
- met_press_releases_agent (met.police.uk press releases)
- met_public_contact_agent (MET non-emergency form filler)
- crime_prevention_agent (NPCC crime prevention advice)
"""

import datetime

from google.adk.agents import LlmAgent

from ._base import CianchosaintAgentBase, DEFAULT_MODEL
from .met_specialists.crime_prevention_agent import met_crime_prevention_agent
from .met_specialists.crime_statistics_agent import met_crime_statistics_agent
from .met_specialists.met_press_releases_agent import met_press_releases_agent
from .met_specialists.met_public_contact_agent import met_public_contact_agent
from .met_specialists.stop_and_search_agent import met_stop_and_search_agent


class METRootAgent(CianchosaintAgentBase):
    """Metropolitan Police + 43 UK forces root agent."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)

        self.root_agent = LlmAgent(
            name="met_root_agent",
            model=self.get_active_model() or DEFAULT_MODEL,
            description=(
                "MET Root — Metropolitan Police Service + 43 UK "
                "territorial forces. Routes queries to crime stats, "
                "stop & search, press releases, public contact, and "
                "crime prevention specialists."
            ),
            instruction=f"""
            You are the MET Root Agent for the Metropolitan Police
            Service and the 43 UK territorial forces (England + Wales).

            **YOUR ROLE:**
            Route queries to the appropriate MET specialist and
            synthesize responses. Always cite the specific force
            (e.g. "Metropolitan Police", "West Midlands Police")
            when answering force-specific questions.

            **SPECIALIST AGENTS:**
            1. crime_statistics_agent — data.police.uk crime data
            2. stop_and_search_agent — data.police.uk stop & search
            3. met_press_releases_agent — met.police.uk press releases
            4. met_public_contact_agent — MET non-emergency form filler
            5. crime_prevention_agent — NPCC crime prevention advice

            **JURISDICTION:** England + Wales (43 forces).
            **OSINT GATE:** All external sources must be on the
            cianchosaint OSINT allowlist.

            Current date: {datetime.datetime.now().strftime("%Y-%m-%d")}
            """,
            sub_agents=[
                met_crime_statistics_agent,
                met_stop_and_search_agent,
                met_press_releases_agent,
                met_public_contact_agent,
                met_crime_prevention_agent,
            ],
            output_key="met_response",
        )


met_root_agent = METRootAgent().root_agent


__all__ = ["METRootAgent", "met_root_agent"]
