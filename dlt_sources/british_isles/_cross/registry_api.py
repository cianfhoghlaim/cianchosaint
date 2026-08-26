"""dlt_sources/british_isles/_cross/registry_api — shim for the cianchosaint wholesale-copy.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change +
`openspec/plans/2026-08-24-dlt-deep-analysis-v2.md` §Phase 4.1.

The cianchosaint sister repo was wholesale-copied from cianfhoghlaim
on 2026-08-23 (per the `cianchosaint-repo-bootstrap-v2` openspec
change). The wholesale-copy preserved the original cianfhoghlaim
package layout where `dlt_sources/british_isles/_cross/registry_api.py`
is the canonical BIEP v3 cross-cutting registry API.

In cianchosaint the BIEP v3 cross-cutting registry was renamed to
`dlt_sources/_cross/registry_api.py` (no `british_isles/` prefix —
the cianchosaint namespace is defence/policing/intel-oversight,
not BIEP v3 cross-cutting). The legacy import path
`from dlt_sources.british_isles._cross.registry_api import (...)`
therefore breaks at import time.

This shim re-exports the canonical cianchosaint-local API surface so
the wholesale-copy continues to work. After Phase 3 carves the BIEP
v3 cross-cutting back into cianfhoghlaim (deferred to the cross-repo
wire-up change), this shim can be deleted.

## What's re-exported

The 6 symbols that the wholesale-copy `dlt_sources/_cross/__init__.py`
imports: `SubjectRegistryRow`, `query_by_jurisdiction`,
`query_by_concept`, `query_by_stage`,
`query_cross_jurisdiction_bridges`, `insert_subject`.
"""
from __future__ import annotations

from dlt_sources._cross.registry_api import (
    SubjectRegistryRow,
    insert_subject,
    query_by_concept,
    query_by_jurisdiction,
    query_by_stage,
    query_cross_jurisdiction_bridges,
)

__all__ = [
    "SubjectRegistryRow",
    "query_by_jurisdiction",
    "query_by_concept",
    "query_by_stage",
    "query_cross_jurisdiction_bridges",
    "insert_subject",
]