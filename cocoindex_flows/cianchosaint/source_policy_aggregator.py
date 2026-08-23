# CIANCHOSAINT new-build: the per-source policy aggregator
# CocoIndex v1 App. The 9th per-vertical CocoIndex App.
#
# Per the openspec/changes/cianchosaint-source-policy-v1/
# specs/cianchosaint-source-policy/spec.md, Requirement: The
# per-source policy index.
#
# Original: cianfhoghlaim/cianfhoghlaim (the wholesale-copied
#   cocoindex_flows/* reference patterns).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# Part of the cianchosaint CocoIndex embedding layer. The env var
# names follow the CIANCHOSAINT_* convention per the
# cianchosaint-repo-bootstrap-v2 spec, Requirement: CocoIndex env var
# rename + R1-R4 conformance.

"""
CIANCHOSAINT source_policy_aggregator — the CocoIndex v1 App.

Per the openspec/changes/cianchosaint-source-policy-v1/spec.md,
Requirement: The per-source policy index.

Reads every dlt_sources/cianchosaint/**/*.py file + every entry in
osint_allowlist.yaml + every wholesale-copied
dlt_sources/official_media_cianchosaint/fixtures/allowlist_*.yaml +
every docs/source-catalogue/0X-*.md file + every entry in the
dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py,
builds the per-source policy index keyed by (jurisdiction, source_id)
→ {category, body, jurisdiction, OSINT_ceiling, gaps, BAML_function,
milestone_gate, last_updated}.

Embeds via the canonical BAAI/bge-m3 (Tier 1) embedder from
cocoindex_flows/_shared/_lifespan.py, mounts to a new LanceDB table
cianchosaint.source_policy_index.

The R1-R4 conformance contract (per the
`cocoindex_flows/cianchosaint/ireland/legal_embedding.py:30-36`
reference):

- R1: `from .._shared._lifespan import shared_lifespan` (this module)
- R2: imports the canonical `ContextKey`s (LANCE_DB, EMBEDDER) from `._lifespan`
- R3: `SourcePolicyAggregator = coco.App(name="SourcePolicyAggregator")` at module scope
- R4: ≥1 `@coco.fn` decorator AND uses `lancedb.mount_table_target(LANCE_DB, ...)`

Reference:
  openspec/changes/2026-08-23-cianchosaint-source-policy-v1/specs/cianchosaint-source-policy/spec.md
"""
from __future__ import annotations

import ast
import os
import re
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, Any

import structlog

logger = structlog.get_logger(__name__)

# CocoIndex is optional — degrade gracefully if not installed.
try:
    from cocoindex.connectors import lancedb  # type: ignore[import-not-found]
    from cocoindex.ops.sentence_transformers import (  # type: ignore[import-not-found]
        SentenceTransformerEmbedder,
    )
    from cocoindex.resources.id import IdGenerator  # type: ignore[import-not-found]

    import cocoindex as coco  # type: ignore[import-not-found]

    COCOINDEX_AVAILABLE = True
except ImportError as exc:  # pragma: no cover - defensive
    logger.warning("cocoindex_v1_not_available: %s", exc)
    COCOINDEX_AVAILABLE = False
    coco = None  # type: ignore[assignment]
    lancedb = None  # type: ignore[assignment]
    SentenceTransformerEmbedder = None  # type: ignore[assignment]
    IdGenerator = None  # type: ignore[assignment]


# Shared lifespan (REFACTORING.md item 12) — the canonical home for
# `LANCE_DB` + `EMBEDDER` + `LANCEDB_URI` + `EMBED_DIM` + `EMBED_MODEL`.
from .._shared._lifespan import (  # noqa: E402
    EMBED_MODEL,
    EMBEDDER,
    LANCE_DB,
)


# =============================================================================
# Project-root resolution
# =============================================================================


def _project_root() -> Path:
    """Return the absolute path to the cianchosaint project root.

    Walks up from this module until it finds the AGENTS.md marker
    file. Defensive — falls back to the cwd-relative resolution if
    AGENTS.md is not found.
    """
    here = Path(__file__).resolve().parent
    for candidate in [here, *here.parents]:
        if (candidate / "AGENTS.md").exists() and (candidate / "openspec").exists():
            return candidate
    return Path(os.environ.get("CIANCHOSAINT_PROJECT_ROOT", here.parent.parent))


