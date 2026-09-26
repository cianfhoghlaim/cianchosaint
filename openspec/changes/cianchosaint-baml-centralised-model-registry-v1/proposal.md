# cianchosaint-baml-centralised-model-registry-v1 — Proposal

> **Change ID:** `cianchosaint-baml-centralised-model-registry-v1`
> **Author:** Cian Mac an Déisigh Uí Liatháin (Deacy-Lyons)
> **Date:** 2026-09-26
> **Status:** Proposed
> **Spec:** [cianchosaint-baml-centralised-model-registry](./specs/cianchosaint-baml-centralised-model-registry/spec.md)
> **Licence:** BUSL-1.1 (per LICENSE.md)

## Why

The cianchosaint BAML clients (`baml_src/clients.baml`) + the provider router
(`baml_src/_shared/provider_router.py`) + the per-deployment YAML
(`baml_src/_shared/provider_router_config.yaml`) currently hardcode model strings:

```baml
// baml_src/clients.baml — CURRENT (hardcoded):
client<llm> Primary {
  options {
    model "minimax-m3"   ← hardcoded
    ...
  }
}
```

```yaml
# baml_src/_shared/provider_router_config.yaml — CURRENT (hardcoded):
provider_overrides:
  unsloth_studio:
    model: minimax-m3    ← hardcoded
```

This creates **3 problems**:

1. **Drift risk** — when the canonical `MODEL_REGISTRY` (52 entries across 7
   families, wholesale-copied from `cianfhoghlaim/meaisinfhoghlaim/models/`)
   changes a model key, the BAML clients + provider router don't track it.
2. **No centralisation** — `mise run lint:registry` (the canonical audit at
   `.agents/skills/centralized-registry/SKILL.md`) catches hardcoded model
   strings, but the BAML clients + provider router YAML aren't covered by it.
3. **No model swap at runtime** — the canonical BAML pattern is `ClientRegistry`
   (per the 2026-09-26 BAML best-practices research via Firecrawl MCP), which
   lets you swap the model for any BAML function at runtime without recompiling.

## What

This change adds **centralised model choice via `MODEL_REGISTRY`** across the
cianchosaint BAML client surface:

### The 4 deliverables

1. **Wholesale-copy `meaisinfhoghlaim/models/`** from
   `cianfhoghlaim/meaisinfhoghlaim/models/` into
   `cianchosaint/meaisinfhoghlaim/models/`. This brings the canonical 52-entry
   `MODEL_REGISTRY` + the 14-entry `llama_swap_config.yaml` + the routing
   helpers into cianchosaint.

