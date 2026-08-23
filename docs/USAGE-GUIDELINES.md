# Cianchosaint Usage Guidelines

> **For:** Cian Pierce Lyons (Licensor) + fresh users (public-sector analysts, intelligence-community engineers, British Isles citizens)
>
> **Companion docs:** [`docs/DEPLOYMENT.md`](./DEPLOYMENT.md) (deployment) + [`docs/case-study/reform-uk-pilot.md`](./case-study/reform-uk-pilot.md) (first case study) + [`docs/source-catalogue/README.md`](./source-catalogue/README.md) (the catalogue of every British Isles intelligence agency / police force / army / navy / air force / government department)
>
> **Licence:** [BUSL-1.1 v2 — CIANCHOSAINT edition](../LICENSE.md)

---

## 1. Who can use cianchosaint (per the licence)

Per the [LICENSE.md](../LICENSE.md) Additional Use Grant:

| Category | Use case | Permitted? |
|---|---|:--:|
| An Garda Síochána (Republic of Ireland police) | Non-emergency form filling + statute search + court judgment lookup | ✅ Yes |
| An Garda Síochána (internal analysts) | PULSE cross-reference + internal circulars + training materials | ✅ Yes |
| Irish Defence Forces (Army / Naval Service / Air Corps) | White Paper + doctrine + press releases | ✅ Yes |
| Department of Foreign Affairs (Ireland) | OSINT + treaty analysis | ✅ Yes |
| MET Police + 43 UK forces | Non-emergency form filling + cross-force comparisons + FOI mining | ✅ Yes |
| PSNI (Police Service of Northern Ireland) | Cross-border queries + APP search | ✅ Yes |
| States of Jersey Police / Bailiwick of Guernsey / IoM Constabulary | Crown Dependencies policing | ✅ Yes |
| Defence Forces of Ireland | Defence doctrine + procurement + press | ✅ Yes |
| His Majesty's Government Communications Centre (HMGCC) | 12-week rolling window of public-facing publications | ✅ Yes |
| Crown Prosecution Service (CPS) | Court judgment cross-reference + prosecution policy | ✅ Yes |
| His Majesty's Courts & Tribunals Service (HMCTS) | Court judgment extraction | ✅ Yes |
| Home Office | Statistical bulletins + press releases | ✅ Yes |
| National Crime Agency (NCA) | Threat assessments + public-facing reports | ✅ Yes |
| Serious Fraud Office (SFO) | Public-facing investigations | ✅ Yes |
| ICO / NAO / C&AG / Electoral Commission | Audit + oversight + regulatory data | ✅ Yes |
| Members of the public (self-hosted) | Self-hosted citizen Docker bundle | ✅ Yes (per the follow-up `cianchosaint-citizen-use-grant-v1` change) |
| **Five Eyes allies** (NSA / CIA / GCSB / ASD / CSIS) | Any | ❌ **Explicitly banned by the licence** |
| **Foreign intelligence agencies** (DGSE / BND / Mossad / MSS / GRU / FSB) | Any | ❌ **Explicitly banned by the licence** |
| **EU institutions** (EU INTCEN) | Any | ❌ **Explicitly banned** (unless STEP 1 + STEP 2 satisfied) |
| **Private sector commercial use** | Any | ❌ **Banned** (non-commercial only) |

**Always check the [BUSL-1.1 v2 licence](../LICENSE.md) before deploying.** If you're unsure, ask first.

---

## 2. The 4-tier provider chain — when each tier is used

Per the [cianchosaint-bootstrap-v2 spec](../openspec/specs/cianchosaint-bootstrap-v2/spec.md), every LLM call routes through this priority chain:

```
Tier 1 (PRIMARY)  Unsloth Studio        (local API at unsloth-serve:8889/api/v1)
Tier 2            LiteLLM Proxy        (litellm.cianchosaint.ie)
Tier 3            MiniMax Token Plan   (direct API at api.minimax.io/v1)
Tier 4 (LAST)     Gemini API           (generativelanguage.googleapis.com)
```

| When... | Use... |
|---|---|
| You're running a self-hosted citizen Docker bundle | Tier 1 (Unsloth Studio) — runs locally, no egress |
| You're operating on a self-hosted deployment (arm1-oci / bunchloch) | Tier 1 + Tier 2 (Unsloth primary, LiteLLM fallback) |
| You're operating from a UK gov secure network with no Gemini access | Tiers 1-3 only (Unsloth → LiteLLM → MiniMax) |
| You're operating from the open internet with all providers available | All 4 tiers (graceful fallback to Gemini last resort) |
| **Gemini should NEVER be used for sensitive intelligence data** | It's the LAST RESORT — only for public-facing demos |

