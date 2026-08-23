# CIANCHOSAINT — GA FOI requests specialist (ROI FOI Act 2014).
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
GA FOIA Requests Specialist.

Drafts Freedom of Information Act 2014 requests to An Garda
Síochána and other ROI public bodies.
"""

from google.adk.agents import LlmAgent

from .._base import CianchosaintAgentBase, DEFAULT_MODEL
from ..tools.foia_request import foia_request


class GAFOIARequestsAgent(CianchosaintAgentBase):
    """ROI FOI Act 2014 requests specialist."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)

        self.agent = LlmAgent(
            name="ga_foia_requests_agent",
            model=self.get_active_model() or DEFAULT_MODEL,
            description=(
                "Drafts ROI Freedom of Information Act 2014 requests "
                "to An Garda Síochána + other ROI public bodies. "
                "Use for: 'How do I request crime stats from Garda?', "
                "'File an FOI request to the Department of Justice'."
            ),
            instruction="""
            You are the GA FOIA Requests Specialist. You draft
            Freedom of Information Act 2014 requests for ROI public
            bodies.

            **YOUR ROLE:**
            1. Help the user scope their FOI request (be specific —
               FOI requests are more likely to succeed when narrow)
            2. Identify the correct public body (An Garda Síochána,
               Department of Justice, etc.)
            3. Use the `foia_request` tool to draft the request
               letter
            4. Cite the FOI Act 2014 fees + exemptions framework
               (s.15 — fees, s.32 — law enforcement exemptions)
            5. NEVER submit — the citizen reviews and sends the
               letter themselves

            **STANDARD FEES:** EUR 15 (non-personal), EUR 0
            (personal records).

            **RESPONSE DEADLINE:** 20 working days (s.13).
            """,
            tools=[foia_request],
            output_key="ga_foia_request",
        )


ga_foia_requests_agent = GAFOIARequestsAgent().agent


__all__ = ["GAFOIARequestsAgent", "ga_foia_requests_agent"]
