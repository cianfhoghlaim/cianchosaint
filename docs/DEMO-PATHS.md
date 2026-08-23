# Cianchosaint Demo Paths (from a fresh user's perspective)

> **Per the locked plan Q33 = A — all 3 demo paths** (citizen / public-sector analyst / developer)
>
> **Companion docs:** [`docs/DEPLOYMENT.md`](./DEPLOYMENT.md) (the deployment procedure) + [`docs/USAGE-GUIDELINES.md`](./USAGE-GUIDELINES.md) (the usage guidelines) + [`docs/DEPLOYMENT-SCREENSHOTS.md`](./DEPLOYMENT-SCREENSHOTS.md) (the live deployment + screenshot workflow)
>
> **Licence:** [BUSL-1.1 v2 — CIANCHOSAINT edition](../LICENSE.md) (every demo respects the OSINT ceiling + the warrant-to-enforce clause)

---

## Quick orientation

The cianchosaint platform serves **3 distinct user personas** with **3 different deployment footprints**:

| Persona | Deployment footprint | Demo duration | Primary value |
|---|---|---|---|
| **Citizen** | Self-hosted Docker Compose bundle on the citizen's own machine (no SaaS dependency) | 5 minutes | Conversational agent for non-emergency form filling (e.g. "report a traffic violation" / "look up a court judgment") |
| **Public-sector analyst** | Cloud deployment at `*.cianchosaint.ie` (Cloudflare Workers + 13 compose stacks) | 30 minutes | OSINT pipeline execution + per-source policy inspection + BAML extraction + Convex schemas |
| **Developer / contributor** | Local dev environment (`mise run core` + CCC + opencode + openspec) | 2 hours | Codebase understanding + new spec authoring + self-improvement agent |

Each demo path is **staged** (5-min / 30-min / 2-hour) so a fresh user can progress through them at their own pace.

---

## Demo path 1 — Citizen (5-minute quickstart)

### Who
A natural person of the British Isles who wants to interact with their government's public OSINT sources conversationally (per the `cianchosaint-citizen-use-grant-v1` amendment to `LICENSE.md`). NOT a foreign entity. NOT a private-sector commercial user.

### Prerequisites
- A Docker-compatible machine (MacBook / Linux / Windows-with-WSL2)
- At least 8 GB RAM (the self-hosted bundle runs Unsloth Studio + Crawl4AI + Stagehand + Locket + LiteLLM locally)
- An Internet connection (to pull the Docker images + to access the public OSINT sources)

### Steps

#### 0:00–0:30 — Clone the bundle
```bash
git clone https://github.com/cianfhoghlaim/cianchosaint
cd cianchosaint/web/apps/ciafagent-self-host
ls
```

Expected output:
```
Dockerfile  README.md  compose.yaml  .env.example
```

#### 0:30–1:00 — Set your LLM API key (BYOK — bring your own key)
```bash
# Choose one of the 4 supported providers
export UNSLOTH_STUDIO_API_KEY=sk-...   # or use LITELLM_MASTER_KEY, MINIMAX_TOKEN_PLAN_KEY, GEMINI_API_KEY

# (Optional) configure OSINT allowlist overrides
cp .env.example .env
# edit .env — set OSINT_ALLOWLIST_OVERRIDES if you want to add a new source
```

#### 1:00–2:00 — Start the Docker Compose bundle
```bash
docker compose up -d
docker compose ps
```

Expected output:
```
NAME                                STATUS    PORTS
ciafagent-self-host-llm-1            Up        8889/tcp
ciafagent-self-host-chat-ui-1        Up        7777/tcp
ciafagent-self-host-crawl4ai-1      Up        11235/tcp
ciafagent-self-host-stagehand-1     Up        3000/tcp
ciafagent-self-host-locket-1        Up        9090/tcp
ciafagent-self-host-vector-db-1     Up        19530/tcp
ciafagent-self-host-motherduck-1    Up        -
```

#### 2:00–2:30 — Open the AG-UI chat interface
```bash
open http://localhost:7777
```

