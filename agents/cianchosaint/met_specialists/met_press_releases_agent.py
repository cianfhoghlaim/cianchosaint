# CIANCHOSAINT — MET press releases specialist (met.police.uk).
#
# Per `cianchosaint-per-constituency-agents-v1` + the
# `cianchosaint-agent-factory-v1` refactor.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""MET Press Releases Specialist.

Searches met.police.uk press releases — appeals, court results,
operations updates.
"""

from .._factory import AGENT_FACTORY_REGISTRY, make_cianchosaint_agent

_wiring = AGENT_FACTORY_REGISTRY["met_press_releases_agent"]

met_press_releases_agent = make_cianchosaint_agent(
    name=_wiring.name,
    description=_wiring.description,
    instruction=_wiring.instruction,
)


__all__ = ["met_press_releases_agent"]
