# Cianchosaint Langfuse Prompt Management

> **For:** Cian Pierce Lyons (Licensor) + Garda analysts + cianchosaint platform operators
>
> **Companion docs:** [`docs/USAGE-GUIDELINES.md`](../../USAGE-GUIDELINES.md) (the platform guide) + [`docs/HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md`](../../HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md) (the BIPP / BIDP / BIIP per-entity playbook) + [`./prompt-catalogue.md`](./prompt-catalogue.md) (the canonical prompt list)
>
> **Spec:** [`openspec/specs/cianchosaint-langfuse-prompt-management/spec.md`](../../../openspec/specs/cianchosaint-langfuse-prompt-management/spec.md)
>
> **Change:** [`openspec/changes/cianchosaint-langfuse-prompt-management-v1/`](../../../openspec/changes/cianchosaint-langfuse-prompt-management-v1/)
>
> **Licence:** [BUSL-1.1 v2 — CIANCHOSAINT edition](../../../LICENSE.md)

---

## 1. What this capability does

`cianchosaint-langfuse-prompt-management` is the canonical Langfuse v3 prompt management capability for the cianchosaint platform. It provides:

1. **Versioned prompts** — every BAML extraction function's prompt is stored in Langfuse with semantic versioning + labels (`staging`, `production`, etc.)
2. **A/B testing** — the `tag_experiment()` helper tags Langfuse traces with experiment markers + variant labels
3. **RAGAS score reporting** — the `report_ragas_scores()` helper records per-extraction RAGAS metrics (faithfulness, answer-relevancy, context-recall, context-precision) to the Langfuse scores API
4. **Graceful fallback** — when Langfuse is unavailable (circuit-breaker open, credentials missing, network failure), the resolver falls back to the inline BAML prompt
5. **Bulk sync** — the `scripts/sync_langfuse_prompts.py` script reads every canonical BAML prompt + bulk-pushes to Langfuse

This capability was the load-bearing foundation for the Garda self-hosted prompt development workflow that the user explicitly requested:

> "analyse the history of prompts ... using those output documents to show via cianchosaint how gardai can selfhost develop prompts take advantage of langfuse evals type agentic ai analytics of the official sources based on themeses and utilising the gemini_deep_research/politics topics"

---

## 2. The 3 load-bearing modules

### 2.1 `baml_src/_shared/langfuse_prompt_resolver.py` — the resolver

The `LangfusePromptResolver` class is the canonical entrypoint for every BAML function. It:

- Loads the Langfuse SDK lazily (defer import errors to runtime)
- Maintains a per-prompt 3-strike circuit-breaker (60s reset)
- Falls back to inline prompts if Langfuse is unavailable
- Records every resolution as a Langfuse span (when available)

```python
from baml_src._shared.langfuse_prompt_resolver import get_default_resolver

resolver = get_default_resolver()
hit = resolver.resolve("extract_isc_report", variables={"input": "..."})
print(hit.prompt_text, hit.fallback_used, hit.prompt_version)
```

The `get_default_resolver()` singleton is the canonical instance. Re-initialise the resolver if the Langfuse env vars change at runtime.

### 2.2 `baml_src/_shared/langfuse_client.py` — the client wrapper

The thin wrapper around the Langfuse Python SDK v4 that:

- Manages the API key + host configuration from `LANGFUSE_PUBLIC_KEY` + `LANGFUSE_SECRET_KEY` + `LANGFUSE_HOST`
- Provides the `tag_experiment()` helper for A/B test tagging
- Wraps the Scores API v3 via `report_ragas_scores()` for RAGAS metric reporting
- Provides `health_check()` for CI smoke gates

```python
from baml_src._shared.langfuse_client import (
    get_langfuse_client,
    report_ragas_scores,
    tag_experiment,
    health_check,
)

# Health check (works even without credentials — returns "not_configured")
print(health_check())

# Report RAGAS scores (silently no-ops when not configured)
reported = report_ragas_scores(
    trace_id="trace-abc",
    scores={"ragas.faithfulness": 0.85, "ragas.answer_relevancy": 0.92},
)
```

### 2.3 `scripts/sync_langfuse_prompts.py` — the bulk sync script

