# Cianchosaint Configuration Surface

> The 8 layers of "configurability surface" — which layer is PRIMARY,
> which are SECONDARY, and which is for emergencies.

## TL;DR

| # | Layer | Type | Purpose | Scope |
|--:|:--|:--|:--|:--|
| 1 | **Per-source policy aggregator** (PRIMARY) | Runtime config (Python) | Per-DLT-source policy: VLM model, OCR confidence floor, extraction pass-rate floor, cost ceiling, retry budget | Per DLT source URL |
| 2 | `baml_src/clients.baml` 4-tier provider chain | Source of truth | The fallback chain (Unsloth Studio primary → local MiniMax-M3 → DeepSeek V4 Pro → Gemini 2.5 Pro) | Global |
| 3 | `BAML` extraction function defaults | Source of truth | Per-vertical conservative posture + per-jurisdiction enum + per-vertical BranchType | Per BAML file |
| 4 | Convex schema (per-persona apps) | Source of truth | Per-app table definitions + per-table validator API + per-table indexes | Per persona app |
| 5 | `mise.toml` task namespace | Source of truth | The 9-namespace task catalogue (`core`, `ts`, `schema`, `py`, `lint`, `opencode`, `baml`, `openspec`, `cic`) | Global |
| 6 | `.infisical.env` template | Source of truth | The canonical env-var URI references (e.g. `infisical://dev-baile/cianchosaint/...`) | Global |
| 7 | `OSINT allowlist` (`dlt_sources/cianchosaint/source_allowlist.py`) | Source of truth (legally binding per `LICENSE.md`) | The list of approved British-Isles official-source URLs | Global |
| 8 | `COCOINSIGHT_ENABLED` env var (future) | Runtime toggle | If CocoIndex V1 ever ships a stable CocoInsight-compatible HTTP server API, this env var enables the swap-in (per `openspec/specs/cianchosaint-pipeline-graph/spec.md` Background) | Global |

The **PRIMARY** layer (1, the per-source policy aggregator) is what
every operator + analyst + lawyer + judge + oversight officer uses
day-to-day. The other 7 layers are SECONDARY — they're the
foundational sources of truth that layer 1 reads from / composes
into.

## Layer 1: Per-source policy aggregator (PRIMARY)

**Status**: Shipped by `openspec/changes/2026-08-23-cianchosaint-pipeline-graph-v1/`
+ `openspec/changes/2026-08-23-cianchosaint-vlm-ocr-pipeline-v1/`.

**What it is**: A Pydantic model (per the wholesale-copied
Cianfhoghlaim pattern) at
`dlt_sources/cianchosaint/source_policy.py` (or similar) that
captures per-DLT-source policy:

```python
class SourcePolicy(BaseModel):
    source_id: str                              # e.g. "met_police"
    source_url_allowlist_entry: str            # points into the OSINT allowlist
    vlm_model: str                              # e.g. "dots.ocr-1b"
    ocr_confidence_floor: float                 # e.g. 0.85 (reject below)
    extraction_pass_rate_floor: float           # e.g. 0.90 (re-extract below)
    cost_ceiling_credits: float                 # e.g. 2.00 (alert above)
    retry_budget: int                           # e.g. 3 (max retries)
    baml_client: Literal["Primary", "Fallback", "Emergency", "Gemini"]
    conservative_posture: bool                  # MUST be True (per LICENCE)
```

**Why it's PRIMARY**: every analyst / lawyer / judge / oversight
officer asks "why did this source fail extraction?" or "why did
this source cost more than expected?" The answer lives in this
Pydantic model. It's the single place that captures per-source
operational policy without re-reading the BAML schemas, the
provider chain config, the Convex schemas, or the OSINT allowlist.

**Day-to-day use**:

```bash
# Inspect the current policy for a source
uv run python -c "from dlt_sources.cianchosaint.source_policy import get_policy; print(get_policy('met_police'))"

# Override a policy (e.g. during an incident response)
uv run python -c "from dlt_sources.cianchosaint.source_policy import set_policy; set_policy('met_police', cost_ceiling_credits=5.0)"

# Audit all policies against the OSINT allowlist
mise run cianchosaint:policy:audit
```

## Layer 2: `baml_src/clients.baml` 4-tier provider chain

**Status**: Shipped by
`openspec/changes/2026-08-23-cianchosaint-baml-schemas-v1/`.

The wholesale-copied Cianfhoghlaim 4-tier provider chain:

1. **Primary** — Unsloth Studio local API at `unsloth-serve:8889`
   (per `openspec/changes/unsloth-studio-pangolin-ingress-v1/`)
2. **Fallback** — local MiniMax-M3 (per
   `baml_src/clients_biep_v3.py` wholesale-copy)
3. **Emergency** — DeepSeek V4 Pro via `https://api.deepseek.com/v1`
4. **Gemini** — Google Gemini 2.5 Pro (final fallback)

Every BAML extraction function declares `client Primary` (or a named
variant of the chain). Operators tune the chain at the BAML layer,
not the per-source policy layer.

## Layer 3: BAML extraction function defaults

**Status**: Shipped by
`openspec/changes/2026-08-23-cianchosaint-baml-schemas-v1/`.

Per-vertical conservative posture + per-jurisdiction enum +
per-vertical `BranchType`. The 8 BAML files at
`baml_src/cianchosaint/processing/` (the 7 existing
+ `political_party.baml` per the wholesale-copy) capture the
vertical-specific extraction contract.

Operators tune the vertical at the BAML layer, not the per-source
policy layer.

