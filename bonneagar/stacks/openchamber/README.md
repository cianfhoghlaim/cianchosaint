# OpenChamber — OpenCode Web/Desktop UI (v1.22.2)

> **UPDATED 2026-09-26** (per the openspec/changes/2026-09-26-openchamber-v1.22-major-upgrade-v1/
> specs/openchamber-major/spec.md, Stage 4 of the package-version-drift saga):
> - Bumped from `1.0.0@sha256:21fda...` → `1.22.2` (the canonical latest release; 22 minor versions)
> - Added the OpenCode 2.x prerequisite (CRITICAL — per the v1.22 release notes)
> - Added the "What's new in OpenChamber 1.22" section
> - Documented the OpenChamber 2.0 hot reload prep roadmap

## Overview

OpenChamber is a browser-based OpenCode UI built on Bun + React.
It can either bundle the `opencode-ai` runtime inside its own
container (the **arm1-oci** production surface) or it can route to
an externally-running OpenCode server (the **bunchloch** development
surface). The UI ships with 18+ themes, persistent session state,
and a provider picker for OpenAI, Anthropic, and
minimax-compatible gateways.

The upstream `openchamber/openchamber` image is pinned to `1.22.2`
(per the openspec change above). The v1.22 release requires
OpenCode 2.x (per the v1.22 release notes: "Startup: connecting to
an OpenCode 1.x server shows a clear 'update OpenCode to 2.x'
screen").

## CRITICAL — OpenCode 2.x prerequisite

Per the v1.22 release notes: **OpenChamber v1.22+ requires OpenCode 2.x**.
Before pulling the new OpenChamber image, the operator MUST upgrade
OpenCode to 2.x:

```bash
# Upgrade opencode via mise
mise install opencode@2.0.0
mise use opencode@2.0.0

# Verify the upgrade
opencode --version   # should print 2.x
```

If the OpenCode server is still on 1.x, OpenChamber v1.22 will start
but display the "update OpenCode to 2.x" screen on every page load.

## What''s new in OpenChamber 1.22 (per the v1.22 changelog)

### New features

1. **Self-service HA and clustering** on Scale + Enterprise tiers
2. **Newt renamed to Pangolin Site** (the dashboard now calls it that)
3. **Sites integrated into the Pangolin CLI** (`pangolin up site ...`)
4. **Master list of organizations** in the server admin panel
5. **Multiple server admin users** supported (promote/demote via the users table)
6. **Resource Launcher side panel** — Sites widget + ready-to-copy `pangolin ssh` commands

### Improvements

- Chat: prompt history (arrow up/down brings back earlier prompts; 40 by default)
- Chat: a queued message keeps its attached context, file mentions, and skill
- Chat: an "Enter sends" switch in Settings → Chat
- Chat: bash output reads as it did in the terminal (no raw escape codes)
- Worktrees: archiving sessions is much faster (~1 second for 121 sessions)
- MCP: auto-reconnect (up to 30 seconds between tries; Web and Desktop only)
- Git: branch picker lists recent branches and marks the ones with unpushed commits
- Models: model picker keeps provider groups open in the order you put them
- Usage: quota limits refresh every 3 minutes
- Sessions: starting a rename selects the whole title

### Fixes (selected)

- Chat: command, skill, and file autocomplete in a chat without a project
  no longer uses the project you had selected before
- Chat: queued messages retry after a failed send or an interrupted turn
- Sessions: sessions you deleted no longer come back after a restart
- Mobile: interface labels are back to their old size after 1.13.6 shrank them
- CLI: `openchamber update` works again
- CLI: fixed a startup regression in global npm/bun installs

## OpenChamber 2.0 (the v2.0 hot reload prep)

Per https://openchamber.dev/blog/opencode-v2/, **OpenChamber 2.0** is in
development with the headline feature of "hot reload":

> Change one line in `SKILL.md`. Restart OpenCode. Watch every running
> session drop its connection. Notice a typo in the line I just changed.

The 2.0 prep shipped in 1.22 is the canonical foundation (per the v2.0
blog post: "we went through the OpenCode 2 API route by route to see
where we had to change").

## Deployment

### Docker Compose (Local)

```bash
cd bonnegar/stacks/openchamber
docker compose up -d
```

### Production (with Locket)

```bash
docker compose -f compose.yaml -f sidecar.yaml up -d
```

### Komodo (GitOps)

Deployed via Komodo on arm1-oci as the primary control-plane service.

## Environment Variables

| Variable | Required | Description | Default |
|:--|:--|:--|:--|
| `OFFLINE_MODE` | No | Use local cache only | `true` |
| `AGENT_LOCALE` | No | Affects jurisdiction selection | `en-GB` |
| `OPENCODE_HOST` | No (dev only) | Points at external OpenCode 2.x server | (bundled) |
| `OPENCODE_PORT` | No (dev only) | Explicit port override | `4096` |
| `OPENCODE_SKIP_START` | No (dev only) | Refuses to launch bundled OpenCode daemon | (false) |

## Access

- **Web UI**: `https://openchamber.cianchosaint.ie` (private, Pangolin Member)
- **API**: `https://openchamber.cianchosaint.ie/api/healthz`

## Upstream

- **Repository**: https://github.com/openchamber/openchamber
- **Changelog**: https://openchamber.dev/changelog/
- **v2.0 blog post**: https://openchamber.dev/blog/opencode-v2/

## Cross-references

- `docs/stacks/openchamber.md` — the per-stack "purpose + why-GitOps" doc
- `bonnegar/komodo/procedures/deploy-openchamber-bunchloch.toml` —
  the deploy procedure (adds a Stage 5 `bunchloch-parity-verification`
  block per this change)
- `bonnegar/komodo/procedures/deploy-openchamber-arm1-oci.toml` —
  the production deploy procedure (arm1-oci bundled mode)
- `.agents/skills/secrets-management/SKILL.md` — the Infisical +
  Locket + mise three-way contract that this stack depends on
- `openspec/changes/2026-09-26-openchamber-v1.22-major-upgrade-v1/`
  — the openspec change for this 1.0 → 1.22 refactor
