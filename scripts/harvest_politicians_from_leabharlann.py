#!/usr/bin/env python3
"""CIANCHOSAINT — harvest politicians + adjacent context from leabharlann politics PDFs.

Per the openspec/changes/cianchosaint-politician-schema-v1/specs/
cianchosaint-baml-schemas/spec.md, Requirement: The bulk-harvest
script that runs across all 87 leabharlann politics PDFs + the 1 .md file
in `leabharlann/gemini_deep_research/politics/`.

The script invokes the 4 BAML extraction functions:

  - ExtractPoliticianFromPDF        — bulk harvest of every politician named
                                     in each PDF (Axis A)
  - ExtractAdjacentContextFromPDF   — bulk harvest of the 4 adjacent axes
                                     (advisors / funders / historical
                                     associations / wikipedia references)
                                     for the primary subject of each PDF

Outputs
-------

The script writes 5 output files to the path specified by --output-dir
(default: /tmp/cianchosaint_politician_harvest_<date>/):

  1. politicians.json              — the full list of Politician records
  2. adjacent_context.json         — the AdjacentContext records per PDF
  3. politician_frequency.md       — the politician → frequency table
  4. advisor_frequency.md          — the advisor → frequency table
  5. funder_frequency.md           — the funder → frequency table
  6. historical_association_frequency.md
  7. wikidata_qid_map.json         — politician → QID reconciliation map
  8. harvest_summary.md            — the human-readable summary

Usage
-----

    python3 scripts/harvest_politicians_from_leabharlann.py
    python3 scripts/harvest_politicians_from_leabharlann.py --dry-run
    python3 scripts/harvest_politicians_from_leabharlann.py \\
        --leabharlann-root /path/to/leabharlann \\
        --output-dir /tmp/my_harvest

Licence: BUSL-1.1 (per LICENSE.md)
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
UTC = timezone.utc
from pathlib import Path

logger = logging.getLogger(__name__)


# The default leabharlann politics root.
DEFAULT_LEABHARLANN_ROOT = os.environ.get(
    "CIANCHOSAINT_LEABHARLANN_ROOT",
    str(Path("~/dev/cianfhoghlaim/leabharlann/gemini_deep_research/politics").expanduser()),
)


def _setup_logging(verbose: bool) -> None:
    """Configure the root logger."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def _enumerate_pdfs(root: Path) -> list[Path]:
    """Enumerate all .pdf + .md files under the leabharlann politics root."""
    if not root.exists():
        logger.error("leabharlann_root_does_not_exist", extra={"root": str(root)})
        return []
    return sorted(root.glob("**/*.pdf")) + sorted(root.glob("**/*.md"))


def _extract_politicians_from_text(text: str, *, pdf_path: Path) -> list[dict[str, object]]:
    """Extract politicians from a single PDF's text.

    This is a conservative regex-based fallback for when the BAML function
    is not available (e.g. in CI without the baml_client generated code).
    The full BAML-driven path is invoked when baml_client is importable.
    """
    try:
        from baml_client.b import ExtractPoliticianFromPDF  # type: ignore
    except ImportError:
        logger.warning("baml_client_not_available_falling_back_to_regex")
        return _regex_politician_extract(text, pdf_path=pdf_path)

    try:
        return [p.model_dump() for p in ExtractPoliticianFromPDF(input=text)]
    except Exception as exc:
        logger.warning("baml_extract_failed_falling_back_to_regex", error=str(exc))
        return _regex_politician_extract(text, pdf_path=pdf_path)


def _extract_adjacent_context_from_text(text: str, *, pdf_path: Path) -> dict[str, object]:
    """Extract adjacent context (Axes B-E) from a single PDF's text."""
    try:
        from baml_client.b import ExtractAdjacentContextFromPDF  # type: ignore
    except ImportError:
        logger.warning("baml_client_not_available_falling_back_to_empty_adjacent_context")
        return _empty_adjacent_context(pdf_path=pdf_path)

    try:
        result = ExtractAdjacentContextFromPDF(input=text)
        return result.model_dump()
    except Exception as exc:
        logger.warning("baml_adjacent_extract_failed", error=str(exc))
        return _empty_adjacent_context(pdf_path=pdf_path)


