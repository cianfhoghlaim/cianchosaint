# CIANCHOSAINT — GA traffic law specialist (non-emergency traffic reports).
#
# Per `cianchosaint-per-constituency-agents-v1` + the
# `cianchosaint-agent-factory-v1` refactor.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""GA Traffic Law Specialist.

Drafts non-emergency traffic violation reports (e.g. dangerous
driving observed, illegal parking, road traffic act breaches).
Generates the form contents but does NOT submit — the citizen
reviews + submits manually at garda.ie.
"""

from .._factory import AGENT_FACTORY_REGISTRY, make_cianchosaint_agent
from ..tools.garda_form_fill import garda_form_fill

_wiring = AGENT_FACTORY_REGISTRY["ga_traffic_law_agent"]

ga_traffic_law_agent = make_cianchosaint_agent(
    name=_wiring.name,
    description=_wiring.description,
    instruction=_wiring.instruction,
    tools=[garda_form_fill],
    output_key="ga_traffic_report",
)


__all__ = ["ga_traffic_law_agent"]
