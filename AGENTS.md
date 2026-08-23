# CIANCHOSAINT — Agent Routing

> **Wordplay (canonical):** *Cianchosaint* = Irish Gaelic "cian" (long/far/longing) + "chosaint" (defence/protection) → "distant defence" / "far protection". Mirrors *Cianfhoghlaim* = "cian" + "fhoghlaim" (learning).
>
> **Scope (per `LICENSE.md`):** OSINT-only British Isles defence / policing / intelligence-oversight data platform. **Strictly restricted** to public-sector bodies of the Republic of Ireland, the United Kingdom of Great Britain and Northern Ireland, the Crown Dependencies (Jersey, Guernsey, Isle of Man), and their respective defence, security, intelligence, and policing bodies. Foreign use requires satisfaction of the 3-step gate (Explain → Do us a favour → Maybe). The warrant-to-enforce is held by every licencee named in `LICENSE.md § Additional Use Grant`.

## Priority quick reference

### What cianchosaint IS

- A sibling repo to `cianfhoghlaim/cianfhoghlaim` (the education / long-distance learning platform)
- A defensive OSINT pipeline: ingest public official-government sources (CSO Ireland, data.police.uk, gov.uk, MoD corporate reports, court judgments, NAO/C&AG reports, Public Inquiries, ISC/IPC/IPT reports) → BAML extraction → CocoIndex v1 embeddings → LanceDB + DuckLake + MotherDuck → TanStack Start + Convex + AG-UI + CopilotKit dashboards for per-persona analysts
- A case study that proves open-source SOTA (Unsloth Studio + LiteLLM + MiniMax + Gemini + HuggingFace) is sufficient for British Isles official government use
- A defensible answer to the question: *"why are we behind organised criminals who can afford proprietary AI?"*

### What cianchosaint IS NOT

- A platform for classified data (Official-Sensitive or above). The DLT sources are URL-allowlisted; CI gates on asset_check per source.
- A platform for foreign intelligence agencies. `LICENSE.md` explicitly bans them.
- A platform for academic / cultural / journalistic / research use. Use `cianfhoghlaim/cianfhoghlaim` for those purposes.
- A CLI for ingesting Person-of-Interest data. The OSINT ceiling is enforced at the source-URL allowlist layer.

## Routing table — "where do I do X in cianchosaint?"

| I want to... | Look at... |
|:--|:--|
| Add a new DLT source for a British Isles official source | `dlt_sources/cianchosaint/<vertical>/<jurisdiction>/<source>.py` — mirror the existing `dlt_sources/official_media/<sub>/sources.py` pattern |
| Add a new BAML extraction function | `baml_src/cianchosaint/processing/official_media.baml` (extend) or `baml_src/cianchosaint/processing/<new>.baml` (new file) |
| Configure the 4-tier provider chain | `baml_src/clients.baml` + `baml_src/_shared/provider_router.py` |
| Add a new per-persona web surface | `web/apps/cianchosaint-<persona>/` — TanStack Start + Convex + AG-UI + CopilotKit |
| Add a new openspec change | `openspec/changes/<change-id>/{proposal.md, tasks.md, cross-repo-sync.md}` + `openspec/changes/<change-id>/specs/<spec-name>/spec.md` |
| Add a new capability spec | `openspec/specs/<spec-name>/spec.md` + sibling `AGENTS.md` (≤30 lines) |
| Run the openspec validation gate | `openspec validate <change-id> --strict` (MUST pass before commit) |
| Run the licence audit | `mise run lint:license` (NEW) — verifies every DLT source URL is in the OSINT allowlist AND every allowlist entry points at a British Isles body |
| Run the provider health check | `mise run cianchosaint:provider:health-check` (NEW) — pings each of the 4 providers, returns health table |

## Cross-repo convention

Cianchosaint is a sibling repo to `cianfhoghlaim/cianfhoghlaim`. The two repos share:

- The openspec workflow (same `openspec/` layout, same `spec-driven` schema, same `proposal.md` + `tasks.md` + spec delta format)
- The 14-layer knowledge sync loop (per the `knowledge-sync-loop` spec — adopted into cianchosaint P0)
- The 5 dispatchable opencode subagents (`data-platform`, `infrastructure`, `agent-platform`, `frontend-apps`, `research`)
- The `mise.toml` task namespace convention
- The Infisical `dev-baile` vault (cianchosaint lives in its own `cianchosaint/` folder within the vault)
- The MotherDuck + Lakehouse + LanceDB stack (cianchosaint uses the `md:cianchosaint` database namespace, parallel to `md:cianfhoghlaim`)