## Layer 4: Convex schema (per-persona apps)

**Status**: Shipped by
`openspec/changes/2026-08-23-cianchosaint-convex-schemas-v1/`.

The 8 per-persona apps each have a Convex schema at
`web/apps/<app>/packages/convex/src/schema.ts` (e.g. the 4
`ciafagent-*-public/internal` apps + the 4 pilot apps). Tables
follow the wholesale-copied Cianfhoghlaim conventions:

- `chat_sessions` — AG-UI chat session metadata
- `form_submissions` — non-emergency form fill submissions
- `statute_queries` — cached OSINT statute search results
- `citation_ledger` — OSINT evidence citations
- (new in this change) `vlmPipelineDashboard` — per-source VLM
  extraction results + cost + latency (per
  `openspec/changes/2026-08-23-cianchosaint-vlm-ocr-pipeline-v1/`)

Operators tune the per-app schema at the Convex layer, not the
per-source policy layer.

## Layer 5: `mise.toml` task namespace

**Status**: Pre-existing (per the wholesale-copied Cianfhoghlaim
pattern).

The 9-namespace task catalogue:

| Namespace | Example task | Purpose |
|:--|:--|:--|
| `core` | `mise run core:ci` | dev env + lint + test + openspec:validate-all |
| `ts` | `mise run ts:typecheck` | TypeScript type-check across `web/packages/` |
| `schema` | `mise run schema:generate` | BAML → Convex schema codegen |
| `py` | `mise run py:lint` | Python linting across `baml_src/`, `dlt_sources/`, `cocoindex_flows/` |
| `lint` | `mise run lint:license` | OSINT allowlist + British Isles body check |
| `opencode` | `mise run opencode:agents:smoke` | 15-agent smoke test |
| `baml` | `mise run baml:test` | BAML extraction function tests |
| `openspec` | `mise run openspec:validate-all` | CI gate for all openspec changes + specs |
| `cic` | `mise run cic:stack-doctor` | 94-stack IaC validation |

Operators add / tune tasks at the mise layer, not the per-source
policy layer.

## Layer 6: `.infisical.env` template

**Status**: Pre-existing (per the wholesale-copied Cianfhoghlaim
pattern + `LICENSE.md` § Infisical-only contract).

Every secret is referenced as an `infisical://dev-baile/...` URI.
The hydration happens at `cd` time via mise directory hooks + at
container start via the Locket sidecar. Operators add / rotate
secrets in the Infisical vault, not the per-source policy layer.

## Layer 7: OSINT allowlist (legally binding)

**Status**: Pre-existing (per `LICENSE.md § Additional Use Grant`).

The list of approved British-Isles official-source URLs at
`dlt_sources/cianchosaint/source_allowlist.py` (or similar — the
exact path is owned by the wholesale-copy). Every DLT source URL
**MUST** be in this list AND every list entry MUST point at a
British Isles body.

**This is the only layer that is legally binding.** Adding a
source that is not on the allowlist is a LICENCE breach. The other
7 layers are operational; this one is legal.

Operators add / audit the allowlist at the allowlist layer, not the
per-source policy layer.

## Layer 8: `COCOINSIGHT_ENABLED` env var (future)

**Status**: Not yet implemented. Tracked by
`openspec/specs/cianchosaint-pipeline-graph/spec.md` Background.

When CocoIndex V1 ever ships a stable CocoInsight-compatible HTTP
server API (tracked upstream as
`cocoindex-io/cocoindex#1351`), this env var enables the
hand-rolled React + d3.js component swap:

```bash
# Disable (default; use the hand-rolled component)
unset COCOINSIGHT_ENABLED

# Enable (use CocoInsight as the pipeline graph UI)
export COCOINSIGHT_ENABLED=true
```

Operators toggle at the env-var layer, not the per-source policy
layer.

## Decision matrix — which layer to touch

| Question | Layer | File |
|:--|:--|:--|
| "Why did extraction fail for `met_police`?" | 1 (PRIMARY) | `dlt_sources/cianchosaint/source_policy.py` |
| "Which provider handled this request?" | 2 | `baml_src/clients.baml` |
| "What does `ExtractCourtJudgment` return?" | 3 | `baml_src/cianchosaint/processing/irish_legal_extraction.baml` |
| "Where is the per-persona chat session stored?" | 4 | `web/apps/ciafagent-ga-public/packages/convex/src/schema.ts` |
| "What's the CI gate?" | 5 | `mise.toml` (`[tasks.core]` block) |
| "Where does `UNSLOTH_API_KEY` come from?" | 6 | `.infisical.env` |
| "Is `data.police.uk` a legal source?" | 7 (LEGAL) | `dlt_sources/cianchosaint/source_allowlist.py` |
| "Should I use CocoInsight or the React component?" | 8 | `COCOINSIGHT_ENABLED` env var |

## Cross-references

- `docs/research/cocoinsight-v0-research.md` — the CocoInsight research that motivates layer 8
- `docs/research/web-stack-best-practices-v0.md` — the web stack drift surface
- `openspec/changes/2026-08-23-cianchosaint-pipeline-graph-v1/` — the pipeline graph change (consumes layer 1 + 4)
- `openspec/changes/2026-08-23-cianchosaint-vlm-ocr-pipeline-v1/` — the VLM OCR pipeline change (populates layer 4's `vlmPipelineDashboard` table)
- `LICENSE.md § Additional Use Grant` — the legal contract for layer 7
- `AGENTS.md` — the operator-facing routing table for the 9 priority mise tasks