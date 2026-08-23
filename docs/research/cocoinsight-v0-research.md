# CocoInsight Research (Q31)

> **Status:** Research complete. Decision recorded below. Filed under
> `openspec/changes/2026-08-23-cianchosaint-pipeline-graph-v1/specs/cianchosaint-pipeline-graph/spec.md`
> as a downstream integration constraint.

## Summary

**CocoInsight exists** and is a real CocoIndex-team product. It is a hosted
data-lineage + observability UI at `https://cocoindex.io/cocoinsight` that
talks to a local CocoIndex HTTP server over CORS, with **zero data
retention** (the server is on your machine, the UI is just a viewer pointed
at it).

**However:** the CocoInsight integration story for CocoIndex V1 — the API
level cianchosaint is pinned at (`cocoindex>=1.0.14`) — is **unclear**. The
V1 launch post explicitly removes the engine-bookkeeping server process in
favour of embedded LMDB, and the CocoInsight docs still reference the V0
`cocoindex server` CLI. The integration gap is tracked upstream as
[cocoindex-io/cocoindex#1351](https://github.com/cocoindex-io/cocoindex/issues/1351)
("clarify HTTP Server") and
[cocoindex-io/cocoindex#1340](https://github.com/cocoindex-io/cocoindex/issues/1340)
(closed bug confirming the V0 import surface: `from cocoindex.setting
import ServerSettings`).

## What we searched

| Surface | Query | Result |
|:--|:--|:--|
| `cianchosaint/` (whole repo) | `cocoinsight\|coco_insight\|coco-insight\|coco.index.insight` | **0 matches** (only `.git/` and `.venv/` ignored) |
| `cianchosaint/openspec/` (specs + changes) | `insight\|dashboard\|visualisation\|visualization` | 4 hits, all pre-existing refs (Cloudflare deploy, agentic interaction, pipeline spec, AGENTS.md), none about CocoInsight |
| `cianchosaint/cocoindex_flows/` | `start_server\|ServerSettings\|http\|cors` | **0 matches** — no HTTP server usage anywhere |
| `cianchosaint/pyproject.toml` | `cocoindex` | `cocoindex>=1.0.14` — pinned to V1 |
| Upstream (`cocoindex.io/blogs/`) | "Introducing CocoInsight" | Launched 2025-06-24, ~10 months before V1 (2026-04-22) |
| Upstream (`cocoindex.io/blogs/cocoindex-v1/`) | (full text read) | "There's no server process to run, schema to migrate, or port to expose" — V1 is intentionally serverless for engine state |
| Upstream GitHub issues | `start_server ServerSettings v1` | #1351 open, #1340 closed (V0 import surface) |

## What we know (from upstream sources, verified 2026-08-23)

### What CocoInsight is

- **URL**: <https://cocoindex.io/cocoinsight> (hosted UI) + <https://cocoindex.io/docs-v0/cocoinsight_access/> (docs)
- **Launch date**: 2025-06-24 (~14 months in market as of this research)
- **Architecture**: a hosted React/web UI that talks to **your** local CocoIndex HTTP server over CORS. The UI renders the dataflow + per-step data preview; your documents, embeddings, and extracted entities **never leave your machine** (zero pipeline data retention, on the marketing page, on the docs page, and in the FAQ).
- **GitHub stars**: 10,000+ on `cocoindex-io/cocoindex` (per the launch post)
- **Use cases demonstrated**: codebase indexing flow (per-file processing, language detection via Tree-sitter, chunk splitting), knowledge-graph flow (LLM summarisation + entity extraction + relationship rows), full data lineage traversal

### How CocoInsight connects

Two ways to expose the HTTP server (both V0 syntax as of docs dated Dec 2025):

```sh
# CLI
cocoindex server path/to/app.py            # default 127.0.0.1:49344 (local-only)
cocoindex server path/to/app.py -ci        # allow https://cocoindex.io (CocoInsight UI)
cocoindex server path/to/app.py -L         # enable live updates while server runs
cocoindex server path/to/app.py -c https://example.com   # custom CORS origin
cocoindex server path/to/app.py -cl 3000   # allow http://localhost:3000 (local frontend)
```

```python
# Python API (V0 import — bug-fixed in cocoindex-io/cocoindex#1341)
from cocoindex.setting import ServerSettings  # NOT cocoindex.settings
from cocoindex import start_server

server_settings = ServerSettings(
    address="127.0.0.1:49344",
    cors_origins=["https://cocoindex.io"],
)
start_server(server_settings)
```

Internal REST API lives under `/cocoindex/api` and is explicitly
**documented as unstable / subject to change / not considered stable**.
The `/healthz` endpoint returns `{"status": "ok", "version": "<build>"}`.

### Why this matters for cianchosaint

- **OSINT privacy stance**: zero data retention aligns exactly with
  cianchosaint's `LICENSE.md § Additional Use Grant` — the platform
  cannot exfiltrate official-source documents, judgments, or extracted
  entities because the UI never sees them.
- **Zero-trust trace**: per-step data preview + lineage traversal makes
  it trivial to verify a CocoIndex V1 flow is reading the right
  UK/ROI/Crown-Dependencies official-source URL and not a URL outside
  the OSINT allowlist.
- **No new infra**: it's a hosted UI you point at a local server
  (already on the analyst's workstation). No new database, no new SaaS
  contract, no data egress.

## What we don't know (the V1 gap)

The reasons this is NOT a turnkey integration for cianchosaint:

### 1. The CocoInsight docs are V0-era

The `cocoindex server` CLI syntax is the V0 (`FlowBuilder` + `DataScope`)
command surface. The V1 launch post (2026-04-22) **explicitly says**:

> "There's no server process to run, schema to migrate, or port to
> expose. CocoIndex V1 stores its internal state in LMDB, an embedded
> key-value store that lives in a single local file."

V1's mental model is serverless for engine bookkeeping. Whether
`start_server` + `ServerSettings` survived into V1 (1.0.x line) is
**not documented** — the docs only describe V0.

### 2. GitHub issue #1351 is open and unresolved

`[Documentation] clarify HTTP Server — Currently the main purpose of
the server is to expose an endpoint for CocoInsight.`

This issue is the upstream maintainers acknowledging the V1 → CocoInsight
story is unclear. Status: open as of research date.

### 3. The V1 example gallery does not mention CocoInsight

The V1 launch post walks through 4 example shapes
(multi-codebase summarisation, conversation-to-knowledge, CSV → Kafka live,
HN trending topics) and references `cocoindex update main.py` (no server).
The CocoIndex Code codebase indexing example (the v1-native version of the
most CocoInsight-touted V0 use case) does not mention `start_server`.

### 4. cianchosaint's V1 code does not import the HTTP server

A grep across `cocoindex_flows/` for `start_server`, `ServerSettings`,
`http`, `cors` returns zero matches. Every flow uses the V1 pattern
(`coco.App` + `@coco.fn` + `lancedb.mount_table_target`). If the V1
line still ships the HTTP server, it's a doc-discoverability problem; if
not, the integration story requires either (a) pinning to V0 or (b)
waiting on upstream.

## Recommendation

**Do NOT pin a CocoInsight integration as a hard deliverable in this
openspec change.** Treat it as:

1. **Documented research** (this file) — explains the privacy-fit and
   what CocoInsight would buy us if V1 ever ships a stable HTTP server.
2. **A future-proofing note** in the canonical spec — the
   `cianchosaint-pipeline-graph` spec should mention that if V1 ever
   exposes the CocoInsight-compatible HTTP API, cianchosaint can swap
   the custom React + d3.js pipeline graph for CocoInsight with a
   one-day config change (the per-source cost + latency + extraction
   pass-rate columns are the ones CocoInsight already shows).
3. **Build the alternative now** — a hand-rolled React + d3.js
   `PipelineGraph` component (per the Sub-task 2 deliverable) that
   visualises the 5-stage pipeline + per-source VLM extraction results
   + per-source cost + latency. The component reads from the existing
   Convex `cianchosaint_vlm_pipeline_dashboard` table (per Sub-task 3),
   so swapping in CocoInsight later is a one-component replacement.

## Why the alternative is fine

The alternative (hand-rolled React + d3.js) gives cianchosaint:

- **Full control over the visual idiom** — cianchosaint needs a
  per-persona view (analyst, lawyer, judge, oversight officer), not a
  generic dataflow viewer. CocoInsight's spreadsheet UX is great for
  pipeline authors but suboptimal for case-file presentation.
- **No external hosted UI dependency** — every UI surface in
  cianchosaint is self-hosted on the analyst's workstation. Adding a
  hosted UI is a posture change that requires warrant-to-enforce
  review (`LICENSE.md § Additional Use Grant`).
- **No version-coupling** — when V1 + CocoInsight stabilises (or V2
  ships, or CocoInsight deprecates), cianchosaint's visualisation
  surface is unaffected.

The downside is more code to maintain (~250 LOC React + ~120 LOC Python
generator, per Sub-task 2 + 3). That cost is bounded and ships with the
`cianchosaint-pipeline-graph` change.

## Decision matrix

| Outcome | Recommendation |
|:--|:--|
| V1 ships a stable `start_server` API (e.g. V1.2+ release notes) | Follow-up change adds a CocoInsight toggle behind `COCOINSIGHT_ENABLED` env var; the React + d3.js component stays as the fallback + the per-persona view layer. |
| V1 never ships a CocoInsight-compatible API | Ship React + d3.js component as the primary visualisation surface; revisit if CocoInsight becomes a paid SaaS or a separate open-source project. |
| Upstream pivots away from CocoInsight | No action — CocoInsight is a hosted UI; cianchosaint's data + flows are unaffected either way. |

## Cross-references

- `openspec/changes/2026-08-23-cianchosaint-pipeline-graph-v1/specs/cianchosaint-pipeline-graph/spec.md` — canonical spec (notes CocoInsight as a future swap-in option)
- `openspec/changes/2026-08-23-cianchosaint-vlm-ocr-pipeline-v1/specs/cianchosaint-vlm-ocr-pipeline/spec.md` — sibling spec providing the `vlmPipelineDashboard` table the React component reads from
- `cocoindex_flows/cianchosaint/vlm_pipeline_aggregator.py` — CocoIndex V1 App that populates `vlmPipelineDashboard` (Sub-task 3)
- `web/packages/ui-kit/components/PipelineGraph.tsx` — hand-rolled React + d3.js component (Sub-task 2)

## Cited sources (verified 2026-08-23)

- <https://cocoindex.io/blogs/cocoinsight/> — Introducing CocoInsight (Linghua Jin, 2025-06-24)
- <https://cocoindex.io/docs-v0/cocoinsight_access/> — CocoInsight access docs (v0, dated 2025-12-02)
- <https://cocoindex.io/blogs/cocoindex-v1/> — CocoIndex V1 is Live! (Linghua Jin + George He, 2026-04-22)
- <https://github.com/cocoindex-io/cocoindex/issues/1351> — `[Documentation] clarify HTTP Server` (open)
- <https://github.com/cocoindex-io/cocoindex/issues/1340> — `'function' object has no attribute 'ServerSettings'` (closed, V0 import path bug)
- <https://github.com/cocoindex-io/cocoindex/issues/430> — port-already-in-use silent failure (closed; default port changed to 49344)