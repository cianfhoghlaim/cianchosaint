# `cianchosaint-intelligence-agency-pipeline` — Agent Routing

> `cianchosaint-intelligence-agency-pipeline` is the capability that provides the 5 UK intelligence agency DLT source modules for the British Isles intelligence ecosystem pipeline.

## Routing

Load this AGENTS.md when the parent spec (`./spec.md`) is in scope.
Use it to find the most relevant mise tasks + skills + adjacent files
without re-reading the full spec.

## Quick start

```bash
# 1. Validate the intelligence agency pipeline spec
openspec validate cianchosaint-intelligence-agency-pipeline --strict

# 2. Run the cohort registry to see all 5 agencies
python -m dlt_sources.cianchosaint.uk.intelligence_agencies._registry

# 3. Ingest a specific agency's public statements
python -c "
from dlt import pipeline
pipeline = dlt.pipeline(pipeline_name='mi5', destination='md:cianchosaint')
load_info = pipeline.run(dlt_sources.cianchosaint.uk.intelligence_agencies.mi5.mi5_source())
print(load_info)
"

# 4. Verify the OSINT allowlist covers every agency URL
mise run lint:license
```

## Key sources

- `openspec/specs/cianchosaint-intelligence-agency-pipeline/spec.md` — the canonical spec
- `dlt_sources/cianchosaint/uk/intelligence_agencies/_base.py` — the `IntelligenceAgencyPipelineBase` class
- `dlt_sources/cianchosaint/uk/intelligence_agencies/_registry.py` — the cohort registry
- `dlt_sources/cianchosaint/uk/intelligence_agencies/{mi5,mi6,gchq,defence_intelligence,hmgcc_rolling_window}.py` — the 5 DLT sources

## Adjacent specs

- `openspec/specs/cianchosaint-pipeline/spec.md` — the data pipeline umbrella
- `openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md` — the per-constituency policing / military / intel oversight DLT sources (the INTELLIGENCE OVERSIGHT companion: ISC + IPCO + IPT + IPB)
- `openspec/specs/cianchosaint-political-party-pipeline/spec.md` — the political party pipeline
- `openspec/specs/cianchosaint-reform-uk-pilot-workflow/spec.md` — the Reform UK pilot workflow (downstream consumer of this pipeline + the political party pipeline)

## DO NOT

- Add an intelligence agency source URL outside `osint_allowlist.yaml`
- Skip the `IntelligenceAgencyPipelineBase` inheritance (every agency source MUST subclass it)
- Use `dlt_sources.common.destinations_cianfhoghlaim` (use `destinations_cianchosaint` — the namespace-refactored factory)
- Treat any of the 5 agencies as "open source" — they're classified by design and the OSINT ceiling is "public-facing content only"

## Skill pointers

- `ccc` — for semantic code search across the 5 agency DLT sources
- `openspec` — for the spec change workflow
- `motherduck` — for the storage layer (uses `md:cianchosaint`)
- `baml` — for the BAML extraction schemas
- `cocoindex` — for the CocoIndex v1 App pattern

<!-- generated: 2026-08-23; do not hand-edit -->
