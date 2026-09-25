# CIANCHOSAINT — GA crime statistics specialist (CSO Ireland).
#
# Per `cianchosaint-per-constituency-agents-v1` + the
# `cianchosaint-agent-factory-v1` refactor.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""GA Crime Statistics Specialist.

Searches CSO Ireland crime & justice statistics (the Central
Statistics Office publishes quarterly crime statistics under
statistical release "Recorded Crime").
"""

from .._factory import AGENT_FACTORY_REGISTRY, make_cianchosaint_agent
from ..tools.cross_jurisdiction_query import cross_jurisdiction_query

_wiring = AGENT_FACTORY_REGISTRY["ga_crime_statistics_agent"]

ga_crime_statistics_agent = make_cianchosaint_agent(
    name=_wiring.name,
    description=_wiring.description,
    instruction=_wiring.instruction,
    tools=[cross_jurisdiction_query],
)


__all__ = ["ga_crime_statistics_agent"]
