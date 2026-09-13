# CIANCHOSAINT — WikipediaArchives cohort registry (5 surfaces).
#
# Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
# cianchosaint-dlt-sources-carveout/spec.md, Requirement: The wikipedia_archives/
# cohort registry.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.wikipedia_archives._registry — cohort registry (5 surfaces)."""

from __future__ import annotations

import logging

from ._base import VALID_LANGUAGE_CODES, WikipediaArchivesCohort

logger = logging.getLogger(__name__)


_WIKIPEDIA_ARCHIVES: dict[str, WikipediaArchivesCohort] = {
    # === English Wikipedia ===
    "wikipedia_en": WikipediaArchivesCohort(
        source_id="wikipedia_en",
        source_name="English Wikipedia Politician Archive",
        source_url="https://en.wikipedia.org/wiki/Category:British_politicians",
        language_code="en",
    ),
    # === Irish-language Wikipedia ===
    "wikipedia_ga": WikipediaArchivesCohort(
        source_id="wikipedia_ga",
        source_name="Irish-language (Gaeilge) Wikipedia Politician Archive",
        source_url="https://ga.wikipedia.org/wiki/Catag%C3%B3ir:Polaiti%C3%BAch%C3%AD_na_h%C3%89ireann",
        language_code="ga",
    ),
    # === Welsh-language Wikipedia ===
    "wikipedia_cy": WikipediaArchivesCohort(
        source_id="wikipedia_cy",
        source_name="Welsh-language (Cymraeg) Wikipedia Politician Archive",
        source_url="https://cy.wikipedia.org/wiki/Categori:Gwleidyddion_yr_20fed_ganrif",
        language_code="cy",
    ),
    # === Scottish Gaelic Wikipedia ===
    "wikipedia_gd": WikipediaArchivesCohort(
        source_id="wikipedia_gd",
        source_name="Scottish Gaelic (Gàidhlig) Wikipedia Politician Archive",
        source_url="https://gd.wikipedia.org/wiki/Roinn-se%C3%B2rsa:Poileataichean",
        language_code="gd",
    ),
    # === Wikidata ===
    "wikidata": WikipediaArchivesCohort(
        source_id="wikidata",
        source_name="Wikidata Politician QID Register",
        source_url="https://www.wikidata.org/wiki/Wikidata:WikiProject_Politics",
        language_code="en",
    ),
}


def WIKIPEDIA_ARCHIVES_REGISTRY() -> list[WikipediaArchivesCohort]:
    """Return the list of all registered Wikipedia archive sources."""
    return list(_WIKIPEDIA_ARCHIVES.values())


def list_wikipedia_archives() -> list[WikipediaArchivesCohort]:
    """Return the list of all registered Wikipedia archive sources."""
    return WIKIPEDIA_ARCHIVES_REGISTRY()


def get_wikipedia_archive(source_id: str) -> WikipediaArchivesCohort | None:
    """Return the Wikipedia archive source with the given id, or None."""
    return _WIKIPEDIA_ARCHIVES.get(source_id)


def add_wikipedia_archive(
    cohort: WikipediaArchivesCohort,
    *,
    overwrite: bool = False,
) -> bool:
    """Add a Wikipedia archive source to the registry."""
    if cohort.language_code not in VALID_LANGUAGE_CODES:
        raise ValueError(
            f"wikipedia archive {cohort.source_id!r}: language_code {cohort.language_code!r} is not in VALID_LANGUAGE_CODES"
        )

    if cohort.source_id in _WIKIPEDIA_ARCHIVES and not overwrite:
        logger.info(
            "wikipedia_archive_already_in_registry",
            extra={"source_id": cohort.source_id, "skipped": True},
        )
        return False

    _WIKIPEDIA_ARCHIVES[cohort.source_id] = cohort
    logger.info(
        "wikipedia_archive_added_to_registry",
        extra={"source_id": cohort.source_id, "language_code": cohort.language_code, "overwrite": overwrite},
    )
    return True


__all__ = [
    "WIKIPEDIA_ARCHIVES_REGISTRY",
    "add_wikipedia_archive",
    "get_wikipedia_archive",
    "list_wikipedia_archives",
]


if __name__ == "__main__":
    print(f"Wikipedia archives registry: {len(list_wikipedia_archives())} surfaces")
    for w in sorted(list_wikipedia_archives(), key=lambda x: x.source_id):
        print(f"  {w.source_id}: {w.source_name} [{w.language_code}]")
        print(f"    url: {w.source_url}")
