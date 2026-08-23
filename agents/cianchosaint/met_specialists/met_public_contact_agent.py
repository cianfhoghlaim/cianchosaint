# CIANCHOSAINT — MET non-emergency public contact form filler.
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
MET Public Contact Specialist.

Drafts non-emergency contact form contents for the Metropolitan
Police Service. Generates the form contents but does NOT submit —
the citizen reviews + submits at met.police.uk themselves.

For emergencies, ALWAYS direct to 999 (UK) or 112 (EU).
"""

from google.adk.agents import LlmAgent

from .._base import CianchosaintAgentBase, DEFAULT_MODEL
from ..tools.met_form_fill import met_form_fill


class METPublicContactAgent(CianchosaintAgentBase):
    """MET non-emergency form filler specialist."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)

        self.agent = LlmAgent(
            name="met_public_contact_agent",
            model=self.get_active_model() or DEFAULT_MODEL,
            description=(
                "Drafts non-emergency contact form contents for the "
                "Metropolitan Police. Generates form contents; does "
                "NOT submit. Use for: 'I want to report something "
                "non-urgent to the Met', 'Anti-social behaviour "
                "report form'."
            ),
            instruction="""
            You are the MET Public Contact Specialist. You help
            citizens prepare non-emergency reports to the
            Metropolitan Police Service.

            **YOUR ROLE:**
            1. Gather the report details (location, time, incident
               type, description)
            2. Categorise against Met's report categories (ASB,
               crime, road incident, lost/found, etc.)
            3. Use the `met_form_fill` tool to generate the form
               contents
            4. NEVER submit — the citizen reviews and submits at
               met.police.uk themselves

            **CRITICAL:**
            - For emergencies: ALWAYS direct to 999 or 112
            - For crimes in progress: 999
            - For hearing/speech impaired: 18000 (textphone)
            - For non-urgent: the form generated here
            """,
            tools=[met_form_fill],
            output_key="met_contact",
        )


met_public_contact_agent = METPublicContactAgent().agent


__all__ = ["METPublicContactAgent", "met_public_contact_agent"]
