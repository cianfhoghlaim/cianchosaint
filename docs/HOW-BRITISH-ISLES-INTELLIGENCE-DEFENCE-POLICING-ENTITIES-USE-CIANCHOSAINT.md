# How British-Isles Intelligence / Defence / Policing Entities Use Cianchosaint

> **Audience:** An Garda Síochána, UK MoD, MET Police, PSNI, RAF, Royal Navy, British Army, Defence Forces of Ireland, HMGCC, Crown Prosecution Service, HMCTS, Home Office, NCA, NAO, C&AG, Electoral Commission, Crown Dependencies police forces.
>
> **Companion docs:** USAGE-GUIDELINES.md · DEMO-PATHS.md · LIVE-DEPLOYMENT-PLAN.md · DEPLOYMENT.md · case-study/reform-uk-pilot.md · source-catalogue/ · configuration-surface.md
>
> **Licence:** BUSL-1.1 v2 — CIANCHOSAINT edition (British-Isles-only Additional Use Grant + 3-step foreign-use gate + warrant-to-enforce clause)

## §1 — Welcome + why this document exists

This document is for the British-Isles public-sector bodies explicitly named in the BUSL-1.1 v2 licence Additional Use Grant.

**The purpose of cianchosaint** is to **minimise the burden of entry** for investigating specific types of crime through public OSINT (Open-Source Intelligence). The platform covers white-collar financial criminal activity, associate corruption from political party members, violent / terroristic activity, institutional corruption + procurement fraud, and the broader range of public-sector-relevant criminal investigations — all through the OSINT ceiling (public-facing content only) and within the BUSL-1.1 v2 licence posture (British-Isles public-sector bodies only).

The case studies in this document — the Reform UK political party pipeline, the Eirigí party coverage, and other examples — are **illustrative examples of what the platform enables** for crime investigation. They are **not** the repository author's research interest. They demonstrate the kinds of cross-source investigations the political party pipeline + intelligence oversight pipeline enable. Other British-Isles public-sector bodies may use the platform for any crime investigation within the OSINT ceiling + the licence posture.

**The meta-purpose of this document** is to explain how a department with NO prior AI/OPS skills can stand up their own use of the platform.

## §2 — The minimal skill set the platform removes

You don't need to be a senior platform engineer to use cianchosaint. The 4-tier provider chain + the 13 compose stacks + the per-source policy aggregator + the 24 agents + the AG-UI chat window remove the need for these specialist skills:

