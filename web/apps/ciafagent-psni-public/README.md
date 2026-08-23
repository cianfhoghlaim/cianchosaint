# ciafagent-psni-public

The **public-facing PSNI (Police Service of Northern Ireland) app**.
Citizen gateway to the `psni_root_agent` Google ADK agent + 5 PSNI
specialists (crime statistics, NI justice, policing board, press releases,
public contact).

## Stack

- TanStack Start + CopilotKit v2 + AG-UI + Hono + Convex + BetterAuth
- Re-uses `@cianchosaint/ui-kit`, `@cianchosaint/auth`, `@cianchosaint/db`
- Routes through `ciafagent-api` to `../../agents/cianchosaint/psni_root_agent`

## Surfaces

| Route | Purpose |
|:--|:--|
| `/` | Landing + 999 disambiguation |
| `/chat` | AG-UI chat window |
| `/form-fill` | Non-emergency form filling |
| `/statute-search` | legislation.gov.uk (NI) search |
| `/about` | Privacy + Pat Finucane Centre referral |
