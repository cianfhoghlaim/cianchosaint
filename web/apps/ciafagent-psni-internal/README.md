# ciafagent-psni-internal

The **internal-facing PSNI app** — for PSNI officers. Integrates with the
**NI Policing Board** (the oversight body) and includes NI-specific
internal circulars + training.

**RESTRICTED ACCESS** — PSNI internal network only.

## Stack

- TanStack Start + CopilotKit v2 + AG-UI + Hono + Convex + BetterAuth
- Routes through `ciafagent-api` to `../../agents/cianchosaint/psni_root_agent`

## Surfaces

| Route | Purpose |
|:--|:--|
| `/` | Internal landing |
| `/chat` | AG-UI chat with psni_root_agent |
| `/policing-board` | NI Policing Board integration (oversight) |
| `/circulars` | Internal PSNI circulars |
| `/training` | Officer training modules |
