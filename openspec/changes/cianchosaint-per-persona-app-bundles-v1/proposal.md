# Change: cianchosaint-per-persona-app-bundles-v1

## Why

The `cianchosaint-repo-bootstrap-v2` change established the **structural foundation** of the cianchosaint platform: 5 canonical specs (pipeline / agentic-interaction / self-hosted-citizen / per-constituency-agents / bootstrap-v2), all wholesale-copied data platform + BAML + CocoIndex + agents + web-packages + IaC + skills + CCC + slimmed-mise layers, plus the 24 per-constituency Google ADK agents (the ga/met/psni root + 15 specialists + 7 FunctionTools). What is missing is the **user-facing surface**: the per-persona web apps that connect the agents to the public-sector analyst + the British Isles citizen.

Per the `cianchosaint-bootstrap-v2` spec Requirement: 7 per-persona web surfaces, every per-constituency agent fleet needs 2 web surfaces (public-facing for citizen interaction + internal-facing for analyst work), plus 1 self-hosted citizen entry point + 1 Hono API gateway. This change authors the 8 web app bundles in `web/apps/`, synthesised from the combined template (per Q23) that adopts the best practices from BOTH `web/apps/cianfhoghlaim-leaving-cert/` AND `web/apps/cianfhoghlaim-web/`.

The user explicitly clarified (verified 2026-08-23): *"the focus on the mi6 github repository can be ignored"* + the agents should empower British Isles public-sector bodies + members of the public to interact conversationally with Cian (the agent persona) for non-emergency form filling (e.g. traffic violation reports), statute search (irishstatutebook.ie / legislation.gov.uk), and cross-jurisdiction queries (PSNI ↔ Garda).

## What changes

- **8 new web app bundles** in `web/apps/`:
  - `ciafagent-ga-public/` — An Garda Síochána (GA) public-facing AG-UI chat for citizen interaction with the `ga_root_agent` (non-emergency form filling + statute search + court judgment lookup)
  - `ciafagent-ga-internal/` — GA internal-facing web surface for Garda members (cross-reference to PULSE schema + internal circulars + training materials)
  - `ciafagent-met-public/` — Metropolitan Police (MET) public-facing AG-UI chat for the `met_root_agent`
  - `ciafagent-met-internal/` — MET internal-facing web surface
  - `ciafagent-psni-public/` — PSNI public-facing AG-UI chat for the `psni_root_agent`
  - `ciafagent-psni-internal/` — PSNI internal-facing web surface (NI Policing Board + justice-ni.gov.uk integration)
  - `ciafagent-self-host/` — the self-hosted citizen Docker entry point (per the `cianchosaint-self-hosted-citizen` spec, Requirement: Self-hosted Docker Compose bundle)
  - `ciafagent-api/` — the Hono API gateway (the AG-UI event source for all 7 persona apps; routes to the 24 Google ADK agents)

Each app bundle adopts the COMBINED TEMPLATE (Q23 synthesis):
- From `web/apps/cianfhoghlaim-leaving-cert/`: the per-app `packages/` structure (`auth`, `db`, `i18n`, `ui`, `convex`, `config`); the per-app `baml_src/`; the AG-UI + CopilotKit integration; the Dockerfile + wrangler.toml
- From `web/apps/cianfhoghlaim-web/`: the simple `apps/web` + `apps/api` + `convex` + `packages` layout; the Turbo monorepo + Biome + Bun workspace; the Convex v1.40+ + Zod v4 dependency pins
- DROPS education-specific patterns: no LC subject catalog, no education i18n translations, no LC subject BAML client

- **2 new ADDs Requirements** to the canonical `cianchosaint-agentic-interaction` spec:
  - Requirement: 7 per-persona web surfaces (GA + MET + PSNI × 2 + self-host)
  - Requirement: 1 Hono API gateway (ciafagent-api)

- **Per-app package.json names** use the `ciafagent-<persona>` prefix (e.g. `@cianchosaint/ciafagent-ga-public`). This naming follows the `web/packages/{ui-kit, auth, db}` pattern (already wholesale-copied in the previous commit `a2a3431`).

## Impact

- Affected specs: 1 MODIFIED spec (`cianchosaint-agentic-interaction/`, +2 ADDED Requirements).
- Affected code/config: 8 new web app bundles in `web/apps/`. Each bundle has ~30-50 files of ~30-100 LOC each. Total: ~80-160 new files, ~3,000-5,000 LOC.
- No secret values are written to disk: all keys resolve via `infisical://dev-baile/cianchosaint/...` template refs hydrated by mise + Locket.
- No cross-repo changes — Cianfhoghlaim remains unchanged.

## Out of scope

- The runtime deployment of these 8 web apps (Pangolin resource exposure, Cloudflare Workers deployment, Docker Compose orchestration) — covered by follow-up `cianchosaint-pangolin-ingress-v1` + `cianchosaint-cloudflare-deploy-v1` changes.
- The internal AG-UI event type definitions (e.g. `form-fill-request`, `form-fill-response`, `osint-evidence-citation`) — covered by follow-up `cianchosaint-ag-ui-event-types-v1`.
- The Convex schema definitions for the 7 per-persona apps — covered by follow-up `cianchosaint-convex-schemas-v1`.
- The web-app-specific BAML extraction functions (per-constituency BAML clients beyond the wholesale-copied `baml_src/clients.baml`) — covered by follow-up `cianchosaint-baml-schemas-v1`.

## Dependencies

`Blocked by: cianchosaint-repo-bootstrap-v2` (must archive first; this is the case).
`Affected repos: cianchosaint.`

## Cross-repo sync

See [`cross-repo-sync.md`](./cross-repo-sync.md) — this change touches ONLY the `cianchosaint` repo. Cianfhoghlaim remains unchanged.
