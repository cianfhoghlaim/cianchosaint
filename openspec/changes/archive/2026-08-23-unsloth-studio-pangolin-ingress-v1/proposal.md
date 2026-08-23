# Change: unsloth-studio-pangolin-ingress-v1

## Why

The cianchosaint platform has a wholesale-copied Unsloth Studio
container stack at `bonneagar/stacks/unsloth-serve/` (per the
wholesale-copied Cianfhoghlaim pattern). Unsloth Studio is the
local-model serving layer that powers the 4-tier provider chain
(Primary / Fallback / Emergency / Gemini — per
`baml_src/clients.baml`).

The Unsloth Studio local API listens on port 8889 inside the
`unsloth-serve` Docker network. The 8 per-persona web apps + the
Hono API gateway need to invoke the Unsloth Studio API from outside
the Docker network — but there is currently NO Pangolin resource
that exposes the API at `*.cianchosaint.ie`.

This change ships the Pangolin resource definition for
`unsloth.cianchosaint.ie` that exposes the Unsloth Studio local API
at `unsloth-serve:8889` via a private Pangolin resource (Member role,
Pocket ID authentication).

The resource is private (not public) — only authenticated Pocket ID
members of the `cianchosaint-ops` organisation can access the
Unsloth Studio API. The BUSL-1.1 v2 licence posture is preserved
(foreign entities remain explicitly banned).

## What changes

- **1 NEW canonical spec**: `unsloth-studio-pangolin-ingress` with 2
  ADDED Requirements:
  - Requirement: The Pangolin resource for Unsloth Studio at
    `unsloth.cianchosaint.ie:8889`
  - Requirement: Pocket ID authentication + Member role enforcement

- **1 NEW YAML resource file** at
  `bonneagar/pangolin/unsloth_studio_resource.yaml` — the canonical
  Pangolin resource definition for the Unsloth Studio local API.

## Impact

- Affected specs: 1 NEW spec (`unsloth-studio-pangolin-ingress/`).
- Affected code/config: 1 NEW YAML resource file at
  `bonneagar/pangolin/unsloth_studio_resource.yaml` (~30 lines).
- No secret values are written to disk: all keys resolve via
  `infisical://dev-baile/cianchosaint/...` template refs hydrated by
  mise + Locket.
- No runtime behaviour changes — the resource definitions are
  declarative and require the operator to run
  `mise run pangolin:resources:apply` to take effect.

## Out of scope

- The Unsloth Studio container stack itself. Already shipped by the
  wholesale-copied Cianfhoghlaim pattern at
  `bonneagar/stacks/unsloth-serve/`.
- The 4-tier provider chain configuration in
  `baml_src/clients.baml`. Out of scope.
- The Unsloth Studio API documentation. Out of scope — the resource
  simply exposes the existing API.

## Validation criteria

1. `openspec validate unsloth-studio-pangolin-ingress-v1 --strict`
   passes (exit code 0).
2. `openspec validate unsloth-studio-pangolin-ingress --strict` passes
   (exit code 0).
3. `python3 -c "import yaml; yaml.safe_load(open('bonneagar/pangolin/unsloth_studio_resource.yaml').read())"`
   passes (valid YAML).
4. The YAML declares exactly 1 resource for `unsloth.cianchosaint.ie`
   pointing at `unsloth-serve:8889`.

## Dependencies

`Blocked by: none`
`Blocked by (soft): cianchosaint-pangolin-ingress-v1` (extends; the
  upstream 8-web-app + Hono API gateway ingress pattern)
`Blocked by (soft): cianchosaint-per-persona-app-bundles-v1` (extends;
  the per-persona apps consume the Unsloth Studio API)
`Affected repos: cianchosaint.` (Cianfhoghlaim + leabharlann remain
  completely unchanged — the wholesale-copied Unsloth Studio pattern
  from Cianfhoghlaim is the upstream reference.)

## Cross-repo sync

This change touches **ONLY the `cianchosaint` repo**. See
`cross-repo-sync.md` for the full commit plan.
