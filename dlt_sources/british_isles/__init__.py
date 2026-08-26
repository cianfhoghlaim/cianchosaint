"""dlt_sources/british_isles — shim for the cianchosaint wholesale-copy.

Per the `2026-09-XX-cianchosaint-initial-carveout-v1` change.

The `dlt_sources/british_isles/` namespace is the legacy wholesale-copy
path from cianfhoghlaim. In cianchosaint the BIEP v3 cross-cutting
content was renamed to `dlt_sources/_cross/` (no `british_isles/`
prefix). This package re-exports under the legacy path so the
wholesale-copy keeps working.
"""
from __future__ import annotations

__all__: list[str] = []