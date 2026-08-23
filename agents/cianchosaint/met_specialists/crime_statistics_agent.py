# CIANCHOSAINT — MET crime statistics specialist (data.police.uk).
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
MET Crime Statistics Specialist.

Searches data.police.uk — the official open-data portal for all
43 UK territorial forces (England + Wales). Provides crime data
at the LSOA (Lower Layer Super Output Area) level.
"""

from google.adk.agents import LlmAgent

from .._base import CianchosaintAgentBase, DEFAULT_MODEL
from ..tools.cross_jurisdiction_query import cross_jurisdiction_query
from ..tools.force_lookup import force_lookup


class METCrimeStatisticsAgent(CianchosaintAgentBase):
    """data.police.uk crime stats specialist."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)

        self.agent = LlmAgent(
            name="met_crime_statistics_agent",
            model=self.get_active_model() or DEFAULT_MODEL,
            description=(
                "Searches data.police.uk for crime statistics across "
                "the 43 UK territorial forces. Use for: 'Burglary "
                "rates in Camden', 'ASB trends in West Midlands'."
            ),
            instruction="""
            You are the MET Crime Statistics Specialist. You consult
            data.police.uk — the official open-data portal for all
            43 UK territorial forces.

            **YOUR ROLE:**
            1. Identify the relevant force via the `force_lookup`
               tool (43 forces available)
            2. Find the crime category (e.g. "burglary", "vehicle
               crime", "violence and sexual offences")
            3. Provide the LSOA-level breakdown where appropriate
            4. Quote the date range and dataset version
            5. Always cite the data.police.uk URL

            **JURISDICTION:** England + Wales only.
            For ROI crime stats, defer to ga_root_agent.
            """,
            tools=[force_lookup, cross_jurisdiction_query],
            output_key="met_crime_stats",
        )


met_crime_statistics_agent = METCrimeStatisticsAgent().agent


__all__ = ["METCrimeStatisticsAgent", "met_crime_statistics_agent"]
