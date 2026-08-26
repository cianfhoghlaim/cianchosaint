# 15 — UK GCHQ stroom (the data processing platform)

> Per the
> [`openspec/changes/cianchosaint-hmgcc-gchq-tooling-v1/`](../../openspec/changes/cianchosaint-hmgcc-gchq-tooling-v1/specs/cianchosaint-hmgcc-gchq-tooling/spec.md)
> spec (stroom track).

## Overview

[GCHQ stroom](https://github.com/gchq/stroom) is GCHQ's "data
processing, storage and analysis platform" — built by GCHQ for
internal use + shared with other UK public-sector bodies. Stroom
provides XSL-based pipelines that convert raw log data into
structured events (with enrichment, dedup, indexing).

The cianchosaint platform wholesale-copies the upstream stroom
catalog (`hmgcc/stroom/`, **Apache 2.0**) + exposes a bounded event-
type catalog + a bounded upstream-source catalog through a
FunctionTool that the AG-UI chat window can invoke. The
`stroom_query` FunctionTool lets analysts route **high-volume log
data through stroom BEFORE the DLT sources ingest it** — see
`[`how/how-british-isles-intelligence-defence-policing-entities-use-cianchosaint.md` §6](../HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md).

## The wholesale source

| Field | Value |
|---|---|
| **Upstream** | `hmgcc/stroom/` (wholesale-copied) |
| **Upstream licence** | Apache 2.0 |
| **Version pinned** | Per `hmgcc/stroom/CHANGELOG.md` (auto-upstream pinning intentionally lags) |
| **Our subset** | 6 event types + 6 upstream sources (see `EVENT_TYPES` + `UPSTREAM_SOURCE_IDS` in `StroomLogPipeline`) |

## Sources

### stroom (the GCHQ data processing platform wholesale copy)

- **URL**: https://github.com/gchq/stroom
- **Wholesale source**: `hmgcc/stroom/` (Apache 2.0)
- **DLT source**: `dlt_sources/cianchosaint/uk/stroom/log_extraction.py`
- **BAML extraction**: `baml_src/cianchosaint/processing/stroom_log_extraction.baml`
- **FunctionTool**: `agents/cianchosaint/tools/stroom_query.py`
- **OSINT allowlist**: yes
- **Coverage**: The 6 bounded event types + the 6 bounded upstream sources we route through stroom
- **Update cadence**: weekly (mirrors upstream stroom releases)
- **Notes**: Apache 2.0 wholesale — we honour the upstream licence + provide attribution in every source file

## Workflow

1. **A high-volume log source emits a log** (e.g. `craw4ai` browser log, `langfuse` LLM trace, `changedetection` page-change event)
2. **`mise run cianchosaint:stroom:route-logs`** forwards the log through the `cianchosaint.craw4ai.page_change` XSL pipeline
3. **Stroom XSL transforms** the raw log into a structured event (e.g. `{url, previous_hash, current_hash, diff_summary}`)
4. **The cianchosaint DLT source pulls the structured events** (`stroom_structured_events` resource) via the `Stroom-Proxy` API
5. **The `ExtractStroomLog` BAML function** structures the post-transform event further
6. **The structured event** lands in the DLT destination + the analyst dashboard

## Gaps

- Upstream stroom has hundreds of pipelines + steps; the cianchosaint FunctionTool wraps only 6 upstream sources + 6 event types. The bounded subset is the most useful for the existing per-constituency DLT sources.
- The `stroom-stack` Docker stack (stroom + stroom-proxy + stroom-db + solr) is NOT yet bundled in the self-hosted Docker bundle. Follow-up `cianchosaint-stroom-stack-v1` change would close this gap (~5 containers, ~3 GiB).
- Auto-pinning of the stroom upstream version intentionally lags (we don't ship upstream releases the moment they're tagged — we vet them first).

## References

- The canonical openspec spec:
  [`openspec/changes/cianchosaint-hmgcc-gchq-tooling-v1/specs/cianchosaint-hmgcc-gchq-tooling/spec.md`](../../openspec/changes/cianchosaint-hmgcc-gchq-tooling-v1/specs/cianchosaint-hmgcc-gchq-tooling/spec.md)
- The wholesale Apache 2.0 source: [`hmgcc/stroom/`](../../hmgcc/stroom/)
- The upstream repo: https://github.com/gchq/stroom
- The British-Isles intelligence / defence / policing entities doc:
  [`HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md`](../HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md)
- The OSINT allowlist:
  [`dlt_sources/cianchosaint/common/osint_allowlist.yaml`](../../dlt_sources/cianchosaint/common/osint_allowlist.yaml)
- The 4-tier provider chain:
  [`baml_src/_shared/provider_router.py`](../../baml_src/_shared/provider_router.py)