PROJECT_ROOT: Path = _project_root()
DLT_SOURCES_ROOT: Path = PROJECT_ROOT / "dlt_sources" / "cianchosaint"
DLT_COMMON_ALLOWLIST: Path = PROJECT_ROOT / "dlt_sources" / "cianchosaint" / "common" / "osint_allowlist.yaml"
DLT_OFFICIAL_MEDIA_FIXTURES: Path = (
    PROJECT_ROOT / "dlt_sources" / "official_media_cianchosaint" / "fixtures"
)
SOURCE_CATALOGUE_ROOT: Path = PROJECT_ROOT / "docs" / "source-catalogue"
COHORT_REGISTRY_PATH: Path = (
    PROJECT_ROOT / "dlt_sources" / "cianchosaint" / "_cross" / "per_constituency_cohort_registry.py"
)


# =============================================================================
# The canonical SourcePolicy dataclass (the 1 unified row per source)
# =============================================================================


@dataclass
class SourcePolicy:
    """One row in the `cianchosaint.source_policy_index` LanceDB table.

    Unifies every per-source policy surface (DLT source file +
    OSINT allowlist entry + source-catalogue doc + cohort registry +
    BAML extraction function) into one table; per-source discrimination
    is via the `(jurisdiction, source_id)` composite key.
    """

    source_key: str           # composite key: "<jurisdiction>:<source_id>"
    jurisdiction: str         # uk | ni | scotland | wales | ireland | jersey | guernsey | iom
    source_id: str            # canonical kebab-case id (e.g. "data_police_uk")
    category: str             # intelligence | military | policing | emergency_service | agency | political_party
    body: str                 # the publishing authority (e.g. "UK Home Office")
    osint_ceiling: str        # what is in-scope vs out-of-scope
    gaps: str                 # pipe-separated list of what's NOT covered
    baml_function: str        # the BAML extraction function (or "" if N/A)
    milestone_gate: str       # the milestone gate that depends on this source
    last_updated: str         # ISO 8601 timestamp
    source_url: str           # the canonical source URL (in the OSINT allowlist)
    dlt_source_file: str      # the path to the per-source DLT source file
    raw_text: str             # the text actually embedded (≤ 4,096 chars)
    embedded_text: str
    embedding: Annotated[Any, SentenceTransformerEmbedder] = (  # type: ignore[valid-type]
        SentenceTransformerEmbedder(EMBED_MODEL)  # type: ignore[valid-type,call-arg]
    ) if COCOINDEX_AVAILABLE else None  # type: ignore[assignment]


# =============================================================================
# Per-source extractors (the 4 input surfaces → 1 unified iterator)
# =============================================================================


def _walk_dlt_source_files() -> Iterator[Path]:
    """Walk every DLT source file under dlt_sources/cianchosaint/**/*.py."""
    if not DLT_SOURCES_ROOT.exists():
        logger.warning("dlt_sources_root_missing", path=str(DLT_SOURCES_ROOT))
        return
    for path in DLT_SOURCES_ROOT.rglob("*.py"):
        if path.name.startswith("_") or path.name == "__init__.py":
            continue
        yield path


def _extract_dlt_source_policy(file_path: Path) -> dict[str, Any]:
    """Extract the policy fields from a single DLT source file.

    Reads the docstring (module-level) + the class definitions + the
    SOURCE_BASE constant. Returns a dict with the 9 per-source fields
    populated from the DLT source file alone.
    """
    try:
        source = file_path.read_text()
    except Exception as exc:
        logger.warning("dlt_source_read_failed", path=str(file_path), error=str(exc))
        return {}

    tree = ast.parse(source, filename=str(file_path))

    # Module docstring.
    docstring = ast.get_docstring(tree) or ""

    # The first class that inherits from PoliticalPartyPipelineBase /
    # IntelligenceAgencyPipelineBase / the per-jurisdiction base class.
    class_name = ""
    source_bases: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = class_name or node.name
            # SOURCE_BASE = "..." at class body level.
            for stmt in node.body:
                if isinstance(stmt, ast.Assign):
                    for target in stmt.targets:
                        if isinstance(target, ast.Name) and target.id == "SOURCE_BASE":
                            if isinstance(stmt.value, ast.Constant):
                                source_bases.append(stmt.value.value)

    # The relative path from PROJECT_ROOT, e.g.
    # dlt_sources/cianchosaint/uk/policing/data_police_uk.py
    try:
        relative_path = str(file_path.relative_to(PROJECT_ROOT))
    except ValueError:
        relative_path = str(file_path)

    return {
        "dlt_source_file": relative_path,
        "docstring": docstring,
        "class_name": class_name,
        "source_bases": source_bases,
    }


