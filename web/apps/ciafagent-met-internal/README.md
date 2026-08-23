# ciafagent-met-internal

The **internal-facing Metropolitan Police (MET) app** — for MET officers.
Cross-references the Police National Computer (PNC), MET internal
circulars, and training materials.

**RESTRICTED ACCESS** — MET internal network only.

## Stack

- TanStack Start + CopilotKit v2 + AG-UI + Hono + Convex + BetterAuth
- Re-uses `@cianchosaint/ui-kit`, `@cianchosaint/auth`, `@cianchosaint/db`
- Routes through `ciafagent-api` to `../../agents/cianchosaint/met_root_agent`

## Surfaces

| Route | Purpose |
|:--|:--|
| `/` | Internal landing |
| `/chat` | AG-UI chat window — streams from `met_root_agent` |
| `/pnc` | Police National Computer (PNC) cross-reference |
| `/circulars` | Internal MET circulars + MPS directives |
| `/training` | Officer training modules + competency tracking |
