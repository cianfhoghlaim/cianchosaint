# CIANCHOSAINT new-build: per-political-party DLT source module.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-
#   party-pipeline/spec.md, Requirement: The 24 per-party DLT source
#   modules).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Per the cianchosaint-repo-bootstrap-v2 change (Phase 3.1), every
# per-political-party DLT source module lives at
# dlt_sources/cianchosaint/political_parties/<jurisdiction>/<party>.py.
# Source URLs (party websites + Electoral Commission + Companies House)
# are British Isles public-sector OSINT and fall within the
# cianchosaint OSINT allowlist (see
# dlt_sources/official_media_cianchosaint/fixtures/allowlist_parties.yaml).

"""cianchosaint.cianchosaint.dlt.british_isles.political_parties — per-party DLT sources.

Phase 4 of the openspec change. Covers the 24 active political parties
of the British Isles — the canonical input layer for the
reform-uk-pilot-workflow (per Q12 = B) + any future political-
accountability investigations.

The 24 parties are enumerated in
``dlt_sources/official_media_cianchosaint/fixtures/allowlist_parties.yaml``
and tracked in ``_registry.py``. Every party is a subclass of
``PoliticalPartyPipelineBase`` (in ``_base.py``) and ships a
``press_releases`` resource (the BAML-extracted entry point).

Honours ``USE_LOCAL_SCRAPES=true`` falling back to
``stedding/ingest_queue/<jurisdiction>/<party>/``.
"""
from __future__ import annotations

import dlt

import dlt_sources
from dlt_sources.common.site_crawler import crawl_site


def _crawl_source(*args, **kwargs):
    """Compatibility shim — drop the legacy ``source_name=`` kwarg if present.

    The legacy ``_crawl_source`` helper took ``(source_name, base_url, ...)``
    where ``source_name`` was used only for logging. The new
    ``crawl_site`` primitive has no ``source_name`` so we drop it.
    """
    if args and isinstance(args[0], str) and args[0] == kwargs.get("source_name"):
        args = args[1:]
    kwargs.pop("source_name", None)
    for page in crawl_site(*args, **kwargs):
        yield page.to_dict()


__all__ = ["_crawl_source"]