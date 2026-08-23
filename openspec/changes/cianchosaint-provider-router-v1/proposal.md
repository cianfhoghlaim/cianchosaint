# Change: cianchosaint-provider-router-v1

## Why

The `cianchosaint-bootstrap-v2` spec (archived) established the
**4-tier ModelProviderRouter chain** as a foundational decision
(Unsloth Studio → LiteLLM → MiniMax Token Plan → Gemini API), and
the wholesale-copied `baml_src/clients.baml` declares the 4 named
clients (`Primary`, `Fallback`, `Emergency`, `LastResort`). However,
the **Python IMPLEMENTATION** that actually:
1. Tries each provider in priority order
2. Skips providers whose circuit-breaker is open
3. Honours per-call timeouts
4. Emits a Langfuse span per call (`provider_used`, `fallback_reason`,
   `circuit_breaker_state`)
5. Reads the per-deployment config from a YAML file (the
   `provider_router_config.yaml` analogue of the
   `deployment-choice.yaml` pattern)

… has not yet been authored. This change implements the
`baml_src/_shared/provider_router.py` module + the
`baml_src/_shared/provider_router_config.yaml` per-deployment config
+ the `ModelProviderRouter` class + the `CircuitBreaker` companion.

The platform's BAML functions reference the 4 named clients; this
change authorises the actual Python class that BAML funnels through.

## What Changes

- **1 NEW canonical spec**: `cianchosaint-provider-router` with 5 ADDED
  Requirements:
  1. The 4-tier provider chain (Unsloth → LiteLLM → MiniMax → Gemini)
  2. The 3-strike circuit-breaker (60-second reset half-open)
  3. Per-call timeout (configurable per deployment)
  4. Langfuse observability (per-call span attributes)
  5. Per-deployment config (YAML-driven provider order + overrides)
- **2 NEW implementation files** at `baml_src/_shared/`:
  - `provider_router.py` — the `ModelProviderRouter` class +
    `CircuitBreaker` companion + `ProviderConfig` dataclass +
    `AllProvidersFailed` exception
  - `provider_router_config.yaml` — the per-deployment config

## Capabilities

### New Capabilities
- `cianchosaint-provider-router`: The 4-tier ModelProviderRouter Python
  implementation that routes every BAML function call through the
  chain with circuit-breaker fallback + Langfuse observability.

### Modified Capabilities
- `cianchosaint-bootstrap-v2` — the wholesale-copy umbrella now has
  its consumer (the `ModelProviderRouter` Python class).

## Impact

- 2 NEW files under `baml_src/_shared/` (1 Python + 1 YAML)
- 1 NEW canonical spec at `openspec/specs/cianchosaint-provider-router/`
- Imports `logger` from the standard logging library (no new
  dependencies)
- DAG: depends on `cianchosaint-bootstrap-v2` (archived) for the
  4-tier client chain at `baml_src/clients.baml`

## Dependencies

- `Blocked by: cianchosaint-repo-bootstrap-v2` (archived) — the
  wholesale-copied 4-tier client chain at `baml_src/clients.baml`
  must exist before this change can author the router.
- `Affected repos: cianchosaint` (Cianfhoghlaim is NOT touched).

## Cross-references

- [`baml_src/clients.baml`](../../../baml_src/clients.baml) — the
  4-tier client chain (wholesale-copied from Cianfhoghlaim)
- [`openspec/specs/cianchosaint-bootstrap-v2/spec.md`](../../specs/cianchosaint-bootstrap-v2/spec.md) —
  the wholesale-copy umbrella spec
- [`openspec/specs/cianchosaint-deployment/spec.md`](../../specs/cianchosaint-deployment/spec.md) —
  the deployment spec (the per-deployment YAML pattern comes from here)
- [`LICENSE.md`](../../../LICENSE.md) — the BUSL-1.1 v2 licence
  posture
