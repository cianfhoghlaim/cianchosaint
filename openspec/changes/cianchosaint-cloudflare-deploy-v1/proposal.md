# Change: cianchosaint-cloudflare-deploy-v1

## Why

The cianchosaint platform needs a consolidated Cloudflare Workers +
Container deployment for the 8 per-persona web apps + the Hono API
gateway. Cloudflare is the canonical edge compute layer (per the
wholesale-copied Cianfhoghlaim pattern at
`web/apps/ciafagent-api/wrangler.toml`).

The 8 web apps + the Hono API gateway are deployed as Cloudflare
Workers + Containers. The consolidated `wrangler.toml` at
`web/apps/ciafagent-api/wrangler.toml` declares the production
deployment for the Hono API gateway at `api.cianchosaint.ie`.

This change extends the existing `wrangler.toml` to declare all 8 web
apps + the Hono API gateway under the `cianchosaint.ie` zone, plus
the canonical Cloudflare-specific config (env vars, routes, KV
namespaces, R2 buckets, D1 databases).

The consolidated `wrangler.toml` is the single source of truth for
Cloudflare deployment — operators run `wrangler deploy` from
`web/apps/ciafagent-api/` and the entire stack is deployed atomically.

## What changes

- **1 NEW canonical spec**: `cianchosaint-cloudflare-deploy` with 2
  ADDED Requirements:
  - Requirement: The consolidated `wrangler.toml` for the 8 web apps
    + the Hono API gateway under the `cianchosaint.ie` Cloudflare zone
  - Requirement: Per-environment Cloudflare Workers config (dev |
    staging | prod)

- **1 MODIFIED file**: `web/apps/ciafagent-api/wrangler.toml` is
  extended to declare all 8 web apps + the Hono API gateway.

## Impact

- Affected specs: 1 NEW spec (`cianchosaint-cloudflare-deploy/`).
- Affected code/config: 1 MODIFIED file at
  `web/apps/ciafagent-api/wrangler.toml` (~80-120 lines after the
  change).
- No secret values are written to disk: all keys resolve via
  `infisical://dev-baile/cianchosaint/...` template refs hydrated by
  mise + Locket.
- No runtime behaviour changes — the existing Hono API gateway
  deployment continues to work. The new web app deployments are
  additive.

## Out of scope

- The per-web-app Cloudflare Workers source code (each per-persona
  app is a separate `web/apps/ciafagent-*/` workspace). Out of scope —
  this change only adds the consolidated `wrangler.toml`.
- The Cloudflare KV / R2 / D1 / Vectorize resource creation (the
  wrangler commands that provision the backing services). Out of scope
  — covered by the follow-up `cianchosaint-cloudflare-resources-provision-v1`
  change.
- The Cloudflare Access / WAF rules. Out of scope — the Pangolin
  layer (per the previous change) handles access control.

## Validation criteria

1. `openspec validate cianchosaint-cloudflare-deploy-v1 --strict`
   passes (exit code 0).
2. `openspec validate cianchosaint-cloudflare-deploy --strict` passes
   (exit code 0).
3. `python3.13 -c "import tomllib; tomllib.loads(open('web/apps/ciafagent-api/wrangler.toml','rb').read())"`
   passes (valid TOML).
4. The `wrangler.toml` declares the `cianchosaint.ie` zone and at
   least 9 routes (8 web apps + 1 API gateway).

## Dependencies

`Blocked by: none`
`Blocked by (soft): cianchosaint-pangolin-ingress-v1` (extends; the
  Pangolin resources are the upstream ingress layer, Cloudflare is
  the compute layer)
`Affected repos: cianchosaint.` (Cianfhoghlaim + leabharlann remain
  completely unchanged.)

## Cross-repo sync

This change touches **ONLY the `cianchosaint` repo**. See
`cross-repo-sync.md` for the full commit plan.
