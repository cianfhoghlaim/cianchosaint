# Cianchosaint Live Deployment + Real-Screenshot Workflow

> **Per the locked plan Q39 = A — plan for live deployment now** + **Q34 = A — replace ASCII with real PNG screenshots**
>
> **Companion docs:** [`docs/DEPLOYMENT.md`](./DEPLOYMENT.md) (the deployment procedure) + [`docs/DEPLOYMENT-SCREENSHOTS.md`](./DEPLOYMENT-SCREENSHOTS.md) (the current 11 ASCII references) + [`docs/DEMO-PATHS.md`](./DEMO-PATHS.md) (the 3 demo paths)

---

## 1. Why plan now

The cianchosaint platform is **fully implemented** at the structural + functional level:
- ✅ 24 canonical specs
- ✅ 23 archived openspec changes
- ✅ 0 pending changes
- ✅ ~97k LOC across ~770 files
- ✅ 8 per-persona web apps
- ✅ 24 per-constituency Google ADK agents
- ✅ 26 per-constituency DLT sources + 24 political party + 5 UK intel agency
- ✅ 13 compose stacks (11 wholesale-copied + 2 new-build)
- ✅ 4-tier ModelProviderRouter (Unsloth Studio → LiteLLM → MiniMax → Gemini)
- ✅ Per-source context-aware UI (SourcePolicyCard + PipelineGraph + VlmPipelineDashboard)
- ✅ 8.5k+ words of documentation across 17 doc files
- ✅ BUSL-1.1 v2 licence (British-Isles-only + 3-step foreign gate + warrant-to-enforce)

**What's left**: live deployment + real screenshots + user feedback.

---

## 2. The 13-stack deployment procedure (live)

The 13 stacks deploy in order. Each stack has its own `.env` + `compose.yaml` + `sidecar.yaml` + `pangolin.yaml` + `blueprint.yaml`. The canonical reference is `docs/DEPLOYMENT.md §4` (per-stack deployment).

### 2.1 The deployment order

| # | Stack | Why this order |
|--:|---|---|
| 1 | `infisical` | Secrets management — everything else needs it |
| 2 | `motherduck` | Storage — DuckLake + LanceDB depend on it |
| 3 | `lakehouse` | DuckLake + LanceDB + Garage S3 + Postgres + Lakekeeper |
| 4 | `unsloth-serve` | PRIMARY LLM provider (Tier 1) |
| 5 | `litellm` | LLM gateway (Tier 2 fallback) |
| 6 | `langfuse` | Observability (Langfuse spans + per-call costs + latency) |
| 7 | `crawl4ai` | Open-source browser tool (Crawl4AI MCP server) |
| 8 | `stagehand` | Open-source Stagehand + headless Chrome |
| 9 | `locket` | Secret-injection sidecar (every container needs it) |
| 10 | `changedetection` | Page-change monitoring (OSINT freshness) |
| 11 | `komodo` | Resource-sync + procedure engine |
| 12 | `pangolin` | Reverse proxy + private resources (`*.cianchosaint.ie`) |
| 13 | `openchamber` | Agent IDE (for per-constituency analysts) |

Plus the **8 per-persona web apps** (ciafagent-ga-public, ciafagent-ga-internal, ciafagent-met-public, ciafagent-met-internal, ciafagent-psni-public, ciafagent-psni-internal, ciafagent-self-host, ciafagent-api) — deployed via Cloudflare Workers + Containers.

### 2.2 The deployment roles

| Role | Who | What they do |
|---|---|---|
| **Licensor** | Cian Pierce Lyons | Approves the licence grant + the warrant-to-enforce invocations |
| **Deployer** | A platform engineer | Provisions cloud + DNS + Pangolin + Cloudflare + deploys the 13 stacks + the 8 web apps |
| **Operator** | A public-sector body analyst | Uses the platform for daily OSINT investigation |
| **Public** | British-Isles citizens | Uses the self-hosted Docker bundle for non-emergency form filling |
| **Developer / contributor** | The community | Files issues + PRs + authors new openspec changes |

---

## 3. The 4 deployment footprints (per the user's deployment scenario)

The 3 user personas map to 4 deployment footprints (per `docs/USAGE-GUIDELINES.md §9`):

