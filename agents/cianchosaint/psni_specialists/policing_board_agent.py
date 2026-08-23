# CIANCHOSAINT — NI Policing Board specialist (oversight reports).
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
NI Policing Board Specialist.

Searches nipolicingboard.org.uk — the Northern Ireland Policing
Board's published oversight reports, performance assessments,
and statutory inspections.
"""

from google.adk.agents import LlmAgent

from .._base import CianchosaintAgentBase, DEFAULT_MODEL


class PolicingBoardAgent(CianchosaintAgentBase):
    """NI Policing Board oversight reports specialist."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)

        self.agent = LlmAgent(
            name="policing_board_agent",
            model=self.get_active_model() or DEFAULT_MODEL,
            description=(
                "Searches NI Policing Board oversight reports. Use "
                "for: 'Latest Policing Board performance report', "
                "'PSNI inspection findings'."
            ),
            instruction="""
            You are the NI Policing Board Specialist. You consult
            nipolicingboard.org.uk — the Northern Ireland Policing
            Board's published oversight work.

            **YOUR ROLE:**
            1. Find the requested oversight report
            2. Distinguish between:
               - Policing Board statutory performance assessments
               - Criminal Justice Inspection Northern Ireland (CJINI)
                 reports
               - HMICFRS (His Majesty's Inspectorate of Constabulary)
                 reports on PSNI
               - Police Ombudsman for Northern Ireland reports
            3. Cite the report date + publisher + canonical URL

            **ROLE OF THE BOARD:**
            The NI Policing Board is the statutory oversight body
            for PSNI (under the Police (Northern Ireland) Act 2000).
            Its role is analogous to Police and Crime Commissioners
            in England/Wales, but with cross-party composition.
            """,
            tools=[],
            output_key="policing_board",
        )


policing_board_agent = PolicingBoardAgent().agent


__all__ = ["PolicingBoardAgent", "policing_board_agent"]
