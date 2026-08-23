# CIANCHOSAINT — PSNI non-emergency public contact form filler.
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
PSNI Public Contact Specialist.

Drafts non-emergency contact form contents for the Police
Service of Northern Ireland. Generates the form contents but
does NOT submit — the citizen reviews + submits at
psni.police.uk themselves.

For emergencies, ALWAYS direct to 999 (UK).
"""

from google.adk.agents import LlmAgent

from .._base import CianchosaintAgentBase, DEFAULT_MODEL
from ..tools.psni_form_fill import psni_form_fill


class PSNIPublicContactAgent(CianchosaintAgentBase):
    """PSNI non-emergency form filler specialist."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)

        self.agent = LlmAgent(
            name="psni_public_contact_agent",
            model=self.get_active_model() or DEFAULT_MODEL,
            description=(
                "Drafts non-emergency contact form contents for "
                "PSNI. Generates form contents; does NOT submit. "
                "Use for: 'I want to report something non-urgent "
                "to PSNI', 'ASB report for Belfast'."
            ),
            instruction="""
            You are the PSNI Public Contact Specialist. You help
            citizens prepare non-emergency reports to the PSNI.

            **YOUR ROLE:**
            1. Gather the report details (location, time, incident
               type, description)
            2. Categorise against PSNI's report categories
            3. Use the `psni_form_fill` tool to generate the form
               contents
            4. NEVER submit — the citizen reviews and submits at
               psni.police.uk themselves

            **CRITICAL:**
            - For emergencies: ALWAYS direct to 999
            - For non-emergency: the form generated here
            - For terrorism-related: Anti-Terrorist Hotline
              0800 789 321

            **CROSS-BORDER NOTE:** For incidents near the border,
            flag that the incident may be in ROI jurisdiction and
            the citizen should also contact An Garda Síochána.
            """,
            tools=[psni_form_fill],
            output_key="psni_contact",
        )


psni_public_contact_agent = PSNIPublicContactAgent().agent


__all__ = ["PSNIPublicContactAgent", "psni_public_contact_agent"]
