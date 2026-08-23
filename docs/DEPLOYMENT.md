# CIANCHOSAINT Deployment Runbook

> Per the [`openspec/changes/cianchosaint-deployment-runbook-v1/`](openspec/changes/cianchosaint-deployment-runbook-v1/specs/cianchosaint-deployment/spec.md) spec.
>
> **Audience:** operators bringing up the cianchosaint platform from cold
> on `arm1-oci` (production), `bunchloch` (MacBook M4 local-dev), or a
> citizen self-host Docker bundle.
>
> **Scope:** the 13 Docker Compose stacks + the 8 per-persona web apps +
> the 24 per-constituency Google ADK agents + the 4-tier
> `ModelProviderRouter` + the CCC indexing + the OSINT allowlist.

## 1. Overview

Cianchosaint is a defensive OSINT pipeline for British Isles
defence / policing / intelligence-oversight public-sector bodies.
The platform comprises:

- **13 Docker Compose stacks** under `bonneagar/stacks/` (see §2).
- **8 per-persona web apps** under `web/apps/ciafagent-*/` (see §6).
- **24 per-constituency Google ADK agents** under
  `agents/cianchosaint/` (3 root + 15 specialists + 6 FunctionTool
  wrappers; see §7).
- **The 4-tier `ModelProviderRouter`** at
  `baml_src/_shared/provider_router.py` — Unsloth Studio → LiteLLM →
  MiniMax → Gemini (see §5).
- **CCC semantic code search** at `.cocoindex_code/` (12 initial concept
  guides; see §5).
- **The OSINT allowlist** at
  `dlt_sources/cianchosaint/common/osint_allowlist.yaml` — enforces the
  licence ceiling (British Isles public-sector bodies only; see §5).

The 32 mise tasks at `mise.toml` group into 6 namespaces: `core:`, `lint:`,
`sync:`, `openspec:`, `devops:`, `cianchosaint:` (the defence-specific
namespace).

## 2. The 13 compose stacks

| # | Stack | Port | Purpose | Env vars | Depends on |
|--:|:--|--:|:--|:--|:--|
| 1 | `infisical` | 8443 | Secrets management (source of truth) | `INFISICAL_TOKEN`, `INFISICAL_PROJECT_ID` | — |
| 2 | `motherduck` | 5432 (pg proxy) | Cloud DuckDB via Postgres endpoint | `MOTHERDUCK_TOKEN`, `MD_DB_NAME` | `infisical` |
| 3 | `lakehouse` | 3900-3904, 5433, 8181-8182 | Garage S3 + Postgres + Lakekeeper | `LAKEHOUSE_DB_PASSWORD`, `LAKEKEEPER_ADMIN_TOKEN` | `infisical`, `motherduck` |
| 4 | `litellm` | 4000 | LLM gateway (the 76-entry MODEL_REGISTRY) | `LITELLM_MASTER_KEY`, `OPENAI_API_KEY` (provider 3+4) | `infisical`, `motherduck` |
| 5 | `unsloth-serve` | 8889 | Tier-1 local LLM (Unsloth Studio GGUF) | `UNSLOTH_MODEL`, `UNSLOTH_QUANT` | `infisical` |
| 6 | `langfuse` | 3000 | LLM observability (traces, costs) | `LANGFUSE_SECRET_KEY`, `LANGFUSE_PUBLIC_KEY` | `infisical`, `motherduck` |
| 7 | `crawl4ai` | 11235 | Self-hosted browser scraper | `CRAWL4AI_API_KEY` | `infisical` |
| 8 | `stagehand` | 11300 | Stagehand + headless Chrome (login-gated) | `STAGEHAND_BROWSER_TOKEN` | `infisical`, `crawl4ai` |
| 9 | `changedetection` | 5000 | Page-change monitor | `CHANGEDETECTION_API_KEY` | `infisical` |
| 10 | `komodo` | 9120 | GitOps deployment orchestrator | `KOMODO_ADMIN_API_KEY`, `KOMODO_WEBHOOK_SECRET` | `infisical`, `pangolin` |
| 11 | `pangolin` | 8443 (alt) | Reverse proxy + identity (Pocket ID) | `PANGOLIN_DOMAIN`, `POCKET_ID_CLIENT_SECRET` | `infisical` |
| 12 | `locket` | (sidecar) | Secret-injection sidecar (no exposed port) | `LOCKET_TOKEN` | `infisical` |
| 13 | `openchamber` | 3030 | OpenCode web/desktop UI | `OPENCHAMBER_ADMIN_TOKEN` | `infisical`, `komodo`, `pangolin` |

