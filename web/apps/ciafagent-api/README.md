# ciafagent-api

The **central Hono API gateway** for the cianchosaint platform. The single
source of AG-UI events for all 7 persona apps
(`ciafagent-ga-public`, `ciafagent-ga-internal`, `ciafagent-met-public`,
`ciafagent-met-internal`, `ciafagent-psni-public`,
`ciafagent-psni-internal`, `ciafagent-self-host`).

## Architecture

```
┌────────────────────────────────┐
│  7 persona apps (ga/met/psni)  │
└───────────┬────────────────────┘
            │ AG-UI events
            ▼
┌────────────────────────────────┐
│  ciafagent-api (this app)      │ ← Hono gateway
│  - /api/agent/<root_agent>     │
│  - /api/osint/<source>         │
└───────────┬────────────────────┘
            │ spawn
            ▼
┌────────────────────────────────┐
│  24-agent Google ADK fleet     │
│  agents/cianchosaint/          │
│  - 3 root: ga/met/psni         │
│  - 15 specialists              │
│  - 7 tools (cross-jurisdiction,│
│    form-fill, statute lookup)  │
└────────────────────────────────┘
```

## Stack

- **Hono** — gateway
- **oRPC** — typed RPC contracts
- **BetterAuth** — auth (via `@cianchosaint/auth`)
- **Convex** — session + audit log (via `@cianchosaint/db`)
- **Python ADK agents** — the 24-agent fleet at `../../agents/cianchosaint/`

## Endpoints

| Method | Path | Purpose |
|:--|:--|:--|
| POST | `/api/agent/<root_agent>` | Stream events from a root agent (AG-UI SSE) |
| GET  | `/api/agent/event-types` | List supported AG-UI event types |
| GET  | `/api/osint/<source>/search` | OSINT statute search (irishstatutebook.ie / legislation.gov.uk / etc.) |
| GET  | `/api/health` | Health check |

## Root agents

- `ga_root_agent` (An Garda Síochána)
- `met_root_agent` (Metropolitan Police + 43 UK forces)
- `psni_root_agent` (Police Service of Northern Ireland)

## AG-UI event types

- `text-delta` — streaming text response
- `tool-call` — agent invokes a tool
- `form-fill-request` — agent requests the UI to render a form
- `form-fill-response` — UI submits the form
- `osint-evidence-citation` — agent returns an OSINT citation
- `jurisdiction-disambiguation` — agent asks the user to confirm jurisdiction
- `done` — stream complete
- `error` — error event

## Dev

```bash
bun install
bun run dev:api
```

## Deploy

```bash
wrangler deploy --env production
```
