# CIANCHOSAINT — MET press releases specialist (met.police.uk).
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
MET Press Releases Specialist.

Searches met.police.uk for Metropolitan Police Service press
releases — appeals, court results, operations updates.
"""

from google.adk.agents import LlmAgent

from .._base import CianchosaintAgentBase, DEFAULT_MODEL


class METPressReleasesAgent(CianchosaintAgentBase):
    """met.police.uk press releases specialist."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)

        self.agent = LlmAgent(
            name="met_press_releases_agent",
            model=self.get_active_model() or DEFAULT_MODEL,
            description=(
                "Searches met.police.uk press releases for the "
                "Metropolitan Police Service. Use for: 'Recent "
                "court results in the Met', 'Operation X press "
                "release'."
            ),
            instruction="""
            You are the MET Press Releases Specialist. You consult
            met.police.uk/news — the official press release feed
            for the Metropolitan Police Service.

            **YOUR ROLE:**
            1. Find the requested press release
            2. Quote the headline + date + the published summary
            3. Link to the canonical met.police.uk URL
            4. Note if the release has been updated (Met occasionally
               issues corrections)

            **SCOPE:** MPS only. For other UK forces, use the
            force_lookup tool to find the force's own press feed.
            """,
            tools=[],
            output_key="met_press",
        )


met_press_releases_agent = METPressReleasesAgent().agent


__all__ = ["METPressReleasesAgent", "met_press_releases_agent"]
