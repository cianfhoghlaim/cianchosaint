# Tasks: cianchosaint-provider-router-v1

## 1. Canonical spec scaffold

- [ ] 1.1 Create `openspec/specs/cianchosaint-provider-router/spec.md`
      (5 ADDED Requirements)
- [ ] 1.2 Create `openspec/specs/cianchosaint-provider-router/AGENTS.md`
      (≤30 lines)
- [ ] 1.3 Create
      `openspec/changes/cianchosaint-provider-router-v1/specs/cianchosaint-provider-router/spec.md`
      (the spec delta)

## 2. Implementation files (2 files at `baml_src/_shared/`)

- [ ] 2.1 `baml_src/_shared/provider_router.py` — the
      `ModelProviderRouter` class + `CircuitBreaker` companion +
      `ProviderConfig` dataclass + `AllProvidersFailed` exception
- [ ] 2.2 `baml_src/_shared/provider_router_config.yaml` — the
      per-deployment config (provider order + per-force overrides)

## 3. Conservative-posture enforcement

- [ ] 3.1 The default provider order is the 4-tier chain
      (Unsloth → LiteLLM → MiniMax → Gemini)
- [ ] 3.2 The router raises `AllProvidersFailed` when all 4 providers
      fail (no silent fallback to a non-allowlisted provider)
- [ ] 3.3 The Langfuse span attributes NEVER include the API key
      (only `provider_used`, `model`, `fallback_reason`,
      `circuit_breaker_state`)

## 4. Validation

- [ ] 4.1 `openspec validate cianchosaint-provider-router-v1 --strict`
      passes
- [ ] 4.2 `openspec validate openspec/specs/cianchosaint-provider-router/ --strict`
      passes
- [ ] 4.3 Python syntax check:
      `/Users/cianmacandeisigh/.local/share/uv/python/cpython-3.13-macos-aarch64-none/bin/python3.13 -c "import ast; ast.parse(open('baml_src/_shared/provider_router.py').read())"`
- [ ] 4.4 YAML syntax check:
      `python -c "import yaml; yaml.safe_load(open('baml_src/_shared/provider_router_config.yaml'))"`

## 5. Commit + archive

- [ ] 5.1 `git add baml_src/_shared/ openspec/specs/cianchosaint-provider-router/
      openspec/changes/cianchosaint-provider-router-v1/` only
- [ ] 5.2 `git commit -m "feat(q3-track1): ModelProviderRouter Python implementation (circuit-breaker + Langfuse span) (Change 12)"`
- [ ] 5.3 `git push origin main`
- [ ] 5.4 `openspec archive cianchosaint-provider-router-v1 --yes`
