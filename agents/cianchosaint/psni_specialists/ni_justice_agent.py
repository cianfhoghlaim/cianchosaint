# CIANCHOSAINT — NI justice + legislation specialist (justice-ni.gov.uk).
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
NI Justice Specialist.

Searches justice-ni.gov.uk — the Department of Justice (NI)
publisher of NI primary legislation, statutory rules, and
justice policy.
"""

from google.adk.agents import LlmAgent

from .._base import CianchosaintAgentBase, DEFAULT_MODEL
from ..tools.statute_lookup import statute_lookup


class NIJusticeAgent(CianchosaintAgentBase):
    """justice-ni.gov.uk NI legislation specialist."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)

        self.agent = LlmAgent(
            name="ni_justice_agent",
            model=self.get_active_model() or DEFAULT_MODEL,
            description=(
                "Searches justice-ni.gov.uk for NI primary "
                "legislation + statutory rules. Use for: 'Find "
                "the Criminal Justice (Northern Ireland) Order "
                "2008', 'Latest NI justice policy'."
            ),
            instruction="""
            You are the NI Justice Specialist. You consult
            justice-ni.gov.uk — the Department of Justice
            (Northern Ireland) publisher of NI legislation.

            **YOUR ROLE:**
            1. Find the requested NI statute or statutory rule
            2. Quote the exact article + paragraph
            3. Cite the SI number / Order number + year
            4. Link to the canonical justice-ni.gov.uk URL

            For ROI statute comparisons, use the cross_jurisdiction_query
            tool or defer to ga_root_agent's irish_statute_book_agent.

            **JURISDICTION NOTE:** NI primary legislation is enacted
            via Orders in Council (pre-1972 Acts of the NI Parliament
            + post-1972 Orders in Council). Be explicit about the
            legislative vehicle.
            """,
            tools=[statute_lookup],
            output_key="ni_justice",
        )


ni_justice_agent = NIJusticeAgent().agent


__all__ = ["NIJusticeAgent", "ni_justice_agent"]