**Configure via `.infisical.env` + `deployment-choice.yaml`:**

```yaml
# deployment-choice.yaml — provider chain (priority order)
provider_chain:
  - unsloth_studio
  - litellm
  - minimax_token_plan
  - gemini_api

# Per-deployment override
per_force_overrides:
  psni:
    provider_chain: [litellm]  # PSNI's IT only approved LiteLLM
  met:
    provider_chain: [unsloth_studio, gemini_api]  # MET uses local + final fallback
```

---

## 3. The 32 mise tasks — quick reference

Per the slimmed `mise.toml` (see `mise.toml`), here are the canonical task groups:

### Dev workflow
```bash
mise run core                        # sync + install + lint + test + format (full bootstrap)
mise run lint                        # openspec + licence + skills
mise run lint:license                # OSINT allowlist + British Isles body check
mise run lint:openspec                # openspec validate
mise run lint:drift-docs             # validate every AGENTS.md number claim
mise run lint:skills                 # validate .agents/skills/ metadata
mise run sync:all                    # all 14 sync layers
mise run openspec:validate-all       # openspec CI gate
mise run openspec:list               # list pending changes
mise run openspec:archive <id>       # archive a deployed change
```

### Provider chain health
```bash
mise run cianchosaint:provider:health-check       # 4-tier chain health
mise run cianchosaint:browser-tool:health-check   # BrowserToolRouter health
mise run cianchosaint:osint:health-check           # OSINT allowlist audit
```

### Milestone gates (per the locked plan)
```bash
# Q1 deliverables (all DONE per the current state)
# BIPP v1 milestones (police data pipeline)
mise run cianchosaint:bipp:v1:m1         # Ireland ROI
mise run cianchosaint:bipp:v1:m2         # UK 43 forces
mise run cianchosaint:bipp:v1:m3         # Crown Dependencies
# BIDP v1 milestones (defence data pipeline)
mise run cianchosaint:bidp:v1:m1         # UK MoD + RAF + RN + Army
mise run cianchosaint:bidp:v1:m2         # Ireland Defence Forces
mise run cianchosaint:bidp:v1:m3         # JSP/JDP doctrine
# BIIP v1 milestones (intelligence oversight pipeline)
mise run cianchosaint:biip:v1:m1         # UK ISC + IPCO + IPT
mise run cianchosaint:biip:v1:m2         # ROI oversight bodies
mise run cianchosaint:biip:v1:m3         # NI Policing Board + Garda Inspectorate
```

### CCC indexing
```bash
mise run cianchosaint:ccc:init          # first-time CCC setup
mise run cianchosaint:ccc:index         # rebuild the semantic code search index
mise run cianchosaint:ccc:search "<query>"  # semantic search over the codebase
```

### Per-persona web apps
```bash
mise run cianchosaint:web:list          # list all 8 per-persona web apps
```

---

## 4. The 11 canonical specs — what each one does

Per the openspec/specs/ directory:

| Spec | Requirements | Purpose |
|---|--:|---|
| `cianchosaint-pipeline` | 9 + 2 | The data-pipeline umbrella (foundation + wholesale-copy) |
| `cianchosaint-bootstrap-v2` | 13 | The wholesale-copy umbrella (the 13 Requirements that lock the platform structure) |
| `cianchosaint-agentic-interaction` | 6 + 2 + 2 | The Google ADK + 4-tier chain + BrowserToolRouter contract |
| `cianchosaint-self-hosted-citizen` | 4 + 2 | The self-hosted citizen Docker Compose bundle + Locket + private Pangolin |
| `cianchosaint-per-constituency-agents` | 6 + 2 | The GA / MET / PSNI root agents + 15 specialists + 7 tools |
| `cianchosaint-per-constituency-dlt-sources` | 2 | The 26-source per-constituency DLT source manifest (Q1 Change 3) |
| `cianchosaint-political-party-pipeline` | 3 | The 24-political-party DLT pipeline (Q1 Change 4) |
| `cianchosaint-intelligence-agency-pipeline` | 2 | The 5-UK-intelligence-agency DLT pipeline (Q1 Change 5) |
| `cianchosaint-deployment` | 6 | The deployment runbook contract (Q2 Change 1) |
| `cianchosaint-source-catalogue` | 4 | The British Isles source catalogue contract (Q2 Change 2) |
| `cianchosaint-reform-uk-pilot-workflow` | 3 | The Reform UK pilot case study workflow (Q2 Change 7) |

