# CIANCHOSAINT — PSNI crime statistics specialist.
#
# Per `cianchosaint-per-constituency-agents-v1` + the
# `cianchosaint-agent-factory-v1` refactor.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""PSNI Crime Statistics Specialist.

Searches PSNI crime statistics (the PSNI publishes quarterly).
"""

from .._factory import AGENT_FACTORY_REGISTRY, make_cianchosaint_agent
from ..tools.cross_jurisdiction_query import cross_jurisdiction_query

_wiring = AGENT_FACTORY_REGISTRY["psni_crime_statistics_agent"]

psni_crime_statistics_agent = make_cianchosaint_agent(
    name=_wiring.name,
    description=_wiring.description,
    instruction=_wiring.instruction,
    tools=[cross_jurisdiction_query],
)


__all__ = ["psni_crime_statistics_agent"]
