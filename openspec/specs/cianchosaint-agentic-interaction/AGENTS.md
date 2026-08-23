# `cianchosaint-agentic-interaction` — Agent Routing

> `cianchosaint-agentic-interaction` is the umbrella capability for the agentic interaction layer — Google ADK + 4-tier provider chain + BrowserToolRouter + AG-UI + per-constituency specialists.

## Routing

Load this AGENTS.md when the parent spec (`./spec.md`) is in scope.
Use it to find the most relevant mise tasks + skills + adjacent files
without re-reading the full spec.

## Quick start

```bash
# 1. Validate the umbrella spec
openspec validate cianchosaint-agentic-interaction --strict

# 2. Run a constituent agent locally (after the Google ADK agents are implemented)
mise run cianchosaint:ga-agent:dev
mise run cianchosaint:met-agent:dev
mise run cianchosaint:psni-agent:dev

# 3. Health check the 4-tier provider chain + browser tool chain
mise run cianchosaint:provider:health-check
mise run cianchosaint:browser-tool:health-check
```

## Key sources

- `openspec/specs/cianchosaint-agentic-interaction/spec.md` — the canonical umbrella spec
- `agents/cianchosaint/` — the per-constituency Google ADK agents
- `baml_src/_shared/provider_router.py` — the 4-tier ModelProviderRouter
- `baml_src/_shared/browser_tool_router.py` — the BrowserToolRouter
- `LICENSE.md` (repo root) — the load-bearing legal document

## Adjacent specs

- `openspec/specs/cianchosaint-pipeline/spec.md` — the data pipeline umbrella
- `openspec/specs/cianchosaint-self-hosted-citizen/spec.md` — self-hosted deployment pattern
- `openspec/specs/cianchosaint-per-constituency-agents/spec.md` — per-constituency agents
- Cianfhoghlaim's `agents/adk/` — the Google ADK pattern (mirror this)

## DO NOT

- Submit forms directly to operational systems (PULSE, crime-recording databases). The OSINT ceiling is licence-level codified.
- Use Personal Data in any cianchosaint agent. OSINT only.
- Ingest a source URL outside the `osint_allowlist.yaml` allowlist.
- Route around the 4-tier ModelProviderRouter. Even citizen self-host goes through it.
- Use Stagehand + BrowserBase in self-hosted citizen image without explicit opt-in (BrowserBase is SaaS).

## Skill pointers

- `ccc` — for semantic code search across the spec's implementation
- `openspec` — for the spec change workflow
- `motherduck` — for the storage layer
- `firecrawl` — for live web scraping of OSINT sources
- `browser-tools` — for the browser tool router (Crawl4AI / Stagehand / Firecrawl)
- `google-adk` — for the Google ADK agent pattern (already in Cianfhoghlaim)

<!-- generated: 2026-08-23; do not hand-edit -->
