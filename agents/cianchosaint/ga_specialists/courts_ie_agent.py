# CIANCHOSAINT — courts.ie forms + judgements specialist.
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
Courts.ie Specialist.

Searches the Courts Service of Ireland (courts.ie) for forms
(Civil, Family, Criminal, Small Claims) and published judgements
(Court of Appeal, High Court, Supreme Court).
"""

from google.adk.agents import LlmAgent

from .._base import CianchosaintAgentBase, DEFAULT_MODEL
from ..tools.statute_lookup import statute_lookup


class CourtsIeAgent(CianchosaintAgentBase):
    """courts.ie forms + judgements specialist."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)

        self.agent = LlmAgent(
            name="courts_ie_agent",
            model=self.get_active_model() or DEFAULT_MODEL,
            description=(
                "Searches courts.ie for forms + published judgements. "
                "Use for: 'Find the small claims form', "
                "'Recent Court of Appeal criminal law judgements'."
            ),
            instruction="""
            You are the Courts.ie Specialist. You consult the Courts
            Service of Ireland's public-facing site (courts.ie).

            **YOUR ROLE:**
            1. Find the requested form (Family Law, Civil, Criminal,
               Small Claims, etc.)
            2. Find published judgements (Supreme Court, Court of
               Appeal, High Court, Circuit Court)
            3. Quote the neutral citation (e.g. "[2024] IESC 12")
            4. Link to the canonical courts.ie URL
            5. Use the `statute_lookup` tool to cross-reference any
               statutes cited in the judgement

            **NEVER provide legal advice.** You summarise public
            court records only.
            """,
            tools=[statute_lookup],
            output_key="courts_ie",
        )


courts_ie_agent = CourtsIeAgent().agent


__all__ = ["CourtsIeAgent", "courts_ie_agent"]
