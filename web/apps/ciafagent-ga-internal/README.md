# ciafagent-ga-internal

The **internal-facing An Garda Síochána (GA) app** — for Garda members.
Cross-references PULSE schema, internal circulars, and training materials
via the `ga_root_agent` + 5 GA specialists.

**RESTRICTED ACCESS** — only available on the Garda internal network.

## Stack

- **Frontend**: TanStack Start + CopilotKit v2 + AG-UI protocol
- **UI kit**: `@cianchosaint/ui-kit` (wholesale-copied from `cianfhoghlaim`)
- **Auth**: `@cianchosaint/auth` (BetterAuth + Garda SSO)
- **DB**: `@cianchosaint/db` (Convex)
- **API**: Hono (`apps/api/`) — routes to `ciafagent-api` for the 24-agent fleet
- **Backend agents**: Python (`../../agents/cianchosaint/ga_root_agent.py`)

## Surfaces

| Route | Purpose |
|:--|:--|
| `/` | Internal landing + active investigations dashboard |
| `/chat` | AG-UI chat window — streams from `ga_root_agent` |
| `/pulse` | PULSE schema cross-reference tool |
| `/circulars` | Internal GA circulars search |
| `/training` | Training materials + e-learning modules |

## Internal-only AG-UI events

| Event | Purpose |
|:--|:--|
| `pulse-schema-lookup` | Look up a PULSE field by name |
| `circular-citation` | Returns an internal GA circular reference |
| `training-module-progress` | Tracks member progress on training modules |

## Dev

```bash
bun install
bun run dev          # turbo: web + api in parallel
bun run typecheck
bun run build
```
