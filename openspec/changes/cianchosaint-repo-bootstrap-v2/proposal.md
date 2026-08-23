# Change: cianchosaint-repo-bootstrap-v2

## Why

The `cianchosaint` repo foundation (`cianchosaint-repo-foundation-v1`) and the agentic-interaction layer (`cianchosaint-agentic-interaction-v1`) established the **spec contracts** + the **4-tier provider chain** + the **BUSL-1.1 v2 licence** + the **per-constituency agents** + the **self-hosted citizen** capability. The **physical code** for these capabilities — DLT sources, BAML schemas, CocoIndex flows, Google ADK agents, the firecrawl_mcp browser tool client, the web app framework, the IaC compose stacks, the agent skills, the CCC indexing setup — has not yet been authored.

Three problems converged on 2026-08-23:

1. **Cianchosaint is a STANDALONE iteration of the project.** It does not depend on Cianfhoghlaim at runtime. The previous plan's `[tool.uv.sources]` cross-repo Python source map (added in `cianchosaint-agentic-interaction-v1`) is **reverted** by this change. The relevant Cianfhoghlaim assets must be wholesale-copied into Cianchosaint, then renamed to the `cianchosaint` namespace and refactored for the defence / policing / intelligence-oversight domain.

2. **The combined web app template** must synthesise the **best practices** from BOTH `web/apps/cianfhoghlaim-leaving-cert/` (the heavier template — AG-UI + CopilotKit + Convex + per-app `packages/`) AND `web/apps/cianfhoghlaim-web/` (the simpler template — Turbo monorepo + apps/web + apps/api), then **refactor** for Cianchosaint's purpose. Neither source should be copied verbatim; the synthesis is the deliverable.

3. **CCC indexing must be set up for Cianchosaint's own code** so agents can semantic-search the cianchosaint codebase. This means `.cocoindex_code/settings.yml` + `.cocoindex_code/guides.yml` (with ~10-12 initial concept guides specific to defence / policing / intel oversight) + the `ccc:init`, `ccc:index`, `ccc:search` mise tasks + the `scripts/init_ccc.sh` setup script + the `scripts/lint_ccc_freshness.sh` CI gate.

The user explicitly clarified (verified 2026-08-23):
- *"ensure that we are also prioritising the fact that this CIANCHOSAINT repository is a new iteration of our project that works independently from other projects"*
- *"we would have a much simpler MISE.TOML without the education task commands but now we have defence software pipelines"*
- *"the stub of the full feature-rich aspects of some pipelines for certain legal websites and previous implementation of official media sources of government branches and intelligence agencies somewhere in Cianfhoghlaim"*
- *"as part of this plant agent you should use our CCC indexing as outline previously"*

## What changes

**ONE monolithic openspec change** (per Q21 = b) that supersedes both `cianchosaint-repo-foundation-v1` and `cianchosaint-agentic-interaction-v1`. The change is structured as a 5-spec-delta bundle (4 existing specs + 1 new spec) + a brand-new `cianchosaint-bootstrap-v2` umbrella spec.

- **1 new spec** (`cianchosaint-bootstrap-v2/`) — the wholesale-copy umbrella, 13 Requirements covering: data platform wholesale-copy, agents framework wholesale-copy, web framework wholesale-copy, IaC wholesale-copy, skills wholesale-copy, CCC indexing setup, combined web app template, renamed DLT destinations factory, renamed CocoIndex env vars, factory pattern for per-jurisdiction CocoIndex flows, R1-R4 conformance contract, per-persona web surfaces (the 7 apps), Stagehand + Locket new stacks.

- **4 spec deltas** to existing specs:
  - `cianchosaint-pipeline/spec.md` — minor extension (add the wholesale-migration manifest + the renamed destinations factory contract + the 11-stacks count)
  - `cianchosaint-agentic-interaction/spec.md` — extension (add the BrowserToolRouter module spec + the 4-tier provider chain integration into browser tools)
  - `cianchosaint-self-hosted-citizen/spec.md` — extension (add the Stagehand + Locket stack requirements)
  - `cianchosaint-per-constituency-agents/spec.md` — extension (add the 7 per-persona web surfaces requirement + the cross-constituency FunctionTool coverage)

