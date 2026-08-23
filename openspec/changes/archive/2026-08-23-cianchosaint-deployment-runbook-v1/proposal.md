# Change: cianchosaint-deployment-runbook-v1

## Why

The cianchosaint platform has reached the milestone where:

- **13 Docker Compose stacks** (`bonneagar/stacks/`) are present and validated
  (`mise run devops:validate-stacks` exits 0).
- **8 per-persona web apps** (`web/apps/ciafagent-*/`) are scaffolded.
- **24 per-constituency Google ADK agents** (`agents/cianchosaint/`) are wired.
- **The 4-tier `ModelProviderRouter`** (Unsloth Studio → LiteLLM → MiniMax →
  Gemini) is the canonical LLM path (per `baml_src/_shared/provider_router.py`).
- **CCC indexing** is set up at `.cocoindex_code/` with 12 initial concept
  guides (per the `cianchosaint-repo-bootstrap-v2` change).
- **The OSINT allowlist** at
  `dlt_sources/cianchosaint/common/osint_allowlist.yaml` enforces the licence
  ceiling (British Isles public-sector bodies only).

But there is **no canonical, operator-facing document** that walks a new
operator through the deployment. Knowledge is scattered across:

- `AGENTS.md` (top-level routing — links to mise tasks, doesn't say how)
- `mise.toml` (32 tasks — names without context)
- `bonneagar/AGENTS.md` (the IaC inventory)
- `LICENSE.md` (the licence, but not the operational binding)
- The canonical openspec specs (the contracts, but not the deployment)

Operators (including the author on a clean machine) hit the same questions
over and over:

1. **Which stack do I start first?** The 13 stacks have a hard lifecycle
   ordering (Infisical → Lakehouse → LiteLLM → Langfuse → browser tools →
   monitoring → governance → UI).
2. **What's the env var contract for stack X?** Each of the 13 stacks has a
   `secrets.env` template that must be hydrated from Infisical.
3. **How do I deploy to `arm1-oci` vs `bunchloch`?** Different procedures,
   different credentials.
4. **What are the smoke tests?** Per-stack + per-feature (`provider:health-check`,
   `browser-tool:health-check`, `osint:health-check`).
5. **What about the citizen self-host bundle?** Different contract, different
   licence posture.
6. **What's the rollback plan?** If stack X fails on bring-up, how do I roll
   it back without taking down the whole mesh?

This change is a **DOCUMENT-ONLY** change that answers all 6 questions in a
single canonical artefact: `docs/DEPLOYMENT.md`.

The user explicitly clarified (verified 2026-08-23, paraphrased):
*"the BIPP / BIDP / BIIP milestones are not the only thing — the operators
need a runbook for the 13 stacks, the 8 apps, the 24 agents, the provider
chain, and the CCC indexing setup"*.

## What changes

**One openspec change** that adds:

- **1 new spec** (`cianchosaint-deployment/spec.md`) — 6 ADDED Requirements
  capturing the contract that `docs/DEPLOYMENT.md` MUST cover (the 13 stacks,
  the 8 web apps, the 24 agents, the 4-tier provider chain, the CCC indexing,
  the OSINT allowlist, the per-stack rollback, the smoke tests, the health
  checks, the arm1-oci + bunchloch procedures, the self-host bundle).

- **1 canonical runbook** at `docs/DEPLOYMENT.md` (~3,000-5,000 words) with 13
  sections (overview, the 13 stacks, stack ordering, per-stack deployment,
  cross-stack contracts, the 8 web apps, the 24 agents, arm1-oci deployment,
  bunchloch deployment, self-host citizen deployment, smoke tests, health
  checks, rollback).

- **1 per-spec AGENTS.md** (`openspec/specs/cianchosaint-deployment/AGENTS.md`)
  for the new spec, ≤30 lines per the repo-hygiene convention.

- **NO code changes** — this is a document-only change. The runbook links to
  the existing mise tasks, openspec specs, IaC stacks, web apps, and agents —
  it does NOT introduce new infrastructure.

## Impact

- Affected specs: 1 NEW spec (`cianchosaint-deployment/`).
- Affected code/config: 0 LOC of code. 1 new markdown file
  (`docs/DEPLOYMENT.md`, ~3,000-5,000 words).
- Supersedes: nothing.
- No secret values are written to disk: the runbook describes the
  `infisical://dev-baile/cianchosaint/...` template refs but does NOT
  materialise any secrets itself.

## Out of scope

- The actual IMPLEMENTATION of new infrastructure — the 13 stacks already
  exist; the runbook just describes them.
- Migrating from the 13 stack model to a Pantheon / 94-stack model — separate
  follow-up `cianchosaint-pantheon-migration-v1` if/when pursued.
- New cites for the licence (the licence amendment for citizen self-host
  may live in a separate follow-up `cianchosaint-citizen-use-grant-v1`).
- New per-persona web apps or new agents (those follow-up changes are
  already enumerated in the bootstrap-v2 §11 task list).

## Dependencies

`Blocked by: none` (the 13 stacks + 8 apps + 24 agents + the 4-tier router
+ CCC indexing + the OSINT allowlist are all already in place from the
bootstrap-v2 + per-constituency changes).

`Blocked by (soft): cianchosaint-repo-bootstrap-v2` (the umbrella wholesale-
copy spec that defines the 13-stacks + 7 per-persona apps + 24-agent fleet
that the runbook documents).

`Blocked by (soft): cianchosaint-per-constituency-dlt-sources-v1`,
`cianchosaint-intelligence-agency-pipeline-v1`,
`cianchosaint-political-party-pipeline-v1` (the 3 sub-pipeline specs whose
sources the runbook summarises).

`Affected repos: cianchosaint.` (Cianfhoghlaim is NOT modified.)

## Cross-repo sync

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) remains completely
unchanged. The `cross-repo-sync.md` file in this change records this in the
standard format but does NOT require any Cianfhoghlaim action.