The 13 stacks implement the 6-file GOLD_STANDARD pattern:
`compose.yaml` + `sidecar.yaml` + `secrets.env` + `pangolin.yaml` +
`blueprint.yaml` + `.env.example`. Per the
[`infrastructure-stacks`](https://github.com/cianfhoghlaim/cianchosaint/blob/main/openspec/specs/cianchosaint-bootstrap-v2/spec.md)
contract.

## 3. Stack ordering — which to start first

When bringing up the platform from cold (e.g. on a fresh machine or
after a power outage on `arm1-oci`), start the 13 stacks in this exact
order. Skipping a tier breaks downstream tier dependencies.

```
1. secrets        →  infisical                  (everything depends on this)
2. storage        →  motherduck, lakehouse      (LLM gateways need to log traces)
3. LLM            →  litellm, unsloth-serve    (Unsloth first; LiteLLM routes to Unsloth)
4. observability  →  langfuse                  (LLM gateways need to flush traces)
5. browser        →  crawl4ai, stagehand       (Firefox + Chrome bring-up is slow)
6. monitoring     →  changedetection           (sensors must come after the sources they watch)
7. governance     →  komodo, pangolin, locket  (orchestration + routing + secret-injection)
8. UI             →  openchamber               (web UI last; it depends on everything above)
```

**Why this order matters:**

- **Infisical first**: every other stack has `infisical://dev-baile/...`
  references in its `secrets.env`. Without Infisical, no secrets hydrate.
- **Motherduck + Lakehouse before LLM**: LiteLLM's Postgres-backed rate-
  limiting + Langfuse's trace storage both need the storage tier up.
- **Unsloth before LiteLLM**: Unsloth Studio is Tier 1 of the 4-tier
  router; LiteLLM's `default_model` aliases route to it. Starting
  LiteLLM first causes a 30s timeout while it waits for Unsloth.
- **Browser tools (crawl4ai, stagehand) before monitoring**: the
  `changedetection` sensors can include browser-driven change-detection
  rules. Starting monitoring first causes "source unavailable" alerts.
- **Governance before UI**: openchamber's UI needs the Komodo API +
  the Pangolin ingress to be live to render the deployment status page.

## 4. Per-stack deployment

Each subsection documents the env vars, deploy commands, smoke test,
and rollback for one of the 13 stacks.

### 4.1 `infisical`

- **Env vars**: `INFISICAL_TOKEN`, `INFISICAL_PROJECT_ID`,
  `INFISICAL_ENVIRONMENT=dev-baile`
- **Deploy**:
  ```bash
  cd bonneagar/stacks/infisical
  mise run secrets:init       # hydrates .env from .infisical.env
  docker compose up -d
  ```
- **Smoke test**: `curl -s http://localhost:8443/api/status | jq .`
- **Rollback**:
  ```bash
  docker compose down -v
  # Infisical is the source of truth — no rollback of secrets, but
  # revoke any leaked tokens via the Infisical UI.
  ```

### 4.2 `motherduck`

- **Env vars**: `MOTHERDUCK_TOKEN`, `MD_DB_NAME=cianchosaint`
- **Deploy**:
  ```bash
  cd bonneagar/stacks/motherduck
  locket inject -- docker compose up -d
  ```
- **Smoke test**:
  `curl -s http://localhost:5432/health || psql -h localhost -p 5432 -U md -c "SELECT 1;"`
- **Rollback**: `docker compose down; locket revoke-token $MOTHERDUCK_TOKEN`

### 4.3 `lakehouse`

- **Env vars**: `LAKEHOUSE_DB_PASSWORD`, `LAKEKEEPER_ADMIN_TOKEN`,
  `GARAGE_ACCESS_KEY`, `GARAGE_SECRET_KEY`
- **Deploy**:
  ```bash
  cd bonneagar/stacks/lakehouse
  docker compose -f compose.yaml -f compose.dev.yaml up -d
  ```
- **Smoke test**:
  `curl -s http://localhost:3900/health && curl -s http://localhost:8181/management/v1/warehouse | jq .`
- **Rollback**:
  `docker compose down; locket revoke-token $LAKEKEEPER_ADMIN_TOKEN`

### 4.4 `litellm`

- **Env vars**: `LITELLM_MASTER_KEY`, `OPENAI_API_KEY` (for tier 4),
  `UNSLOTH_SERVE_URL=http://unsloth-serve:8889`
- **Deploy**:
  ```bash
  cd bonneagar/stacks/litellm
  docker compose up -d
  ```
- **Smoke test**:
  `curl -s -H "Authorization: Bearer $LITELLM_MASTER_KEY" http://localhost:4000/v1/models | jq '.data[].id'`
- **Rollback**:
  `docker compose down; # Master key rotation via locket revoke-token`

### 4.5 `unsloth-serve`

- **Env vars**: `UNSLOTH_MODEL=unsloth/Qwen3-8B-Instruct-UD-Q4_K_XL`,
  `UNSLOTH_QUANT=UD-Q4_K_XL`
- **Deploy**:
  ```bash
  cd bonneagar/stacks/unsloth-serve
  docker compose up -d
  ```
- **Smoke test**:
  `curl -s http://localhost:8889/v1/models | jq '.data[].id'`
- **Rollback**:
  `docker compose down; # The GGUF model files live on the host's
  /Volumes/bunchloch/models/ — no rollback needed`

### 4.6 `langfuse`

- **Env vars**: `LANGFUSE_SECRET_KEY`, `LANGFUSE_PUBLIC_KEY`,
  `DATABASE_URL=postgresql://postgres:$POSTGRES_PASSWORD@motherduck:5432/langfuse`
- **Deploy**:
  ```bash
  cd bonneagar/stacks/langfuse
  docker compose up -d
  ```
- **Smoke test**:
  `curl -s http://localhost:3000/api/public/health | jq .`
- **Rollback**:
  `docker compose down; # Trace data is in Postgres — backup first if
  you care about the history`

### 4.7 `crawl4ai`

- **Env vars**: `CRAWL4AI_API_KEY`
- **Deploy**:
  ```bash
  cd bonneagar/stacks/crawl4ai
  docker compose up -d
  ```
- **Smoke test**:
  `curl -s -H "Authorization: Bearer $CRAWL4AI_API_KEY" http://localhost:11235/health | jq .`
- **Rollback**: `docker compose down`

### 4.8 `stagehand`

- **Env vars**: `STAGEHAND_BROWSER_TOKEN`
- **Deploy**:
  ```bash
  cd bonneagar/stacks/stagehand
  docker compose up -d
  ```
- **Smoke test**:
  `curl -s -H "Authorization: Bearer $STAGEHAND_BROWSER_TOKEN" http://localhost:11300/health | jq .`
- **Rollback**: `docker compose down; locket revoke-token $STAGEHAND_BROWSER_TOKEN`

### 4.9 `changedetection`

- **Env vars**: `CHANGEDETECTION_API_KEY`
- **Deploy**:
  ```bash
  cd bonneagar/stacks/changedetection
  docker compose up -d
  ```
- **Smoke test**:
  `curl -s http://localhost:5000/ | jq .status`
- **Rollback**: `docker compose down`

### 4.10 `komodo`

- **Env vars**: `KOMODO_ADMIN_API_KEY`, `KOMODO_WEBHOOK_SECRET`
- **Deploy**:
  ```bash
  cd bonneagar/stacks/komodo
  docker compose up -d
  ```
- **Smoke test**:
  `curl -s -H "Authorization: Bearer $KOMODO_ADMIN_API_KEY" http://localhost:9120/health | jq .`
- **Rollback**: `docker compose down; locket revoke-token $KOMODO_ADMIN_API_KEY`

### 4.11 `pangolin`

- **Env vars**: `PANGOLIN_DOMAIN=*.cianchosaint.ie`,
  `POCKET_ID_CLIENT_SECRET`
- **Deploy**:
  ```bash
  cd bonneagar/stacks/pangolin
  docker compose up -d
  ```
- **Smoke test**:
  `curl -s https://pangolin.cianchosaint.ie/api/v1/ | jq .`
- **Rollback**: `docker compose down; locket revoke-token $POCKET_ID_CLIENT_SECRET`

### 4.12 `locket`

- **Env vars**: `LOCKET_TOKEN`, `INFISICAL_PROJECT_ID`
- **Deploy**:
  ```bash
  cd bonneagar/stacks/locket
  docker compose up -d
  ```
- **Smoke test**:
  `docker logs locket && curl -s http://localhost:9999/health | jq .`
- **Rollback**:
  `docker compose down; locket revoke-token $LOCKET_TOKEN`

### 4.13 `openchamber`

- **Env vars**: `OPENCHAMBER_ADMIN_TOKEN`, `KOMODO_API_URL`,
  `PANGOLIN_API_URL`
- **Deploy**:
  ```bash
  cd bonneagar/stacks/openchamber
  docker compose up -d
  ```
- **Smoke test**:
  `curl -s -H "Authorization: Bearer $OPENCHAMBER_ADMIN_TOKEN" http://localhost:3030/health | jq .`
- **Rollback**: `docker compose down`

## 5. Cross-stack contracts

### 5.1 Locket sidecar pattern

The Locket sidecar (`bonneagar/stacks/locket/`) is the canonical secret-
injection mechanism. The pattern:

1. Every other stack's `secrets.env` declares `infisical://dev-baile/...`
   template refs (e.g. `LITELLM_MASTER_KEY=infisical://dev-baile/cianchosaint/litellm-master-key`).
2. The mise hook (in `~/.config/mise/config.toml`) watches `cd` into the
   cianchosaint repo and runs `bun run secrets:init` which writes `.env`
   from the template.
3. At container start time, Locket (running as a sidecar or via
   `locket inject -- <cmd>`) reads the `.env` template, resolves the
   `infisical://` refs against the live Infisical vault, and injects
   the resolved values into the container's environment.
4. `.env` is gitignored — only `.infisical.env` (the template) is
   committed.

**Why Locket:** the previous `op run` (1Password) + SOPS pattern from
Cianfhoghlaim's predecessor was superseded by the Infisical + Locket +
mise three-way contract per the `cianchosaint-repo-foundation-v1`
change. 1Password was migrated to Infisical in 2026-06.

### 5.2 Komodo + Pangolin wiring

Komodo orchestrates stack deployment; Pangolin provides the reverse
proxy + identity layer. The wiring:

- Komodo has resource-syncs for each of the 13 stacks (in
  `bonneagar/komodo/stacks/`). The resource-sync declares the
  `compose.yaml` URL + the env vars + the health check.
- Pangolin has a resource declaration for each stack (in
  `bonneagar/stacks/<name>/pangolin.yaml`). The resource declares the
  domain (e.g. `litellm.cianchosaint.ie`), the upstream target (e.g.
  `http://litellm:4000`), and the auth (Pocket ID).
- When Komodo brings up a stack, it notifies Pangolin via webhook, which
  provisions the DNS record + the TLS cert + the routing rule.

### 5.3 The 4-tier provider chain

The `ModelProviderRouter` (at `baml_src/_shared/provider_router.py`)
routes LLM calls through 4 tiers:

| Tier | Provider | URL | Role |
|--:|:--|:--|:--|
| 1 | **Unsloth Studio** (local GGUF) | `http://localhost:8889/v1` | **Primary**. Default for all BAML calls. |
| 2 | **LiteLLM** (our gateway) | `http://litellm:4000/v1` | Fallback #1. Routes the 76-entry MODEL_REGISTRY. |
| 3 | **MiniMax Token Plan** | `https://api.minimax.chat/v1` | Fallback #2. Hosted. |
| 4 | **Gemini API** | `https://generativelanguage.googleapis.com/v1` | Fallback #3. Last-resort. |

**Failover algorithm** (per `provider_router.py:get_active_config()`):

1. Try Tier 1. If response received within 30s, return.
2. On timeout/5xx, fall through to Tier 2 with the same model name.
3. On timeout/5xx, fall through to Tier 3 with the model name remapped
   (e.g. `qwen3.7-max` → `MiniMax-Text-01`).
4. On timeout/5xx, fall through to Tier 4 (Gemini).
5. If Tier 4 fails, raise `ProviderChainExhausted`.

The active tier is logged via Langfuse with the `provider_tier` attribute
on every trace.

### 5.4 The OSINT allowlist

The OSINT allowlist at
`dlt_sources/cianchosaint/common/osint_allowlist.yaml` enforces the
licence ceiling (British Isles public-sector bodies only). Every DLT
source URL MUST be in the allowlist; `mise run lint:license` will
fail CI if a source URL is unallowlisted.

The allowlist is currently maintained by hand. A future
`cianchosaint-allowlist-curator-v1` change may automate the
classifier-based extension.

### 5.5 CCC indexing

The CCC semantic code search index lives at `.cocoindex_code/`. The
3 setup tasks:

```bash
bun run ccc:init       # first time only
bun run ccc:index      # incremental refresh
bun run ccc:search "Dagster asset partition"
```

The `.cocoindex_code/guides.yml` file ships with 12 initial concept
guides (`openspec-change-search`, `dlt-source-search`,
`baml-function-search`, `cocoindex-flow-search`,
`browser-tool-router-search`, `bipp-v1-policing`, `bidp-v1-defence`,
`biip-v1-intel-oversight`, `firecrawl-corpus-search`,
`agent-fleet-search`, `per-persona-web-surfaces`,
`cianchosaint-pipeline-overview`).

## 6. The 8 per-persona web apps

The 8 apps live under `web/apps/ciafagent-*/`. Each is a TanStack Start
app + AG-UI + CopilotKit surface.

| # | App | URL | Route | Backing agent |
|--:|:--|:--|:--|:--|
| 1 | `ciafagent-ga-public` | `ga-public.cianchosaint.ie` | `/` | `ga_root_agent` (An Garda Síochána) |
| 2 | `ciafagent-ga-internal` | `ga-internal.cianchosaint.ie` | `/internal` | `ga_root_agent` (auth-gated) |
| 3 | `ciafagent-met-public` | `met-public.cianchosaint.ie` | `/` | `met_root_agent` (Met Police + 43 UK forces) |
| 4 | `ciafagent-met-internal` | `met-internal.cianchosaint.ie` | `/internal` | `met_root_agent` (auth-gated) |
| 5 | `ciafagent-psni-public` | `psni-public.cianchosaint.ie` | `/` | `psni_root_agent` (PSNI) |
| 6 | `ciafagent-psni-internal` | `psni-internal.cianchosaint.ie` | `/internal` | `psni_root_agent` (auth-gated) |
| 7 | `ciafagent-self-host` | `localhost:7777` | `/` | All 3 root agents (unified citizen surface) |
| 8 | `ciafagent-api` | `api.cianchosaint.ie` | `/api/*` | (Hono API gateway; no UI) |

The `${X}-public` surfaces are anonymous read-only dashboards. The
`${X}-internal` surfaces require Pocket ID auth (Pangolin-gated) and
expose the FOIA form filler + the case file builder. The `ciafagent-api`
Hono gateway is the OpenAI-compatible API for the agent fleet (used
by `web/apps/ciafagent-self-host` to call agents without going through
the web).

## 7. The 24 per-constituency agents

The 24-agent fleet lives at `agents/cianchosaint/`. The breakdown:

| # | Agent | Constituency | Sub-domain | Backing BAML |
|--:|:--|:--|:--|:--|
| 1 | `ga_root_agent` | An Garda Síochána | orchestration | (router) |
| 2 | `ga_crime_statistics_agent` | An Garda Síochána | crime_statistics | `ExtractCrimeStatistics` |
| 3 | `ga_traffic_law_agent` | An Garda Síochána | traffic_law | `ExtractTrafficLaw` |
| 4 | `ga_foia_requests_agent` | An Garda Síochána | foia | `ExtractFOIARequest` |
| 5 | `irish_statute_book_agent` | An Garda Síochána | statutory | `ExtractStatute` |
| 6 | `courts_ie_agent` | An Garda Síochána | courts | `ExtractCourtJudgement` |
| 7 | `met_root_agent` | Met Police + 43 UK forces | orchestration | (router) |
| 8 | `met_crime_statistics_agent` | Met Police + 43 UK | crime_statistics | `ExtractCrimeStatistics` |
| 9 | `met_stop_and_search_agent` | Met Police + 43 UK | stop_and_search | `ExtractStopSearch` |
| 10 | `met_press_releases_agent` | Met Police + 43 UK | press_releases | `ExtractPressRelease` |
| 11 | `met_public_contact_agent` | Met Police + 43 UK | public_contact | `ExtractPublicContact` |
| 12 | `met_crime_prevention_agent` | Met Police + 43 UK | crime_prevention | `ExtractCrimePrevention` |
| 13 | `psni_root_agent` | PSNI | orchestration | (router) |
| 14 | `psni_crime_statistics_agent` | PSNI | crime_statistics | `ExtractCrimeStatistics` |
| 15 | `psni_press_releases_agent` | PSNI | press_releases | `ExtractPressRelease` |
| 16 | `psni_public_contact_agent` | PSNI | public_contact | `ExtractPublicContact` |
| 17 | `ni_justice_agent` | PSNI | justice_ni | `ExtractNIJustice` |
| 18 | `policing_board_agent` | PSNI | policing_board | `ExtractPolicingBoard` |
| 19 | `garda_form_fill` (tool) | An Garda Síochána | form_fill | `ExtractFormFields` |
| 20 | `met_form_fill` (tool) | Met Police + 43 UK | form_fill | `ExtractFormFields` |
| 21 | `psni_form_fill` (tool) | PSNI | form_fill | `ExtractFormFields` |
| 22 | `statute_lookup` (tool) | All jurisdictions | statutory | (read-only) |
| 23 | `force_lookup` (tool) | All UK forces | metadata | (read-only) |
| 24 | `foia_request` (tool) | All jurisdictions | foia | `ExtractFOIARequest` |

The 3 root agents orchestrate their 5 specialists each (15 specialists
total). The 6 FunctionTool wrappers are shared across all 3 roots.

## 8. Deployment to `arm1-oci`

The control-plane host (`arm1-oci` — Oracle Cloud A1.Flex ARM instance)
hosts the production deployment. The procedure:

```bash
# 1. SSH to arm1-oci
ssh cianfhoghlaim@arm1-oci.local

# 2. Sync the latest infra branch
cd /opt/cianchosaint
git fetch origin
git checkout main
git pull --ff-only

# 3. Hydrate Infisical secrets (the Locket sidecar handles per-container
# injection at runtime, but the .env on the host needs hydration too)
mise run secrets:init

# 4. Bring up the 13 stacks in lifecycle order
for tier in infisical motherduck lakehouse unsloth-serve litellm langfuse \
            crawl4ai stagehand changedetection komodo pangolin locket openchamber; do
  komodo deploy stack $tier
done

# 5. Bring up the 8 web apps (each is its own wrangler deploy)
for app in ciafagent-ga-public ciafagent-ga-internal ciafagent-met-public \
           ciafagent-met-internal ciafagent-psni-public ciafagent-psni-internal \
           ciafagent-api ciafagent-self-host; do
  mise run cianchosaint:web:deploy --app=$app
done

# 6. Run the 3 health checks (§12)
mise run cianchosaint:provider:health-check
mise run cianchosaint:browser-tool:health-check
mise run cianchosaint:osint:health-check

# 7. Validate the Pangolin ingress for each public-facing service
for host in ga-public ciafagent-met-public ciafagent-psni-public \
            ciafagent-api; do
  curl -sf https://$host.cianchosaint.ie/health || echo "FAIL: $host"
done
```

## 9. Deployment to `bunchloch` (MacBook M4 local-dev)

The local-dev host (`bunchloch` — MacBook M4 Max) hosts a single-node
deployment for development. The procedure:

```bash
# 1. cd into the repo (mise hooks auto-hydrate .env)
cd /Users/cianmacandeisigh/dev/cianchosaint

# 2. Hydrate secrets
mise run secrets:init

# 3. Bring up a SUBSET of the stacks (drop the governance tier;
#    use local Komodo + local Pangolin for dev)
for tier in infisical motherduck lakehouse unsloth-serve litellm langfuse \
            crawl4ai stagehand; do
  cd bonneagar/stacks/$tier
  docker compose -f compose.yaml -f compose.dev.yaml up -d
  cd -
done

# 4. Bring up the 8 web apps in dev mode (TanStack Start `bun run dev`)
mise run web:dev ciafagent-ga-public
mise run web:dev ciafagent-met-public
mise run web:dev ciafagent-psni-public
# ... etc.

# 5. Run the 3 health checks (they should all pass; if Tier 1 fails,
#    confirm Unsloth GGUF is at /Volumes/bunchloch/models/)
mise run cianchosaint:provider:health-check
mise run cianchosaint:browser-tool:health-check
mise run cianchosaint:osint:health-check

# 6. Open the CCC search UI
ccc describe .     # project overview
ccc status         # chunk count + file count + language histogram
```

## 10. Self-host citizen deployment

The self-host bundle (`docker/ciafagent-self-host/`) is a single-Docker-
Compose bundle that lets a citizen run a private Cian instance on their
own laptop. It is **strictly restricted** by the licence — no commercial
use, no public exposure, no shared Infisical token.

```bash
# 1. Citizen downloads the bundle from the releases page
curl -L https://github.com/cianfhoghlaim/cianchosaint/releases/download/v1.0/docker-ciafagent-self-host.tar.gz | tar xz
cd ciafagent-self-host

# 2. Generate a per-tenant Infisical read-only token
# (this is a one-time operator-side action; the citizen never sees the
# Infisical master token)
# Operator-side:
mise run cianchosaint:self-host:infisical:provision --citizen-id=<id>

# 3. Set the citizen's local .env (Locket hydrates the rest)
echo "INFISICAL_READONLY_TOKEN=<the token from step 2>" > .env
echo "CITIZEN_ID=<id>" >> .env

# 4. Bring up the bundle
docker compose up -d

# 5. Access Cian in the browser
open http://localhost:7777

# 6. (Optional) Enable the private Pangolin resource
# (operator-side; creates a WireGuard tunnel into the citizen's laptop)
mise run cianchosaint:self-host:pangolin:enable --citizen-id=<id>
```

The self-host bundle includes only 5 of the 13 stacks (infisical-readonly,
unsloth-serve, crawl4ai, locket, openchamber). It deliberately excludes
the governance tier (komodo, pangolin, locket-wide) and the multi-tenant
storage (motherduck, lakehouse) — the citizen's data stays on their
laptop.

## 11. Smoke tests

| Stack | Smoke test command |
|:--|:--|
| `infisical` | `curl -s http://localhost:8443/api/status` |
| `motherduck` | `psql -h localhost -p 5432 -U md -c "SELECT 1;"` |
| `lakehouse` | `curl -s http://localhost:3900/health && curl -s http://localhost:8181/management/v1/warehouse` |
| `litellm` | `curl -s -H "Authorization: Bearer $LITELLM_MASTER_KEY" http://localhost:4000/v1/models` |
| `unsloth-serve` | `curl -s http://localhost:8889/v1/models` |
| `langfuse` | `curl -s http://localhost:3000/api/public/health` |
| `crawl4ai` | `curl -s -H "Authorization: Bearer $CRAWL4AI_API_KEY" http://localhost:11235/health` |
| `stagehand` | `curl -s -H "Authorization: Bearer $STAGEHAND_BROWSER_TOKEN" http://localhost:11300/health` |
| `changedetection` | `curl -s http://localhost:5000/` |
| `komodo` | `curl -s -H "Authorization: Bearer $KOMODO_ADMIN_API_KEY" http://localhost:9120/health` |
| `pangolin` | `curl -s https://pangolin.cianchosaint.ie/api/v1/` |
| `locket` | `curl -s http://localhost:9999/health` |
| `openchamber` | `curl -s -H "Authorization: Bearer $OPENCHAMBER_ADMIN_TOKEN" http://localhost:3030/health` |

The "all green" check is `mise run devops:validate-stacks && for stack in
$(ls bonneagar/stacks/); do mise run smoke:$stack; done`.

## 12. Health checks

The 3 platform-wide health checks:

```bash
# 1. The 4-tier provider chain — pings each of Unsloth Studio, LiteLLM,
# MiniMax, and Gemini in order. Returns the active tier + the round-trip
# latency for each.
mise run cianchosaint:provider:health-check
# Expected output:
#   Tier 1 (Unsloth Studio @ localhost:8889) : OK (124ms)
#   Tier 2 (LiteLLM @ litellm:4000)         : OK (342ms)
#   Tier 3 (MiniMax @ api.minimax.chat)    : OK (812ms)
#   Tier 4 (Gemini @ generativelanguage...) : OK (1240ms)
#   Active tier: 1 (Unsloth Studio)

# 2. The browser tools — confirms crawl4ai + stagehand can both scrape
# a known page (https://www.met.police.uk/) successfully.
mise run cianchosaint:browser-tool:health-check
# Expected output:
#   crawl4ai : OK (scrape of https://www.met.police.uk/ returned 200)
#   stagehand: OK (login flow against https://www.psni.police.uk/ succeeded)

# 3. The OSINT allowlist integrity — verifies every NEW DLT source URL
# is in the allowlist AND every allowlist entry points at a British Isles
# public-sector body.
mise run cianchosaint:osint:health-check
# Expected output:
#   Allowlist: 42 entries
#   British Isles bodies: 42/42
#   Unallowlisted DLT source URLs: 0
#   OSINT ceiling: intact
```

## 13. Rollback plan

If a stack fails on bring-up, the rollback is the inverse of §4. Per-stack:

### 13.1 Generic rollback procedure

For every stack except `infisical` (the source of truth):

```bash
cd bonneagar/stacks/<name>
docker compose down -v
# Then revoke any leaked tokens:
locket revoke-token $<LEAKED_TOKEN_VAR>
```

For `infisical` itself (the source of truth):

1. `docker compose down -v` (kills the Infisical container)
2. Revoke the leaked Infisical token via the Infisical UI directly
   (operator must log in to https://app.infisical.com/ and rotate)
3. Spin up a fresh `infisical` instance
4. Re-run `mise run secrets:init` to re-hydrate all dependent stacks

### 13.2 Per-stack rollback cheat-sheet

| Stack | Rollback command | Token to revoke |
|:--|:--|:--|
| `infisical` | manual UI rotation | `INFISICAL_TOKEN` |
| `motherduck` | `docker compose down; locket revoke-token $MOTHERDUCK_TOKEN` | `MOTHERDUCK_TOKEN` |
| `lakehouse` | `docker compose down -v` | `LAKEKEEPER_ADMIN_TOKEN` |
| `litellm` | `docker compose down` | `LITELLM_MASTER_KEY` |
| `unsloth-serve` | `docker compose down` | (no remote token) |
| `langfuse` | `docker compose down` | `LANGFUSE_SECRET_KEY` |
| `crawl4ai` | `docker compose down` | `CRAWL4AI_API_KEY` |
| `stagehand` | `docker compose down` | `STAGEHAND_BROWSER_TOKEN` |
| `changedetection` | `docker compose down` | `CHANGEDETECTION_API_KEY` |
| `komodo` | `docker compose down` | `KOMODO_ADMIN_API_KEY` |
| `pangolin` | `docker compose down` | `POCKET_ID_CLIENT_SECRET` |
| `locket` | `docker compose down` | `LOCKET_TOKEN` |
| `openchamber` | `docker compose down` | `OPENCHAMBER_ADMIN_TOKEN` |

### 13.3 Full-mesh rollback (the nuclear option)

If the entire mesh is in a bad state (e.g. an Infisical misconfig
poisoned all downstream stacks):

```bash
# 1. Stop everything (Komodo handles the orchestration)
komodo rollback all

# 2. Verify all stacks are down
docker ps --format '{{.Names}}' | grep -E 'cianchosaint|infisical|litellm' && echo "STILL RUNNING" || echo "ALL STOPPED"

# 3. Rotate the Infisical master token (via the Infisical UI)
# 4. Re-hydrate secrets
mise run secrets:init

# 5. Bring up the cold-start sequence again
for tier in infisical motherduck lakehouse unsloth-serve litellm langfuse \
            crawl4ai stagehand changedetection komodo pangolin locket openchamber; do
  komodo deploy stack $tier
done

# 6. Run the 3 health checks
mise run cianchosaint:provider:health-check
mise run cianchosaint:browser-tool:health-check
mise run cianchosaint:osint:health-check
```

---

**End of runbook.** For the canonical umbrella spec, see
[`openspec/specs/cianchosaint-deployment/spec.md`](openspec/specs/cianchosaint-deployment/spec.md).
For the openspec change that introduced this runbook, see
[`openspec/changes/cianchosaint-deployment-runbook-v1/`](openspec/changes/cianchosaint-deployment-runbook-v1/).