### 3.1 Self-hosted citizen footprint (~8 GB RAM, ~1 hour to deploy)
- **Who**: A British-Isles citizen on their own machine
- **Components**: Docker Compose bundle at `docker/ciafagent-self-host/` + 5 containers (Unsloth Studio + LiteLLM + Locket + Crawl4AI + Stagehand)
- **Cloud dependencies**: NONE (all local)
- **Cost**: ~$0/month (only electricity for the machine)
- **Live deployment**: `git clone` → `docker compose up -d` → `open http://localhost:7777`

### 3.2 Public-sector analyst footprint (cloud deployment, ~$3k/month)
- **Who**: An Garda Síochána analyst + UK Home Office analyst + PSNI analyst + etc.
- **Components**: 13 compose stacks + 8 per-persona web apps + MotherDuck + Cloudflare Workers
- **Cloud dependencies**: arm1-oci (or Hetzner) + Pangolin + Cloudflare + Infisical + MotherDuck SaaS
- **Cost**: ~$3k/month (4 OCPU + 24 GB RAM + MotherDuck + Cloudflare + domain)
- **Live deployment**: provision cloud + DNS + deploy 13 stacks + deploy 8 web apps

### 3.3 Developer / contributor footprint (local dev, ~30 minutes to deploy)
- **Who**: A developer working on the platform
- **Components**: `mise run core` (sync + install + lint + test + format) + CCC indexing + opencode + openspec
- **Cloud dependencies**: NONE (local dev)
- **Cost**: ~$0/month
- **Live deployment**: `git clone` → `mise install` → `mise run core` → `openspec list` → `bun run ccc:init`

### 3.4 Pilot / case-study footprint (Reform UK, ~1 hour to deploy)
- **Who**: A public-sector analyst running the Q12 = B Reform UK pilot
- **Components**: The political party pipeline + the intelligence oversight pipeline + the Reform UK pilot FunctionTool + the per-source context-aware UI
- **Cloud dependencies**: Same as 3.2 (cloud deployment)
- **Cost**: ~$3k/month (same as 3.2)
- **Live deployment**: provision cloud + deploy 13 stacks + run `mise run cianchosaint:reform-uk-pilot:run`

---

## 4. The real-screenshot workflow (per Q34 = A)

### 4.1 The 11 screenshots to capture (live)

Per `docs/DEPLOYMENT-SCREENSHOTS.md §Live deployment checklist`, capture real PNG screenshots during each deployment step:

| # | Screenshot | When | How |
|--:|---|---|---|
| 1 | `mise run core` | After `mise install` | `open -a Terminal` + run command + screenshot |
| 2 | `mise run cianchosaint:provider:health-check` | After deploying unsloth-serve + litellm | Same |
| 3 | `mise run cianchosaint:bipp:v1:m1` | After deploying the GA pipeline | Same |
| 4 | `mise run cianchosaint:osint:health-check` | After extending the OSINT allowlist | Same |
| 5 | `bun run ccc:search "British Isles policing"` | After `bun run ccc:init && bun run ccc:index` | Same |
| 6 | `openspec list --specs` + `openspec list` | After `openspec archive` | Same |
| 7 | `python -c "from agents.cianchosaint.tools.reform_uk_pilot import reform_uk_pilot; ..."` | After running the Reform UK pilot | Same |
| 8 | `git log --oneline | head` | After committing all the deployment work | Same |
| 9 | `docker/ciafagent-self-host` | After running `docker compose up -d` for the citizen bundle | `open http://localhost:7777` + screenshot |
| 10 | `mise tasks ls --all` | After the platform is fully deployed | Same as #1 |
| 11 | `ls openspec/specs/` + `ls docs/` | After the documentation is finalised | Same |

### 4.2 Where to store the real PNGs

Store at `docs/screenshots/<step-name>.png` (a NEW directory under `docs/`):

```bash
mkdir -p docs/screenshots
```

Then replace the ASCII references in `docs/DEPLOYMENT-SCREENSHOTS.md` with the real PNGs using `git mv` or follow-up commits:

