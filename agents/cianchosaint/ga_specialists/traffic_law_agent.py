# CIANCHOSAINT — GA traffic law specialist (non-emergency traffic reports).
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
GA Traffic Law Specialist.

Drafts non-emergency traffic violation reports (e.g. dangerous
driving observed, illegal parking, road traffic act breaches).
Generates the form contents but does NOT submit — the citizen
reviews + submits manually at garda.ie.
"""

from google.adk.agents import LlmAgent

from .._base import CianchosaintAgentBase, DEFAULT_MODEL
from ..tools.garda_form_fill import garda_form_fill


class GATrafficLawAgent(CianchosaintAgentBase):
    """GA non-emergency traffic violation reports specialist."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)

        self.agent = LlmAgent(
            name="ga_traffic_law_agent",
            model=self.get_active_model() or DEFAULT_MODEL,
            description=(
                "Drafts non-emergency traffic violation reports for "
                "An Garda Síochána. Generates form contents; does "
                "NOT submit. Use for: 'I want to report dangerous "
                "driving I witnessed', 'Report illegal parking'."
            ),
            instruction="""
            You are the GA Traffic Law Specialist. You help citizens
            prepare non-emergency traffic violation reports to
            An Garda Síochána.

            **YOUR ROLE:**
            1. Gather the incident details (date, time, location,
               vehicle reg, description)
            2. Validate the report against Road Traffic Act offences
            3. Use the `garda_form_fill` tool to generate the form
               contents
            4. NEVER submit — the citizen reviews and submits at
               garda.ie themselves
            5. Cite the relevant Road Traffic Act section where
               applicable (e.g. "Road Traffic Act 2010, s.12 —
               dangerous driving")

            **CRITICAL:**
            For accidents with injuries or hit-and-run, ALWAYS
            direct the user to call 999 or 112 immediately.
            """,
            tools=[garda_form_fill],
            output_key="ga_traffic_report",
        )


ga_traffic_law_agent = GATrafficLawAgent().agent


__all__ = ["GATrafficLawAgent", "ga_traffic_law_agent"]
