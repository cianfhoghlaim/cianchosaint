# Tasks: cianchosaint-per-persona-app-bundles-v1

## 0. Pre-flight

- [ ] Verify `cianchosaint-repo-bootstrap-v2` is archived (it is, as of `f8c72d5`)
- [ ] Verify openspec CLI: `openspec --version` (expected 1.4.1)
- [ ] Verify `web/packages/{ui-kit,auth,db}/` are present (wholesale-copied in `a2a3431`)

## 1. OpenSpec artifacts

- [ ] Author `openspec/changes/cianchosaint-per-persona-app-bundles-v1/proposal.md` (this file's purpose) — DONE
- [ ] Author `openspec/changes/cianchosaint-per-persona-app-bundles-v1/tasks.md` (this file) — DONE
- [ ] Author `openspec/changes/cianchosaint-per-persona-app-bundles-v1/cross-repo-sync.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-per-persona-app-bundles-v1/specs/cianchosaint-agentic-interaction/spec.md` (the ADDED Requirements delta) — DONE

## 2. Validation gates

- [ ] Run `openspec validate cianchosaint-per-persona-app-bundles-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-agentic-interaction --strict` and verify exit code 0

## 3. Implementation: 8 web app bundles

- [ ] `web/apps/ciafagent-ga-public/` — TanStack Start + Convex + AG-UI + CopilotKit
- [ ] `web/apps/ciafagent-ga-internal/` — same framework, internal-facing
- [ ] `web/apps/ciafagent-met-public/`
- [ ] `web/apps/ciafagent-met-internal/`
- [ ] `web/apps/ciafagent-psni-public/`
- [ ] `web/apps/ciafagent-psni-internal/`
- [ ] `web/apps/ciafagent-self-host/` — the self-hosted citizen Docker entry point
- [ ] `web/apps/ciafagent-api/` — the Hono API gateway (the AG-UI event source)

For each app, the file structure (per the combined Q23 template):

```
web/apps/ciafagent-<persona>/
├── Dockerfile                              # Cloudflare Container / Workers build
├── README.md
├── package.json
├── tsconfig.json
├── turbo.json
├── wrangler.toml                           # Cloudflare Workers config
├── apps/
│   ├── web/                                # TanStack Start entry
│   │   ├── package.json
│   │   ├── src/
│   │   │   ├── routes/                     # file-based routing
│   │   │   ├── components/                # AG-UI + CopilotKit
│   │   │   ├── hooks/                     # AG-UI event subscription
│   │   │   └── app.tsx
│   │   └── tsconfig.json
│   └── api/                                # Hono API gateway
│       ├── package.json
│       ├── src/
│       │   ├── routes/                    # agent streaming + OSINT queries
│       │   └── middleware/                 # BetterAuth + rate limiting
│       └── tsconfig.json
├── packages/                               # per-app internal packages
│   ├── auth/                              # BetterAuth per-app config
│   ├── convex/                             # Convex schema + functions
│   ├── db/                                 # Convex client wrapper
│   ├── ui/                                 # per-app UI primitives
│   ├── i18n/                               # i18n (en + ga)
│   └── config/                             # shared config
└── baml_src/                               # per-app BAML client (4-tier chain)
    └── clients.baml
```

For `ciafagent-api/`, skip the `apps/web/` (it's API-only).

For `ciafagent-self-host/`, skip the `apps/api/` (it's a self-contained Docker entry point + AG-UI only).

## 4. CI gates + commit + push

- [ ] Run `mise run lint:web` (NEW) — verify TypeScript syntax + per-app package.json validity
- [ ] Run `openspec validate --all --strict` and verify ALL pass
- [ ] Commit on `cianchosaint:main` with message: `feat(openspec): cianchosaint-per-persona-app-bundles-v1 — 8 web apps from the combined template (TanStack Start + Convex + AG-UI + CopilotKit)`
- [ ] Push to `github.com/cianfhoghlaim/cianchosaint`

## 5. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-pangolin-ingress-v1` — expose the 8 web apps at `*.cianchosaint.ie` via Pangolin
- [ ] `cianchosaint-cloudflare-deploy-v1` — Cloudflare Workers + Container deployment for the 8 apps
- [ ] `cianchosaint-ag-ui-event-types-v1` — the AG-UI event type definitions (form-fill-request, form-fill-response, osint-evidence-citation, etc.)
- [ ] `cianchosaint-convex-schemas-v1` — the Convex schema definitions for the 7 per-persona apps
- [ ] `cianchosaint-baml-schemas-v1` — the per-constituency BAML extraction functions (beyond the wholesale-copied `baml_src/clients.baml`)
