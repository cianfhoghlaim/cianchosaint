# `cianchosaint-pangolin-ingress` — Agent Routing

> `cianchosaint-pangolin-ingress` is the capability that exposes the 8 per-persona web apps + the Hono API gateway at `*.cianchosaint.ie` via Pangolin private + public resources.

## Routing

Load this AGENTS.md when the parent spec (`./spec.md`) is in scope.
Use it to find the most relevant mise tasks + skills + adjacent files
without re-reading the full spec.

## Quick start

```bash
# 1. Validate the Pangolin ingress spec
openspec validate cianchosaint-pangolin-ingress --strict

# 2. Verify the YAML resource file
python3.13 -c "import yaml; print(len(yaml.safe_load(open('bonneagar/pangolin/cianchosaint_resources.yaml').read())['resources']))"
# Expected: 9

# 3. Apply the resources to the live Pangolin instance
mise run cianchosaint:pangolin:resources:apply
```

## Key sources

- `openspec/specs/cianchosaint-pangolin-ingress/spec.md` — the canonical spec
- `bonneagar/pangolin/cianchosaint_resources.yaml` ⭐ — the canonical Pangolin resource definitions
- `bonneagar/pangolin/README.md` — the Pangolin ops guide
- `LICENSE.md` (repo root) — the BUSL-1.1 v2 load-bearing legal document

## Adjacent specs

- `openspec/specs/cianchosaint-deployment/spec.md` — the deployment umbrella
- `openspec/specs/cianchosaint-per-constituency-agents/spec.md` — the per-persona apps exposed by the resources
- `openspec/specs/cianchosaint-reform-uk-pilot-workflow/spec.md` — the reform-uk-pilot consumer
- `openspec/specs/cianchosaint-self-hosted-citizen/spec.md` — the self-host consumer

## DO NOT

- Expose any of the private resources publicly — `ga-internal`,
  `met-internal`, `psni-internal`, `reform-uk-pilot`, `self-host`,
  and `api` SHALL remain private by design.
- Skip the Pocket ID authentication requirement on any resource —
  even the public-facing per-persona apps require Pocket ID auth
  per the wholesale-copied Cianfhoghlaim pattern.
- Add a new resource without the 6 canonical labels (constituency,
  app, persona, role, jurisdiction, environment).
- Apply the resources without running
  `openspec validate cianchosaint-pangolin-ingress --strict` first
  (CI gate).

## Skill pointers

- `ccc` — for semantic code search across the per-persona apps
- `openspec` — for the spec change workflow
- `pangolin` — for the wholesale-copied Pangolin ops pattern
- `secrets-management` — for the Pocket ID + Infisical + Locket contract

<!-- generated: 2026-08-23; do not hand-edit -->
