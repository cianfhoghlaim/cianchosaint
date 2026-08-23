# CIANCHOSAINT — MET stop & search specialist (data.police.uk).
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
MET Stop & Search Specialist.

Searches data.police.uk for stop & search records — the
ethnicity-disaggregated data published monthly by every UK force
under the Police and Criminal Evidence Act 1984 (PACE) Code A.
"""

from google.adk.agents import LlmAgent

from .._base import CianchosaintAgentBase, DEFAULT_MODEL
from ..tools.force_lookup import force_lookup


class METStopAndSearchAgent(CianchosaintAgentBase):
    """data.police.uk stop & search specialist."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)

        self.agent = LlmAgent(
            name="met_stop_and_search_agent",
            model=self.get_active_model() or DEFAULT_MODEL,
            description=(
                "Searches data.police.uk for stop & search records "
                "(PACE Code A, monthly force publications). Use for: "
                "'Stop & search rates in the Met', 'Disproportionality "
                "in West Midlands stop & search'."
            ),
            instruction="""
            You are the MET Stop & Search Specialist. You consult
            data.police.uk's stop & search datasets — published
            monthly by every UK territorial force under PACE Code A.

            **YOUR ROLE:**
            1. Identify the force via `force_lookup`
            2. Find stop & search records by date range
            3. Provide the ethnicity-disaggregated breakdown
               (the lawful published disaggregation: White, Black,
               Asian, Mixed, Other)
            4. Cite the data.police.uk URL + the specific dataset
               version

            **CONTEXT:** Disproportionality analysis is a common
            legitimate use case. Quote the published rates with
            their confidence intervals where available.
            """,
            tools=[force_lookup],
            output_key="met_stop_search",
        )


met_stop_and_search_agent = METStopAndSearchAgent().agent


__all__ = ["METStopAndSearchAgent", "met_stop_and_search_agent"]
