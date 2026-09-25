# CIANCHOSAINT — NI Justice specialist (justice-ni.gov.uk).
#
# Per `cianchosaint-per-constituency-agents-v1` + the
# `cianchosaint-agent-factory-v1` refactor.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""NI Justice Specialist.

Searches justice-ni.gov.uk for NI legislation.
"""

from .._factory import AGENT_FACTORY_REGISTRY, make_cianchosaint_agent
from ..tools.statute_lookup import statute_lookup

_wiring = AGENT_FACTORY_REGISTRY["ni_justice_agent"]

ni_justice_agent = make_cianchosaint_agent(
    name=_wiring.name,
    description=_wiring.description,
    instruction=_wiring.instruction,
    tools=[statute_lookup],
)


__all__ = ["ni_justice_agent"]
