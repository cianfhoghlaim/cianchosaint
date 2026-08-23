"""
CIANCHOSAINT — Static pipeline graph generator.

Per the canonical spec at
``openspec/specs/cianchosaint-pipeline-graph/spec.md``.

Produces docs-embeddable SVG + PNG pipeline graph images from the
hard-coded per-source metadata below. The output is suitable for the
README, the governance docs, and the case-study pages.

Usage::

    # Default: writes to docs/figures/pipeline-graph-{YYYY-MM-DD}.{svg,png}
    python scripts/pipeline_graph_generator.py

    # Custom output dir
    python scripts/pipeline_graph_generator.py --output-dir ./out

Wholesale-copy pattern: cianfhoghlaim/cianfhoghlaim @ main branch
(per the openspec/changes/cianchosaint-repo-bootstrap-v2 change).
Licence: BUSL-1.1 (per LICENSE.md).
"""

from __future__ import annotations

import datetime as _dt
import pathlib as _pl
import sys as _sys

try:
    import click as _click
except ImportError:  # pragma: no cover
    _click = None  # type: ignore[assignment]

try:
    import svgwrite as _svgwrite  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    _svgwrite = None  # type: ignore[assignment]

try:
    import cairosvg as _cairosvg  # type: ignore[import-not-found]
