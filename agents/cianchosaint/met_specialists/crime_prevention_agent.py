# CIANCHOSAINT — MET crime prevention specialist (NPCC advice).
#
# Per `cianchosaint-per-constituency-agents-v1` + the
# `cianchosaint-agent-factory-v1` refactor.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""MET Crime Prevention Specialist.

Provides crime prevention advice published by the National Police
Chiefs' Council (NPCC) — covering burglary, vehicle crime, cyber
crime, fraud, and personal safety.
"""

from .._factory import AGENT_FACTORY_REGISTRY, make_cianchosaint_agent

_wiring = AGENT_FACTORY_REGISTRY["met_crime_prevention_agent"]

met_crime_prevention_agent = make_cianchosaint_agent(
    name=_wiring.name,
    description=_wiring.description,
    instruction=_wiring.instruction,
)


__all__ = ["met_crime_prevention_agent"]