The two repos diverge on:

- Domain (education vs defence/policing/intel oversight)
- Licence (Cianfhoghlaim: broader cultural grant; Cianchosaint: tighter British-Isles-only OSINT grant with warrant-to-enforce)
- Persona surfaces (Cianfhoghlaim: students + teachers + parents; Cianchosaint: government analysts)
- Provider chain (Cianfhoghlaim: LiteLLM-primary; Cianchosaint: Unsloth Studio primary + 3-tier fallback)

Cross-repo changes use the `cross-repo-sync.md` convention — see `openspec/changes/cianchosaint-repo-foundation-v1/cross-repo-sync.md` for the wholesale-migration plan.

## Priority mise tasks (cianchosaint ns.)

```bash
# P1a — Policing Pipeline
mise run cianchosaint:bipp:v1:m1         # Ireland ROI (An Garda Síochána) — 14 cohorts
mise run cianchosaint:bipp:v1:m2         # UK-wide (data.police.uk + 43 forces) — 392 cohorts
mise run cianchosaint:bipp:v1:m3         # Crown Dependencies — 21 cohorts

# P1b — Defence Pipeline
mise run cianchosaint:bidp:v1:m1        # UK MoD + RAF + RN + Army — 32 cohorts
mise run cianchosaint:bidp:v1:m2        # Irish Defence Forces — 16 cohorts
mise run cianchosaint:bidp:v1:m3        # Doctrine series (JSP/JDP/AP/BR) — 16 cohorts

# P1c — Intelligence Oversight Pipeline
mise run cianchosaint:biip:v1:m1        # UK ISC + IPCO + IPT — 24 cohorts
mise run cianchosaint:biip:v1:m2        # ROI oversight bodies — 12 cohorts
mise run cianchosaint:biip:v1:m3        # NI Policing Board + Garda Inspectorate — 12 cohorts

# Cross-cutting
mise run cianchosaint:provider:health-check   # 4-tier provider health
mise run lint:license                          # OSINT allowlist + British Isles body check
mise run openspec:validate                     # CI gate for all openspec changes
```

## Skill pointers

- `openspec` — the openspec workflow (see `.agents/skills/openspec/SKILL.md`)
- `motherduck` — the MotherDuck storage pattern
- `ccc` — semantic code search
- `firecrawl` — live web scraping for OSINT refresh

## The 5 opencode subagents

This repo mirrors Cianfhoghlaim's 5 functional subagents (`data-platform`, `infrastructure`, `agent-platform`, `frontend-apps`, `research`) plus 1 new cianchosaint-specific subagent:

| Subagent | Skill filter | When to dispatch |
|:--|:--|:--|
| `data-platform` | 16 skills | DLT + Dagster + BAML + CocoIndex + MotherDuck + marimo tasks |
| `infrastructure` | 16 skills | Komodo + Pangolin + Locket + Infisical + 94-stack IaC |
| `agent-platform` | 24 skills | BAML + LiteLLM + Langfuse + MLflow + RAGAS + Graphiti + Cognee + 12-agent fleet |
| `frontend-apps` | 21 skills | TanStack Start + Convex + Hono + CopilotKit + AG-UI + marimo + Babylon.js |
| `research` | 12 skills | BrowserBase + Firecrawl + CCC + Cognee + change-detection |
| **`cianchosaint-per-persona`** | NEW | Persona surfaces + per-British-Isles-sub-nation routing |

## DO NOT

- Ingest a source URL outside the OSINT allowlist. The DLT source layer MUST refuse to add an unallowlisted URL.
- Allow foreign intelligence agency access without satisfying the 3-step gate (`LICENSE.md` § Conditional foreign use).
- Treat person-of-interest data as in-scope. OSINT only.
- Bypass the openspec validation gate. `openspec validate --strict` MUST pass before commit.
- Use LiteLLM-primary in production. Unsloth Studio is the primary provider; LiteLLM is fallback #1 only.

## The licence is the load-bearing constraint

Every architectural decision in cianchosaint is subordinate to the
licence in `LICENSE.md`. If a decision would violate the licence, the
decision is wrong. If a decision would require a licence amendment,
the decision is wrong. The licence is the contract between the
Licensor and every British Isles public-sector body that depends on
this platform.
