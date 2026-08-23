# `unsloth-studio-pangolin-ingress` — Agent Routing

> `unsloth-studio-pangolin-ingress` is the capability that exposes the Unsloth Studio local API at `unsloth.cianchosaint.ie` via a private Pangolin resource (Member role, Pocket ID authentication).

## Routing

Load this AGENTS.md when the parent spec (`./spec.md`) is in scope.
Use it to find the most relevant mise tasks + skills + adjacent files
without re-reading the full spec.

## Quick start

```bash
# 1. Validate the Unsloth Studio ingress spec
openspec validate unsloth-studio-pangolin-ingress --strict

# 2. Verify the YAML resource file
python3 -c "import yaml; print(len(yaml.safe_load(open('bonneagar/pangolin/unsloth_studio_resource.yaml').read())['resources']))"
# Expected: 1

# 3. Apply the resource to the live Pangolin instance
mise run cianchosaint:pangolin:resources:apply
```

## Key sources

- `openspec/specs/unsloth-studio-pangolin-ingress/spec.md` — the canonical spec
- `bonneagar/pangolin/unsloth_studio_resource.yaml` ⭐ — the canonical Pangolin resource definition
- `bonneagar/stacks/unsloth-serve/` — the wholesale-copied Unsloth Studio container stack (the upstream target)
- `baml_src/clients.baml` — the 4-tier provider chain (`Primary` / `Fallback` / `Emergency` / `Gemini`) that consumes the Unsloth Studio API
- `LICENSE.md` (repo root) — the BUSL-1.1 v2 load-bearing legal document

## Adjacent specs

- `openspec/specs/cianchosaint-pangolin-ingress/spec.md` — the upstream 8-web-app + Hono API gateway ingress pattern
- `openspec/specs/cianchosaint-per-constituency-agents/spec.md` — the per-persona apps that consume the Unsloth Studio API

## DO NOT

- Expose the Unsloth Studio API publicly (the resource is private
  by design — only Pocket ID members of `cianchosaint-ops` may
  access).
- Skip the Pocket ID authentication requirement (the wholesale-
  copied Cianfhoghlaim pattern requires auth on every resource).
- Allow non-Member Pocket ID users to access the resource (the
  `role: member` enforcement is mandatory).
- Issue additional `unsloth.cianchosaint.ie/*` routes without
  updating this spec.

## Skill pointers

- `ccc` — for semantic code search across the BAML clients + the
  Unsloth Studio stack
- `openspec` — for the spec change workflow
- `pangolin` — for the wholesale-copied Pangolin ops pattern
- `unsloth` — for the wholesale-copied Unsloth Studio container
  stack
- `secrets-management` — for the Infisical + Locket contract

<!-- generated: 2026-08-23; do not hand-edit -->
