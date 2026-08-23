# CIANCHOSAINT — GA crime statistics specialist (CSO Ireland).
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
GA Crime Statistics Specialist.

Searches CSO Ireland crime & justice statistics (the Central
Statistics Office publishes quarterly crime statistics under
statistical release "Recorded Crime").
"""

from google.adk.agents import LlmAgent

from .._base import CianchosaintAgentBase, DEFAULT_MODEL
from ..tools.cross_jurisdiction_query import cross_jurisdiction_query


class GACrimeStatisticsAgent(CianchosaintAgentBase):
    """CSO Ireland crime & justice statistics specialist."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)

        self.agent = LlmAgent(
            name="ga_crime_statistics_agent",
            model=self.get_active_model() or DEFAULT_MODEL,
            description=(
                "Searches CSO Ireland crime & justice statistics. "
                "Use for: 'What are the latest robbery statistics in Dublin?', "
                "'Burglary trends in Ireland over the last 5 years'."
            ),
            instruction="""
            You are the GA Crime Statistics Specialist. You consult
            CSO Ireland's Recorded Crime statistics (published
            quarterly under the CJQ series).

            **YOUR DATA SOURCES:**
            - cso.ie (CSO Recorded Crime releases)
            - justice.ie (Department of Justice annual reports)

            **YOUR ROLE:**
            1. Find the relevant CSO statistical release
            2. Quote the headline figures with year + quarter
            3. Provide context (trend, regional breakdown if asked)
            4. Always cite the source URL

            Use the cross_jurisdiction_query tool when comparing
            with PSNI or MET statistics.
            """,
            tools=[cross_jurisdiction_query],
            output_key="ga_crime_stats",
        )


ga_crime_statistics_agent = GACrimeStatisticsAgent().agent


__all__ = ["GACrimeStatisticsAgent", "ga_crime_statistics_agent"]
