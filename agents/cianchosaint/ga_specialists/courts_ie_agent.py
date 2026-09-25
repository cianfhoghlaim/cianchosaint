# CIANCHOSAINT — courts.ie forms + judgements specialist.
#
# Per `cianchosaint-per-constituency-agents-v1` + the
# `cianchosaint-agent-factory-v1` refactor.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""Courts.ie Specialist.

Searches the Courts Service of Ireland (courts.ie) for forms
(Civil, Family, Criminal, Small Claims) and published judgements
(Court of Appeal, High Court, Supreme Court).
"""

from .._factory import AGENT_FACTORY_REGISTRY, make_cianchosaint_agent
from ..tools.statute_lookup import statute_lookup

_wiring = AGENT_FACTORY_REGISTRY["courts_ie_agent"]

courts_ie_agent = make_cianchosaint_agent(
    name=_wiring.name,
    description=_wiring.description,
    instruction=_wiring.instruction,
    tools=[statute_lookup],
)


__all__ = ["courts_ie_agent"]