```bash
# Example: replace the ASCII Screenshot 1 with the real PNG
git mv docs/DEPLOYMENT-SCREENSHOTS.md docs/DEPLOYMENT-SCREENSHOTS.md.ascii-archive
cp docs/screenshots/01-mise-run-core.png docs/DEPLOYMENT-SCREENSHOTS.md
# (Then edit docs/DEPLOYMENT-SCREENSHOTS.md to add the image references)
```

### 4.3 The screenshot capture workflow (step-by-step)

#### Step 1 — Set up the screenshot capture
```bash
# macOS: use Cmd+Shift+4 to capture a region, or use the `screencapture` command
# Linux: use `gnome-screenshot -f /tmp/step1.png` or `import` (ImageMagick)

# Or use a CLI like `spectacle` (Linux) / `cleanshot` (macOS)

# Or use the browser's screenshot feature (Chrome DevTools)
```

#### Step 2 — For each of the 11 deployment steps
1. Execute the command (e.g. `mise run cianchosaint:bipp:v1:m1`)
2. Wait for the output to render (10-60 seconds for most commands)
3. Capture a PNG of the output (region screenshot, ~1600x1200 px)
4. Save to `docs/screenshots/<step-number>-<step-name>.png`
5. Verify the PNG is readable (open in Preview / image viewer)
6. If the output differs from the ASCII reference, file an issue

#### Step 3 — Update the docs/DEPLOYMENT-SCREENSHOTS.md
Replace each ASCII section with a markdown image reference:
```markdown
## Screenshot 1 — `mise run core` (the dev bootstrap)

![mise run core output](./screenshots/01-mise-run-core.png)

The output shows the 7-step bootstrap pipeline: paths + CCC + openspec + skills + drift-docs + licence + smoke tests, all passing.
```

#### Step 4 — Commit + push the screenshots
```bash
git add docs/screenshots/ docs/DEPLOYMENT-SCREENSHOTS.md
git commit -m "docs(screenshots): capture real deployment screenshots + replace ASCII references"
git push origin main
```

---

## 5. The deployment timeline (per footprint)

### 5.1 Self-hosted citizen footprint (~1 hour)

| Step | Duration | Command |
|---|--:|---|
| Clone the bundle | 5 min | `git clone https://github.com/cianfhoghlaim/cianchosaint && cd cianchosaint/web/apps/ciafagent-self-host` |
| Set LLM API key | 5 min | `export UNSLOTH_STUDIO_API_KEY=sk-...` |
| Start Docker Compose | 10 min | `docker compose up -d` |
| Verify the stack | 10 min | `docker compose ps` (all 7 containers should be Up) |
| Capture the screenshot | 5 min | `open http://localhost:7777` + screenshot |
| Test the per-source UI | 15 min | Click on a suggested prompt + screenshot the `SourcePolicyCard` |
| Q&A | 10 min | — |

### 5.2 Public-sector analyst footprint (~2 days)

| Day | Task |
|---|---|
| Day 1 morning | Provision arm1-oci (or Hetzner) + reserve DNS + set up Infisical |
| Day 1 afternoon | Deploy stacks 1-6 (infisical → motherduck → lakehouse → unsloth-serve → litellm → langfuse) |
| Day 2 morning | Deploy stacks 7-13 (crawl4ai → stagehand → locket → changedetection → komodo → pangolin → openchamber) |
| Day 2 afternoon | Deploy the 8 per-persona web apps + capture the 11 screenshots |
| Day 2 evening | Onboard the analyst + run the 3 demo paths |

### 5.3 Developer / contributor footprint (~30 minutes)

| Step | Duration | Command |
|---|--:|---|
| Clone the repo | 5 min | `git clone https://github.com/cianfhoghlaim/cianchosaint && cd cianchosaint` |
| Install mise + uv + bun | 10 min | `brew install mise && mise install` |
| Run `mise run core` | 5 min | `mise run core` |
| Set up CCC | 5 min | `bun run ccc:init && bun run ccc:index` |
| Read the openspec | 5 min | `openspec list` |

### 5.4 Pilot / case-study footprint (Reform UK, ~1 hour)

| Step | Duration | Command |
|---|--:|---|
| Deploy the 13 stacks | ~1.5 days (overlaps with the analyst footprint) | (per 5.2) |
| Deploy the 8 web apps | 30 min | (per 5.2) |
| Run the Reform UK pilot | 5 min | `mise run cianchosaint:reform-uk-pilot:run` |
| Capture the screenshot | 5 min | (per 4.2) |
| Review with a public-sector analyst | 30 min | — |

