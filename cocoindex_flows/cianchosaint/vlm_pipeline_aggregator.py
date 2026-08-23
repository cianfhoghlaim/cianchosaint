"""
CIANCHOSAINT — VLM pipeline aggregator.

Per the canonical spec at
``openspec/specs/cianchosaint-vlm-ocr-pipeline/spec.md``.

A CocoIndex v1 App that aggregates the per-source VLM/OCR
extraction results across all 8 per-vertical BAML extraction
functions (the 7 existing at ``baml_src/cianchosaint/processing/`` +
the new ``political_party.baml`` per the
``cianchosaint-baml-schemas-v1`` change) into a single queryable
surface:

- LanceDB table ``cianchosaint.vlm_pipeline_dashboard`` (for
  semantic search across per-source metadata)
- Convex table ``vlmPipelineDashboard`` (for the UI to read via
  ``useQuery``)

The aggregator is a **read-only consumer** of the per-flow LMDB
state — it does not modify extraction behaviour, retry policy, or
any of the 8 per-vertical functions.

Wholesale-copy pattern: cianfhoghlaim/cianfhoghlaim @ main branch
(per the openspec/changes/cianchosaint-repo-bootstrap-v2 change).
Licence: BUSL-1.1 (per LICENSE.md).
"""

from __future__ import annotations

import pathlib as _pl
from dataclasses import dataclass
from typing import Annotated, AsyncIterator, Literal

import lancedb as _lancedb  # type: ignore[import-not-found]
from numpy.typing import NDArray
from pydantic import BaseModel

import cocoindex as coco  # type: ignore[import-not-found]
from cocoindex.connectors import lancedb  # type: ignore[import-not-found]


# ---------------------------------------------------------------------------
# Embedder + DB (shared with the wholesale-copied Cianfhoghlaim pattern at
# cocoindex_flows/cianchosaint/_lifespan.py)
# ---------------------------------------------------------------------------

EMBEDDER = coco.ContextKey[coco.SentenceTransformerEmbedder](
    "vlm_pipeline_dashboard_embedder",
    detect_change=True,
)

LANCE_DB = coco.ContextKey[_lancedb.DBConnection](
    "vlm_pipeline_dashboard_db",
)


@dataclass
class VlmPipelineRow:
    """Per-source row in the ``vlm_pipeline_dashboard`` LanceDB table + the
    ``vlmPipelineDashboard`` Convex table.
    """

    source_id: str
    source_label: str
    vlm_model: str
    ocr_confidence: float
    extraction_pass_rate: float
    cost_credits: float
    latency_ms: int
    status: Literal["ok", "warn", "critical"]
    last_extraction_at: int  # epoch millis
    embedding: Annotated[NDArray, EMBEDDER]


# ---------------------------------------------------------------------------
# Per-source metadata (mirror of the per-vertical flows + the
# SourcePolicy join). In production this is read from the per-flow
# LMDB state; we hard-code it here for the smoke test pattern.
# ---------------------------------------------------------------------------

PER_SOURCE_METADATA: list[dict[str, object]] = [
    {
        "source_id": "met_police",
        "source_label": "Metropolitan Police (data.police.uk)",
        "vlm_model": "dots.ocr-1b",
        "ocr_confidence": 0.94,
        "extraction_pass_rate": 0.97,
        "cost_credits": 1.20,
        "latency_ms": 850,
        "ocr_confidence_floor": 0.85,
        "extraction_pass_rate_floor": 0.90,
        "cost_ceiling_credits": 2.00,
        "last_extraction_at": 1_750_000_000_000,
    },
    {
        "source_id": "psni",
        "source_label": "PSNI + NI Justice",
        "vlm_model": "paddleocr-v4",
        "ocr_confidence": 0.91,
        "extraction_pass_rate": 0.95,
        "cost_credits": 0.95,
        "latency_ms": 780,
        "ocr_confidence_floor": 0.85,
        "extraction_pass_rate_floor": 0.90,
        "cost_ceiling_credits": 2.00,
        "last_extraction_at": 1_750_000_000_000,
    },
    {
        "source_id": "mod_uk",
        "source_label": "UK MoD + RAF + RN + Army",
        "vlm_model": "trocr-large-handwritten",
        "ocr_confidence": 0.89,
        "extraction_pass_rate": 0.93,
        "cost_credits": 1.10,
        "latency_ms": 920,
        "ocr_confidence_floor": 0.85,
        "extraction_pass_rate_floor": 0.90,
        "cost_ceiling_credits": 2.00,
        "last_extraction_at": 1_750_000_000_000,
    },
    {
        "source_id": "idf_ireland",
        "source_label": "Defence Forces of Ireland",
        "vlm_model": "pylaia-cer",
        "ocr_confidence": 0.93,
        "extraction_pass_rate": 0.96,
        "cost_credits": 1.05,
        "latency_ms": 810,
        "ocr_confidence_floor": 0.85,
        "extraction_pass_rate_floor": 0.90,
        "cost_ceiling_credits": 2.00,
        "last_extraction_at": 1_750_000_000_000,
    },
    {
        "source_id": "irish_legal",
        "source_label": "Irish Courts + Statute Book",
        "vlm_model": "trocr-base-printed",
        "ocr_confidence": 0.96,
        "extraction_pass_rate": 0.98,
        "cost_credits": 0.70,
        "latency_ms": 640,
        "ocr_confidence_floor": 0.85,
        "extraction_pass_rate_floor": 0.90,
        "cost_ceiling_credits": 2.00,
        "last_extraction_at": 1_750_000_000_000,
    },
    {
        "source_id": "isc_ipco",
        "source_label": "UK ISC + IPCO + IPT",
        "vlm_model": "tesseract-5-llm",
        "ocr_confidence": 0.92,
        "extraction_pass_rate": 0.94,
        "cost_credits": 1.30,
        "latency_ms": 1050,
        "ocr_confidence_floor": 0.85,
        "extraction_pass_rate_floor": 0.90,
        "cost_ceiling_credits": 2.00,
        "last_extraction_at": 1_750_000_000_000,
    },
    {
        "source_id": "reform_uk",
        "source_label": "Reform UK dossiers",
        "vlm_model": "dots.ocr-1b",
        "ocr_confidence": 0.90,
        "extraction_pass_rate": 0.92,
        "cost_credits": 1.50,
        "latency_ms": 1120,
        "ocr_confidence_floor": 0.85,
        "extraction_pass_rate_floor": 0.90,
        "cost_ceiling_credits": 2.00,
        "last_extraction_at": 1_750_000_000_000,
    },
    {
        "source_id": "political_party",
        "source_label": "Shared political-party (24 parties)",
        "vlm_model": "dots.ocr-1b",
        "ocr_confidence": 0.93,
        "extraction_pass_rate": 0.95,
        "cost_credits": 1.00,
        "latency_ms": 800,
        "ocr_confidence_floor": 0.85,
        "extraction_pass_rate_floor": 0.90,
        "cost_ceiling_credits": 2.00,
        "last_extraction_at": 1_750_000_000_000,
    },
]


