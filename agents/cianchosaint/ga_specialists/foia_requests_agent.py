# CIANCHOSAINT — GA FOI requests specialist (ROI FOI Act 2014).
#
# Per `cianchosaint-per-constituency-agents-v1` + the
# `cianchosaint-agent-factory-v1` refactor.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""GA FOIA Requests Specialist.

Drafts Freedom of Information Act 2014 requests to An Garda
Síochána and other ROI public bodies.
"""

from .._factory import AGENT_FACTORY_REGISTRY, make_cianchosaint_agent
from ..tools.foia_request import foia_request

_wiring = AGENT_FACTORY_REGISTRY["ga_foia_requests_agent"]

ga_foia_requests_agent = make_cianchosaint_agent(
    name=_wiring.name,
    description=_wiring.description,
    instruction=_wiring.instruction,
    tools=[foia_request],
)


__all__ = ["ga_foia_requests_agent"]