---

## 6. The screenshot file naming convention

```
docs/screenshots/
├── 01-mise-run-core.png
├── 02-provider-health-check.png
├── 03-bipp-v1-m1-ga-pipeline.png
├── 04-osint-allowlist-audit.png
├── 05-ccc-search-british-isles-policing.png
├── 06-openspec-list-specs-changes.png
├── 07-reform-uk-pilot-dossier.png
├── 08-git-log-commit-history.png
├── 09-ciafagent-self-host-interface.png
├── 10-mise-tasks-ls-all.png
└── 11-openspec-specs-docs-tree.png
```

Total: 11 screenshots, each ~100-500 KB, ~3 MB total.

---

## 7. What happens after the screenshots are captured

Once the 11 real screenshots are captured + committed:

1. **The `docs/DEPLOYMENT-SCREENSHOTS.md` becomes canonical documentation** — no longer ASCII placeholders
2. **The README.md should reference the deployment + screenshots** as the canonical entry point for fresh users
3. **The USAGE-GUIDELINES.md should reference the screenshots** as the visual companion to the textual guidelines
4. **The DEMO-PATHS.md should reference the screenshots** as the visual companion to the textual demo paths

---

## 8. Questions for you (the deployer)

These are the things I need your decision on before executing the deployment:

### Q43 — Deployment footprint for the first demo
> - A) Self-hosted citizen footprint (cheapest, fastest, but only the citizen bundle) — Recommended (low risk)
> - B) Public-sector analyst footprint (cloud, ~$3k/month, full platform)
> - C) Both in parallel
> - D) Different — please specify

### Q44 — Screenshot capture tool
> - A) macOS native `screencapture` command (built-in, no extra tool) — Recommended
> - B) Linux `spectacle` or `gnome-screenshot`
> - C) Browser DevTools screenshot (Chrome / Firefox)
> - D) Different — please specify

### Q45 — Screenshot file format
> - A) PNG (lossless, ~100-500 KB per image) — Recommended
> - B) JPG (smaller, ~50-100 KB per image)
> - C) SVG (vector, but only for diagrams — not for terminal output)
> - D) Mix: PNG for screenshots, SVG for diagrams

### Q46 — Screenshot resolution
> - A) 1600x1200 px (high DPI, ~300 KB per PNG) — Recommended
> - B) 1280x720 px (lower DPI, ~100 KB per PNG)
> - C) 1920x1080 px (full HD, ~500 KB per PNG)
> - D) Different — please specify

### Q47 — Screenshot replacement strategy
> - A) Replace the ASCII sections in `docs/DEPLOYMENT-SCREENSHOTS.md` with image references (keep the section headings + add `![screenshot](./screenshots/NN-name.png)`)
> - B) Add a new section at the end of `docs/DEPLOYMENT-SCREENSHOTS.md` called "Real screenshots (post-deployment)" + link from the ASCII sections
> - C) Replace the entire `docs/DEPLOYMENT-SCREENSHOTS.md` with a fresh version that ONLY uses real PNGs — Recommended (cleaner)
> - D) Different — please specify

---

## 9. What I can do for you when you're ready

When you answer Q43–Q47 + say "proceed", I can:

1. **Dispatch a subagent** to author the deployment runbook update (per Q47 = C)
2. **Author a new openspec change** (if needed) for the deployment automation (e.g. `cianchosaint-deploy-automation-v1` for the GitHub Actions deployment workflow)
3. **Run the deployment checklist** for the footprint you choose (the checklist lives at `docs/DEPLOYMENT-SCREENSHOTS.md §Live deployment checklist`)
4. **Validate the deployment** (per `openspec validate --all --strict` + `mise run lint:license` + `mise run lint:openspec`)

For now, I'll stop here. The plan is ready, the screenshots workflow is documented, and the deployment procedure is at `docs/DEPLOYMENT.md`. Whenever you have a deployment window + the cloud infrastructure ready + credentials for `*.cianchosaint.ie`, you can execute the live deployment + screenshot capture + push.
