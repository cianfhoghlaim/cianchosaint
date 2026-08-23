# `cianchosaint-cloudflare-deploy` — Agent Routing

> `cianchosaint-cloudflare-deploy` is the capability that deploys the 8 per-persona web apps + the Hono API gateway to Cloudflare Workers + Containers under the `cianchosaint.ie` zone.

## Routing

Load this AGENTS.md when the parent spec (`./spec.md`) is in scope.
Use it to find the most relevant mise tasks + skills + adjacent files
without re-reading the full spec.

## Quick start

```bash
# 1. Validate the Cloudflare deploy spec
openspec validate cianchosaint-cloudflare-deploy --strict

# 2. Verify the wrangler.toml file
python3 -c "import tomllib; data = tomllib.loads(open('web/apps/ciafagent-api/wrangler.toml','rb').read()); print('routes:', len(data['env']['production']['routes']))"
# Expected: 9

# 3. Deploy to dev
cd web/apps/ciafagent-api
wrangler deploy --env dev

# 4. Deploy to production
wrangler deploy --env production
```

## Key sources

- `openspec/specs/cianchosaint-cloudflare-deploy/spec.md` — the canonical spec
- `web/apps/ciafagent-api/wrangler.toml` ⭐ — the consolidated wrangler config
- `web/apps/ciafagent-api/apps/api/src/index.ts` — the Hono API gateway source
- `LICENSE.md` (repo root) — the BUSL-1.1 v2 load-bearing legal document

## Adjacent specs

- `openspec/specs/cianchosaint-deployment/spec.md` — the deployment umbrella
- `openspec/specs/cianchosaint-pangolin-ingress/spec.md` — the upstream ingress layer
- `openspec/specs/cianchosaint-per-constituency-agents/spec.md` — the per-persona apps deployed

## DO NOT

- Deploy to production without running
  `openspec validate cianchosaint-cloudflare-deploy --strict` first.
- Skip the per-environment vars block (each env MUST have its own
  `CONVEX_DEPLOYMENT` + `COPILOTKIT_RUNTIME_URL` values).
- Add a new route without updating both this spec + the
  corresponding Pangolin resource declaration.
- Bypass the `wrangler deploy --env production` flow — operators MUST
  use the canonical `wrangler` CLI, not the Cloudflare dashboard
  directly.

## Skill pointers

- `ccc` — for semantic code search across the per-persona apps
- `openspec` — for the spec change workflow
- `cloudflare` — for the wholesale-copied Cloudflare Workers pattern
- `secrets-management` — for the Infisical + Locket contract

<!-- generated: 2026-08-23; do not hand-edit -->
