# cianchosaint-baml-centralised-model-registry — Capability Spec

> **Spec ID:** `cianchosaint-baml-centralised-model-registry`
> **Capability umbrella:** `cianchosaint-pipeline` (the broader British Isles defence / policing / intelligence-oversight pipeline)
> **Status:** PROPOSED (post-`cianchosaint-baml-centralised-model-registry-v1` archive)
> **Last updated:** 2026-09-26

## Purpose

Centralise every model choice in the cianchosaint BAML client surface (the 4 named clients: Primary, Fallback, Emergency, LastResort) so that all model keys resolve via the canonical `MODEL_REGISTRY` (52 entries across 7 families, wholesale-copied from `cianfhoghlaim/meaisinfhoghlaim/models/`).

## ADDED Requirements

### Requirement: Wholesale-copy the MODEL_REGISTRY

The system SHALL wholesale-copy `meaisinfhoghlaim/models/` from `cianfhoghlaim/meaisinfhoghlaim/models/` into `cianchosaint/meaisinfhoghlaim/models/`. The 5 wholesale-copied files SHALL be:

- `__init__.py`
- `registry.py` (the 22-entry `VISION_MODELS` + `CLASSICAL_OCR`)
- `model_registry.py` (the 52-entry unified `MODEL_REGISTRY`)
- `routing.py`
- `llama_swap_config.yaml` (the 14-entry llama-swap GGUF config)

Plus the `ci/` subdirectory (CI helpers).

#### Scenario: Smoke test passes

- **WHEN** the wholesale-copy completes
- **THEN** `python3 -c "from meaisinfhoghlaim.models import MODEL_REGISTRY, model_for; print(model_for('text_llm', 'default'))"` SHALL print `minimax-m3`

### Requirement: The model_registry_helper

The system SHALL provide a `baml_src/_shared/model_registry_helper.py` module that exposes:

- `_resolve_registry_placeholder(family: str, role: str) -> str` — resolves a `(family, role)` tuple via `meaisinfhoghlaim.models.model_for()`
- `_substitute_registry_placeholders(value: str) -> str` — substitutes all `{{ registry.<family>.<role> }}` Jinja-style placeholders in a string
- `load_resolved_provider_configs(config_path: Path | None = None) -> list[ResolvedProviderConfig]` — loads the per-deployment YAML + resolves all placeholders
- `configure_client_registry(config_path: Path | None = None) -> baml_py.ClientRegistry` — builds a BAML `ClientRegistry` with the 4 named clients (Primary, Fallback, Emergency, LastResort), each pointing at the MODEL_REGISTRY-resolved model
- `get_model_for_tier(tier: str) -> str` — convenience function returning the model key for a given provider tier name

#### Scenario: Substitution works

- **WHEN** `_substitute_registry_placeholders("{{ registry.text_llm.default }}")` is called
- **THEN** it SHALL return `"minimax-m3"` (the canonical MODEL_REGISTRY resolution)

#### Scenario: ClientRegistry is built correctly

- **WHEN** `configure_client_registry()` is called
- **THEN** it SHALL return a `baml_py.ClientRegistry` with 4 added clients:
  - `Primary` (provider: `openai-generic`, model: `minimax-m3`)
  - `Fallback` (provider: `openai-generic`, model: `minimax-m3`)
  - `Emergency` (provider: `openai-generic`, model: `qwen3.7-plus`)
  - `LastResort` (provider: `google-ai`, model: `gemini-2.5-pro`)

### Requirement: BAML clients use the canonical ClientRegistry pattern

The system SHALL update `baml_src/clients.baml` to:
- Change the Tier 4 (Gemini) provider from `openai-generic` to `google-ai` (the canonical BAML Gemini provider)
- Add header comments to each client block explaining the runtime `ClientRegistry` override pattern
- Keep the hardcoded `model "minimax-m3"` placeholders (BAML needs a default at compile time; the helper overrides at runtime)

#### Scenario: Gemini uses google-ai provider

- **WHEN** the Tier 4 `LastResort` client is configured
- **THEN** it SHALL use the `google-ai` BAML provider (not `openai-generic`)

### Requirement: provider_router_config.yaml uses MODEL_REGISTRY placeholders

The system SHALL update `baml_src/_shared/provider_router_config.yaml` so that all 4 `model:` fields use `{{ registry.<family>.<role> }}` Jinja-style placeholders instead of hardcoded model strings.

The canonical 4-tier mapping SHALL be:

| Tier | Client name | Provider | MODEL_REGISTRY family | MODEL_REGISTRY role | Resolved model |
|---|---|---|---|---|---|
| 1 | Primary | unsloth_studio | text_llm | default | minimax-m3 |
| 2 | Fallback | litellm | text_llm | default | minimax-m3 |
| 3 | Emergency | minimax_token_plan | text_llm | token_plan_primary | qwen3.7-plus |
| 4 | LastResort | gemini_api | text_llm | strong_hosted | gemini-2.5-pro |

#### Scenario: All 4 placeholders resolve

- **WHEN** `load_resolved_provider_configs()` is called
- **THEN** it SHALL return 4 `ResolvedProviderConfig` entries with the resolved models listed in the table above

### Requirement: provider_router.py delegates MODEL_REGISTRY resolution

The system SHALL update `baml_src/_shared/provider_router.py:_providers_from_yaml()` to call `_substitute_registry_placeholders()` on the `model` field, so that the YAML placeholders are resolved at load time.

#### Scenario: Provider router uses resolved models

- **WHEN** `ModelProviderRouter()` is instantiated
- **THEN** the `providers` list SHALL contain 4 `ProviderConfig` entries with the MODEL_REGISTRY-resolved model keys

## MODIFIED Requirements

### Requirement: The 4-tier provider chain (modified)

The 4-tier provider chain (Unsloth Studio → LiteLLM → Qwen3.7-Plus hosted tier → Gemini API) SHALL be preserved, but the model choice for each tier SHALL be centralised via `MODEL_REGISTRY` instead of hardcoded.

#### Scenario: Provider chain order is preserved

- **WHEN** the provider router resolves
- **THEN** the order SHALL be: unsloth_studio → litellm → minimax_token_plan → gemini_api (same as before)
- **AND** the `minimax_token_plan` tier SHALL resolve to `qwen3.7-plus` (the canonical `MODEL_REGISTRY["text_llm"]["token_plan_primary"]` role — NOT the previously incorrect "minimax-m3" assumption)

#### Scenario: All 4 tiers resolve via MODEL_REGISTRY

- **WHEN** `load_resolved_provider_configs()` is called
- **THEN** each of the 4 `ResolvedProviderConfig.model` fields SHALL be a model key that exists in the canonical `MODEL_REGISTRY`

### Requirement: The BAML function surface (preserved)

The 7 BAML functions (`ExtractDefencePublication`, `ExtractCourtJudgment`, `ExtractStatuteReference`, `ExtractPoliceCrimeStatistics`, `ExtractStopAndSearchRecord`, `ExtractIntelligenceOversightReport`, `ExtractCrossJurisdictionFinding`) SHALL be unchanged. Only the model choice behind them is centralised.

#### Scenario: BAML function surface is preserved

- **WHEN** a cianchosaint agent calls `b.ExtractDefencePublication(input)`
- **THEN** the function signature SHALL remain `(input: string) -> DefencePublication`
- **AND** the `DefencePublication` class schema SHALL remain unchanged
- **AND** the only change SHALL be which model is selected by the `ClientRegistry` at runtime

## REMOVED Requirements

None — this is a pure refactor with no removals.