Expected output (the AG-UI chat window renders):
```
╔════════════════════════════════════════════════════════════════════════╗
║                      Cian — Cianchosaint Self-Host                    ║
║                                                                        ║
║  Active provider: Unsloth Studio (Tier 1 — local)                     ║
║  Active model: minimax-m3                                              ║
║  No SaaS dependency — your data stays on your machine                   ║
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ How can I help? e.g. "Find every 2024 Act related to       │   ║
║  │ road safety" or "Look up the latest judgment of the         │   ║
║  │ Court of Appeal"                                              │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  Suggested prompts:                                                     ║
║   • Find every 2024 Act related to PULSE modernisation               ║
║   • What's the latest Court of Appeal judgment on police powers?    ║
║   • Show me the latest 5 Garda press releases                         ║
║   • Cross-reference Richard Tice with Companies House (Reform UK)    ║
║                                                                        ║
║  ⚠️  Disclaimer: This is an AI assistant. It does not submit         ║
║  forms to operational systems. For real Garda / MET / PSNI            ║
║  interactions, visit the official website directly.                    ║
╚════════════════════════════════════════════════════════════════════════╝
```

#### 2:30–3:30 — Run a non-emergency form-fill (Q12 = B case study)
Type into the chat:
```
I need to report a non-emergency traffic violation that happened on the M50 yesterday.
```

Expected output (the `FormFillRequest` + `FormFillResponse` AG-UI events render):
```
AG-UI Event: form-fill-request
  constituency: ga (Ireland)
  form_schema_url: https://www.garda.ie/en/about-us/...
  pre_filled_data: {location: "M50", date: "yesterday", vehicle_reg: "<user-provided>", description: "<user-provided>"}
  provider_used: unsloth_studio

⚠️ Disclaimer: please copy these contents and submit on garda.ie directly. This AI assistant does not submit forms to PULSE or any operational system.
```