def _regex_politician_extract(text: str, *, pdf_path: Path) -> list[dict[str, object]]:
    """Conservative regex-based politician name extraction (BAML fallback).

    Looks for the patterns:
    - "<Title> <Name>" where Title is in a curated set of honorifics
    - Returns a minimal Politician record (name only) for the BFS
    """
    # A small but well-known set of case-study + leabharlann-frequently
    # mentioned names. The BAML extraction is the canonical path; this
    # regex fallback is for environments where the baml_client is not
    # available.
    name_pattern = re.compile(
        r"\b(Nigel Farage|Zack Polanski|John O'?Dowd|Gordon Lyons|Paul Givan|"
        r"Gavin Robinson|Lara Bird|Richard Tice|Arlene Foster|Mary Lou McDonald|"
        r"Simon Harris|Paschal Donohoe|Keir Starmer|Rishi Sunak|Ed Davey|"
        r"Carla Denyer|Adrian Ramsay|Nicola Sturgeon|Humza Yousaf|John Swinney|"
        r"Michelle O'Neill|Jeffrey Donaldson|Sammy Wilson|Ian Paisley Jr|"
        r"Colum Eastwood|Clare Bailey|Gerry Carroll|Matthew O'Toole|"
        r"Naomi Long|Doug Beattie|Mike Nesbitt|Jim Allister|Gavin Robinson)\b"
    )

    found_names = sorted(set(name_pattern.findall(text)))
    out: list[dict[str, object]] = []
    for name in found_names:
        out.append(
            {
                "canonical_name": name,
                "extraction_source": "leabharlann_pdf",
                "source_urls": [str(pdf_path)],
                "extraction_confidence": 0.4,  # regex fallback is lower-confidence
                "osint_ceiling_enforced": True,
                "analyst_review_required": True,
            }
        )
    return out


def _empty_adjacent_context(*, pdf_path: Path) -> dict[str, object]:
    """Return an empty AdjacentContext record (BAML fallback)."""
    return {
        "subject": None,
        "advisors": [],
        "funders": [],
        "historical_associations": [],
        "wikipedia_archives": None,
        "extracted_at": datetime.now(UTC).isoformat(),
        "source_urls": [str(pdf_path)],
    }


def _read_pdf_text(pdf_path: Path) -> str:
    """Read the text content of a PDF or markdown file.

    For .md files we read the file directly. For .pdf files we attempt
    to use pdfplumber; if not available we read the raw bytes and decode
    them (best-effort). The output is a single string.
    """
    if pdf_path.suffix.lower() == ".md":
        try:
            return pdf_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return pdf_path.read_text(encoding="latin-1", errors="replace")

    # PDF: try pdfplumber first
    try:
        import pdfplumber  # type: ignore
    except ImportError:
        return _pdf_fallback_text(pdf_path)

    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            return "\n".join((page.extract_text() or "") for page in pdf.pages)
    except Exception as exc:
        logger.warning("pdfplumber_failed_falling_back_to_bytes", error=str(exc))
        return _pdf_fallback_text(pdf_path)


def _pdf_fallback_text(pdf_path: Path) -> str:
    """Fallback: read the raw PDF bytes (text extraction may not work for
    scanned PDFs)."""
    try:
        return pdf_path.read_bytes().decode("utf-8", errors="replace")
    except Exception:
        return ""


