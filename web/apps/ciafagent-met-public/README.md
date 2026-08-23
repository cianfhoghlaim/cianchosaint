# ciafagent-met-public

The **public-facing Metropolitan Police (MET) app** — citizen gateway to the
`met_root_agent` Google ADK agent + 5 MET specialists. Covers the 43 UK
forces via `force_lookup`.

## Stack

- TanStack Start + CopilotKit v2 + AG-UI + Hono + Convex + BetterAuth
- Re-uses `@cianchosaint/ui-kit`, `@cianchosaint/auth`, `@cianchosaint/db`
- Routes through `ciafagent-api` gateway to `../../agents/cianchosaint/met_root_agent`

## Surfaces

| Route | Purpose |
|:--|:--|
| `/` | Landing + 999 disambiguation |
| `/chat` | AG-UI chat with `met_root_agent` |
| `/form-fill` | Non-emergency form filling (crime report, lost property) |
| `/statute-search` | legislation.gov.uk search |
| `/about` | Privacy + sections covered |

## AG-UI events

`form-fill-request`, `form-fill-response`, `osint-evidence-citation`,
`jurisdiction-disambiguation` (between MET and the 42 other UK forces).

## Dev

```bash
bun install && bun run dev
```
