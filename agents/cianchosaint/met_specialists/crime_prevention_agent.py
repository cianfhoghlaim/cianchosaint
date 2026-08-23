# CIANCHOSAINT — MET crime prevention specialist (NPCC advice).
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
MET Crime Prevention Specialist.

Provides crime prevention advice published by the National Police
Chiefs' Council (NPCC) — covering burglary, vehicle crime, cyber
crime, fraud, and personal safety.
"""

from google.adk.agents import LlmAgent

from .._base import CianchosaintAgentBase, DEFAULT_MODEL


class METCrimePreventionAgent(CianchosaintAgentBase):
    """NPCC crime prevention advice specialist."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)

        self.agent = LlmAgent(
            name="met_crime_prevention_agent",
            model=self.get_active_model() or DEFAULT_MODEL,
            description=(
                "Provides NPCC crime prevention advice for England "
                "+ Wales. Use for: 'How do I prevent burglary?', "
                "'Protect my bike from theft', 'Personal safety "
                "advice'."
            ),
            instruction="""
            You are the MET Crime Prevention Specialist. You
            provide crime prevention advice aligned with the
            National Police Chiefs' Council (NPCC) published
            guidance.

            **YOUR ROLE:**
            1. Identify the threat category (burglary, vehicle
               crime, cyber crime, fraud, personal safety)
            2. Provide the standard NPCC mitigation steps
            3. Reference the Secured by Design (SBD) accreditation
               where relevant
            4. Cite the NPCC source URL

            **CATEGORIES COVERED:**
            - Home security (locks, lighting, alarms, CCTV)
            - Vehicle crime (keyless entry, dashcams)
            - Cyber crime (phishing, passwords, 2FA)
            - Fraud (Action Fraud referral)
            - Personal safety (street, online, domestic)
            """,
            tools=[],
            output_key="met_crime_prevention",
        )


met_crime_prevention_agent = METCrimePreventionAgent().agent


__all__ = ["METCrimePreventionAgent", "met_crime_prevention_agent"]
