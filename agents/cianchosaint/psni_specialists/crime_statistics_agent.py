# CIANCHOSAINT — PSNI crime statistics specialist.
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
PSNI Crime Statistics Specialist.

Searches the Police Service of Northern Ireland's published
crime statistics — annual trends recorded by the PSNI under
the Police (Northern Ireland) Act 2000.
"""

from google.adk.agents import LlmAgent

from .._base import CianchosaintAgentBase, DEFAULT_MODEL
from ..tools.cross_jurisdiction_query import cross_jurisdiction_query


class PSNICrimeStatisticsAgent(CianchosaintAgentBase):
    """PSNI crime statistics specialist."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)

        self.agent = LlmAgent(
            name="psni_crime_statistics_agent",
            model=self.get_active_model() or DEFAULT_MODEL,
            description=(
                "Searches PSNI crime statistics for Northern Ireland. "
                "Use for: 'Crime trends in Belfast', 'Recent PSNI "
                "annual crime report'."
            ),
            instruction="""
            You are the PSNI Crime Statistics Specialist. You
            consult the Police Service of Northern Ireland's
            published crime statistics.

            **YOUR ROLE:**
            1. Find the requested PSNI statistical release
            2. Quote the headline figures with year + quarter
            3. Distinguish recorded crime (PSNI figures) from
               the broader NI Justice statistics (DoJ)
            4. Always cite the psni.police.uk URL

            For cross-border comparisons (NI vs ROI), use the
            cross_jurisdiction_query tool.

            **JURISDICTION:** Northern Ireland only.
            """,
            tools=[cross_jurisdiction_query],
            output_key="psni_crime_stats",
        )


psni_crime_statistics_agent = PSNICrimeStatisticsAgent().agent


__all__ = ["PSNICrimeStatisticsAgent", "psni_crime_statistics_agent"]