except ImportError:
    _cairosvg = None  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Hard-coded per-source metadata (mirror of the per-source rows in the
# Convex vlmPipelineDashboard table — populated by the sibling change's
# CocoIndex v1 App). Update when a new source goes live.
# ---------------------------------------------------------------------------

STAGES: list[tuple[str, str]] = [
    ("dlt", "DLT source"),
    ("baml", "BAML extraction"),
    ("embedding", "CocoIndex v1 embedding"),
    ("target", "LanceDB / DuckLake target"),
    ("agui", "AG-UI consumer"),
]

PERSONA_HIGHLIGHT: dict[str, str] = {
    "analyst": "#0ea5e9",
    "lawyer": "#a855f7",
    "judge": "#f59e0b",
    "oversight": "#ef4444",
}

# stage_id, label, vlm_model, ocr_confidence, extraction_pass_rate,
# cost_credits, latency_ms
SOURCES: list[tuple[str, str, str, float, float, float, int]] = [
    ("met_police", "Metropolitan Police (data.police.uk)",
     "dots.ocr-1b", 0.94, 0.97, 1.20, 850),
    ("psni", "PSNI + NI Justice",
     "paddleocr-v4", 0.91, 0.95, 0.95, 780),
    ("mod_uk", "UK MoD + RAF + RN + Army",
     "trocr-large-handwritten", 0.89, 0.93, 1.10, 920),
    ("idf_ireland", "Defence Forces of Ireland",
     "pylaia-cer", 0.93, 0.96, 1.05, 810),
    ("irish_legal", "Irish Courts + Statute Book",
     "trocr-base-printed", 0.96, 0.98, 0.70, 640),
    ("isc_ipco", "UK ISC + IPCO + IPT",
     "tesseract-5-llm", 0.92, 0.94, 1.30, 1050),
    ("reform_uk", "Reform UK dossiers",
     "dots.ocr-1b", 0.90, 0.92, 1.50, 1120),
]


# ---------------------------------------------------------------------------
# SVG generation
# ---------------------------------------------------------------------------

STAGE_WIDTH = 160
STAGE_HEIGHT = 60
STAGE_GAP = 20
SVG_WIDTH = 960
SVG_HEIGHT = 360


def stage_x(index: int) -> int:
    return index * (STAGE_WIDTH + STAGE_GAP) + 20


def stage_y() -> int:
    return SVG_HEIGHT // 2 - STAGE_HEIGHT // 2


def generate_pipeline_graph(
    sources: list[tuple[str, str, str, float, float, float, int]] | None = None,
    persona: str = "analyst",
) -> str:
    """Render the pipeline graph as an SVG string."""
    if _svgwrite is None:
        raise RuntimeError(
            "svgwrite is required: pip install svgwrite",
        )

    sources = sources if sources is not None else SOURCES
    highlight = PERSONA_HIGHLIGHT.get(persona, PERSONA_HIGHLIGHT["analyst"])

    drawing = _svgwrite.Drawing(
        size=(f"{SVG_WIDTH}px", f"{SVG_HEIGHT}px"),
        viewBox=f"0 0 {SVG_WIDTH} {SVG_HEIGHT}",
    )

    drawing.add(
        drawing.rect(
            insert=(0, 0),
            size=(SVG_WIDTH, SVG_HEIGHT),
            fill="#0f172a",
        ),
    )

    # Stage nodes
    for i, (_stage_id, label) in enumerate(STAGES):
        x = stage_x(i)
        y = stage_y()
        drawing.add(
            drawing.rect(
                insert=(x, y),
                size=(STAGE_WIDTH, STAGE_HEIGHT),
                rx=8,
                ry=8,
                fill="#1e293b",
                stroke=highlight,
                stroke_width=2,
            ),
        )
        drawing.add(
            drawing.text(
                label,
                insert=(x + STAGE_WIDTH // 2, y + STAGE_HEIGHT // 2 + 4),
                text_anchor="middle",
                fill="#f8fafc",
                font_size=12,
            ),
        )

    # Edge labels (per-stage cost + latency, summed over sources)
    sources_per_stage: dict[str, list[tuple[str, str, str, float, float, float, int]]] = {}
    for s in sources:
        sources_per_stage.setdefault(_stage_for_source(s[0]), []).append(s)

    for i in range(len(STAGES) - 1):
        s_id = STAGES[i][0]
        t_id = STAGES[i + 1][0]
        cost = sum(src[5] for src in sources_per_stage.get(s_id, []))
        latency = int(
            sum(src[6] for src in sources_per_stage.get(s_id, []))
            / max(len(sources_per_stage.get(s_id, [])), 1),
        )
        x = (stage_x(i) + STAGE_WIDTH + stage_x(i + 1)) // 2
        y = stage_y() + STAGE_HEIGHT + 18
        drawing.add(
            drawing.text(
                f"{cost:.1f} cr · {latency}ms",
                insert=(x, y),
                text_anchor="middle",
                fill="#94a3b8",
                font_size=10,
            ),
        )

    # Source nodes (one circle per source, with title tooltip)
    sources_per_stage_list: dict[str, list[tuple[str, str, str, float, float, float, int]]] = {}
    for src in sources:
        sources_per_stage_list.setdefault(_stage_for_source(src[0]), []).append(src)

    for stage_id, stage_sources in sources_per_stage_list.items():
        stage_idx = next(i for i, (sid, _) in enumerate(STAGES) if sid == stage_id)
        for idx, src in enumerate(stage_sources):
            base_x = stage_x(stage_idx) + STAGE_WIDTH // 2
            base_y = stage_y() - 30 - idx * 14
            drawing.add(
                drawing.circle(
                    center=(base_x, base_y),
                    r=5,
                    fill=highlight,
                ),
            )
            tooltip = (
                f"{src[1]}\n"
                f"VLM: {src[2]}\n"
                f"OCR confidence: {src[3] * 100:.1f}%\n"
                f"Pass rate: {src[4] * 100:.1f}%\n"
                f"Cost: {src[5]:.2f} credits\n"
                f"Latency: {src[6]}ms"
            )
            drawing.add(
                drawing.title(tooltip),
            )

    return drawing.tostring()


def _stage_for_source(source_id: str) -> str:
    """Map a source id to the pipeline stage it sits at."""
    mapping = {
        "met_police": "dlt",
        "psni": "dlt",
        "mod_uk": "dlt",
        "idf_ireland": "dlt",
        "irish_legal": "dlt",
        "isc_ipco": "dlt",
        "reform_uk": "dlt",
    }
    return mapping.get(source_id, "dlt")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def _run(output_dir: _pl.Path) -> int:
    if _svgwrite is None:
        print(
            "ERROR: svgwrite is required. Install with: pip install svgwrite",
            file=_sys.stderr,
        )
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)
    today = _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%d")
    svg_path = output_dir / f"pipeline-graph-{today}.svg"
    png_path = output_dir / f"pipeline-graph-{today}.png"

    svg_str = generate_pipeline_graph(SOURCES)
    svg_path.write_text(svg_str, encoding="utf-8")
    print(f"wrote {svg_path}", file=_sys.stderr)

    if _cairosvg is None:
        print(
            "WARNING: cairosvg is not installed; skipping PNG output. "
            "Install with: pip install cairosvg",
            file=_sys.stderr,
        )
    else:
        _cairosvg.svg2png(
            bytestring=svg_str.encode("utf-8"),
            write_to=str(png_path),
        )
        print(f"wrote {png_path}", file=_sys.stderr)

    return 0


if _click is not None:

    @_click.command()
    @_click.option(
        "--output-dir",
        default="docs/figures",
        type=_click.Path(exists=False, file_okay=False, dir_okay=True, path_type=_pl.Path),
        help="Output directory (default: docs/figures)",
    )
    def _cli(output_dir: _pl.Path) -> None:
        """Generate the static pipeline graph SVG + PNG."""
        raise _sys.exit(_run(output_dir))

    main = _cli
else:

    def main() -> int:  # type: ignore[no-redef]
        """Generate the static pipeline graph SVG (and PNG if cairosvg available)."""
        return _run(_pl.Path("docs/figures"))


if __name__ == "__main__":
    raise _sys.exit(main())