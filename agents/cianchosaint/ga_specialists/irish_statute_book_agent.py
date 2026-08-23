# CIANCHOSAINT — Irish Statute Book specialist (irishstatutebook.ie).
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
Irish Statute Book Specialist.

Searches irishstatutebook.ie — the official publisher of ROI
statutes, statutory instruments, and Acts of the Oireachtas.
"""

from google.adk.agents import LlmAgent

from .._base import CianchosaintAgentBase, DEFAULT_MODEL
from ..tools.statute_lookup import statute_lookup


class IrishStatuteBookAgent(CianchosaintAgentBase):
    """irishstatutebook.ie search specialist."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)

        self.agent = LlmAgent(
            name="irish_statute_book_agent",
            model=self.get_active_model() or DEFAULT_MODEL,
            description=(
                "Searches irishstatutebook.ie for ROI statutes + "
                "statutory instruments. Use for: 'Find the Criminal "
                "Justice (Theft and Fraud Offences) Act 2001', "
                "'Latest Road Traffic Act amendments'."
            ),
            instruction="""
            You are the Irish Statute Book Specialist. You search
            irishstatutebook.ie — the canonical publisher of ROI
            legislation.

            **YOUR ROLE:**
            1. Find the requested statute or SI
            2. Quote the exact section + subsection
            3. Cite the Act/SI number + year + commencement date
            4. Link to the canonical irishstatutebook.ie URL

            For cross-border statute comparisons (ROI vs UK), use
            the cross_jurisdiction_query tool.

            **JURISDICTION NOTE:** ROI only. For NI legislation,
            defer to the psni_root_agent's ni_justice_agent.
            """,
            tools=[statute_lookup],
            output_key="irish_statute",
        )


irish_statute_book_agent = IrishStatuteBookAgent().agent


__all__ = ["IrishStatuteBookAgent", "irish_statute_book_agent"]
