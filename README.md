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

**Disclaimer** In future (2 years): I will create software available to cianchosaint users similar in scope and purpose to past projects outlined by His Majesty's Government Communication Centre https://co-creation.hmgcc.gov.uk/. There is no reason for those users to wait for me to build their internal versions.

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

## HMGCC + GCHQ + NCSC + UKRI + Imperial College integration

The platform integrates with 7 GCHQ + HMGCC + NCSC + UKRI + Imperial College open-source projects (wholesale-copied from `hmgcc/`). These integrations eliminate the burden of building custom UI components + ML model registries + graph databases + data processing pipelines + data analysis tools + device security standards + TRL assessment from scratch.

### Integrations

| Integration | Source | License | What it does |
|---|---|---|---|
| **ic-ui-kit** | MI6 + GCHQ + MI5 + HMGCC | OGLv3 + MIT | The UK Intelligence Community UI Kit — the `ic-classification-banner` (top of every page), `ic-top-navigation`, `ic-search-bar`, `ic-data-table`, `ic-tab-group`, `ic-drawer`, `ic-card-vertical`, `ic-footer`, `ic-footer-link` are adopted in the 8 ciafagent-* web apps (`web/packages/ciafagent-ui-kit/src/`). |
| **Bailo** | GCHQ | Apache 2.0 | The ML model registry — the 4-tier provider chain models (Unsloth Studio / LiteLLM / MiniMax Token Plan / Gemini API) are registered in Bailo for provenance + approvals + access control + audit trails. The `ModelProviderRouter.get_active_config()` method gates every LLM call on the Bailo provenance + access control. |
| **Gaffer** | GCHQ | Apache 2.0 (archived but still usable) | The graph database framework — the cross-source relationship graph (which source URL cross-references which other source URL) is stored in Gaffer. The 5 relationship types are: `source_cites_source`, `source_financed_by`, `source_oversees_source`, `source_is_branch_of_source`, `source_is_in_jurisdiction_of`. The initial graph has 12 edges covering all 5 relationship types (per `scripts/build_gaffer_graph.py`). |
| **CyberChef** | GCHQ | Apache 2.0 | The Cyber Swiss Army Knife — the 300+ operations (encoding, encryption, hashing, IPv6, X.509) are available via the AG-UI chat window. The `ExtractCyberChefRecipe` BAML function generates a recipe from the user's analysis request, the `cyberchef_execute` FunctionTool invokes CyberChef's API. The new `web/apps/ciafagent-cyberchef/` web app is the GUI-based companion. |
| **stroom** | GCHQ | Apache 2.0 | The data processing pipeline — high-volume log data (craw4ai browser logs + Langfuse observability traces) is routed through stroom for transformation + enrichment. The `ExtractStroomLog` BAML function parses the structured events. The stroom XSL transforms convert raw log data into structured events that the DLT sources can ingest. |
| **Device-Security-Guidance-Configuration-Packs** | NCSC | Apache 2.0 (Crown Copyright 2025) | The official UK government device security guidance for Apple/Google/Microsoft MDM (Intune, Jamf Pro, Workspace) — the ciafagent-self-host Docker bundle includes a `setup_ncsc_device_security.sh` script that validates + configures the citizen's device per the official standards (encryption, lock screen, app allowlist, OS up-to-date). The `ncsc_device_security_status` FunctionTool is available via the AG-UI chat. |
| **TRL doc** | UKRI / STFC | (open UK gov doc) | The official UK government Technology Readiness Level definitions (TRL 1-9) — the `ExtractTRLAssessment` BAML function evaluates every openspec change against the 9 TRL definitions. The `cianchosaint:trl:assess` mise task runs the assessment on all pending openspec changes. The TRL assessment feeds into the openspec validate gate. |
| **PDF reference** | HMGCC | (with MSIP Purview label) | The HMGCC Co-Creation Challenge Form PDF (OFFICIAL classification, MSIP label `d8a60473-494b-4586-a1bb-b0e663054676`) — the `ExtractPDFReference` BAML function parses the PDF. The `pdf_reference_search` FunctionTool is available via the AG-UI chat. |

### Example use cases

1. **A citizen** running the self-hosted Docker bundle can verify their device is configured per NCSC standards before consulting Cian (via `setup_ncsc_device_security.sh`).
2. **A public-sector analyst** investigating a Reform UK donation can trace the chain through Bailo-approved models + Gaffer graph relationships.
3. **An analyst** decoding a leaked document can use CyberChef's 300+ operations via the AG-UI chat window.
4. **An analyst** investigating cross-border activity (PSNI + Garda) can see the relationship graph via Gaffer + the per-source policy context via ic-ui-kit.
5. **A department** deploying ciafagent can follow the official UK government TRL assessment to determine if the platform is production-ready.
6. **An investigator** processing high-volume log data can use stroom for the transformation + cianchosaint DLT sources for the structured extraction.

For the canonical sub-projects, see the [hmgcc sub-directory](hmgcc/).


## Cross-references

- [`LICENSE.md`](LICENSE.md) — the load-bearing legal document
- [`AGENTS.md`](AGENTS.md) — the canonical agent routing
- [`openspec/AGENTS.md`](openspec/AGENTS.md) — the openspec workflow
- [`openspec/changes/cianchosaint-repo-foundation-v1/`](openspec/changes/cianchosaint-repo-foundation-v1/) — the first openspec change
- [`openspec/specs/cianchosaint-pipeline/spec.md`](openspec/specs/cianchosaint-pipeline/spec.md) — the umbrella capability spec
