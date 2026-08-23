# Spec Delta: cianchosaint-bootstrap-v2

This delta is applied by the openspec change
[`cianchosaint-repo-bootstrap-v2`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-bootstrap-v2/spec.md`](../../../../specs/cianchosaint-bootstrap-v2/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: Data platform wholesale-copy (DLT + BAML + CocoIndex)

The system SHALL wholesale-copy the relevant Cianfhoghlaim data
platform assets into cianchosaint, with the `cianchosaint` namespace
rename applied uniformly.

#### Scenario: DLT destinations factory renamed

- **WHEN** the operator runs
  `python -c "from dlt_sources.common.destinations_cianchosaint import get_dlt_destination, LAKEHOUSE_DUCKDB"`
- **THEN** `get_dlt_destination(mode="local")` SHALL return a
  local DuckDB destination at `./data/cianchosaint.duckdb`
- **AND** `LAKEHOUSE_DUCKDB` SHALL equal `"md:cianchosaint"`
- **AND** the factory SHALL use `DEFAULT_NAMESPACE = "cianchosaint"`

#### Scenario: Irish Statute Book DLT source lateralised

- **WHEN** the operator runs the BIPP v1 m1 milestone
- **THEN** the Irish Statute Book DLT source at
  `dlt_sources/cianchosaint/ireland/law/irish_statute_book.py`
  SHALL ingest every Act from `https://www.irishstatutebook.ie/eli/`
- **AND** rows SHALL land at `md:cianchosaint.ireland.statute_book.acts`
- **AND** the irish_statute_book.py file SHALL start with the LICENCE
  attribution header
  (`Original: cianfhoghlaim/cianfhoghlaim @ <commit-sha>` etc.)

### Requirement: CocoIndex env var rename + R1-R4 conformance

The system SHALL rename all CocoIndex env vars from `CIANFHOGHLAIM_*`
to `CIANCHOSAINT_*` and SHALL enforce the R1-R4 conformance contract
on every CocoIndex v1 App.

#### Scenario: Shared lifespan uses cianchosaint env vars

- **WHEN** the operator starts the CocoIndex runtime
- **THEN** the `_shared/_lifespan.py` SHALL honour
  `CIANCHOSAINT_LANCEDB_URL` (not `CIANFHOGHLAIM_LANCEDB_URL`)
- **AND** SHALL honour `CIANCHOSAINT_EMBED_MODEL` (defaulting to
  `BAAI/bge-m3`)
- **AND** the 3 ContextKeys (`LANCE_DB`, `EMBEDDER`,
  `RESOLVED_FILE_REGISTRY`) SHALL be exported from `_lifespan.py`
  only

#### Scenario: R1-R4 linter passes for all cianchosaint v1 Apps

- **WHEN** the operator runs `mise run cocoindex:conformance`
- **THEN** the linter SHALL static-AST-inspect every
  `cocoindex_flows/cianchosaint/**/` module
- **AND** SHALL pass with `ConformanceViolation` raised only for
  violations of R1 (lifespan import), R2 (no new ContextKey outside
  `_lifespan.py` without `# R2-exempt:`), R3 (`coco.App(...)` at
  module scope), or R4 (at least one `@coco.fn(`)

### Requirement: CocoIndex factory pattern for per-jurisdiction flows

The system SHALL use the factory pattern (mirroring
`cocoindex_flows/european_nations/_factory.py`) for the per-
jurisdiction CocoIndex flows in BIPP v1 (53 forces) and BIIP v1
(6 oversight bodies).

#### Scenario: BIPP v1 per-force CocoIndex flow uses the factory

- **WHEN** the operator runs `mise run cianchosaint:bipp:v1:full`
- **THEN** the factory module
  `cocoindex_flows/cianchosaint/_factory.py` SHALL instantiate 53
  per-force CocoIndex Apps (one per UK + Crown Dependency force)
- **AND** the factory SHALL produce 53 1-line re-export shims (e.g.
  `met_police_embedding`, `psni_embedding`, `garda_embedding`)
- **AND** every factory-built App SHALL conform to R1+R2+R3+R4
- **AND** the total LOC SHALL be ≤ 1,200 (vs ~7,000 if each force had
  its own module — 83% reduction)

### Requirement: Combined web app template (Q23 synthesis)

The system SHALL provide a combined web app template that synthesises
the best practices from BOTH
`web/apps/cianfhoghlaim-leaving-cert/` AND `web/apps/cianfhoghlaim-web/`,
refactored for cianchosaint's defence / policing / intel-oversight
purpose.

#### Scenario: Best of cianfhoghlaim-leaving-cert adopted

- **WHEN** the operator creates a new per-persona web app
  (`cianchosaint-ga-public/`)
- **THEN** the app SHALL adopt the per-app `packages/` structure
  (`auth`, `db`, `i18n`, `ui`, `convex`, `config`)
- **AND** SHALL adopt the per-app `baml_src/` for the BAML client
- **AND** SHALL adopt the AG-UI + CopilotKit integration pattern
  from leaving-cert
- **AND** SHALL adopt the Dockerfile + wrangler.toml deployment
  configs

#### Scenario: Best of cianfhoghlaim-web adopted

- **WHEN** the operator creates a new per-persona web app
- **THEN** the app SHALL adopt the simple `apps/web` + `apps/api` +
  `convex` + `packages` + `src` layout from cianfhoghlaim-web
- **AND** SHALL use Turbo monorepo + Biome + Bun workspace
- **AND** SHALL use Convex v1.40+ + Zod v4 dependency pins

#### Scenario: Education-specific patterns dropped

- **WHEN** the operator creates a new per-persona web app
- **THEN** the app SHALL NOT include the LC subject catalog
  components from cianfhoghlaim-leaving-cert
- **AND** SHALL NOT include the education i18n translations
- **AND** SHALL NOT include the LC subject BAML client from
  cianfhoghlaim-leaving-cert/baml_src/ireland/

### Requirement: 7 per-persona web surfaces

The system SHALL ship 7 per-persona web surfaces (1 per constituency
× 2 surfaces + the self-hosted citizen entry point).

#### Scenario: GA + MET + PSNI each have 2 surfaces

- **WHEN** the operator runs `mise run cianchosaint:web:list`
- **THEN** the list SHALL include 7 surfaces:
  `cianchosaint-ga-public/`, `cianchosaint-ga-internal/`,
  `cianchosaint-met-public/`, `cianchosaint-met-internal/`,
  `cianchosaint-psni-public/`, `cianchosaint-psni-internal/`,
  `cianchosaint-self-host/`
- **AND** each SHALL pass `openspec validate --strict`
- **AND** each SHALL have its own `Dockerfile` + `wrangler.toml` +
  `turbo.json` + `package.json`

### Requirement: 11 wholesale-copied IaC compose stacks + 2 new builds

The system SHALL provide 13 Docker Compose stacks under
`bonneagar/stacks/`: 11 wholesale-copied from Cianfhoghlaim +
2 built from scratch.

#### Scenario: 11 wholesale-copied stacks present

- **WHEN** the operator runs `ls bonneagar/stacks/`
- **THEN** the 11 wholesale-copied stacks SHALL exist:
  `litellm/`, `langfuse/`, `motherduck/`, `lakehouse/`,
  `unsloth-serve/`, `openchamber/`, `crawl4ai/`,
  `changedetection/`, `komodo/`, `pangolin/`, `infisical/`
- **AND** each SHALL have the 6-file GOLD_STANDARD pattern
  (`compose.yaml`, `sidecar.yaml`, `secrets.env`, `pangolin.yaml`,
  `blueprint.yaml`, `.env.example`)
- **AND** each SHALL validate with `mise run devops:validate-stacks`

#### Scenario: Stagehand + Locket new builds

- **WHEN** the operator runs `ls bonneagar/stacks/`
- **THEN** the 2 new-build stacks SHALL exist:
  - `stagehand/` — open-source Stagehand + headless Chrome (built
    from scratch since Cianfhoghlaim has no equivalent)
  - `locket/` — the secret-injection sidecar (built from scratch
    since Cianfhoghlaim has no equivalent)
- **AND** each SHALL have the 6-file GOLD_STANDARD pattern

### Requirement: ~25 wholesale-copied agent skills

The system SHALL wholesale-copy ~25 of the 166 Cianfhoghlaim
`.agents/skills/<skill>/SKILL.md` files, focused on the
defence / policing / intel-overshoot-relevant subset.

#### Scenario: Skill files present

- **WHEN** the operator runs `ls .agents/skills/`
- **THEN** the 25 wholesale-copied skill directories SHALL exist
  (firecrawl + browser-tools + crawl4ai + baml + cocoindex + motherduck
  + dlt + lancedb + litellm + unsloth + google-adk + tanstack-start +
  copilotkit + ag-ui + convex + hono + better-auth + infisical +
  komodo + pangolin + langfuse + mlflow + ragas + opencode + mise +
  openspec + ccc + agno + centralized-registry)
- **AND** each SHALL pass `mise run lint:skills`

### Requirement: CCC indexing setup with 12 initial concept guides

The system SHALL set up CocoIndex Code (CCC) semantic search over
the cianchosaint codebase via `.cocoindex_code/`.

#### Scenario: CCC settings file present

- **WHEN** the operator runs `bun run ccc:init`
- **THEN** `.cocoindex_code/settings.yml` SHALL be created with the
  whitelist of file extensions (Python, TypeScript, BAML, Markdown,
  etc.) and exclude patterns (`.git`, `__pycache__`, `node_modules`,
  `target`, `dist`, `.cocoindex_code`)

#### Scenario: CCC guides file ships with 12 initial guides

- **WHEN** the operator runs `bun run ccc:search "British Isles
  policing"`
- **THEN** the `.cocoindex_code/guides.yml` SHALL match the query
  against the 12 initial concept guides:
  `openspec-change-search`, `dlt-source-search`,
  `baml-function-search`, `cocoindex-flow-search`,
  `browser-tool-router-search`, `bipp-v1-policing`,
  `bidp-v1-defence`, `biip-v1-intel-oversight`,
  `firecrawl-corpus-search`, `agent-fleet-search`,
  `per-persona-web-surfaces`, `cianchosaint-pipeline-overview`

### Requirement: Slimmed mise.toml (~25 tasks, REMOVE education tasks)

The system SHALL provide a slimmed `mise.toml` (~25 tasks) that
REMOVES the education-specific tasks and ADDS the defence-specific
tasks.

#### Scenario: Education-specific tasks removed

- **WHEN** the operator runs `mise run --list`
- **THEN** the list SHALL NOT include any of: `cic:*`,
  `biep:v3:*`, `subjects:*`, the bulk of `notebooks:*`, all
  `meaisin:*`

#### Scenario: Defence-specific tasks added

- **WHEN** the operator runs `mise run --list`
- **THEN** the list SHALL include the defence-specific tasks:
  `cianchosaint:bipp:v1:m{1-3}`, `cianchosaint:bidp:v1:m{1-3}`,
  `cianchosaint:biip:v1:m{1-3}`, `cianchosaint:provider:health-check`,
  `cianchosaint:browser-tool:health-check`,
  `cianchosaint:ccc:{init,index,search}`,
  `cianchosaint:crawl4ai:smoke`, `cianchosaint:stagehand:smoke`,
  `cianchosaint:osint:health-check`

### Requirement: pyproject.toml has NO cross-repo Python source map

The system SHALL NOT declare any `[tool.uv.sources]` cross-repo
Python source map in `pyproject.toml` (per Q24 = remove).

#### Scenario: No cross-repo source map

- **WHEN** the operator reads `pyproject.toml`
- **THEN** the file SHALL NOT contain a `[tool.uv.sources]` section
- **AND** the file SHALL have a comment block documenting the
  standalone decision
- **AND** the file SHALL import only cianchosaint-local packages

### Requirement: Agents framework wholesale-copy (Google ADK + firecrawl_mcp)

The system SHALL wholesale-copy the Cianfhoghlaim Google ADK agent
framework + the firecrawl_mcp browser tool client, then REFACTOR the
firecrawl_mcp client to use the cianchosaint 4-tier
`ModelProviderRouter`.

#### Scenario: agents/adk/ framework present

- **WHEN** the operator searches `agents/adk/agent_registry.py`
- **THEN** the file SHALL exist with the cianchosaint MODEL_REGISTRY
  (52+ entries across 7 families: ocr_vision / text_llm / embedder /
  rerank / image_gen / voice / translation)
- **AND** the file SHALL pass `mise run models:list`

#### Scenario: firecrawl_mcp client refactored

- **WHEN** the operator imports `FirecrawlMCPClient`
- **THEN** the constructor SHALL accept a `provider_router:
  ModelProviderRouter` parameter (the 4-tier router)
- **AND** the LLM-using endpoints (`/extract`, `/agent`, `/research`)
  SHALL route through the provider router
- **AND** the non-LLM endpoints (`/scrape`, `/crawl`, `/search`)
  SHALL NOT route through the provider router

### Requirement: firecrawl_mcp client uses the 4-tier ModelProviderRouter

The system SHALL integrate the existing 4-tier `ModelProviderRouter`
into the firecrawl_mcp client (per the
`cianchosaint-agentic-interaction-v1` extension).

#### Scenario: Firecrawl /extract injects provider_router

- **WHEN** the operator calls
  `await FirecrawlMCPClient(...).provider_router.get_active_config()`
- **THEN** the active config SHALL include the LLM base URL + API key
  + model name
- **AND** the config SHALL match the active provider (Unsloth
  Studio by default)
- **AND** the LLM-using endpoint calls SHALL use the active config

### Requirement: 13-stacks IaC validation gate

The system SHALL provide a CI gate that validates all 13 Docker
Compose stacks against the 6-file GOLD_STANDARD pattern.

#### Scenario: Stack-doctor passes for all 13 stacks

- **WHEN** the operator runs `mise run devops:validate-stacks`
- **THEN** the linter SHALL inspect each of the 13 stacks
- **AND** SHALL pass with `ConformanceViolation` raised only for
  missing files in the GOLD_STANDARD pattern
- **AND** the exit code SHALL be 0