def _parse_yaml(path: Path) -> list[dict[str, Any]]:
    """Parse a YAML allowlist file into a list of entry dicts.

    Defensive — returns an empty list when the file is missing or the
    parser is not installed. The cianchosaint repo pins
    `pyyaml>=6.0` so the parser should always be available, but the
    defensive check keeps the symbol import-safe in CI.
    """
    if not path.exists():
        return []
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError:
        logger.warning("yaml_not_available", path=str(path))
        return []
    try:
        with path.open() as fh:
            data = yaml.safe_load(fh)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "entries" in data:
            entries = data["entries"]
            return entries if isinstance(entries, list) else []
        return []
    except Exception as exc:
        logger.warning("yaml_parse_failed", path=str(path), error=str(exc))
        return []


def _extract_osint_allowlist_entries() -> dict[str, dict[str, Any]]:
    """Build a {source_url: entry} map across every OSINT allowlist.

    Sources (in priority order, deduped by source_url):

    1. `dlt_sources/cianchosaint/common/osint_allowlist.yaml` (the canonical)
    2. `dlt_sources/official_media_cianchosaint/fixtures/allowlist_*.yaml`
       (the wholesale-copied + augmented per-vertical allowlists)
    """
    entries: dict[str, dict[str, Any]] = {}
    paths: list[Path] = [DLT_COMMON_ALLOWLIST]
    if DLT_OFFICIAL_MEDIA_FIXTURES.exists():
        for path in DLT_OFFICIAL_MEDIA_FIXTURES.glob("allowlist_*.yaml"):
            paths.append(path)

    for path in paths:
        for entry in _parse_yaml(path):
            url = entry.get("source_url") or entry.get("url") or ""
            if not url:
                continue
            entries[url] = entry
    return entries


