# CIANCHOSAINT — NI Policing Board specialist (oversight reports).
#
# Per `cianchosaint-per-constituency-agents-v1` + the
# `cianchosaint-agent-factory-v1` refactor.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""NI Policing Board Specialist.

Searches nipolicingboard.org.uk — the Northern Ireland Policing
Board's published oversight reports, performance assessments,
and statutory inspections.
"""

from .._factory import AGENT_FACTORY_REGISTRY, make_cianchosaint_agent

_wiring = AGENT_FACTORY_REGISTRY["policing_board_agent"]

policing_board_agent = make_cianchosaint_agent(
    name=_wiring.name,
    description=_wiring.description,
    instruction=_wiring.instruction,
)


__all__ = ["policing_board_agent"]
