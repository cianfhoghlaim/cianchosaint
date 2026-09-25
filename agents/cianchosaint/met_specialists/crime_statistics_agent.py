# CIANCHOSAINT — MET crime statistics specialist (data.police.uk).
#
# Per `cianchosaint-per-constituency-agents-v1` + the
# `cianchosaint-agent-factory-v1` refactor.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""MET Crime Statistics Specialist.

Searches data.police.uk crime statistics for the 43 UK
territorial forces.
"""

from .._factory import AGENT_FACTORY_REGISTRY, make_cianchosaint_agent
from ..tools.cross_jurisdiction_query import cross_jurisdiction_query

_wiring = AGENT_FACTORY_REGISTRY["met_crime_statistics_agent"]

met_crime_statistics_agent = make_cianchosaint_agent(
    name=_wiring.name,
    description=_wiring.description,
    instruction=_wiring.instruction,
    tools=[cross_jurisdiction_query],
)


__all__ = ["met_crime_statistics_agent"]
