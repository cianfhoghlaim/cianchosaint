# cianchosaint-baml-centralised-model-registry-v1 — Tasks

> Ordered checklist for shipping `cianchosaint-baml-centralised-model-registry-v1`.

## Phase 1 — Wholesale-copy the MODEL_REGISTRY (deliverable 1)

- [ ] 1.1 Wholesale-copy `meaisinfhoghlaim/models/__init__.py` from `cianfhoghlaim/meaisinfhoghlaim/models/__init__.py`
- [ ] 1.2 Wholesale-copy `meaisinfhoghlaim/models/registry.py` (the 22-entry `VISION_MODELS` + `CLASSICAL_OCR`)
- [ ] 1.3 Wholesale-copy `meaisinfhoghlaim/models/model_registry.py` (the 52-entry unified `MODEL_REGISTRY`)
- [ ] 1.4 Wholesale-copy `meaisinfhoghlaim/models/routing.py`
- [ ] 1.5 Wholesale-copy `meaisinfhoghlaim/models/llama_swap_config.yaml`
- [ ] 1.6 Wholesale-copy `meaisinfhoghlaim/models/ci/` subdirectory (CI helpers)
- [ ] 1.7 Verify with `python3 -c "from meaisinfhoghlaim.models import MODEL_REGISTRY, model_for; print(model_for('text_llm', 'default'))"` → expect `minimax-m3`

## Phase 2 — Create the model_registry_helper.py (deliverable 2)

- [ ] 2.1 Create `baml_src/_shared/model_registry_helper.py` with:
  - `_resolve_registry_placeholder(family, role)` → `model_for(family, role)`
  - `_substitute_registry_placeholders(value)` → regex sub of `{{ registry.<family>.<role> }}`
  - `load_resolved_provider_configs(config_path=None)` → `list[ResolvedProviderConfig]`
  - `configure_client_registry(config_path=None)` → `baml_py.ClientRegistry`
  - `get_model_for_tier(tier)` → `str`
- [ ] 2.2 Verify with `python3 -m baml_src._shared.model_registry_helper` → expect 4 configs printed

## Phase 3 — Update the YAML config (deliverable 4)

- [ ] 3.1 Update `baml_src/_shared/provider_router_config.yaml` — change all 4 `model:` fields from hardcoded strings to `{{ registry.<family>.<role> }}` placeholders
- [ ] 3.2 Verify the 4 mappings resolve correctly:
  - Tier 1 → `text_llm.default` → `minimax-m3`
  - Tier 2 → `text_llm.default` → `minimax-m3`
  - Tier 3 → `text_llm.token_plan_primary` → `qwen3.7-plus`
  - Tier 4 → `text_llm.strong_hosted` → `gemini-2.5-pro`

## Phase 4 — Update the provider_router.py (deliverable 4)

- [ ] 4.1 Update `_providers_from_yaml()` to call `_substitute_registry_placeholders()` on the `model` field
- [ ] 4.2 Verify with `python3 -c "from baml_src._shared.provider_router import ModelProviderRouter; r = ModelProviderRouter(); print(r.providers)"` → expect 4 providers with the resolved models

## Phase 5 — Update clients.baml (deliverable 3)

- [ ] 5.1 Update Tier 4 (Gemini) provider from `openai-generic` to `google-ai` (the canonical BAML Gemini provider)
- [ ] 5.2 Add header comments to each client block explaining the runtime ClientRegistry override pattern
- [ ] 5.3 Keep the hardcoded `model "minimax-m3"` placeholders (BAML needs a default at compile time; the helper overrides at runtime)

## Phase 6 — Create the smoke test (deliverable verification)

- [ ] 6.1 Create `tests/baml/test_centralised_model_registry.py` with 5 assertions:
  - The 4 providers load with the correct MODEL_REGISTRY-resolved models
  - The 4 provider names match the canonical chain order
  - The `{{ registry.<family>.<role> }}` placeholders are substituted correctly
  - The Tier 4 provider uses `google-ai` (not `openai-generic`)
  - The helper exposes `configure_client_registry()` returning a baml_py.ClientRegistry
- [ ] 6.2 Verify with `PYTHONPATH=. python3 tests/baml/test_centralised_model_registry.py` → expect all 5 assertions pass

## Phase 7 — Cross-reference in README

- [ ] 7.1 Add a "Why centralised" sub-section to README §11 pointing at the new helper + the audit + the wholesale-copy
- [ ] 7.2 Add 1-line per-user-type pointer to the new helper

## Phase 8 — Validate + verify + push

- [ ] 8.1 `openspec validate cianchosaint-baml-centralised-model-registry-v1 --strict` passes
- [ ] 8.2 `mise run test:smoke` — 14 suites pass (13 existing + 1 new)
- [ ] 8.3 `mise run lint:registry` — no hardcoded model strings outside the registry
- [ ] 8.4 `mise run lint:license` — no new URLs added
- [ ] 8.5 `git add -A && git commit -m "feat(cianchosaint): centralise BAML model choice via MODEL_REGISTRY"` + force-push to `2026-08-27-kcg-rename-v1` + `main`
