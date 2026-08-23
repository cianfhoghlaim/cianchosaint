# CIANCHOSAINT — Police Service of Northern Ireland (PSNI) root agent.
#
# NEW-BUILD code (not wholesale-copied). Authored per the
# `cianchosaint-per-constituency-agents-v1` change.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
PSNI Root Agent — Police Service of Northern Ireland.

Orchestrates 5 specialist agents:
- crime_statistics_agent (PSNI crime statistics)
- psni_press_releases_agent (psni.police.uk press releases)
- psni_public_contact_agent (PSNI non-emergency form filler)
- ni_justice_agent (justice-ni.gov.uk NI legislation)
- policing_board_agent (NI Policing Board oversight reports)
"""

import datetime

from google.adk.agents import LlmAgent

from ._base import CianchosaintAgentBase, DEFAULT_MODEL
from .psni_specialists.crime_statistics_agent import psni_crime_statistics_agent
from .psni_specialists.ni_justice_agent import ni_justice_agent
from .psni_specialists.policing_board_agent import policing_board_agent
from .psni_specialists.psni_press_releases_agent import psni_press_releases_agent
from .psni_specialists.psni_public_contact_agent import psni_public_contact_agent


class PSNIRootAgent(CianchosaintAgentBase):
    """Police Service of Northern Ireland root agent."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)

        self.root_agent = LlmAgent(
            name="psni_root_agent",
            model=self.get_active_model() or DEFAULT_MODEL,
            description=(
                "PSNI Root — Police Service of Northern Ireland. "
                "Routes queries to crime stats, press releases, "
                "public contact, NI justice, and Policing Board "
                "specialists."
            ),
            instruction=f"""
            You are the PSNI Root Agent for the Police Service of
            Northern Ireland.

            **YOUR ROLE:**
            Route queries to the appropriate PSNI specialist and
            synthesize responses. Maintain a factual, public-record
            tone.

            **SPECIALIST AGENTS:**
            1. crime_statistics_agent — PSNI crime statistics
            2. psni_press_releases_agent — psni.police.uk press releases
            3. psni_public_contact_agent — PSNI non-emergency form filler
            4. ni_justice_agent — NI legislation (justice-ni.gov.uk)
            5. policing_board_agent — NI Policing Board oversight

            **JURISDICTION:** Northern Ireland only.
            **CROSS-BORDER NOTE:** For cross-border queries
            (e.g. PSNI ↔ An Garda Síochána), defer to the
            `cross_jurisdiction_query` tool.

            Current date: {datetime.datetime.now().strftime("%Y-%m-%d")}
            """,
            sub_agents=[
                psni_crime_statistics_agent,
                psni_press_releases_agent,
                psni_public_contact_agent,
                ni_justice_agent,
                policing_board_agent,
            ],
            output_key="psni_response",
        )


psni_root_agent = PSNIRootAgent().root_agent


__all__ = ["PSNIRootAgent", "psni_root_agent"]
