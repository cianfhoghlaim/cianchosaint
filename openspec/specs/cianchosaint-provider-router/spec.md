# cianchosaint-provider-router Capability

## Purpose

`cianchosaint-provider-router` captures the contract for the
**4-tier ModelProviderRouter Python implementation** that routes
every LLM call through the chain with circuit-breaker fallback +
Langfuse observability + per-deployment config. The wholesale-copied
`baml_src/clients.baml` is the transport; this spec is the
**consumer** of that transport.

## Background

The 4-tier chain (Unsloth Studio → LiteLLM → MiniMax Token Plan →
Gemini API) was established as a foundational decision in
`cianchosaint-bootstrap-v2` and `cianchosaint-repo-foundation-v1`.
This spec authorises the Python class that BAML functions actually
funnel through: `ModelProviderRouter` + `CircuitBreaker` +
`ProviderConfig` + `AllProvidersFailed` + the YAML-driven
per-deployment config.

## Requirements

### Requirement: The 4-tier provider chain

The system SHALL provide a `ModelProviderRouter` Python class at
`baml_src/_shared/provider_router.py` that routes every LLM call
through the 4-tier chain declared in
`baml_src/clients.baml`:

1. **Tier 1 (PRIMARY)** — Unsloth Studio (`minimax-m3`)
2. **Tier 2** — LiteLLM Proxy (`minimax-m3`)
3. **Tier 3** — MiniMax Token Plan (`minimax-m3`)
4. **Tier 4 (LAST RESORT)** — Gemini API (`gemini-2.5-pro`)

#### Scenario: The router returns the active provider's config

- **WHEN** the operator instantiates
  `ModelProviderRouter([Tier1, Tier2, Tier3, Tier4])` and all
  circuit-breakers are closed
- **THEN** `router.get_active_config()` SHALL return the `Tier1`
  `ProviderConfig`
- **AND** the `ProviderConfig.base_url` SHALL match the Unsloth
  Studio endpoint

#### Scenario: The router falls back to Tier 2 when Tier 1 fails

- **WHEN** the operator invokes `router.invoke(prompt)` and the
  Tier 1 call raises an exception
- **THEN** the router SHALL mark Tier 1's circuit-breaker as
  having recorded a failure
- **AND** SHALL retry the call against Tier 2
- **AND** the returned `ProviderResponse.fallback_reason` SHALL be
  the Tier 1 exception message

### Requirement: The 3-strike circuit-breaker (60-second reset)

The system SHALL provide a `CircuitBreaker` class with a 3-strike
threshold (`fail_threshold=3`) and a 60-second reset window
(`reset_seconds=60.0`).

#### Scenario: The circuit-breaker opens after 3 failures

- **WHEN** the operator invokes `cb.record_failure()` 3 times in
  succession
- **THEN** `cb.is_open` SHALL be `True`
- **AND** the router SHALL skip the provider on the next
  `invoke()` call

### Requirement: Per-call timeout (configurable per deployment)

The system SHALL honour a `timeout_seconds: float = 30.0` field on
every `ProviderConfig`.

#### Scenario: A slow Tier 1 falls over to Tier 2

- **WHEN** Tier 1 takes longer than `timeout_seconds` to respond
- **THEN** the router SHALL fall over to Tier 2
- **AND** the Langfuse span attributes SHALL record
  `fallback_reason="TimeoutError"`

### Requirement: Langfuse observability (per-call span attributes)

The system SHALL emit a Langfuse span per `invoke()` call with
`provider_used`, `model`, `fallback_reason`, and
`circuit_breaker_state`. The router SHALL NOT include any API key
or any other secret in the span attributes.

#### Scenario: The Langfuse span is emitted for every call

- **WHEN** the operator invokes `router.invoke(prompt)`
- **THEN** a Langfuse span SHALL be emitted with the 4 canonical
  attributes
- **AND** no API key SHALL appear in the span attributes

### Requirement: Per-deployment config (YAML-driven)

The system SHALL read the provider chain from
`baml_src/_shared/provider_router_config.yaml`.

#### Scenario: The router loads the YAML config at startup

- **WHEN** the operator instantiates `ModelProviderRouter()`
  without arguments
- **THEN** the router SHALL load the chain from
  `baml_src/_shared/provider_router_config.yaml`
- **AND** SHALL fall back to the env-var chain if the YAML file is
  missing

#### Scenario: Per-force overrides take precedence

- **WHEN** the operator invokes
  `router.invoke(prompt, force_id="metropolitan")` and the YAML
  config has a `metropolitan` override
- **THEN** the router SHALL honour the override
- **AND** SHALL emit a Langfuse span attribute
  `per_force_override_applied: true`

## Cross-references

- [`../../LICENSE.md`](../../LICENSE.md) — the load-bearing legal document
- [`../../AGENTS.md`](../../AGENTS.md) — the canonical agent routing
- [`./AGENTS.md`](./AGENTS.md) — the per-spec agent routing
- [`../cianchosaint-bootstrap-v2/spec.md`](../cianchosaint-bootstrap-v2/spec.md) —
  the wholesale-copy umbrella (defines the 4-tier chain)
- [`../cianchosaint-deployment/spec.md`](../cianchosaint-deployment/spec.md) —
  the deployment spec (the YAML config pattern)
- [`../cianchosaint-baml-schemas/spec.md`](../cianchosaint-baml-schemas/spec.md) —
  the per-vertical BAML extractions that consume this router
