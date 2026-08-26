"""dlt_sources/british_isles/_cross — shim for the cianchosaint wholesale-copy.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.

Re-exports the cianchosaint-local `_cross/` API surface under the
legacy cianfhoghlaim wholesale-copy namespace so the
`dlt_sources/_cross/__init__.py` import chain (and any other code
that imports via the wholesale-copy namespace) keeps working.
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