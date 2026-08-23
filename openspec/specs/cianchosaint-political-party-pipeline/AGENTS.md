# `cianchosaint-political-party-pipeline` — Agent Routing

> `cianchosaint-political-party-pipeline` is the capability that provides the 24 per-political-party DLT source modules for the British Isles political-party monitoring pipeline.

## Routing

Load this AGENTS.md when the parent spec (`./spec.md`) is in scope.
Use it to find the most relevant mise tasks + skills + adjacent files
without re-reading the full spec.

## Quick start

```bash
# 1. Validate the political party pipeline spec
openspec validate cianchosaint-political-party-pipeline --strict

# 2. Run the cohort registry to see all 24 parties
python -m dlt_sources.cianchosaint.political_parties._registry

# 3. Ingest a specific party's press releases
python -c "
from dlt import pipeline
pipeline = dlt.pipeline(pipeline_name='reform_uk', destination='md:cianchosaint')
load_info = pipeline.run(dlt_sources.cianchosaint.political_parties.uk.reform_uk.reform_uk_source())
print(load_info)
"

# 4. Verify the OSINT allowlist covers every party URL
mise run lint:license
```

## Key sources

- `openspec/specs/cianchosaint-political-party-pipeline/spec.md` — the canonical spec
- `dlt_sources/cianchosaint/political_parties/_base.py` — the `PoliticalPartyPipelineBase` class
- `dlt_sources/cianchosaint/political_parties/_registry.py` — the cohort registry
- `dlt_sources/cianchosaint/political_parties/uk/reform_uk.py` ⭐ — the canonical Reform UK pilot source
- `baml_src/cianchosaint/processing/party.baml` — the shared `ExtractPartyPressRelease` BAML function

## Adjacent specs

- `openspec/specs/cianchosaint-pipeline/spec.md` — the data pipeline umbrella
- `openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md` — the per-constituency policing / military / intel oversight DLT sources
- `openspec/specs/cianchosaint-reform-uk-pilot-workflow/spec.md` — the Reform UK pilot workflow (downstream consumer of the reform_uk.py DLT source)
- `openspec/specs/cianchosaint-intelligence-agency-pipeline/spec.md` — the intelligence agency pipeline (companion)

## DO NOT

- Add a party source URL outside `allowlist_parties.yaml` or `osint_allowlist.yaml`
- Skip the `PoliticalPartyPipelineBase` inheritance (every party source MUST subclass it)
- Use `dlt_sources.common.destinations_cianfhoghlaim` (use `destinations_cianchosaint` — the namespace-refactored factory)
- Treat Reform UK specially — it's just one of 24 parties in the registry

## Skill pointers

- `ccc` — for semantic code search across the 24 party DLT sources
- `openspec` — for the spec change workflow
- `motherduck` — for the storage layer (uses `md:cianchosaint`)
- `baml` — for the BAML extraction schemas
- `cocoindex` — for the CocoIndex v1 App pattern

<!-- generated: 2026-08-23; do not hand-edit -->
