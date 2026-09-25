# CIANCHOSAINT — MET public contact agent (non-emergency form filler).
#
# Per `cianchosaint-per-constituency-agents-v1` + the
# `cianchosaint-agent-factory-v1` refactor.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""MET Public Contact Specialist.

Drafts non-emergency contact forms for the Metropolitan Police
Service. Generates form contents but does NOT submit — the
citizen reviews + submits manually at met.police.uk.
"""

from .._factory import AGENT_FACTORY_REGISTRY, make_cianchosaint_agent
from ..tools.met_form_fill import met_form_fill

_wiring = AGENT_FACTORY_REGISTRY["met_public_contact_agent"]

met_public_contact_agent = make_cianchosaint_agent(
    name=_wiring.name,
    description=_wiring.description,
    instruction=_wiring.instruction,
    tools=[met_form_fill],
)


__all__ = ["met_public_contact_agent"]
