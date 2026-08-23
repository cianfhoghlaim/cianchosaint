# Change: cianchosaint-pangolin-ingress-v1

## Why

The cianchosaint platform has 8 web apps + the Hono API gateway that
need public + private ingress at `*.cianchosaint.ie` via Pangolin.
Pangolin is the reverse proxy + WireGuard tunnel layer (per the
wholesale-copied Cianfhoghlaim Pangolin pattern at
`bonneagar/pangolin/`).

The 8 web apps + the Hono API gateway are:

1. `ciafagent-ga-public` — An Garda Síochána public-facing (port 7777)
2. `ciafagent-ga-internal` — An Garda Síochána internal-facing (private)
3. `ciafagent-met-public` — Metropolitan Police public-facing (port 7777)
4. `ciafagent-met-internal` — Metropolitan Police internal-facing (private)
5. `ciafagent-psni-public` — PSNI public-facing (port 7777)
6. `ciafagent-psni-internal` — PSNI internal-facing (private)
7. `ciafagent-reform-uk-pilot` — Reform UK pilot app (private — UK HoC only)
8. `ciafagent-self-host` — Self-hosted citizen app (private — citizen's VPN)
9. `ciafagent-api` — Hono API gateway (port 8787, private)

There is currently NO Pangolin resource definitions for these 9
services. The `bonneagar/pangolin/` directory exists but is empty.
The cianchosaint platform cannot expose the web apps at
`*.cianchosaint.ie` without these resource definitions.

This change ships the canonical Pangolin resource definitions at
`bonneagar/pangolin/cianchosaint_resources.yaml`, plus the openspec
capability spec (`cianchosaint-pangolin-ingress`) that documents the
9 resources, the 6-label private resource pattern, the Pocket ID
authentication requirement, and the BUSL-1.1 v2 licence posture.

## What changes

- **1 NEW canonical spec**: `cianchosaint-pangolin-ingress` with 2
  ADDED Requirements:
  - Requirement: The 8 web apps + Hono API gateway exposed at
    `*.cianchosaint.ie` via Pangolin private resources
  - Requirement: Pocket ID authentication + 6-label pattern on every
    private resource

- **1 NEW YAML resource file** at
  `bonneagar/pangolin/cianchosaint_resources.yaml` — the canonical
  Pangolin resource definitions for the 9 services.

## Impact

- Affected specs: 1 NEW spec (`cianchosaint-pangolin-ingress/`).
- Affected code/config: 1 NEW YAML resource file at
  `bonneagar/pangolin/cianchosaint_resources.yaml` (~80 lines).
- No secret values are written to disk: all keys resolve via
  `infisical://dev-baile/cianchosaint/...` template refs hydrated by
  mise + Locket.
- No runtime behaviour changes in this change — the resource
  definitions are declarative and require the operator to run
  `mise run pangolin:resources:apply` to take effect. A follow-up
  change will wire the apply step into the CI pipeline.

## Out of scope

- The Pocket ID identity provider itself. Pocket ID is the wholesale-
  copied identity provider from Cianfhoghlaim — out of scope for this
  change.
- The WireGuard tunnel configuration (per the wholesale-copied Pangolin
  pattern). Out of scope — the resources declare the targets, the
  tunnels are configured separately.
- The Cloudflare Workers + Container deployment for the 9 services.
  Covered by the next change (`cianchosaint-cloudflare-deploy-v1`).

## Validation criteria

1. `openspec validate cianchosaint-pangolin-ingress-v1 --strict`
   passes (exit code 0).
2. `openspec validate cianchosaint-pangolin-ingress --strict` passes
   (exit code 0).
3. `python3.13 -c "import yaml; yaml.safe_load(open('bonneagar/pangolin/cianchosaint_resources.yaml').read())"`
   passes (valid YAML).
4. The YAML declares all 9 resources (8 web apps + 1 API gateway).
5. Every private resource has the 6 canonical labels (constituency,
   app, persona, role, jurisdiction, environment).

## Dependencies

`Blocked by: none`
`Blocked by (soft): cianchosaint-per-persona-app-bundles-v1` (extends;
  the 8 per-persona apps are the targets of the Pangolin resources)
`Affected repos: cianchosaint.` (Cianfhoghlaim + leabharlann remain
  completely unchanged — the wholesale-copied Pangolin pattern from
  Cianfhoghlaim is the upstream reference; this change is a
  cianchosaint-specific deployment.)

## Cross-repo sync

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) and leabharlann
(`/Users/cianmacandeisigh/dev/kings_college_galway/leabharlann/`)
remain **completely unchanged**. See `cross-repo-sync.md` for the
full commit plan.
