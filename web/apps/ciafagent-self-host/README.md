# ciafagent-self-host

The **self-hosted citizen Docker entry point** — bundles the AG-UI chat
window + a minimal Hono API + the 3 cianchosaint root agents (for offline
fallback) into a single Docker image that citizens can run on their own
hardware (Raspberry Pi 5, NAS, laptop).

Per the **cianchosaint-self-hosted-citizen** spec, Requirement:
*Self-hosted Docker Compose bundle*.

## Stack

- TanStack Start (AG-UI chat window)
- Embedded Hono API (minimal, in-container)
- Embedded Python agent runner (3 root agents + 7 tools)
- Local SQLite cache for offline responses

## Quick start

```bash
docker compose up
# OR
docker run -p 3086:3086 ciafagent-self-host
```

Then visit http://localhost:3086 to chat with the AG-UI window.

## Offline mode

When the network is unavailable, the embedded Python agents answer from
the local SQLite cache (pre-baked at build time with the canonical
responses for the most common queries).

## AG-UI event types

- `form-fill-request`, `form-fill-response`
- `osint-evidence-citation` (offline only)
- `jurisdiction-disambiguation` (suggests based on user's locale)

## Configuration

Environment variables:
- `OFFLINE_MODE` (default: `true`) — use local cache only
- `AGENT_LOCALE` (default: `en-GB`) — affects jurisdiction selection
