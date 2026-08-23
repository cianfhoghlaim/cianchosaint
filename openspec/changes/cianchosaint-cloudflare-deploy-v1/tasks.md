# Tasks: cianchosaint-cloudflare-deploy-v1

## 0. Pre-flight

- [x] Verify `cianchosaint-pangolin-ingress-v1` is archived
- [x] Verify `web/apps/ciafagent-api/wrangler.toml` exists
- [x] Verify the 8 per-persona apps + the Hono API gateway exist
  on disk
- [x] Verify Cloudflare account ID is available (per the wholesale-
  copied Cianfhoghlaim pattern)

## 1. OpenSpec artifacts

- [ ] Author `openspec/changes/cianchosaint-cloudflare-deploy-v1/proposal.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-cloudflare-deploy-v1/tasks.md` (this file) — DONE
- [ ] Author `openspec/changes/cianchosaint-cloudflare-deploy-v1/cross-repo-sync.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-cloudflare-deploy-v1/specs/cianchosaint-cloudflare-deploy/spec.md` (the 2 ADDED Requirements delta) — DONE
- [ ] Author `openspec/specs/cianchosaint-cloudflare-deploy/spec.md` (canonical END-STATE spec) — DONE
- [ ] Author `openspec/specs/cianchosaint-cloudflare-deploy/AGENTS.md` (per-spec routing) — DONE

## 2. Validation gates

- [ ] Run `openspec validate cianchosaint-cloudflare-deploy-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchososaint-cloudflare-deploy --strict` and verify exit code 0
- [ ] Run `python3 -c "import tomllib; tomllib.loads(open('web/apps/ciafagent-api/wrangler.toml','rb').read())"` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL pass

## 3. Implementation: 1 MODIFIED file

### ciafagent-api (1 file at `web/apps/ciafagent-api/`)
- [ ] `wrangler.toml` — extended to declare all 8 web apps + the Hono
  API gateway under the `cianchosaint.ie` Cloudflare zone

## 4. Per-file pattern

```toml
name = "ciafagent-api"
compatibility_date = "2026-08-23"
main = "apps/api/src/index.ts"

[env.production]
routes = [
  { pattern = "api.cianchosaint.ie/*", zone_name = "cianchosaint.ie" },
  { pattern = "ga.cianchosaint.ie/*", zone_name = "cianchosaint.ie" },
  # ... 7 more routes ...
]
vars = { CONVEX_DEPLOYMENT = "prod:conic-api", COPILOTKIT_RUNTIME_URL = "/api/copilotkit" }
```

## 5. CI gates + commit + push

- [ ] Run `python3 -c "import tomllib; tomllib.loads(open('web/apps/ciafagent-api/wrangler.toml','rb').read())"` and verify
- [ ] Run `openspec validate --all --strict` and verify ALL pass
- [ ] Commit on `cianchosaint:main` with message: `feat(q3q4-track2): Cloudflare deploy for 8 web apps + Hono API gateway (Change 14)`
- [ ] Push to `github.com/cianfhoghlaim/cianchosaint`

## 6. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-cloudflare-resources-provision-v1` — provision
  the KV / R2 / D1 / Vectorize backing services
