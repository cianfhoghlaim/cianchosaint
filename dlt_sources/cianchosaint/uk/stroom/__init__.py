# CIANCHOSAINT new-build: stroom DLT source package marker.

"""cianchosaint.cianchosaint.dlt.british_isles.stroom namespace.

Per the openspec/changes/cianchosaint-hmgcc-gchq-tooling-v1/
specs/cianchosaint-hmgcc-gchq-tooling/spec.md (stroom track).

Wholesale source: hmgcc/stroom/ (Apache 2.0).
Licence: BUSL-1.1 (per LICENSE.md)
"""

from .log_extraction import StroomLogPipeline, stroom_log_source

__all__ = ["StroomLogPipeline", "stroom_log_source"]