For each spec, the **canonical** version lives at `openspec/specs/<spec-name>/spec.md`. **Never hand-edit** the canonical spec directly — use openspec changes.

---

## 5. The OSINT allowlist — when to add to it

The OSINT allowlist at `dlt_sources/cianchosaint/common/osint_allowlist.yaml` is the **single source of truth** for what URLs the platform considers lawful OSINT. Every DLT source URL MUST be in the allowlist before `mise run lint:license` will pass.

**To add a new entry:**

1. Edit `dlt_sources/cianchosaint/common/osint_allowlist.yaml`
2. Add the new entry with the appropriate category:
   ```yaml
   - url: "<new url>"
     category: <intelligence_agency | military | emergency_service | agency | party | court | government | university | school | jurisdiction>
     body: "<name of the body>"
     jurisdiction: <uk | ireland | ni | scotland | wales | jersey | guernsey | iom>
     note: "<any caveats — e.g. 'public-facing content only'>"
   ```
3. Run `mise run lint:license` to verify
4. Run `mise run openspec:validate-all` to verify

**Never add:**
- Foreign intelligence agencies (DGSE, BND, Mossad, MSS, GRU, FSB, etc.) — explicitly banned by the licence
- Private-sector commercial URLs — banned (non-commercial only)
- Personal-data URLs — banned (the platform is OSINT-only)
- Classified-material URLs — banned (the OSINT ceiling is "public-facing content only")

---

## 6. The 13 compose stacks — when each is needed

Per the [deployment runbook](./DEPLOYMENT.md), the 13 compose stacks are:

| Stack | When you need it |
|---|---|
| `litellm` | Always (the LLM gateway) |
| `langfuse` | Always (the observability layer) |
| `motherduck` | Always (the storage layer — DuckDB + MotherDuck SaaS) |
| `lakehouse` | Always (DuckLake + LanceDB + Garage S3 + Postgres + Lakekeeper) |
| `unsloth-serve` | Always (the PRIMARY LLM provider) |
| `openchamber` | Always (the agent IDE for per-constituency analysts) |
| `crawl4ai` | Always (open-source browser tool) |
| `changedetection` | Optional (page-change monitoring for OSINT freshness) |
| `komodo` | Always (the resource-sync + procedure engine) |
| `pangolin` | Always (the reverse proxy + private resources) |
| `infisical` | Always (the secrets management) |
| `locket` | Always (the secret-injection sidecar) |
| `stagehand` | Always (the open-source Stagehand + headless Chrome browser automation) |

**13 stacks total** (was 12 named; `stagehand` + `locket` were built from scratch per the bootstrap-v2 change).

---

## 7. The 24 per-constituency Google ADK agents

Per the `cianchosaint-per-constituency-agents` spec:

### 3 root agents
- `ga_root_agent.py` — An Garda Síochána (Ireland)
- `met_root_agent.py` — Metropolitan Police + 43 UK forces
- `psni_root_agent.py` — PSNI (Northern Ireland)

### 15 specialist agents (5 per constituency)
- **GA**: `crime_statistics_agent`, `traffic_law_agent`, `foia_requests_agent`, `irish_statute_book_agent`, `courts_ie_agent`
- **MET**: `crime_statistics_agent`, `stop_and_search_agent`, `met_press_releases_agent`, `met_public_contact_agent`, `crime_prevention_agent`
- **PSNI**: `crime_statistics_agent`, `psni_press_releases_agent`, `psni_public_contact_agent`, `ni_justice_agent`, `policing_board_agent`

### 7 FunctionTool agents (cross-constituency)
- `garda_form_fill.py`, `met_form_fill.py`, `psni_form_fill.py` — non-emergency form fillers
- `statute_lookup.py`, `force_lookup.py`, `foia_request.py` — cross-constituency lookups
- `cross_jurisdiction_query.py` — PSNI ↔ Garda cross-border queries

Plus the new `reform_uk_pilot.py` (per Q12 = B — the first case study pilot).

---

## 8. The 8 per-persona web apps — deployment overview

| App | URL pattern | Backing agent |
|---|---|---|
| `ciafagent-ga-public` | `ga.cianchosaint.ie` | `ga_root_agent` (public) |
| `ciafagent-ga-internal` | `ga-internal.cianchosaint.ie` | `ga_root_agent` (analyst) |
| `ciafagent-met-public` | `met.cianchosaint.ie` | `met_root_agent` (public) |
| `ciafagent-met-internal` | `met-internal.cianchosaint.ie` | `met_root_agent` (analyst) |
| `ciafagent-psni-public` | `psni.cianchosaint.ie` | `psni_root_agent` (public) |
| `ciafagent-psni-internal` | `psni-internal.cianchosaint.ie` | `psni_root_agent` (analyst) |
| `ciafagent-self-host` | `localhost:7777` (self-hosted citizen) | (all agents, self-hosted) |
| `ciafagent-api` | `api.cianchosaint.ie` | (Hono API gateway to all agents) |