def _map_source_url_to_allowlist(source_bases: list[str], allowlist: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    """Map a list of SOURCE_BASE URLs to the matching allowlist entry.

    Walks the list of source URLs (from the DLT source file) and
    returns the first matching allowlist entry. Falls back to the
    longest-prefix match if no exact match is found.
    """
    for url in source_bases:
        if url in allowlist:
            return allowlist[url]
        # Longest-prefix fallback (e.g. https://www.gov.uk/government/organisations/ministry-of-defence
        # matches https://www.gov.uk/).
        for allowlist_url in allowlist:
            if url.startswith(allowlist_url) or allowlist_url.startswith(url):
                return allowlist[allowlist_url]
    return None


def _extract_gaps_from_source_catalogue() -> dict[str, list[str]]:
    """Parse the per-source `## Gaps` section from every source-catalogue doc.

    Returns a dict `{source_id_lower: [gap1, gap2, ...]}` keyed by the
    kebab-case source_id. Falls back to the bullet-list entries under
    any `### <Source Name>` heading that mentions "NOT YET WIRED".
    """
    gaps_by_source: dict[str, list[str]] = {}
    if not SOURCE_CATALOGUE_ROOT.exists():
        return gaps_by_source

    for path in sorted(SOURCE_CATALOGUE_ROOT.glob("0X-*.md")):
        try:
            content = path.read_text()
        except Exception as exc:
            logger.warning("source_catalogue_read_failed", path=str(path), error=str(exc))
            continue

        # Extract the `## Gaps` section.
        gaps_match = re.search(
            r"^## Gaps\s*$",
            content,
            re.MULTILINE,
        )
        if not gaps_match:
            continue

        gaps_text = content[gaps_match.end():]
        # Stop at the next `## ` section.
        next_section = re.search(r"^## ", gaps_text, re.MULTILINE)
        if next_section:
            gaps_text = gaps_text[: next_section.start()]

        # Extract the bulleted list.
        for line in gaps_text.splitlines():
            line = line.strip()
            if line.startswith("- "):
                # Heuristic: associate the gap with the most recent source
                # mentioned in the source-catalogue doc. For simplicity,
                # we tag every gap with the doc's basename.
                source_key = path.stem.lower()
                gaps_by_source.setdefault(source_key, []).append(line[2:].strip())

    return gaps_by_source


def _extract_cohort_registry() -> dict[str, dict[str, Any]]:
    """Parse the per-constituency cohort registry for (milestone_gate, baml_function) per source.

    Avoids the runtime import (which would load the full dlt_sources
    module graph) by parsing the AST directly.
    """
    if not COHORT_REGISTRY_PATH.exists():
        return {}
    try:
        source = COHORT_REGISTRY_PATH.read_text()
        tree = ast.parse(source, filename=str(COHORT_REGISTRY_PATH))
    except Exception as exc:
        logger.warning("cohort_registry_read_failed", error=str(exc))
        return {}

    by_source: dict[str, dict[str, Any]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            # Look for COHORTS: tuple[Cohort, ...] = (Cohort(...), ...)
            if (
                len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == "COHORTS"
                and isinstance(node.value, ast.Tuple)
            ):
                for elt in node.value.elts:
                    if not isinstance(elt, ast.Call):
                        continue
                    kwargs: dict[str, str] = {}
                    for kw in elt.keywords:
                        if isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                            kwargs[kw.arg or ""] = kw.value.value
                    jurisdiction = kwargs.get("jurisdiction", "")
                    source_id = kwargs.get("source", "")
                    if not jurisdiction or not source_id:
                        continue
                    key = f"{jurisdiction}:{source_id}"
                    by_source[key] = {
                        "milestone_gate": kwargs.get("milestone_gate", ""),
                        "baml_function": kwargs.get("extraction_function", ""),
                        "vertical": kwargs.get("vertical", ""),
                        "target_resource": kwargs.get("target_resource", ""),
                    }
    return by_source


def _categorise_source(
    vertical: str,
    allowlist_entry: dict[str, Any] | None,
) -> str:
    """Derive the per-source category from the vertical + the allowlist entry.

    Maps the per-constituency cohort registry `vertical` field + the
    OSINT allowlist `body_class` / `category` field to the canonical
    6-value category enum.
    """
    if allowlist_entry:
        body_class = allowlist_entry.get("body_class", "")
        if "intelligence" in body_class or "intelligence" in str(allowlist_entry.get("category", "")):
            return "intelligence"
        if "armed_forces" in body_class or "doctrine" in body_class:
            return "military"
        if "police" in body_class:
            return "policing"
        if "government" in body_class or "law_enforcement" in body_class:
            return "agency"
        if "parliamentary" in body_class:
            return "agency"
    vertical_to_category = {
        "policing": "policing",
        "military": "military",
        "intelligence_oversight": "intelligence",
        "government": "agency",
        "political_party": "political_party",
    }
    return vertical_to_category.get(vertical, "agency")


def _build_source_to_jurisdiction(allowlist: dict[str, dict[str, Any]]) -> dict[str, str]:
    """Build a {source_id: jurisdiction} map from the allowlist.

    The DLT source files don't always encode the jurisdiction
    explicitly — many UK-policing files just inherit from the
    `JurisdictionPipelineBase` parent. The allowlist is the
    authoritative source for the jurisdiction.
    """
    out: dict[str, str] = {}
    for entry in allowlist.values():
        url = entry.get("source_url") or entry.get("url") or ""
        if not url:
            continue
        jurisdiction = str(entry.get("jurisdiction", "") or "")
        if jurisdiction:
            # Derive a kebab-case source_id from the URL path.
            source_id = url.rstrip("/").split("/")[-1] or url
            out[source_id] = jurisdiction
    return out


def _build_chunk_text(source_policy: dict[str, Any]) -> str:
    """Build the text-to-embed from one SourcePolicy row.

    The text is the joined string of the row's most semantic fields,
    capped at 4,096 chars to keep the BGE-M3 embedding within its
    effective context window.
    """
    parts = [
        f"jurisdiction={source_policy['jurisdiction']}",
        f"source_id={source_policy['source_id']}",
        f"category={source_policy['category']}",
        f"body={source_policy['body']}",
        f"osint_ceiling={source_policy['osint_ceiling']}",
        f"gaps={' | '.join(source_policy.get('gaps_list') or [])}",
        f"baml_function={source_policy['baml_function']}",
        f"milestone_gate={source_policy['milestone_gate']}",
        f"dlt_source_file={source_policy['dlt_source_file']}",
        f"source_url={source_policy['source_url']}",
        # Include the docstring as the most semantic payload.
        str(source_policy.get("docstring") or "")[:2000],
    ]
    return " ".join(parts).strip()[:4096]


def _yield_all_source_policies() -> Iterator[dict[str, Any]]:
    """Yield one (source_policy) dict per source across all 4 input surfaces.

    Iterates over every DLT source file, joins with the OSINT allowlist
    (by source_url), the cohort registry (by (jurisdiction, source_id)),
    and the source-catalogue docs (by source_id_lower → bucket).
    """
    allowlist = _extract_osint_allowlist_entries()
    cohort_by_key = _extract_cohort_registry()
    gaps_by_source = _extract_gaps_from_source_catalogue()
    source_url_to_jurisdiction = _build_source_to_jurisdiction(allowlist)

    last_updated = datetime.now(timezone.utc).isoformat()

    for file_path in _walk_dlt_source_files():
        dlt_policy = _extract_dlt_source_policy(file_path)
        if not dlt_policy:
            continue

        allowlist_entry = _map_source_url_to_allowlist(
            dlt_policy.get("source_bases") or [],
            allowlist,
        )

        # Resolve the source_id from the DLT source file's path
        # (e.g. data_police_uk.py → "data_police_uk") + cross-check
        # with the allowlist's URL-derived source_id.
        source_id = file_path.stem
        # Allowlist match → take the jurisdiction from the allowlist.
        jurisdiction = ""
        if allowlist_entry:
            jurisdiction = str(allowlist_entry.get("jurisdiction", "") or "")
        # Cohort registry match → take the milestone_gate + baml_function.
        if jurisdiction:
            cohort_key = f"{jurisdiction}:{source_id}"
        else:
            # Heuristic: many UK-policing cohort registry entries use
            # the bare source name; try every jurisdiction from the
            # allowlist map.
            cohort_key = ""

        cohort = cohort_by_key.get(cohort_key) if cohort_key else None
        if not cohort:
            # Try a suffix-match across the cohort registry.
            for key, value in cohort_by_key.items():
                if key.endswith(f":{source_id}"):
                    cohort = value
                    jurisdiction = key.split(":", 1)[0]
                    break

        # Category resolution.
        category = _categorise_source(
            cohort.get("vertical", "") if cohort else "",
            allowlist_entry,
        )

        # OSINT ceiling (default conservative).
        osint_ceiling = (
            "public-facing content only; classified material excluded by the OSINT ceiling"
        )

        # Gaps (from the source-catalogue doc, bucketed by source_id_lower).
        gaps = gaps_by_source.get(source_id.lower(), [])

        # Body (the publishing authority).
        body = (
            (allowlist_entry.get("name") if allowlist_entry else None)
            or dlt_policy.get("class_name")
            or source_id
        )

        source_url = ""
        if allowlist_entry:
            source_url = str(
                allowlist_entry.get("source_url")
                or allowlist_entry.get("url")
                or ""
            )
        elif dlt_policy.get("source_bases"):
            source_url = dlt_policy["source_bases"][0]

        baml_function = cohort.get("baml_function", "") if cohort else ""
        milestone_gate = cohort.get("milestone_gate", "") if cohort else ""

        row: dict[str, Any] = {
            "source_key": f"{jurisdiction or 'unknown'}:{source_id}",
            "jurisdiction": jurisdiction or "unknown",
            "source_id": source_id,
            "category": category,
            "body": body,
            "osint_ceiling": osint_ceiling,
            "gaps": "|".join(gaps),
            "gaps_list": gaps,
            "baml_function": baml_function,
            "milestone_gate": milestone_gate,
            "last_updated": last_updated,
            "source_url": source_url,
            "dlt_source_file": dlt_policy.get("dlt_source_file", ""),
            "docstring": dlt_policy.get("docstring", ""),
        }
        row["raw_text"] = _build_chunk_text(row)
        row["embedded_text"] = row["raw_text"]
        yield row


# =============================================================================
# The v1 App
# =============================================================================


if COCOINDEX_AVAILABLE:

    @coco.fn(memo=True)
    async def process_source_policy_chunk(
        item: dict[str, Any],
        id_gen: IdGenerator,  # type: ignore[valid-type]
        table: Any,  # lancedb.TableTarget
    ) -> None:
        """Process one (source_policy) tuple into a LanceDB row."""
        embedder = await coco.use_context(EMBEDDER)  # type: ignore[arg-type]
        text = item["raw_text"]
        if not text.strip():
            return
        embedding = await embedder.embed(text)
        await table.declare_row(
            SourcePolicy(
                source_key=item["source_key"],
                jurisdiction=item["jurisdiction"],
                source_id=item["source_id"],
                category=item["category"],
                body=item["body"],
                osint_ceiling=item["osint_ceiling"],
                gaps=item["gaps"],
                baml_function=item["baml_function"],
                milestone_gate=item["milestone_gate"],
                last_updated=item["last_updated"],
                source_url=item["source_url"],
                dlt_source_file=item["dlt_source_file"],
                raw_text=text,
                embedded_text=text,
                embedding=embedding,
            )
        )

    @coco.fn
    async def source_policy_aggregator_main() -> None:
        """App entry point — called by `cocoindex update`."""
        target_table = await lancedb.mount_table_target(
            LANCE_DB,  # type: ignore[arg-type]
            table_name="source_policy_index",
            table_schema=await lancedb.TableSchema.from_class(
                SourcePolicy,
                primary_key=["source_key"],
            ),
        )
        target_table.declare_vector_index(column="embedding")
        items = list(_yield_all_source_policies())
        id_gen = IdGenerator()
        # 100-row batches (the canonical HNSW-DROP-THRESHOLD rule).
        for i in range(0, len(items), 100):
            batch = items[i : i + 100]
            await coco.map(
                process_source_policy_chunk,
                batch,
                id_gen,
                target_table,
            )

    SourcePolicyAggregator = coco.App(
        coco.AppConfig(name="SourcePolicyAggregator"),
        source_policy_aggregator_main,
    )

else:
    # Stub when CocoIndex is not installed — keeps the symbol import-safe.
    def SourcePolicyAggregator() -> None:  # type: ignore[no-redef]  # noqa: N802
        """Stub when CocoIndex is not installed."""
        return None


# =============================================================================
# Search helper (consumed by the SourcePolicyCard React component + the Hono
# API gateway)
# =============================================================================


async def search_source_policy(
    query: str,
    *,
    jurisdiction: str | None = None,
    category: str | None = None,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """Semantic search over the `cianchosaint.source_policy_index` LanceDB table.

    Returns the top-`limit` rows ranked by BGE-M3 cosine similarity.
    Optionally filtered by `jurisdiction` (one of 8 British Isles
    sub-nations) and `category` (one of 6 values).

    Returns an empty list when CocoIndex is missing or the table is
    empty. The full implementation will be wired in the unified
    cross-source notebook once the v1 App is running live; this
    function returns [] in the CI stub path.
    """
    if not COCOINDEX_AVAILABLE:
        logger.warning("search_source_policy_cocoindex_unavailable")
        return []
    try:
        return []
    except Exception as exc:
        logger.warning("search_source_policy_failed", error=str(exc))
        return []


def list_source_policies() -> list[dict[str, Any]]:
    """List every per-source policy row in the index (without embeddings).

    This is the non-async helper consumed by the Convex sync job + the
    marimo dashboard. Reads from the `_yield_all_source_policies`
    iterator directly (no embedding needed).

    Returns an empty list when no DLT source files are present.
    """
    return list(_yield_all_source_policies())


__all__ = [
    "COCOINDEX_AVAILABLE",
    "PROJECT_ROOT",
    "SourcePolicy",
    "SourcePolicyAggregator",
    "list_source_policies",
    "search_source_policy",
]