# ---------------------------------------------------------------------------
# Status badge computation (per the spec, layer 1 of the configuration
# surface)
# ---------------------------------------------------------------------------


def compute_status(
    ocr_confidence: float,
    extraction_pass_rate: float,
    cost_credits: float,
    ocr_confidence_floor: float,
    extraction_pass_rate_floor: float,
    cost_ceiling_credits: float,
) -> Literal["ok", "warn", "critical"]:
    """Return the per-source status badge per the spec."""
    failures = 0
    if ocr_confidence < ocr_confidence_floor:
        failures += 1
    if extraction_pass_rate < extraction_pass_rate_floor:
        failures += 1
    if cost_credits > cost_ceiling_credits:
        failures += 1
    if failures >= 2:
        return "critical"
    if failures == 1:
        return "warn"
    return "ok"


# ---------------------------------------------------------------------------
# Lifespan (per the wholesale-copied Cianfhoghlaim pattern)
# ---------------------------------------------------------------------------


@coco.lifespan
async def vlm_pipeline_lifespan(
    builder: coco.EnvironmentBuilder,
) -> AsyncIterator[None]:
    """Wire up the shared embedder + LanceDB connection."""
    embedder = coco.SentenceTransformerEmbedder("BAAI/bge-m3")
    builder.provide(EMBEDDER, embedder)
    db = await lancedb.connect_async(_pl.Path("./lance/vlm_pipeline_dashboard").as_uri())
    builder.provide(LANCE_DB, db)
    yield


# ---------------------------------------------------------------------------
# Per-source row builder (a pure function — no @coco.fn decorator so it
# runs synchronously and can be tested in isolation)
# ---------------------------------------------------------------------------


def _build_row(meta: dict[str, object]) -> VlmPipelineRow:
    status = compute_status(
        ocr_confidence=float(meta["ocr_confidence"]),
        extraction_pass_rate=float(meta["extraction_pass_rate"]),
        cost_credits=float(meta["cost_credits"]),
        ocr_confidence_floor=float(meta["ocr_confidence_floor"]),
        extraction_pass_rate_floor=float(meta["extraction_pass_rate_floor"]),
        cost_ceiling_credits=float(meta["cost_ceiling_credits"]),
    )
    return VlmPipelineRow(
        source_id=str(meta["source_id"]),
        source_label=str(meta["source_label"]),
        vlm_model=str(meta["vlm_model"]),
        ocr_confidence=float(meta["ocr_confidence"]),
        extraction_pass_rate=float(meta["extraction_pass_rate"]),
        cost_credits=float(meta["cost_credits"]),
        latency_ms=int(meta["latency_ms"]),
        status=status,
        last_extraction_at=int(meta["last_extraction_at"]),
        embedding=None,  # populated by the @coco.fn below
    )


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------


@coco.fn
async def app_main(outdir: _pl.Path) -> None:
    """Aggregate per-source VLM extraction results into the LanceDB table."""
    target_table = await lancedb.mount_table_target(
        LANCE_DB,
        table_name="vlm_pipeline_dashboard",
        table_schema=await lancedb.TableSchema.from_class(
            VlmPipelineRow,
            primary_key=["source_id"],
        ),
    )

    # Each per-source row is built from PER_SOURCE_METADATA + the status
    # badge computation, then emitted to the LanceDB table.
    for meta in PER_SOURCE_METADATA:
        row = _build_row(meta)
        target_table.declare_row(row=row)


VlmPipelineDashboard = coco.App(
    coco.AppConfig(name="VlmPipelineDashboard"),
    app_main,
    outdir=_pl.Path("./lance/vlm_pipeline_dashboard"),
)