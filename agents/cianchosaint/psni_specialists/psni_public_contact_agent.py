# CIANCHOSAINT — PSNI public contact agent (non-emergency form filler).
#
# Per `cianchosaint-per-constituency-agents-v1` + the
# `cianchosaint-agent-factory-v1` refactor.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""PSNI Public Contact Specialist.

Drafts non-emergency contact forms for the Police Service of
Northern Ireland. Generates form contents but does NOT submit.
"""

from .._factory import AGENT_FACTORY_REGISTRY, make_cianchosaint_agent
from ..tools.psni_form_fill import psni_form_fill

_wiring = AGENT_FACTORY_REGISTRY["psni_public_contact_agent"]

psni_public_contact_agent = make_cianchosaint_agent(
    name=_wiring.name,
    description=_wiring.description,
    instruction=_wiring.instruction,
    tools=[psni_form_fill],
)


__all__ = ["psni_public_contact_agent"]
