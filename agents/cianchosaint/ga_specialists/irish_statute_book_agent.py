# CIANCHOSAINT — Irish statute book specialist (irishstatutebook.ie).
#
# Per `cianchosaint-per-constituency-agents-v1` + the
# `cianchosaint-agent-factory-v1` refactor.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""Irish Statute Book Specialist.

Searches irishstatutebook.ie for Acts + statutory instruments.
"""

from .._factory import AGENT_FACTORY_REGISTRY, make_cianchosaint_agent
from ..tools.statute_lookup import statute_lookup

_wiring = AGENT_FACTORY_REGISTRY["irish_statute_book_agent"]

irish_statute_book_agent = make_cianchosaint_agent(
    name=_wiring.name,
    description=_wiring.description,
    instruction=_wiring.instruction,
    tools=[statute_lookup],
)


__all__ = ["irish_statute_book_agent"]