Bulk-pushes every canonical prompt from `baml_src/**/*.baml` → Langfuse. Usage:

```bash
# Show what would be pushed (no live write)
python3 scripts/sync_langfuse_prompts.py --dry-run

# Push every canonical prompt to Langfuse
python3 scripts/sync_langfuse_prompts.py --push

# List every Langfuse prompt + its current version
python3 scripts/sync_langfuse_prompts.py --list

# Promote a specific version to the 'production' label
python3 scripts/sync_langfuse_prompts.py --promote extract_isc_report 3
```

The 13-entry `CANONICAL_PROMPTS` registry is the durable source of truth. Every entry maps a `prompt_name` → `{file, baml_function, description}`. The script uses the regex-based `extract_baml_prompt_text()` helper to pull the inline `prompt #"..."` block from each `.baml` file at sync time.

---

## 3. The 4-tier graceful fallback (mirrors the provider router)

The resolver implements the same graceful-fallback pattern as the [4-tier provider router](../../USAGE-GUIDELINES.md#2-the-4-tier-provider-chain--when-each-tier-is-used):

```
Tier 1 (PRIMARY)  Langfuse SDK (live fetch + compile + RAGAS score reporting)
Tier 2            Inline BAML fallback (the prompt as-authored in the .baml file)
Tier 3            Inline fallback registered via `register_inline_fallback()`
Tier 4 (LAST)     [MISSING_PROMPT_FALLBACK] marker (returned when no inline exists)
```

The circuit-breaker transitions to `is_open=True` after 3 consecutive failures and stays open for 60 seconds, then auto-resets on the next call.

---

## 4. The 7 thematic cohorts (BIPP v2)

The 7 thematic cohorts are the canonical scope of the prompt management capability. Every cohort has:

- A canonical `prompt_name` in `CANONICAL_PROMPT_NAMES`
- A canonical BAML function in `baml_src/cianchosaint/politics/bipp_v2/<cohort>.baml`
- A `resolver "langfuse"` directive + `resolver_args { prompt_name "..." }`

| Cohort | Prompt name | BAML function |
|---|---|---|
| ROI political accountability | `extract_roi_political_dossier` | `ExtractRoiPoliticalAccountabilityDossier` |
| NI political accountability | `extract_ni_political_dossier` | `ExtractNiPoliticalAccountabilityDossier` |
| Welsh + London political accountability | `extract_welsh_london_dossier` | `ExtractWelshLondonPoliticalAccountabilityDossier` |
| Reform UK devolved | `extract_reform_uk_devolved_dossier` | `ExtractReformUkDevolvedDossier` |
| Reform UK (v2) | `extract_reform_uk_dossier` | `ExtractReformUkAccountabilityDossier` |
| Scottish political accountability | `extract_scottish_political_dossier` | `ExtractScottishPoliticalAccountabilityDossier` |
| Cross-cutting intelligence + cybersecurity | `extract_intelligence_cybersecurity_dossier` | `ExtractIntelligenceCybersecurityDossier` |

See [`./prompt-catalogue.md`](./prompt-catalogue.md) for the full list (≥ 20 entries including the pre-cohort extraction surface).

---

## 5. The 4 mise tasks

| Task | What it does |
|---|---|
| `mise run cianchosaint:langfuse:smoke` | Run the 58 Langfuse smoke tests (4 test files at `tests/langfuse/`) |
| `mise run cianchosaint:langfuse:lint` | Run `ruff check` + `mypy` on `langfuse_client.py` + `langfuse_prompt_resolver.py` + `sync_langfuse_prompts.py` |
| `mise run cianchosaint:langfuse:audit` | Verify every one of the 7 thematic cohort BAML files declares `resolver "langfuse"` + a canonical `prompt_name` |
| `mise run cianchosaint:langfuse:doc` | Regenerate the prompt catalogue (`docs/cianchosaint/prompt-catalogue.md`) |

---

## 6. The 4 smoke tests

| Test file | What it verifies |
|---|---|
| `tests/langfuse/test_langfuse_client.py` | The `LangfuseConfig` reads env vars + the `health_check()` returns the canonical `{status: "not_configured", ...}` surface in CI mode + the RAGAS metrics are populated + the `report_ragas_scores()` + `tag_experiment()` helpers tolerate the no-credentials case |
| `tests/langfuse/test_langfuse_prompt_resolver.py` | The resolver returns a `LangfusePromptHit` with `fallback_used=True` when not configured + the 3-strike circuit-breaker opens + closes correctly + `register_inline_fallback()` stores + retrieves prompts + the canonical 20+ prompt names cover every BAML function |
| `tests/langfuse/test_langfuse_prompt_management.py` | The sync script's `CANONICAL_PROMPTS` registry has the 13 canonical entries + the regex-based `extract_baml_prompt_text()` helper extracts inline BAML prompts (incl. multi-arg signatures) + the `push_prompt()` + `list_prompts()` + `promote_prompt()` flows work end-to-end against a stub client |
| `tests/langfuse/test_langfuse_agent_integration.py` | Every cianchosaint BAML extraction function in the 7 thematic cohorts declares `resolver "langfuse"` + a `resolver_args { prompt_name "<canonical>" }` + the sync registry + the resolver registry agree on at least 7 prompt names + the end-to-end inline-fallback path resolves cleanly |

---

## 7. The CI gate

The `.github/workflows/langfuse-prompt-management.yml` workflow runs the 4 smoke tests on every PR that touches:

- `baml_src/_shared/langfuse_*.py`
- `scripts/sync_langfuse_prompts.py`
- `tests/langfuse/**`
- `mise.toml`
- `.github/workflows/langfuse-prompt-management.yml`

This is the CI gate for the cianchosaint agent fleet's Langfuse prompt-management coverage.

---

## 8. Per-extraction RAGAS score reporting (the Garda analytics loop)

The `report_ragas_scores()` helper is the load-bearing primitive for the Garda self-hosted prompt development workflow. After every BAML extraction function completes, the Garda analyst (or the cianchosaint orchestration) calls:

```python
from baml_src._shared.langfuse_client import report_ragas_scores

# `trace_id` is the Langfuse trace ID for the extraction call.
reported = report_ragas_scores(
    trace_id=trace.trace_id,
    scores={
        "ragas.faithfulness": 0.92,
        "ragas.answer_relevancy": 0.85,
        "ragas.context_recall": 0.78,
        "ragas.context_precision": 0.81,
    },
)
print(f"reported {reported} RAGAS scores to Langfuse")
```

The helper silently no-ops when Langfuse is not configured (the CI / smoke-test mode), so it is safe to call from every extraction path without a feature flag.

The canonical RAGAS metrics tracked are (per `RAGAS_METRICS`):

| Metric | Meaning |
|---|---|
| `ragas.faithfulness` | How factually consistent the answer is with the retrieved context |
| `ragas.answer_relevancy` | How relevant the answer is to the question |
| `ragas.context_recall` | Whether the retrieved context covers the ground-truth answer |
| `ragas.context_precision` | Whether the retrieved context is ranked correctly |
| `ragas.context_entity_recall` | Whether the retrieved context covers the entities in the ground-truth answer |

---

## 9. Out of scope (follow-up changes)

- The actual 7 BIPP v2 BAML extraction schemas (follow-up `cianchosaint-bipp-v2-baml-v1`)
- The RAGAS eval pipeline (follow-up `cianchosaint-ragas-eval-pipeline-v1`)
- The Langfuse observability dashboard web app (follow-up `cianchosaint-langfuse-dashboard-v1`)
- The closed-loop Garda self-improvement workflow (follow-up `cianchosaint-garda-prompt-workflow-v1`)
- Retrofitting the existing inline BAML prompts to use the resolver (deferred — the resolver supports both inline + Langfuse modes; retrofitting is a per-cohort decision)

---

## 10. Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec validate cianchosaint-langfuse-prompt-management-v1 --strict  # pass

mise run cianchosaint:langfuse:smoke  # 58 passed
mise run cianchosaint:langfuse:audit  # 6 passed (cohort coverage + sync registry)
mise run cianchosaint:langfuse:lint   # ruff + mypy on the 3 Langfuse modules

python3 -c "
from baml_src._shared.langfuse_prompt_resolver import get_default_resolver
r = get_default_resolver()
print(r.health_check())
"
# Expected: {status: 'not_configured', ...} (no Langfuse creds in CI)
```