- **~15,000 LOC of wholesale-copied code** (renamed to `cianchosaint` namespace):
  - DLT layer: `dlt_sources/common/*` (~3,000 LOC) + `dlt_sources/british_isles/_cross/*` (~1,200 LOC) + `dlt_sources/british_isles/ireland/law/*` (~800 LOC) + `dlt_sources/official_media_cianchosaint/*` (~2,000 LOC)
  - BAML layer: 5 Ireland-law BAML files + shared_legal_enums.baml + rewritten clients.baml + clients_cianchosaint.py (~1,500 LOC)
  - CocoIndex layer: `_shared/_lifespan.py` + 6 helpers + 3 Ireland legal embedding flows (~1,200 LOC)
  - Agents layer: `agents/adk/*` + `agents/meaisinfhoghlaim/firecrawl_mcp/*` + `agents/agent_registry.py` + 24 new per-constituency agents (~2,500 LOC)
  - Web layer: `web/packages/{ui-kit,auth,db}/*` + 7 new per-persona web apps synthesised from both Cianfhoghlaim templates (~5,000 LOC)
  - IaC layer: 11 wholesale-copied stacks (`litellm/`, `langfuse/`, `motherduck/`, `lakehouse/`, `unsloth-serve/`, `openchamber/`, `crawl4ai/`, `changedetection/`, `komodo/`, `pangolin/`, `infisical/`) + 2 new builds (`stagehand/`, `locket/`) (~3,000 LOC across the 13 stacks)

- **~25 wholesale-copied SKILL.md files** mirroring Cianfhoghlaim's `.agents/skills/` SKILL.md surface (firecrawl, browser-tools, baml, cocoindex, motherduck, dlt, lancedb, litellm, unsloth, google-adk, agno, tanstack-start, copilotkit, ag-ui, convex, hono, better-auth, infisical, komodo, pangolin, langfuse, mlflow, ragas, openspec, opencode, mise, ccc, firecrawl-search, crawl4ai, ag-ui, agent-observability, agent-memory-systems, dlthub, centralized-registry)