---

## 9. Fresh-user onboarding (5-minute quickstart)

If you're a fresh user (public-sector analyst, intelligence-community engineer, or British Isles citizen) wanting to USE the platform:

### For self-hosted citizen use:
```bash
# 1. Download the self-hosted bundle
git clone https://github.com/cianfhoghlaim/cianchosaint
cd cianchosaint/web/apps/ciafagent-self-host

# 2. Set your LLM API key (BYOK — bring your own key)
export UNSLOTH_STUDIO_API_KEY=...
# or use LiteLLM, MiniMax, or Gemini instead

# 3. Start the Docker Compose bundle
docker compose up -d

# 4. Open the AG-UI interface
open http://localhost:7777
```

### For public-sector analyst use:
```bash
# 1. Clone the cianchosaint repo
git clone https://github.com/cianfhoghlaim/cianchosaint
cd cianchosaint

# 2. Sync + install
mise run sync:all

# 3. Verify the OSINT allowlist + openspec
mise run lint:license
mise run openspec:validate-all

# 4. Run a milestone gate
mise run cianchosaint:bipp:v1:m1  # Ireland ROI

# 5. Browse the source catalogue
ls docs/source-catalogue/

# 6. Read the case study
cat docs/case-study/reform-uk-pilot.md
```

### For developer / contributor use:
```bash
# 1. Clone + setup
git clone https://github.com/cianfhoghlaim/cianchosaint
cd cianchosaint
mise run core  # full bootstrap

# 2. Browse the openspec
openspec list --specs
openspec list

# 3. Set up CCC for semantic code search
bun run ccc:init
bun run ccc:index

# 4. Search the codebase
bun run ccc:search "British Isles policing"

# 5. Read the wholesale-copy docs
cat AGENTS.md
cat openspec/AGENTS.md
cat docs/DEPLOYMENT.md
```

---

## 10. Common gotchas + troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `openspec validate` fails with "ADDED failed — already exists" | The delta conflicts with an already-applied spec | Use `--skip-specs` flag during archive; the canonical spec already has the Requirements |
| `mise run lint:license` reports URLs outside the allowlist | The DLT source URL is not in `osint_allowlist.yaml` | Add the URL to the allowlist (see §5) |
| The 4-tier provider chain is "stuck on Tier 4 (Gemini)" | The other 3 providers are unreachable | Check `mise run cianchosaint:provider:health-check`; ensure UNSLOTH_STUDIO_BASE_URL + LITELLM_BASE_URL + MINIMAX_BASE_URL are set |
| `mise run cianchosaint:bipp:v1:m2` fails with "no data returned" | data.police.uk API is down OR the force_id is misconfigured | Check `data_police_uk.py` + the curl example in `docs/DEPLOYMENT.md` §11 |
| The platform returns OSINT for a foreign entity | The OSINT allowlist has been bypassed | This is a licence violation — file an issue immediately |
| `bun run ccc:search` returns no results | The CCC index hasn't been built yet | Run `bun run ccc:init && bun run ccc:index` |
| The Locket sidecar is "secret not found" | The Locket is running but the Pangolin-issued token isn't there | Check Pangolin resource config + the Locket logs |

---

## 11. When in doubt

1. **Read [`docs/DEPLOYMENT.md`](./DEPLOYMENT.md)** first — it's the canonical deployment reference
2. **Browse [`docs/source-catalogue/`](./source-catalogue/)** — every British Isles source is documented there
3. **Read [`docs/case-study/reform-uk-pilot.md`](./case-study/reform-uk-pilot.md)** — the first concrete use case
4. **Read the [LICENSE.md](../LICENSE.md)** — the licence is the load-bearing legal document
5. **Ask the openspec validate gate** — `mise run openspec:validate-all`
6. **Search the CCC index** — `bun run ccc:search "<query>"`
7. **File an issue** on https://github.com/cianfhoghlaim/cianchosaint/issues if you find a bug

---

## 12. Contact

- **Licensor:** Cian Pierce Lyons (Irish Passport Name: Cian Mac Liatháin)
- **Email:** cianmacliathain@gmail.com
- **Repository:** https://github.com/cianfhoghlaim/cianchosaint
- **Licence questions:** see [LICENSE.md](../LICENSE.md) §3-step foreign-use gate + §warrant-to-enforce clause