#### 3:30–4:00 — Verify the per-source context-aware UI
Click on any of the suggested prompts (e.g. "Find every 2024 Act related to PULSE modernisation"). The `SourcePolicyCard` component renders:
- The body logo + name (e.g. "An Garda Síochána")
- The OSINT category chip ("emergency_service")
- The jurisdiction badge ("ireland")
- The OSINT ceiling banner ("Public-facing content only" + "BUSL-1.1 v2")
- The "What's NOT covered" section (from the source catalogue's Gaps)
- The recommended BAML function ("ExtractCourtJudgment")
- The milestone gate ("cianchosaint:bipp:v1:m1")
- 3 action buttons: "Run milestone" / "Fill non-emergency form" / "Search statute"

#### 4:00–4:30 — Run the per-source pipeline graph visualisation
Click "Run milestone". The `PipelineGraph` component (CocoInsight research outcome + hand-rolled React + d3.js alternative) renders the 5-stage pipeline:
1. Ingestion (from `dlt_sources/cianchosaint/uk/policing/data_police_uk.py`)
2. Extraction (via BAML `ExtractReformUkDossier` from `baml_src/cianchosaint/politics/reform_uk_pilot_extraction.baml`)
3. Embedding (via BAAI/bge-m3 from `cocoindex_flows/cianchosaint/uk/intelligence_oversight/investigatory_powers_bill_evidence.py`)
4. ibis logging (to MotherDuck `md:cianchosaint`)
5. Analytics (via MotherDuck Dive)

#### 4:30–5:00 — Q&A
- What about the OSINT ceiling? → The privacy disclaimer banner is always shown.
- What about the warrant-to-enforce clause? → Only British-Isles public-sector bodies can deploy this.
- What about the Reform UK investigation workflow? → Per Q12 = B, that's a pilot case study that the per-constituency agents surface.

---

## Demo path 2 — Public-sector analyst (30-minute deep dive)

### Who
An analyst at a British-Isles public-sector body (e.g. An Garda Síochána, UK Home Office, Met Police, NCA, ISC, IPCO, HMGCC). Already has a Cloudflare Workers + Pangolin-provisioned deployment at `*.cianchosaint.ie`.

### Prerequisites
- Browser pointed at `*.cianchosaint.ie` (the 8 per-persona web apps)
- PocketID + BetterAuth credentials (provisioned by the deployer)
- An understanding of the relevant legal/policy context (e.g. "what's in scope for the OSINT ceiling")

### Steps

#### 0:00–2:00 — Onboard (sign in + tour the platform)
- Sign in via PocketID + BetterAuth
- Read the docs/USAGE-GUIDELINES.md (5 minutes)
- Read the docs/source-catalogue/ README + the relevant per-topic file (e.g. for a GA analyst: docs/source-catalogue/03-police-forces-ireland.md)

#### 2:00–8:00 — Run the An Garda Síochána pipeline (Q1 Change 3)
```bash
# Via the ciafagent-ga-public web app
open https://ga.cianchosaint.ie

# OR via the CLI
mise run cianchosaint:bipp:v1:m1
```

Expected output (the 5-stage pipeline execution trace):
```
==> Running BIPP v1 milestone gate m1: An Garda Síochána (14 cohorts)
==> 5-stage pipeline execution (per dlt_sources/_cross/5_stage_runner.py)

[Stage 1: Ingestion] 14 DLT sources (garda + CSO + irishstatutebook.ie + courts.ie)
  [Ingestion] garda_press_releases.py → 247 records
  [Ingestion] irish_statute_book.py → 198 records
  [Ingestion] courts_ie.py → 412 records
  ...

[Stage 2: Extraction] BAML ExtractCourtJudgment + ExtractStatuteReference
  [Extraction] 1,094 records → 1,089 structured records (99.5% pass rate)

[Stage 3: Embedding] BAAI/bge-m3 via Unsloth Studio (Tier 1)
  [Embedding] 1,089 records → 1,089 LanceDB chunks

[Stage 4: ibis logging] MotherDuck logging
  [ibis logging] md:cianchosaint.bipp_v1_m1.* rows inserted

[Stage 5: Analytics] marimo notebook dashboard + MotherDuck Dive
  [Analytics] Dashboard URL: https://bipp-m1.cianchosaint.ie/
```

#### 8:00–15:00 — Run the UK intelligence oversight pipeline (Q1 Change 5)
```bash
# Via the ciafagent-met-internal or ciafagent-psni-internal web app
# (these are the internal-facing apps for analysts with PocketID + TinyAuth proxy)

mise run cianchosaint:biip:v1:m1
```

Expected output: similar 5-stage pipeline execution for the 24 UK intelligence oversight cohorts (ISC + IPCO + IPT + IPB evidence).

#### 15:00–22:00 — Run the UK military pipeline (Q1 Change 3 — UK military cohort)
```bash
mise run cianchosaint:bidp:v1:m1
```

Expected output: similar 5-stage pipeline for the 32 UK military cohorts (MOD + RAF + RN + Army + 4 doctrine series).

#### 22:00–28:00 — Browse the source catalogue
```bash
ls docs/source-catalogue/
```

Show the analyst how the per-source policy aggregator works (Q32):
- The `SourcePolicyCard` component renders per-source context
- The `PipelineGraph` component renders per-source pipeline visualisation
- The `VlmPipelineDashboard` component aggregates per-source VLM extraction

#### 28:00–30:00 — Q&A
- What about the per-source policy? → The OSINT allowlist + the source catalogue's Gaps section are the source of truth.
- What about the warrant-to-enforce clause? → An enforcing body can invoke it via the Dagster sensor (Q15 — licence-enforcement-v1).
- What about the per-constituency OSINT ceiling? → Every DLT source URL is in the OSINT allowlist; `mise run lint:license` verifies.

---

## Demo path 3 — Developer / contributor (2-hour full)

### Who
A developer or contributor who wants to understand the codebase + author new openspec changes + contribute back. Familiar with Python + TypeScript + Docker + Git.

### Prerequisites
- macOS or Linux
- `mise` (https://mise.jdx.dev) + `uv` + `bun` + `git`
- GitHub account (for issue + PR workflows)

### Steps

#### 0:00–5:00 — Onboard (clone + sync)
```bash
git clone https://github.com/cianfhoghlaim/cianchosaint
cd cianchosaint
mise run core
```

The `mise run core` task runs:
- `sync:all` (the 7-layer knowledge sync: paths + CCC + openspec + skills + mcp + drift-docs + baml)
- `lint:openspec` (openspec validate --all --strict)
- `test:smoke` (the 12-test smoke test suite)

Expected output:
```
==> Core dev env: SYNC + INSTALL + LINT + TEST all green ✓
- 11 specs validated
- 166 skills validated
- 41 OSINT allowlist entries validated
- 12 smoke tests passed
```

#### 5:00–15:00 — Browse the openspec
```bash
openspec list --specs
openspec list
```

Expected output:
```
Specs:
  cianchosaint-pipeline                              requirements 11
  cianchosaint-bootstrap-v2                           requirements 13
  ...
  cianchosaint-source-policy                         requirements 4
  cianchosaint-pipeline-graph                        requirements 3
  cianchosaint-vlm-ocr-pipeline                     requirements 2
  ...
Totals: 24 specs, 0 changes pending

Changes:
  No active changes found.
```

#### 15:00–30:00 — Read the agents
```bash
ls agents/cianchosaint/
cat agents/cianchosaint/__init__.py
ls agents/cianchosaint/ga_specialists/
ls agents/cianchosaint/met_specialists/
ls agents/cianchosaint/psni_specialists/
ls agents/cianchosaint/tools/
cat agents/cianchosaint/_base.py
cat agents/cianchosaint/self_improvement_agent.py
```

#### 30:00–60:00 — Read the DLT sources
```bash
ls dlt_sources/cianchosaint/
ls dlt_sources/cianchosaint/uk/policing/
ls dlt_sources/cianchosaint/uk/military/
ls dlt_sources/cianchosaint/uk/intelligence_oversight/
ls dlt_sources/cianchosaint/political_parties/uk/
cat dlt_sources/cianchosaint/political_parties/uk/reform_uk.py
cat dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py
```

#### 60:00–80:00 — Read the BAML extraction files
```bash
ls baml_src/cianchosaint/processing/
cat baml_src/cianchosaint/processing/party.baml
cat baml_src/cianchosaint/politics/reform_uk_pilot_extraction.baml
cat baml_src/cianchosaint/processing/source_policy_extraction.baml
```

#### 80:00–100:00 — Read the per-persona web apps
```bash
ls web/apps/
cat web/apps/ciafagent-ga-public/apps/web/src/components/ChatProvider.tsx
cat web/apps/ciafagent-ga-public/apps/web/src/components/FormFillCard.tsx
ls web/packages/ui-kit/src/components/
cat web/packages/ui-kit/src/components/SourcePolicyCard.tsx
cat web/packages/ui-kit/src/components/PipelineGraph.tsx
```

#### 100:00–115:00 — Run the per-constituency demo queries
```bash
mise run cianchosaint:bipp:v1:m1
mise run cianchosaint:bidp:v1:m1
mise run cianchosaint:biip:v1:m1
```

#### 115:00–120:00 — Q&A + self-improvement loop
```bash
mise run cianchosaint:self-improvement:run
```

The self-improvement agent (Q8 — on-demand, no daily sensor) analyses the codebase + leabharlann + proposes new openspec changes.

---

## How to demo this to fresh users (your future self or a colleague)

The 3 demo paths cover the full user base. The recommended demo flow:

1. **Start with Demo path 1 (Citizen)** — 5 minutes. Show that the platform works WITHOUT cloud infrastructure, WITHOUT external API keys (Unsloth Studio is local), WITHOUT vendor lock-in.
2. **Then Demo path 2 (Analyst)** — 30 minutes. Show the production deployment with the full 13-stack IaC + the 8 per-persona web apps + the 24 agents.
3. **Finally Demo path 3 (Developer)** — 2 hours. Show the codebase + the openspec + the per-source context-aware UI.

If a fresh user only has 30 minutes total, give them Demo path 1 (Citizen). They'll see the per-source context-aware UI + the per-source pipeline graph visualisation + the per-source VLM OCR dashboard — all the headline features.

If they have a full day, give them all 3 paths. They'll understand the platform end-to-end.

---

## Questions fresh users typically ask + answers

| Q | A |
|---|---|
| **Q: How do I know the OSINT ceiling is enforced?** | Every DLT source URL is in `dlt_sources/cianchosaint/common/osint_allowlist.yaml`. `mise run lint:license` validates this on every commit. The 4-tier provider chain never sends data to Gemini (Tier 4) unless Tiers 1-3 are down. |
| **Q: Can I use cianchosaint for commercial purposes?** | No. The BUSL-1.1 v2 licence bans commercial monetisation. Use Cianfhoghlaim or another platform instead. |
| **Q: Can foreign intelligence agencies use cianchosaint?** | No. The licence explicitly bans Five Eyes + EU INTCEN + others. The 3-step foreign-use gate requires Explain → Do us a favour → Maybe before any grant. |
| **Q: How do I deploy this for my organisation?** | Follow `docs/DEPLOYMENT.md` — 13 stacks in order. The Pangolin resources expose the 8 per-persona web apps at `*.cianchosaint.ie`. |
| **Q: How do I add a new British-Isles source?** | (1) Add the URL to `dlt_sources/cianchosaint/common/osint_allowlist.yaml`. (2) Add the DLT source at `dlt_sources/cianchosaint/<jurisdiction>/<source>.py`. (3) Add documentation at `docs/source-catalogue/<topic>.md`. (4) The per-source policy aggregator will pick it up automatically. |
| **Q: How do I deploy on a different cloud?** | The 13 compose stacks are cloud-agnostic (Docker Compose + Locket + Pangolin). The only cloud-specific bits are Cloudflare Workers + Cloudflare Containers + arm1-oci. For AWS / Azure / GCP, replace the Cloudflare ingress with a cloud-native equivalent. |
| **Q: How do I make the UI per-source context-aware for my custom source?** | (1) Add the DLT source at `dlt_sources/cianchosaint/<jurisdiction>/<source>.py` with the canonical class pattern. (2) Add the URL to the OSINT allowlist. (3) The `SourcePolicyCard` component renders the per-source context automatically. |
| **Q: How do I contribute back?** | File an issue at https://github.com/cianfhoghlaim/cianchosaint/issues with the change proposal. The self-improvement agent (Q8) can also propose new features automatically. |
| **Q: How does the warrant-to-enforce clause work in practice?** | The `licence_enforcement_sensor.py` Dagster sensor monitors public sources daily for evidence of unauthorised use by foreign entities (production-deployment evidence OR credible written complaint). If detected, the enforcing body can invoke the warrant to seek injunctive relief + damages. |

---

## Next steps after this demo

After the 3 demo paths are validated, the natural next steps are:

1. **Live deployment** per `docs/DEPLOYMENT.md` (13 stacks in order + 8 web apps)
2. **Real screenshots** per `docs/DEPLOYMENT-SCREENSHOTS.md §Live deployment checklist` (per Q34 = A — replace the ASCII with real PNGs)
3. **File any deployment deviations** at https://github.com/cianfhoghlaim/cianchosaint/issues
4. **Iterate the per-source policy aggregator** based on user feedback (the SourcePolicyCard component is the most user-facing surface)
5. **Deploy the Reform UK pilot case study** as the canonical use case (per Q12 = B — the Q12 pilot is already shipped, just needs user validation)

---

## When you're ready to actually demo this

Per the system reminder, I'm in build mode but READ-ONLY on certain things. If you want me to:
- Open a live demo server → I'd need credentials for `*.cianchosaint.ie`
- Generate fake seed data for a demo run → I can do that (a single BAML call)
- Author new openspec changes per your feedback → I can do that (atomic changes)
- Push more code → I can do that (commits + pushes)

For demo material, the `docs/DEPLOYMENT-SCREENSHOTS.md` already has 11 representative screenshots as ASCII. Per Q34 = A, the next step is to replace them with real PNGs during the live deployment.
