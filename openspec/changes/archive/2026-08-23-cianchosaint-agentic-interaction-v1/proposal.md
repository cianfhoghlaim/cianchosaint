# Change: cianchosaint-agentic-interaction-v1

## Why

Two problems converged on 2026-08-23:

1. **British Isles public-sector bodies have no open-source agentic
   interaction layer for OSINT** — every force (An Garda Síochána,
   MET, PSNI, the 4 Welsh forces, the devolved administrations, the
   Crown Dependencies) currently operates its own bespoke tooling or
   relies on proprietary AI vendors. There is no shared, auditable,
   sovereign-capability agentic stack that mediates access to
   irishstatutebook.ie, courts.ie, data.police.uk, psni.police.uk,
   met.police.uk, gov.uk, etc.

2. **Members of the British Isles public cannot interact
   conversationally with their own government's OSINT sources** —
   every citizen-facing interface (garda.ie, met.police.uk,
   psni.police.uk) is a bottom-up form-filling exercise with no
   conversational layer. The Gemini hackathon experience from
   Cianfhoghlaim demonstrated that Google ADK + Convex + AG-UI +
   CopilotKit can deliver a tutor-grade agentic experience to
   end-users; this pattern needs to lateralise to the defence /
   policing / intelligence-oversight domain.

The user explicitly asked (verified 2026-08-23): *"make sure you
prioritise the integration of the existing pipelines and features
within our BONNEAGAR stacks browser docker compose combination of open
source software is like CRAWL4AI and stagehand which can be used
with different AI API combining with not only are already implemented
fallback of Unsloth studio and light LLM and our minimax token plan
but also then easily transferable to what others may happen to be
using like Gemini cloud API"*.

The overarching purpose: help the public + defence + intelligence +
law-enforcement public servants reduce burnout + barrier of entry +
simplify processes. *"in this day and age are very easily done
identically that will help would help things happen on bulk and
things like that that help use the already existing infrastructure to
reduce workload in a similar way as we were prioritising for
teachers and students and parents in the education system to be able
to do for those types of users"*.

## What changes

- **3 new capability specs** under `openspec/specs/`:
  - `cianchosaint-agentic-interaction/` — the umbrella capability
    (Google ADK + 4-tier provider chain + BrowserToolRouter + AG-UI)
  - `cianchosaint-self-hosted-citizen/` — self-hosted citizen Docker
    Compose bundle + Locket + private Pangolin + per-tenant Infisical
  - `cianchosaint-per-constituency-agents/` — GA / MET / PSNI root
    agents + 15 specialists (5 per constituency) + 7 cross-constituency
    form-filling tools

- **6 new Requirements** in the `cianchosaint-agentic-interaction`
  spec (see `specs/cianchosaint-agentic-interaction/spec.md`):
  1. Agentic interaction layer (Google ADK + 4-tier provider chain)
  2. Form-filling agents (Google ADK FunctionTool)
  3. Lateralised GA + irishstatutebook.ie + courts.ie pipelines
  4. MET + PSNI new pipelines
  5. Lateralised AG-UI + CopilotKit web surface
  6. Self-hosted citizen Docker image

- **6 new Requirements** in the
  `cianchosaint-self-hosted-citizen` spec (4 Requirements, 4 Scenarios)

- **6 new Requirements** in the
  `cianchosaint-per-constituency-agents` spec (6 Requirements, 7
  Scenarios — GA root + 5 specialists, MET root + 5 specialists,
  PSNI root + 5 specialists, 7 cross-constituency tools)

- **Cross-repo mirror pattern** — the Cianfhoghlaim legal pipelines
  (irishstatutebook.ie + courts.ie + 5 BAML files + Ireland legal
  CocoIndex embedding) are **mirrored**, not migrated wholesale, to
  the cianchosaint repo. Cianfhoghlaim retains ownership for
  education use; cianchosaint references them via `pyproject.toml`
  `[tool.uv.sources]` entries.

## Impact

- Affected specs: 3 NEW specs in cianchosaint
  (`cianchosaint-agentic-interaction`,
  `cianchosaint-self-hosted-citizen`,
  `cianchosaint-per-constituency-agents`). Cianfhoghlaim's
  `official-media-pipeline` spec is unchanged.

- Affected code/config (cianchosaint side):
  - `agents/cianchosaint/` — 24 new Google ADK agent files (3 root +
    15 specialist + 6 module init)
  - `agents/cianchosaint/tools/` — 7 new FunctionTool files
  - `baml_src/cianchosaint/processing/` — 3 new BAML files
    (met_police.baml, psni.baml, garda_traffic.baml)
  - `baml_src/_shared/browser_tool_router.py` — the BrowserToolRouter
  - `baml_src/_shared/browser_tool_config.py` — per-deployment config
  - `dlt_sources/cianchosaint/` — 9 new DLT sources (MET + PSNI +
    GA traffic + lateralised legal)
  - `web/apps/cianchosaint-{ga,met,psni,ga-internal,met-internal,psni-internal,self-host}/`
    — 7 new web apps
  - `docker/cianchosaint-citizen/` — the self-hosted Docker Compose
    bundle

- Affected code/config (cianfhoghlaim side):
  - `baml_src/british_isles/ireland/education/law/` is **unchanged**
    (mirror pattern — Cianfhoghlaim keeps ownership)
  - `dlt_sources/british_isles/ireland/law/` is **unchanged**
  - Cross-repo openspec dependency: cianchosaint consumes the
    Cianfhoghlaim legal pipelines via `pyproject.toml`
    `[tool.uv.sources]` (a Python-native cross-repo source map)

- No secret values are written to disk: all keys resolve via
  `infisical://dev-baile/cianchosaint/...` template refs hydrated by
  mise + Locket.

## Out of scope

- The actual implementation of the 24 Google ADK agent files (P1a
  follow-up work).
- The 9 new DLT sources (P1a-P2b follow-up work).
- The 7 new web apps (P1a-P3 follow-up work).
- The self-hosted citizen Docker image build (P3 follow-up work).
- Retrofitting the `BrowserToolRouter` into Cianfhoghlaim's
  `firecrawl_mcp/client.py` (separate follow-up change
  `firecrawl-mcp-browser-tool-router-integration-v1` per the
  cross-repo mirror pattern).
- The license amendment for citizen use (separate follow-up
  `cianchosaint-citizen-use-grant-v1`).

## Dependencies

`Blocked by: cianchosaint-repo-foundation-v1` (the foundation must
archive first so that the 4-tier ModelProviderRouter contract is
locked).
`Blocked by (soft): cianfhoghlaim/cianfhoghlaim@official-media-pipeline`
(the legal pipelines must remain in Cianfhoghlaim for cianchosaint
to mirror them).
`Affected repos: cianchosaint, cianfhoghlaim.`

## Cross-repo sync

See [`cross-repo-sync.md`](./cross-repo-sync.md) for the commit plan
+ branch + push target for each repo + the order of operations
(cianfhoghlaim unchanged; cianchosaint imports + archives this
change).
