# CIANCHOSAINT — PSNI press releases specialist (psni.police.uk).
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
PSNI Press Releases Specialist.

Searches psni.police.uk for PSNI press releases — appeals, court
results, operations updates.
"""

from google.adk.agents import LlmAgent

from .._base import CianchosaintAgentBase, DEFAULT_MODEL


class PSNIPressReleasesAgent(CianchosaintAgentBase):
    """psni.police.uk press releases specialist."""

    def __init__(self, provider_router=None) -> None:
        super().__init__(provider_router=provider_router)

        self.agent = LlmAgent(
            name="psni_press_releases_agent",
            model=self.get_active_model() or DEFAULT_MODEL,
            description=(
                "Searches psni.police.uk press releases. Use for: "
                "'Recent PSNI court results', 'PSNI appeal for "
                "witnesses'."
            ),
            instruction="""
            You are the PSNI Press Releases Specialist. You
            consult psni.police.uk/news — the official press
            release feed for the Police Service of Northern
            Ireland.

            **YOUR ROLE:**
            1. Find the requested press release
            2. Quote the headline + date + the published summary
            3. Link to the canonical psni.police.uk URL
            4. Note that PSNI press releases are signed off by
               the PSNI Press Office
            """,
            tools=[],
            output_key="psni_press",
        )


psni_press_releases_agent = PSNIPressReleasesAgent().agent


__all__ = ["PSNIPressReleasesAgent", "psni_press_releases_agent"]