- **CCC indexing setup** at `.cocoindex_code/`:
  - `.cocoindex_code/settings.yml` (refactored from Cianfhoghlaim's pattern)
  - `.cocoindex_code/guides.yml` with 10-12 initial concept guides (`openspec-change-search`, `dlt-source-search`, `baml-function-search`, `cocoindex-flow-search`, `browser-tool-router-search`, `bipp-v1-policing`, `bidp-v1-defence`, `biip-v1-intel-oversight`, `firecrawl-corpus-search`, `agent-fleet-search`, `per-persona-web-surfaces`, `cianchosaint-pipeline-overview`)
  - `mise.toml` adds `ccc:init`, `ccc:index`, `ccc:search` tasks
  - `scripts/init_ccc.sh` + `scripts/lint_ccc_freshness.sh` (NEW)

- **The slimmed `mise.toml`** (~25 tasks, down from ~60 in Cianfhoghlaim):
  - REMOVE: `cic:*` (author-archive DLT targets), `biep:v3:*` (BIEP milestones), `subjects:*` (NCCA subject specialists), most `notebooks:*` tasks, all `meaisin:*` tasks
  - KEEP: `core:*` (dev env), `lint:*` (openspec + licence + drift + skills), `sync:*` (14-layer knowledge sync loop), `openspec:*`
  - ADD: `cianchosaint:bipp:v1:m{1-3}` (British Isles Policing Pipeline milestones), `cianchosaint:bidp:v1:m{1-3}` (Defence), `cianchosaint:biip:v1:m{1-3}` (Intel Oversight), `cianchosaint:provider:health-check`, `cianchosaint:browser-tool:health-check`, `cianchosaint:ccc:{init,index,search}`, `cianchosaint:crawl4ai:smoke`, `cianchosaint:stagehand:smoke`, `cianchosaint:osint:health-check`

- **The pyproject.toml `[tool.uv.sources]` block is REVERTED** (per Q24 = remove). Cianchosaint is standalone; no cross-repo Python imports.

## Impact

- Affected specs: 1 NEW spec (`cianchosaint-bootstrap-v2/`) + 4 MODIFIED specs (`cianchosaint-pipeline/`, `cianchosaint-agentic-interaction/`, `cianchosaint-self-hosted-citizen/`, `cianchosaint-per-constituency-agents/`).
- Affected code/config: ~15,000 LOC of new code, all under `dlt_sources/`, `baml_src/`, `cocoindex_flows/`, `agents/`, `web/`, `bonneagar/stacks/`, `.agents/skills/`, `.cocoindex_code/`, plus the slimmed `mise.toml` + simpler `pyproject.toml` + 4 new scripts.
- Supersedes: `cianchosaint-repo-foundation-v1` and `cianchosaint-agentic-interaction-v1` (their spec deltas are subsumed into this change).
- No secret values are written to disk: all keys resolve via `infisical://dev-baile/cianchosaint/...` template refs hydrated by mise + Locket.

## Out of scope

- The actual IMPLEMENTATION of the BIPP v1 / BIDP v1 / BIIP v1 verticals (the ~60 DLT sources + ~24 Google ADK agent files) — covered by follow-up P1+ openspec changes that Block by this change.
- The Pantheon / 94-stack migration of Cianfhoghlaim's existing compose stacks (this change copies the 11 relevant ones wholesale).
- The 8 NCCA subject specialist agents (`agents/tuatha/{chem,engl,hist,...}_agent.py`) — DROPPED; the PATTERN they implement is replicated as `agents/cianchosaint/{ga,met,psni}_specialists/*_agent.py` in a follow-up change.
- Retrofitting Cianfhoghlaim's `firecrawl_mcp/client.py` to use the 4-tier `ModelProviderRouter` (separate follow-up `firecrawl-mcp-browser-tool-router-integration-v1` in Cianfhoghlaim).
- The license amendment for citizen use (separate follow-up `cianchosaint-citizen-use-grant-v1`).
- The Pangolin ingress for Unsloth Studio (separate `unsloth-studio-pangolin-ingress-v1` in bonneagar).

## Dependencies

`Blocked by: cianchosaint-repo-foundation-v1` (must archive first).
`Blocked by: cianchosaint-agentic-interaction-v1` (must archive first).
`Blocked by (soft): cianfhoghlaim/cianfhoghlaim` (source of wholesale-copied assets; Cianfhoghlaim itself does not need to change for this — only its files are read).
`Affected repos: cianchosaint.` (Cianfhoghlaim is NOT modified.)

## Cross-repo sync

See [`cross-repo-sync.md`](./cross-repo-sync.md) — this change touches ONLY the `cianchosaint` repo. Cianfhoghlaim remains unchanged.

After this change lands:
- Cianfhoghlaim's `dlt_sources/british_isles/ireland/law/*`, `baml_src/british_isles/ireland/education/law/*`, `cocoindex_flows/british_isles/ireland/*`, `agents/adk/*`, `agents/meaisinfhoghlaim/firecrawl_mcp/*`, `web/packages/{ui-kit,auth,db}/*`, `web/apps/cianfhoghlaim-leaving-cert/*`, `web/apps/cianfhoghlaim-web/*`, `bonneagar/stacks/{litellm,langfuse,...}/*`, `.agents/skills/*` — all continue to serve Cianfhoghlaim's education use UNCHANGED.
- Cianchosaint has its own copies (wholesale-copied + renamed + refactored) that serve its defence / policing / intel-oversight use INDEPENDENTLY.
