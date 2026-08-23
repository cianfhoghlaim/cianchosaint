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

"""
cianfhoghlaim.cianfhoghlaim.dlt.british_isles.ireland.law.lawreform — Law Reform Commission (Ireland).

Source: `https://www.lawreform.ie` — reports and consultation
papers on Irish statute reform.
"""
from __future__ import annotations
import dlt


from collections.abc import Iterator
from typing import Any

import dlt_sources

from dlt_sources.common.site_crawler import crawl_site

def _crawl_source(*args, **kwargs):
    # The legacy _crawl_source took (source_name, base_url, ...) — source_name
    # was used only for logging in the legacy helper. The new crawl_site
    # primitive has no source_name, so we drop it if present.
    if args and isinstance(args[0], str) and args[0] == kwargs.get("source_name"):
        args = args[1:]
    kwargs.pop("source_name", None)
    for page in crawl_site(*args, **kwargs):
        yield page.to_dict()

LAWREFORM_URLS = {
    "homepage": "https://www.lawreform.ie",
    "reports": "https://www.lawreform.ie/reports-and-publications/",
    "consultation": "https://www.lawreform.ie/consultation-papers/",
}


def _crawl_lawreform(max_pages: int = 30) -> Iterator[dict[str, Any]]:
    for url_key, url in LAWREFORM_URLS.items():
        for page in _crawl_source(
            source_name=f"lawreform.{url_key}",
            base_url=url,
            include_paths=["/reports-and-publications/*", "/consultation-papers/*", "/about-us/*"],
            max_pages=max_pages,
            max_depth=2,
        ):
            page["nation"] = "ie"
            page["domain"] = "law"
            page["entity"] = "lawreform"
            yield page


@dlt.source(name="lawreform")
def lawreform_source(max_pages: int = 30):
    @dlt.resource(
        name="pages",
        write_disposition="merge",
        primary_key=["url"],
    )
    def pages():
        yield from _crawl_lawreform(max_pages=max_pages)

    return pages