def _build_summary(
    *,
    pdf_paths: list[Path],
    politicians: list[dict[str, object]],
    adjacent_contexts: list[dict[str, object]],
) -> str:
    """Build the human-readable summary markdown."""
    out: list[str] = []
    out.append("# Politician + Adjacent-Context Harvest Summary")
    out.append("")
    out.append(f"- Leabharlann PDFs processed: **{len(pdf_paths)}**")
    out.append(f"- Politicians harvested: **{len(politicians)}**")
    out.append(f"- Adjacent contexts harvested: **{len(adjacent_contexts)}**")
    out.append("")

    # Top-10 politicians by frequency
    out.append("## Top-10 Politicians by Frequency")
    out.append("")
    counter = Counter(p.get("canonical_name", "?") for p in politicians)
    out.append("| Politician | Frequency |")
    out.append("|---|---:|")
    for name, count in counter.most_common(10):
        out.append(f"| {name} | {count} |")
    out.append("")

    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Harvest politicians + adjacent context from leabharlann PDFs.")
    parser.add_argument(
        "--leabharlann-root",
        type=Path,
        default=Path(DEFAULT_LEABHARLANN_ROOT),
        help="Path to the leabharlann/gemini_deep_research/politics/ root.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(f"/tmp/cianchosaint_politician_harvest_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
        help="Path where the harvest outputs are written.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List the PDFs that would be processed without actually running the extraction.",
    )
    parser.add_argument(
        "--max-pdfs",
        type=int,
        default=None,
        help="Maximum number of PDFs to process (useful for smoke tests).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging.",
    )
    args = parser.parse_args(argv)

    _setup_logging(verbose=args.verbose)

    pdf_paths = _enumerate_pdfs(args.leabharlann_root)
    if not pdf_paths:
        logger.error("no_pdfs_found", extra={"root": str(args.leabharlann_root)})
        return 1

    if args.max_pdfs:
        pdf_paths = pdf_paths[: args.max_pdfs]

    logger.info(
        "harvest_started",
        extra={"pdf_count": len(pdf_paths), "root": str(args.leabharlann_root)},
    )

    if args.dry_run:
        logger.info("dry_run_listing_pdfs")
        for i, p in enumerate(pdf_paths[:50]):
            print(f"  [{i+1:3d}] {p}")
        if len(pdf_paths) > 50:
            print(f"  ... and {len(pdf_paths) - 50} more")
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)

    politicians: list[dict[str, object]] = []
    adjacent_contexts: list[dict[str, object]] = []
    failed_pdfs: list[Path] = []

    for i, pdf_path in enumerate(pdf_paths):
        try:
            text = _read_pdf_text(pdf_path)
        except Exception as exc:
            logger.warning("pdf_read_failed", extra={"path": str(pdf_path), "error": str(exc)})
            failed_pdfs.append(pdf_path)
            continue

        # Axis A extraction
        for politician in _extract_politicians_from_text(text, pdf_path=pdf_path):
            politicians.append(politician)

        # Axes B-E extraction
        adjacent = _extract_adjacent_context_from_text(text, pdf_path=pdf_path)
        adjacent_contexts.append(adjacent)

        if (i + 1) % 10 == 0:
            logger.info(
                "harvest_progress",
                extra={"processed": i + 1, "total": len(pdf_paths)},
            )

    # ------------------------------------------------------------------------
    # Write outputs
    # ------------------------------------------------------------------------
    politicians_json = args.output_dir / "politicians.json"
    politicians_json.write_text(
        json.dumps(politicians, indent=2, default=str),
        encoding="utf-8",
    )
    logger.info("wrote_politicians_json", extra={"path": str(politicians_json)})

    adjacent_json = args.output_dir / "adjacent_context.json"
    adjacent_json.write_text(
        json.dumps(adjacent_contexts, indent=2, default=str),
        encoding="utf-8",
    )
    logger.info("wrote_adjacent_context_json", extra={"path": str(adjacent_json)})

    # Politician frequency table
    counter = Counter(p.get("canonical_name", "?") for p in politicians)
    politician_freq_md = args.output_dir / "politician_frequency.md"
    with politician_freq_md.open("w", encoding="utf-8") as fh:
        fh.write("# Politician Frequency\n\n")
        fh.write("| Politician | Frequency |\n|---|---:|\n")
        for name, count in counter.most_common():
            fh.write(f"| {name} | {count} |\n")
    logger.info("wrote_politician_frequency", extra={"path": str(politician_freq_md)})

    # Advisor + Funder + Historical-Association frequency tables
    for axis_name, axis_key in (
        ("advisor_frequency", "advisors"),
        ("funder_frequency", "funders"),
        ("historical_association_frequency", "historical_associations"),
    ):
        all_records: list[str] = []
        for ctx in adjacent_contexts:
            all_records.extend(r.get("canonical_name", "?") for r in ctx.get(axis_key, []) if isinstance(r, dict))
        axis_counter = Counter(all_records)
        axis_md = args.output_dir / f"{axis_name}.md"
        with axis_md.open("w", encoding="utf-8") as fh:
            fh.write(f"# {axis_name.replace('_', ' ').title()}\n\n")
            fh.write("| Name | Frequency |\n|---|---:|\n")
            for name, count in axis_counter.most_common():
                fh.write(f"| {name} | {count} |\n")
        logger.info("wrote_axis_frequency", extra={"axis": axis_name, "path": str(axis_md)})

    # Wikidata QID map (politician → QID)
    qid_map: dict[str, str | None] = {}
    for ctx in adjacent_contexts:
        archives = ctx.get("wikipedia_archives")
        if archives and isinstance(archives, dict):
            subject = archives.get("subject_canonical_name")
            qid = archives.get("wikidata_qid")
            if subject:
                qid_map[subject] = qid
    qid_map_path = args.output_dir / "wikidata_qid_map.json"
    qid_map_path.write_text(
        json.dumps(qid_map, indent=2, default=str),
        encoding="utf-8",
    )
    logger.info("wrote_qid_map", extra={"path": str(qid_map_path)})

    # Summary
    summary = _build_summary(
        pdf_paths=pdf_paths,
        politicians=politicians,
        adjacent_contexts=adjacent_contexts,
    )
    summary_path = args.output_dir / "harvest_summary.md"
    summary_path.write_text(summary, encoding="utf-8")
    logger.info("wrote_summary", extra={"path": str(summary_path)})

    logger.info(
        "harvest_completed",
        extra={
            "pdf_count": len(pdf_paths),
            "politician_count": len(politicians),
            "adjacent_context_count": len(adjacent_contexts),
            "failed_pdf_count": len(failed_pdfs),
        },
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