2. **NEW `baml_src/_shared/model_registry_helper.py`** — the canonical Python
   module that:
   - Loads `provider_router_config.yaml`
   - Resolves all `{{ registry.<family>.<role> }}` Jinja-style placeholders via
     `meaisinfhoghlaim.models.model_for(family, role)`
   - Builds a BAML `ClientRegistry` (per the canonical BAML pattern from
     https://docs.boundaryml.com/guide/baml-advanced/llm-client-registry) with
     the 4 named clients (Primary, Fallback, Emergency, LastResort) pointing at
     the MODEL_REGISTRY-resolved models

3. **UPDATE `baml_src/clients.baml`** to use the canonical BAML `ClientRegistry`
   pattern. The hardcoded `model "minimax-m3"` strings stay as placeholders
   (BAML needs a default at compile time), but the runtime
   `model_registry_helper.configure_client_registry()` overrides them at app
   startup. The Tier 4 (Gemini) client changes from `openai-generic` provider
   to `google-ai` provider (the canonical Gemini provider).

4. **UPDATE `baml_src/_shared/provider_router_config.yaml`** to use
   `{{ registry.<family>.<role> }}` placeholders instead of hardcoded model
   strings. The 4-tier chain maps to canonical MODEL_REGISTRY roles:
   - Tier 1 (Unsloth Studio) → `text_llm.default` → `minimax-m3`
   - Tier 2 (LiteLLM) → `text_llm.default` → `minimax-m3`
   - Tier 3 (MiniMax Token Plan) → `text_llm.token_plan_primary` → `qwen3.7-plus` (canonical registry fact — NOT minimax-m3, which the previous plan v3 had wrong)
   - Tier 4 (Gemini) → `text_llm.strong_hosted` → `gemini-2.5-pro`

### The 5-step app startup integration

```python
# In cianchosaint's app startup (e.g. baml_src/_shared/app_init.py or per-agent init)
from baml_src._shared.model_registry_helper import configure_client_registry

# 1. Build the BAML ClientRegistry from MODEL_REGISTRY
registry = configure_client_registry()

# 2. Bind it to the BAML client (per BAML docs)
import baml_client
b = baml_client.with_client_registry(registry)

# 3. Every BAML function call now uses the MODEL_REGISTRY-resolved model
result = b.ExtractDefencePublication(input)

# 4. To override per-call, pass baml_options
result = b.ExtractCourtJudgment(
    input,
    baml_options={"client_registry": registry, "model": "kimi-k3"}  # override for this call only
)

# 5. To override at the function level (e.g. for the political-accountability pipeline)
registry.set_primary("Fallback")  # use LiteLLM gateway instead of Unsloth for this pipeline
```

## Impact

### What's new

- **1 new directory**: `cianchosaint/meaisinfhoghlaim/models/` (wholesale-copied from cianfhoghlaim)
- **1 new file**: `cianchosaint/baml_src/_shared/model_registry_helper.py` (~315 LOC)
- **1 new test**: `cianchosaint/tests/baml/test_centralised_model_registry.py` (~120 LOC)
- **1 new openspec change**: this proposal + tasks.md + spec.md delta

### What's changed (4 files)

- `cianchosaint/baml_src/clients.baml` — Tier 4 (Gemini) provider changes from `openai-generic` to `google-ai`; all 4 client blocks get a header comment explaining the runtime ClientRegistry override pattern
- `cianchosaint/baml_src/_shared/provider_router_config.yaml` — 4 `provider_overrides` blocks change from hardcoded `model: minimax-m3` / `model: gemini-2.5-pro` to `{{ registry.<family>.<role> }}` placeholders
- `cianchosaint/baml_src/_shared/provider_router.py` — `_providers_from_yaml()` gains 1 line that calls `_substitute_registry_placeholders()` to resolve the placeholders
- `cianchosaint/README.md` — §10 "The licence" and §11 "Hardware footprint + cloud options" gain cross-references to the new centralised registry pattern

### What's NOT changed

- The 4 declarative BAML client names (Primary, Fallback, Emergency, LastResort) — same names, same role
- The 3-strike circuit-breaker pattern — unchanged
- The per-force + per-jurisdiction overrides — unchanged (they're a different layer)
- The 8 per-persona web apps — unchanged (they consume the BAML client surface indirectly)

## Dependencies

- **Requires**: `meaisinfhoghlaim/models/` wholesale-copy (deliverable 1 above)
- **Requires**: `baml-py` package (already a runtime dep via `litellm`)
- **Conflicts with**: none — pure refactor, no breaking changes to the BAML function surface

## Firecrawl MCP research basis

Per the 2026-09-26 Firecrawl research:
- **BAML best practices**: https://docs.boundaryml.com/guide/baml-advanced/llm-client-registry (canonical ClientRegistry pattern, replaces the {{ registry.<family>.<role> }} template-string syntax the previous plan v3 had guessed at)
- **MODEL_REGISTRY canonical source**: `cianfhoghlaim/meaisinfhoghlaim/models/model_registry.py` (52 entries, 7 families)
- **Tier 3 model key fact**: the canonical `text_llm.token_plan_primary` role resolves to `qwen3.7-plus` (NOT `minimax-m3` — the previous plan v3 had this wrong)

## Migration

No migration needed — the BAML function surface (the `function ExtractX(input) -> X`
declarations) is unchanged. Only the model choice is centralised.

## Verification

After this change ships, run:

```bash
# 1. The new smoke test passes
PYTHONPATH=. python3 tests/baml/test_centralised_model_registry.py

# 2. The provider router resolves correctly
python3 -c "
from baml_src._shared.model_registry_helper import load_resolved_provider_configs
for c in load_resolved_provider_configs():
    print(f'{c.name}: model={c.model}')
"

# 3. The model_registry audit passes
mise run lint:registry  # fails CI on hardcoded model strings outside the registry

# 4. The openspec change validates
openspec validate cianchosaint-baml-centralised-model-registry-v1 --strict

# 5. All existing smoke tests still pass
mise run test:smoke
```
