# CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# This file is part of the cianchosaint DLT Irish law source family.
# It is a wholesale-copy of the corresponding Cianfhoghlaim file at
# dlt_sources/cianchosaint/ireland/law/<X>.py, with the destination
# path renamed to dlt_sources/cianchosaint/ireland/law/<X>.py.
#
# Source URLs (e.g. irishstatutebook.ie/eli/<year>/act/<number>/enacted/en/xml)
# are verbatim from the Cianfhoghlaim version. The Irish Statute
# Book / Courts.ie / Department of Justice / Citizens Information /
# Law Reform Commission / Workplace Relations / Injuries Board / GOV.IE
# legal content is public-sector OSINT and falls within the cianchosaint
# OSINT allowlist (per the cianchosaint-repo-foundation-v1 openspec
# change, Requirement: OSINT source URL allowlist).
#
# The wholesale-copy preserves the original implementation including
# the @dlt.source + @dlt.resource decorators + the SOURCE_BASE URLs +
# the content-hash + metadata extraction patterns.

"""cianfhoghlaim.cianfhoghlaim.dlt.british_isles.ireland.law — Ireland legal DLT sources.

Phase 6 of the openspec change. Covers both **statutory** law sources
(`irish_statute_book`, `doj`, `lawreform`) and the **operational** law
sources added in `2026-07-06-ireland-legal-pipeline` (`injuries_ie`,
`courts_ie`, `workplace_relations`, `citizensinformation`,
`gov_ie_law`).
"""
from __future__ import annotations

from dlt_sources.cianchosaint.ireland.law import (
    citizensinformation,
    courts_ie,
    doj,
    gov_ie_law,
    injuries_ie,
    irish_statute_book,
    lawreform,
    workplace_relations,
)

__all__ = [
    "citizensinformation",
    "courts_ie",
    "doj",
    "gov_ie_law",
    "injuries_ie",
    "irish_statute_book",
    "lawreform",
    "workplace_relations",
]