| Skill | How the platform abstracts it |
|---|---|
| OpenAI-compatible API key management | LiteLLM abstracts it — see baml_src/_shared/provider_router.py |
| Docker orchestration debugging | The 6-file GOLD_STANDARD pattern (compose.yaml + sidecar.yaml + secrets.env + pangolin.yaml + blueprint.yaml + .env.example) |
| VLM / OCR model selection | BAML abstracts it — see baml_src/cianchosaint/processing/*.baml |
| Vector embedding | LanceDB + BAAI/bge-m3 abstracts it — see cocoindex_flows/_shared/_lifespan.py |
| Knowledge graph construction | Cognee + Graphiti abstracts it — see agents/meaisinfhoghlaim/firecrawl_mcp/memory/ |
| Browser automation | Stagehand + Crawl4AI + headless Chrome abstracts it |
| Pipeline orchestration | Dagster abstracts it — see orchestration/defs/ |
| Secret injection | Locket sidecar abstracts it |
| Reverse proxy + identity | Pangolin abstracts it |
| Resource-sync + procedure engine | Komodo abstracts it |
| CocoIndex embedding pipeline | CocoIndex v1 abstracts it |

You only need to:
1. Run `mise run core` (the full bootstrap)
2. Open the AG-UI chat window
3. Use the per-source context-aware UI
4. For new feature requests: edit osint_allowlist.yaml + the relevant DLT source + the relevant BAML extraction + the relevant agent FunctionTool

If you're already comfortable with Docker + Git + YAML + Python, the entire setup takes ~1 hour for the self-hosted citizen footprint or ~2 days for the full public-sector analyst footprint.

## §3 — The 3 deployment footprints

### §3.1 — Self-hosted citizen footprint (~8 GB RAM, ~1 hour, $0/month)
- **Who:** A British-Isles citizen on their own machine (Raspberry Pi 5, NAS, laptop)
- **Components:** Docker Compose bundle at docker/ciafagent-self-host/ + 5 containers (Unsloth Studio + LiteLLM + Locket + Crawl4AI + Stagehand)
- **Cloud dependencies:** NONE (all local)
- **Live deployment:** `git clone` → `docker compose up -d` → `open http://localhost:7777`

### §3.2 — Public-sector analyst footprint (cloud, ~$3k/month, ~2 days)
- **Who:** An Garda Síochána analyst + UK Home Office analyst + PSNI analyst + MET analyst
- **Components:** 13 compose stacks + 8 per-persona web apps + MotherDuck + Cloudflare Workers
- **Cloud dependencies:** arm1-oci (or Hetzner) + Pangolin + Cloudflare + Infisical + MotherDuck SaaS
- **Live deployment:** provision cloud + DNS + deploy 13 stacks + deploy 8 web apps

### §3.3 — Developer / contributor footprint (local dev, ~30 minutes, $0/month)
- **Components:** `mise run core` + CCC indexing + opencode + openspec
- **Live deployment:** `git clone` → `mise install` → `mise run core` → `openspec list` → `bun run ccc:init`

## §4 — The 13 stacks

The 13 stacks deploy in order (per DEPLOYMENT.md §2):

| # | Stack | Port | Purpose |
|--:|:--|--:|:--|
| 1 | infisical | 8443 | Secrets management |
| 2 | motherduck | (SaaS) | Cloud DuckDB via Postgres endpoint |
| 3 | lakehouse | 3900-3904, 5433, 8181-8182 | Garage S3 + Postgres + Lakekeeper |
| 4 | litellm | 4000 | LLM gateway |
| 5 | unsloth-serve | 8889 | Tier-1 local LLM |
| 6 | langfuse | 3000 | LLM observability |
| 7 | crawl4ai | 11235 | Self-hosted browser scraper |
| 8 | stagehand | 11300 | Stagehand + headless Chrome |
| 9 | changedetection | 5000 | Page-change monitor |
| 10 | komodo | 9120 | GitOps deployment orchestrator |
| 11 | pangolin | 8443 (alt) | Reverse proxy + identity |
| 12 | locket | (sidecar) | Secret-injection sidecar |
| 13 | openchamber | 3030 | OpenCode web/desktop UI |

## §5 — The per-source context-aware UI

Per the Q32 change, every per-constituency DLT source + political party + UK intel agency has a per-source policy context. The `SourcePolicyCard` React component renders this context at the top of the AG-UI chat window. For each source, the card shows:

| Field | What it tells the user |
|---|---|
| **Body name** | The body that operates the source (e.g. "An Garda Síochána" / "Reform UK" / "MI5") |
| **OSINT category chip** | The OSINT category (intelligence / military / emergency_service / agency / party / court / government) |
| **Jurisdiction badge** | The jurisdiction (ireland / uk / ni / scotland / wales / jersey / guernsey / iom) |
| **OSINT ceiling banner** | "Public-facing content only" + "BUSL-1.1 v2" (always visible) |
| **"What's NOT covered" section** | From the source catalogue's Gaps section |
| **BAML function** | The recommended BAML extraction function |
| **Milestone gate** | Which mise task runs the source's pipeline |
| **3 action buttons** | Run milestone / Fill non-emergency form / Search statute |

## §6 — The crime-investigation workflow patterns

### §6.1 — White-collar financial criminal activity + associate corruption (the Reform UK case study)

The canonical first case study (per Q12 = B + case-study/reform-uk-pilot.md). The workflow demonstrates how a department investigating white-collar financial crime can use the platform's political party pipeline + intelligence oversight pipeline + Companies House cross-reference + Reform UK pilot FunctionTool.

**Platform's tools for this crime type:**

| DLT source / BAML / Agent | What it does |
|---|---|
| dlt_sources/cianchosaint/political_parties/uk/reform_uk.py | Ingests Reform UK press releases |
| dlt_sources/official_media_cianchosaint/companies_house/crown_filter.py | Cross-references Reform UK-linked entities in Companies House bulk data |
| dlt_sources/cianchosaint/uk/intelligence_oversight/investigatory_powers_bill_evidence.py | Cross-references Investigatory Powers Bill submissions |
| dlt_sources/cianchosaint/uk/government/{home_office_statistics, moj_statistics}.py | Cross-references government statistics |
| baml_src/cianchosaint/politics/reform_uk_pilot_extraction.baml | The ExtractReformUkDossier BAML function |
| baml_src/cianchosaint/processing/political_party_extraction.baml | The shared ExtractPartyPressRelease BAML function |
| agents/cianchosaint/tools/reform_uk_pilot.py | The Reform UK pilot FunctionTool |

**The workflow:**

1. IDENTIFY the entity of interest
2. CONFIGURE the platform to focus on this entity (URL in osint_allowlist.yaml + BAML extraction wired)
3. RUN the political party pipeline (mise run cianchosaint:bipp:v1:m2)
4. RUN the intelligence oversight pipeline (mise run cianchosaint:biip:v1:m1)
5. RUN the Reform UK pilot FunctionTool (mise run cianchosaint:reform-uk-pilot:run)
6. ANALYST REVIEWS the dossier

**Licence posture:** the pilot NEVER directly submits forms to operational systems.

### §6.2 — Violent terroristic activity (the Eirigí party case study)

**Platform's tools for this crime type:**

| DLT source / BAML / Agent | What it does |
|---|---|
| dlt_sources/cianchosaint/political_parties/roi/sinn_fein_roi.py | Ingests Sinn Féin press releases |
| dlt_sources/cianchosaint/ireland/defence_forces/idf_press_releases.py | Cross-references Irish Defence Forces |
| dlt_sources/cianchosaint/ireland/defence_forces/idf_white_paper.py | Cross-references the White Paper on Defence |
| dlt_sources/cianchosaint/uk/intelligence_oversight/ipt_decisions.py | Cross-references Investigatory Powers Tribunal decisions |
| dlt_sources/cianchosaint/uk/intelligence_oversight/ipco_reports.py | Cross-references Investigatory Powers Commissioner reports |
| dlt_sources/cianchosaint/uk/intelligence_oversight/isc_annual_reports.py | Cross-references ISC annual reports |
| dlt_sources/cianchosaint/uk/intelligence_agencies/mi5.py + mi6.py + gchq.py | Cross-references the 5 UK intel agencies |

### §6.3 — Institutional corruption + procurement fraud (general)

| DLT source / BAML / Agent | What it does |
|---|---|
| dlt_sources/cianchosaint/uk/government/home_office_statistics.py | Cross-references Home Office statistical bulletins |
| dlt_sources/cianchosaint/uk/government/moj_statistics.py | Cross-references MoJ statistics |
| dlt_sources/cianchosaint/uk/government/nca_threat_assessments.py | Cross-references NCA threat assessments |
| dlt_sources/cianchosaint/political_parties/{uk,roi,ni,wales,scotland,crown_dependencies}/ | Cross-references all 24 political parties |
| dlt_sources/cianchosaint/uk/intelligence_oversight/ | Cross-references ISC + IPCO + IPT + IPB evidence |

### §6.4 — General crime investigation

The platform's broad capability covers any public-OSINT crime investigation within the OSINT ceiling + the licence posture. The per-source context-aware UI makes it easy for analysts to discover what's available + what's NOT covered + how to extend with new sources.

## §7 — The 24 political parties + the political party pipeline

The dlt_sources/cianchosaint/political_parties/ directory (the 49 files wholesale-copied from Cianfhoghlaim in Q1 Change 4) covers 24 active political parties across 8 jurisdictions:

| Jurisdiction | Parties |
|---|---|
| **UK HoC** | Conservative, Labour, Liberal Democrats, **Reform UK**, Green (E&W), Plaid Cymru, SNP |
| **ROI Dáil + Seanad** | Fianna Fáil, Fine Gael, Sinn Féin, Labour, Social Democrats, PBP-Solidarity, Green Party, Aontú, Independent Ireland, Irish Freedom Party, National Party, Rise |
| **NI Assembly** | DUP, Sinn Féin, Alliance, UUP, SDLP, TUV, PBP |
| **Wales Senedd** | Plaid Cymru (Senedd), Labour (Wales), Conservative (Wales), Liberal Democrats (Wales), Plaid Cymru Voice |
| **Scotland Holyrood** | SNP (Scottish), Scottish Labour, Scottish Conservatives, Scottish Liberal Democrats, Scottish Greens |
| **Crown Dependencies** | States of Jersey, Bailiwick of Guernsey, Isle of Man (parish-level) |

**The shared BAML extraction** for all 24 parties is `ExtractPartyPressRelease` (defined in baml_src/cianchosaint/processing/political_party_extraction.baml per Q3 Track 1).

## §8 — The 5 UK intel agencies + the intelligence oversight pipeline

The dlt_sources/cianchosaint/uk/intelligence_oversight/ directory + the dlt_sources/cianchosaint/uk/intelligence_agencies/ directory cover the British-Isles intelligence ecosystem:

| Body | Purpose | DLT source |
|---|---|---|
| ISC | UK parliament's intelligence oversight | uk/intelligence_oversight/isc_annual_reports.py |
| IPCO | Independent oversight of MI5/MI6/GCHQ | uk/intelligence_oversight/ipco_reports.py |
| IPT | Tribunal for complaints against the agencies | uk/intelligence_oversight/ipt_decisions.py |
| IPB | Evidence submissions | uk/intelligence_oversight/investigatory_powers_bill_evidence.py |
| MI5 | Security Service (domestic counter-intelligence) | uk/intelligence_agencies/mi5.py |
| MI6 | Secret Intelligence Service (foreign intelligence) | uk/intelligence_agencies/mi6.py |
| GCHQ | Signals intelligence | uk/intelligence_agencies/gchq.py |
| DI | Defence Intelligence (military intelligence) | uk/intelligence_agencies/defence_intelligence.py |
| HMGCC | Cross-government communications | uk/intelligence_agencies/hmgcc_rolling_window.py |

## §9 — The "go more in-depth" workflow (DOMESTIC, OFFLINE)

### §9.1 — IDENTIFY your specific feature request

Examples:
- "I want to add a CSO Ireland court judgment extractor"
- "I want to add a WHO IRIS adverse event monitor"
- "I want to add a Defence Forces procurement contract monitor"
- "I want to add a UK Home Office FOI request monitor"

### §9.2 — CONFIGURE your domain (DOMESTICALLY)

1. **Add the URL to the OSINT allowlist** — edit dlt_sources/cianchosaint/common/osint_allowlist.yaml
2. **Run `mise run lint:license`** — verifies the URL
3. **Add the jurisdiction enum** (if your jurisdiction is new) — edit baml_src/clients.baml
4. **Run `mise run openspec:validate-all`** — verifies all specs pass

### §9.3 — AUTHOR the new code (DOMESTICALLY on your machine)

1. **Add the DLT source** at dlt_sources/cianchosaint/<jurisdiction>/<source>.py (following the canonical pattern in dlt_sources/cianchosaint/ireland/law/irish_statute_book.py)
2. **Add the BAML extraction** at baml_src/cianchosaint/processing/<source>_extraction.baml
3. **Register the cohort** in dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py
4. **Add the agent FunctionTool** (if your feature needs a new domain-specific agent)
5. **Add the web app surface** (if your feature needs a new per-persona web app)

### §9.4 — DEPLOY + VALIDATE (DOMESTICALLY, no cloud required)

1. Run `mise run core` — the full bootstrap
2. Run `mise run lint:license` — verifies the OSINT allowlist
3. Run `mise run openspec:validate-all` — verifies every openspec change + every canonical spec
4. Run `mise run cianchosaint:provider:health-check` — verifies the 4-tier provider chain
5. Run `mise run cianchosaint:browser-tool:health-check` — verifies the BrowserToolRouter
6. Run `mise run cianchosaint:osint:health-check` — verifies the OSINT allowlist
7. Run `mise run cianchosaint:<vertical>:v1:m<N>` — verifies your milestone gate
8. Run the self-hosted citizen Docker bundle:
   ```bash
   cd docker/ciafagent-self-host
   docker compose up -d
   open http://localhost:7777
   ```

### §9.5 — DOCUMENT your work

1. Add the new source to docs/source-catalogue/<topic>.md
2. Add the new policy aggregator entry
3. Update this document

### §9.6 — FILE an issue

At https://github.com/cianfhoghlaim/cianchosaint/issues

## §10 — The 4-tier provider chain (config overview)

Per USAGE-GUIDELINES.md §2, every LLM call routes through this priority chain:

| Tier | Provider | When to use | Cost |
|---|---|---|---|
| 1 (PRIMARY) | **Unsloth Studio** (local API at http://unsloth-serve:8889/api/v1) | Local inference (self-hosted + sovereign) | $0/month |
| 2 | **LiteLLM Proxy** (litellm.cianfhoghlaim.ie) | Cloud proxy (the 76-entry MODEL_REGISTRY) | Variable |
| 3 | **MiniMax Token Plan** (direct API at api.minimax.io/v1) | Direct API for MiniMax coding plan users | Variable |
| 4 (LAST RESORT) | **Gemini API** (generativelanguage.googleapis.com) | Last resort only | Variable |

Per-deployment overrides via deployment-choice.yaml:

```yaml
provider_chain:
  - unsloth_studio
  - litellm
  - minimax_token_plan
  - gemini_api

per_force_overrides:
  psni:
    provider_chain: [litellm]
```

## §11 — The OSINT ceiling + the British-Isles-only posture + the warrant-to-enforce

### §11.1 — The OSINT allowlist

The OSINT allowlist at dlt_sources/cianchosaint/common/osint_allowlist.yaml enforces the licence ceiling: 41 entries across intelligence_oversight (12) + military (9) + emergency_service (18) + intelligence_agency (5) + agency (5) + jurisdiction (11) categories. Every DLT source URL MUST be in this allowlist.

### §11.2 — The per-source policy aggregator (Q32)

The Q32 cianchosaint-source-policy-v1 change ships source_policy_aggregator.py + SourcePolicyCard.tsx that reads every DLT source + osint_allowlist.yaml + source-catalogue/*.md + builds a per-source policy index keyed by (jurisdiction, source_id) + embeds via BAAI/bge-m3 + mounts in LanceDB + renders in the AG-UI chat window.

### §11.3 — The 3-step foreign-use gate

Per the licence posture (BUSL-1.1 v2 grant, §Warrant to enforce): Governmental bodies of sub-nations OUTSIDE the British Isles MAY use the Licensed Work only after satisfying STEP 1 (EXPLAIN) + STEP 2 (DO US A FAVOUR) + STEP 3 (MAYBE). The 4 EXHAUSTIVE exemplars for STEP 2 are: (1) reciprocal OSINT data access; (2) treaty-level cooperation; (3) diplomatic recognition; (4) open-source contribution.

### §11.4 — The warrant-to-enforce clause

The licence posture grants each licence body a warrant to enforce the licence against unauthorised use. The cianchosaint-licence-enforcement-v1 change ships a Dagster sensor that monitors public sources for evidence of unauthorised use.

## §12 — Common gotchas + troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `openspec validate` fails with "ADDED failed — already exists" | The delta conflicts with an already-applied spec | Use `--skip-specs` flag during archive |
| `mise run lint:license` reports URLs outside the allowlist | The DLT source URL is not in osint_allowlist.yaml | Add the URL to the allowlist |
| The 4-tier provider chain is "stuck on Tier 4 (Gemini)" | The other 3 providers are unreachable | Check `mise run cianchosaint:provider:health-check` |
| `mise run cianchosaint:bipp:v1:m2` fails with "no data returned" | data.police.uk API is down OR the force_id is misconfigured | Check `data_police_uk.py` |
| The platform returns OSINT for a foreign entity | The OSINT allowlist has been bypassed | **This is a licence violation** — file an issue immediately |
| `bun run ccc:search` returns no results | The CCC index hasn't been built yet | Run `bun run ccc:init && bun run ccc:index` |
| The Locket sidecar is "secret not found" | The Locket is running but the Pangolin-issued token isn't there | Check Pangolin resource config + the Locket logs |
| The Reform UK pilot returns empty | The ExtractReformUkDossier BAML function isn't wired | Verify the BAML client config |
| The per-source policy aggregator doesn't pick up my new source | The source isn't in osint_allowlist.yaml | Add it |

## §13 — Resources + cross-references

### §13.1 — Canonical docs (read these first)
- README.md · AGENTS.md · LICENSE.md · docs/USAGE-GUIDELINES.md · docs/DEPLOYMENT.md · docs/DEMO-PATHS.md · docs/LIVE-DEPLOYMENT-PLAN.md · docs/DEPLOYMENT-SCREENSHOTS.md

### §13.2 — Per-topic docs (read these for depth)
- docs/case-study/reform-uk-pilot.md · docs/source-catalogue/ · docs/source-policy/ · docs/configuration-surface.md · docs/research/ · docs/case-study/

### §13.3 — OpenSpec specs (the source of truth)
- openspec/specs/ (24 canonical specs) · openspec/changes/archive/ (23 archived changes)

### §13.4 — GitHub
- **Repository**: https://github.com/cianfhoghlaim/cianchosaint
- **Issue tracker**: https://github.com/cianfhoghlaim/cianchosaint/issues
- **Parent repo**: https://github.com/cianfhoghlaim/cianfhoghlaim
- **leabharlann**: https://github.com/cianfhoghlaim/leabharlann

## Final note

This document is designed for **replication** by departments that usually have different sets of skills than required by this combination of opensource package software in data engineering + infrastructure + web development + associated analytics. Every step can be done DOMESTICALLY on your own machine with the self-hosted Docker bundle. The 4-tier provider chain starts with Unsloth Studio (local inference, no egress). The OSINT allowlist enforces the licence posture. The 3-step foreign-use gate + the warrant-to-enforce clause ensure that the platform remains sovereign + auditable + British-Isles-only.

The Reform UK + Eirigí case studies are **illustrative examples of what the platform enables** for crime investigation — they are NOT the repository author's research interest. The platform's value is **reducing the burden of entry** for investigating any crime within the OSINT ceiling + the licence posture, using pipelines + sources that already exist for all relevant parties + governmental bodies + defence entities of the British Isles.

For the meta-prompt template that lets you author your own domain-specific tangent (medical / legal / financial / environmental / etc.) — see TANGENT-FORK-PROMPT-TEMPLATE.md.
