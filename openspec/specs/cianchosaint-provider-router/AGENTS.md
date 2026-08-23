# AGENTS.md — cianchosaint-provider-router

## Routing

The 4-tier ModelProviderRouter Python implementation.
Authored by `cianchosaint-provider-router-v1`.

## Quick start

```python
# Default instantiation: loads from baml_src/_shared/provider_router_config.yaml
router = ModelProviderRouter()
config = router.get_active_config()  # Tier 1 by default
result = router.invoke(prompt="Summarise the Charter of Rights", model_family="text_llm")
# {"provider_used": "unsloth_studio", "model": "minimax-m3",
#  "response": "...", "fallback_reason": None, "circuit_breaker_state": "closed"}
```

## Key sources

- `baml_src/_shared/provider_router.py` — `ModelProviderRouter` + `CircuitBreaker`
- `baml_src/_shared/provider_router_config.yaml` — per-deployment config
- `baml_src/clients.baml` — the 4-tier client chain

## Adjacent specs

- `cianchosaint-bootstrap-v2` — the wholesale-copy umbrella
- `cianchosaint-deployment` — the deployment spec (YAML pattern)
- `cianchosaint-baml-schemas` — the consumers of this router

## DO NOT

- DO NOT introduce a 5th provider without an openspec change.
- DO NOT include any API key or secret in the Langfuse span
  attributes.
- DO NOT bypass the circuit-breaker (3-strike + 60s reset is the
  contract).

## Skill pointers

- `.agents/skills/litellm/SKILL.md` — LLM router patterns
