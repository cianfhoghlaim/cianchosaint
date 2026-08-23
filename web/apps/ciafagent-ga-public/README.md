# ciafagent-ga-public

The **public-facing An Garda Síochána (GA) app** — citizen gateway to the
`ga_root_agent` Google ADK agent + 5 GA specialists.

## Stack

- **Frontend**: TanStack Start + CopilotKit v2 + AG-UI protocol
- **UI kit**: `@cianchosaint/ui-kit` (wholesale-copied from `cianfhoghlaim`)
- **Auth**: `@cianchosaint/auth` (BetterAuth)
- **DB**: `@cianchosaint/db` (Convex)
- **API**: Hono (`apps/api/`) — routes to `ciafagent-api` for the 24-agent fleet
- **Backend agents**: Python (`../../agents/cianchosaint/ga_root_agent.py`)
- **Deployment**: Cloudflare Workers + R2 + D1

## Surfaces

| Route | Purpose |
|:--|:--|
| `/` | Landing + emergency (999/112) vs non-emergency disambiguation |
| `/chat` | AG-UI chat window — streams from `ga_root_agent` |
| `/form-fill` | Non-emergency form filling (lost property, minor crime report) |
| `/statute-search` | irishstatutebook.ie search via `IrishStatuteBookAgent` |
| `/about` | Privacy + data retention + section disclosures |

## AG-UI event types

The chat window emits + listens for these events:

| Event | Direction | Purpose |
|:--|:--|:--|
| `form-fill-request` | UI → agent | Initiates a non-emergency form fill |
| `form-fill-response` | agent → UI | Returns the structured form fields |
| `osint-evidence-citation` | agent → UI | Returns an OSINT evidence citation |
| `jurisdiction-disambiguation` | agent → UI | Asks user to confirm jurisdiction (GA vs NI vs MET) |

## Privacy

A privacy disclaimer banner is rendered at the top of every public-facing
chat window. All conversation data is retained for **30 days** for safety
+ audit purposes, then deleted.

## Dev

```bash
bun install
bun run dev          # turbo: web + api in parallel
bun run typecheck
bun run build
```

## Deploy

```bash
wrangler deploy --env production
```
