# CIANCHOSAINT

> **Wordplay (canonical):** *Cianchosaint* = Irish Gaelic "cian" (long/far/longing) + "chosaint" (defence/protection) → "distant defence" / "far protection". Mirrors the structure of [cianfhoghlaim](https://github.com/cianfhoghlaim/cianfhoghlaim) = "cian" + "fhoghlaim" (learning).

**The British Isles defence / policing / intelligence-oversight open-source data platform.**

Cianchosaint is a defensive OSINT (Open-Source Intelligence) data
platform for public-sector bodies of the British Isles. It ingests
public official-government sources — government press releases,
court judgments, NAO / C&AG reports, intelligence oversight reports,
police force statistics, defence doctrine PDFs, procurement contracts,
and FOI responses — and routes them through a 4-tier model provider
chain (Unsloth Studio → LiteLLM → MiniMax → Gemini) for BAML
extraction, CocoIndex v1 embedding, LanceDB + DuckLake storage, and
per-persona TanStack Start + Convex + AG-UI + CopilotKit dashboards.

## Why does this exist?

Two reasons.

**First — equalisation.** British Isles public-sector bodies should
not have to negotiate a bespoke licence with a vendor every time they
want to ingest their own country's official statistics. This platform
ships a permissive-internal BUSL-1.1 grant covering every governmental
body of the Republic of Ireland, the United Kingdom of Great Britain
and Northern Ireland (including the devolved administrations of
Scotland, Wales, and Northern Ireland), and the Crown Dependencies
(Jersey, Guernsey, Isle of Man).

**Second — open-source SOTA is good enough.** The platform is a case
study that proves the open-source SOTA stack (Unsloth Studio for local
fine-tuning, HuggingFace for OCR/VLM/embedding, LiteLLM + MiniMax +
Gemini as fallback, BAML for typed extraction, CocoIndex v1 for
embeddings, LanceDB + DuckLake + MotherDuck for storage, Dagster for
orchestration, TanStack Start + Convex + AG-UI + CopilotKit for
dashboards) is sufficient for British Isles official government use.
Without this stack, public-sector teams fall behind well-funded
organised crime groups that can afford proprietary AI; with this
stack, they have parity.

## The 3 flagship verticals

| Vertical | Sub-domains | Cohorts |
|---|---|---:|
| **BIPP v1** — British Isles Policing Pipeline | 14 forces × 7 domains (street crime, stop & search, outcomes, ASB, workforce, FOI, press releases) | 392 |
| **BIDP v1** — British Isles Defence Pipeline | 4 UK services + Irish DF + UK MoD + 2 doctrine series + procurement + 8 service-level doctrinal categories | 64 |
| **BIIP v1** — British Isles Intelligence Oversight Pipeline | 6 oversight bodies × 8 document kinds | 48 |

**Total: 504 cohorts** across 8 sub-nations + UK-wide + Crown Dependencies.

## The 4-tier model provider chain

Every LLM-touching surface in cianchosaint routes through
`ModelProviderRouter` (`baml_src/_shared/provider_router.py`) with a
30-second timeout per provider and a 3-strike circuit-breaker:

| Tier | Provider | URL | Why |
|---|---|---|---|
| 1 (PRIMARY) | Unsloth Studio (local API) | `http://unsloth-serve:8889/api/v1` (Pangolin ingress later) | Self-hosted, audited, no egress |
| 2 | LiteLLM Proxy | `https://litellm.cianfhoghlaim.ie` | Existing fallback |
| 3 | MiniMax Token Plan | `https://api.minimax.io/v1` | Direct, metered |
| 4 (LAST RESORT) | Gemini API | `https://generativelanguage.googleapis.com/v1beta` | Universal fallback |

## The licence

This repository is licensed under **Business Source License 1.1 — CIANCHOSAINT edition** (see `LICENSE.md`). The licence:

- Grants broad production use to every governmental body of the Republic of Ireland, the United Kingdom, and the Crown Dependencies
- Bans commercial use, foreign use (without satisfying the 3-step gate), academic / cultural / journalistic / research use, and Person-of-Interest data
- Grants a **warrant-to-enforce** to every licencee named in the Additional Use Grant, triggered by either publicly observable evidence OR a credible written complaint

The licence is the load-bearing architectural constraint. Every design
decision is subordinate to it.

## The 7 per-persona web surfaces

| Persona | App | Primary value |
|---|---|---|
| Active Garda member | `web/apps/cianchosaint-garda/` | PULSE-aware search of CSO crime stats + statutory instruments + Dáil/Seanad justice debates |
| Active PSNI officer | `web/apps/cianchosaint-psni/` | Cross-border queries with Garda + APP search + NI-specific law |
| Irish Defence Forces member | `web/apps/cianchosaint-idf/` | White Paper on Defence + capability docs + Irish DF doctrine |
| UK MoD policy analyst | `web/apps/cianchosaint-mod/` | JSP/JDP doctrine index + Global Strategic Trends + NAO defence reports |
| MI5 / SIS / GCHQ engineer | `web/apps/cianchosaint-intel-oversight/` | ISC reports + IPT decisions + IPCO reports + RIPA evidence |
| Welsh / English / Scottish police analyst | `web/apps/cianchosaint-policing/` | data.police.uk + force-level + cross-force comparisons + FOI mining |
| NI Justice practitioner | `web/apps/cianchosaint-ni-justice/` | NICTS judgments + NI legislation + justice-ni.gov.uk press |

## OpenSpec

This repository uses [OpenSpec](https://github.com/Fission-AI/OpenSpec)
for spec-driven change management. Every non-trivial change lives in
`openspec/changes/<id>/` as a 3-artifact bundle (`proposal.md` +
`tasks.md` + spec deltas) before any code is written.

```bash
openspec list --specs                   # list all capability specs
openspec list                           # list all pending changes
openspec validate <change-id> --strict  # MUST pass before commit
openspec archive <change-id> --yes      # after deploy
```

## Repo boundary

| Domain | Location |
|:--|:--|
| Data platform (DLT + Dagster + BAML + CocoIndex + MotherDuck + marimo) | `dlt_sources/`, `orchestration/`, `baml_src/`, `cocoindex_flows/`, `notebooks/` |
| Agent fleet (12-agent + per-persona routing) | `agents/` |
| Per-persona web surfaces (TanStack Start + Convex + AG-UI + CopilotKit) | `web/apps/<persona>/` |
| OpenSpec changes + specs | `openspec/` |
| MotherDuck Dives / Flights metadata | `motherduck/` |
| IaC (Komodo + Pangolin + Infisical clients) | `bonneagar/iac/` |
| Docker Compose stacks | `bonneagar/stacks/<name>/` |

## Cross-repo convention

Cianchosaint is a **sibling repo** to `cianfhoghlaim/cianfhoghlaim`
(the education / long-distance learning platform). The two repos share
the openspec workflow, the 14-layer knowledge sync loop, the 5
opencode subagents, the Infisical `dev-baile` vault (cianchosaint has
its own `cianchosaint/` folder), and the Lakehouse stack.

The two repos diverge on domain (education vs defence / policing /
intel oversight), licence (broader cultural grant vs tighter
British-Isles-only OSINT grant with warrant-to-enforce), and provider
chain (LiteLLM-primary vs Unsloth Studio primary + 3-tier fallback).

## Cross-references

- [`LICENSE.md`](LICENSE.md) — the load-bearing legal document
- [`AGENTS.md`](AGENTS.md) — the canonical agent routing
- [`openspec/AGENTS.md`](openspec/AGENTS.md) — the openspec workflow
- [`openspec/changes/cianchosaint-repo-foundation-v1/`](openspec/changes/cianchosaint-repo-foundation-v1/) — the first openspec change
- [`openspec/specs/cianchosaint-pipeline/spec.md`](openspec/specs/cianchosaint-pipeline/spec.md) — the umbrella capability spec
