# CIANCHOSAINT — workflows package (canonical 3am-workflow surface).
#
# Per `openspec/changes/cianchosaint-3am-workflow-v1/specs/cianchosaint-3am-workflow/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's `monstertix/agent/concert/`:
# - `nightly.py` → `Workflow` graph with LongRunningFunctionTool nodes
# - `trigger_server.py` → FastAPI trigger server
# - `deploy.sh` → Cloud Run deployment script
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.workflows — canonical 3am-workflow surface.

Re-exports (lazy):
- `politician_resolver_workflow` (the canonical Workflow graph)
- `fastapi_app` (the canonical trigger server)
"""

from __future__ import annotations


def __getattr__(name):
    """Lazy re-export (per cianfhoghlaim's workflow package convention).

    Avoids pulling in `google.adk` (which is not installed in dev) at
    import-time. Modules are loaded on first access.
    """
    if name == "politician_resolver_workflow":
        from .nightly import politician_resolver_workflow as _fn

        return _fn
    if name == "fastapi_app":
        from .trigger_server import fastapi_app as _fn

        return _fn
    raise AttributeError(f"module 'agents.cianchosaint.workflows' has no attribute {name!r}")


__all__ = ["politician_resolver_workflow", "fastapi_app"]
