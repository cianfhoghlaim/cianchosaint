# CIANCHOSAINT — MET stop & search specialist (data.police.uk).
#
# Per `cianchosaint-per-constituency-agents-v1` + the
# `cianchosaint-agent-factory-v1` refactor.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""MET Stop & Search Specialist.

Searches data.police.uk stop & search records — the
ethnicity-disaggregated data published monthly by every UK force
under the Police and Criminal Evidence Act 1984 (PACE) Code A.
"""

from .._factory import AGENT_FACTORY_REGISTRY, make_cianchosaint_agent
from ..tools.force_lookup import force_lookup

_wiring = AGENT_FACTORY_REGISTRY["met_stop_and_search_agent"]

met_stop_and_search_agent = make_cianchosaint_agent(
    name=_wiring.name,
    description=_wiring.description,
    instruction=_wiring.instruction,
    tools=[force_lookup],
)


__all__ = ["met_stop_and_search_agent"]
