# Spec Delta: cianchosaint-provider-router

This delta is applied by the openspec change
[`cianchosaint-provider-router-v1`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-provider-router/spec.md`](../../../../specs/cianchosaint-provider-router/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: The 4-tier provider chain

The system SHALL provide a `ModelProviderRouter` Python class at
`baml_src/_shared/provider_router.py` that routes every LLM call
through the 4-tier chain declared in
[`baml_src/clients.baml`](../../../baml_src/clients.baml):

1. **Tier 1 (PRIMARY)** — Unsloth Studio (`minimax-m3`)
2. **Tier 2** — LiteLLM Proxy (`minimax-m3`)
3. **Tier 3** — MiniMax Token Plan (`minimax-m3`)
4. **Tier 4 (LAST RESORT)** — Gemini API (`gemini-2.5-pro`)

The router SHALL accept the 4 `ProviderConfig` dataclasses in
priority order. The first provider whose circuit-breaker is `closed`
(per the next Requirement) SHALL receive the call.

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

The system SHALL provide a `CircuitBreaker` class (in the same
module as `ModelProviderRouter`) with the following contract:

- `fail_threshold: int = 3` — number of consecutive failures before
  the circuit opens
- `reset_seconds: float = 60.0` — seconds before the circuit
  transitions from `open` back to `closed` (half-open state)
- `record_failure()` — increments `failure_count`; opens the circuit
  when `failure_count >= fail_threshold`
- `record_success()` — resets `failure_count` to 0; closes the
  circuit
- `is_open_now()` — returns `True` if the circuit is open and the
  reset window has NOT elapsed; transitions to `closed` (half-open)
  when the reset window HAS elapsed

#### Scenario: The circuit-breaker opens after 3 failures

- **WHEN** the operator invokes `cb.record_failure()` 3 times in
  succession (within the reset window)
- **THEN** `cb.is_open` SHALL be `True`
- **AND** `cb.is_open_now()` SHALL return `True`
- **AND** the router SHALL skip the provider on the next
  `invoke()` call

#### Scenario: The circuit-breaker closes after the reset window

- **WHEN** the operator invokes `cb.record_failure()` 3 times, then
  waits `reset_seconds + 1` seconds
- **THEN** `cb.is_open_now()` SHALL return `False`
- **AND** the router SHALL use the provider on the next `invoke()`
  call (half-open transition)

### Requirement: Per-call timeout (configurable per deployment)

The system SHALL honour a `timeout_seconds: float = 30.0` field on
every `ProviderConfig`. The router SHALL pass the timeout to the
underlying SDK call (e.g. `openai.ChatCompletion.create(..., timeout=cfg.timeout_seconds)`).

#### Scenario: A slow Tier 1 falls over to Tier 2

- **WHEN** Tier 1 takes longer than `timeout_seconds` to respond
- **THEN** the router SHALL raise a `TimeoutError` from the Tier 1
  call
- **AND** SHALL fall over to Tier 2 (per Requirement: The 4-tier
  provider chain)
- **AND** the Langfuse span attributes SHALL record
  `fallback_reason="TimeoutError"` for the Tier 1 attempt

### Requirement: Langfuse observability (per-call span attributes)

The system SHALL emit a Langfuse span per `invoke()` call with the
following attributes:

- `provider_used` — the provider name that actually answered (one of
  `unsloth_studio`, `litellm`, `minimax_token_plan`, `gemini_api`)
- `model` — the model name (e.g. `minimax-m3`, `gemini-2.5-pro`)
- `fallback_reason` — the exception message from the previous failed
  tier (or `None` for Tier 1 successes)
- `circuit_breaker_state` — the state of the breaker when the call
  started (`closed`, `half-open`, or `open`)

The router SHALL NOT include any API key or any other secret in the
span attributes.

#### Scenario: The Langfuse span is emitted for every call

- **WHEN** the operator invokes `router.invoke(prompt)`
- **THEN** a Langfuse span SHALL be emitted with the 4 canonical
  attributes (per above)
- **AND** no API key SHALL appear in the span attributes

### Requirement: Per-deployment config (YAML-driven)

The system SHALL read the provider chain from
`baml_src/_shared/provider_router_config.yaml`. The YAML schema
SHALL match the `deployment-choice.yaml` pattern (per
`cianchosaint-deployment` spec) and SHALL include:

- `provider_order: list[str]` — the priority order of the 4 providers
- `per_force_overrides: dict[str, dict[str, Any]]` — per-force
  overrides (the `force_id` keys from the
  `met_police_extraction.baml` schema)
- `per_jurisdiction_overrides: dict[str, dict[str, Any]]` —
  per-jurisdiction overrides (the jurisdiction enum from the BAML
  schemas)

#### Scenario: The router loads the YAML config at startup

- **WHEN** the operator instantiates `ModelProviderRouter()`
  without arguments
- **THEN** the router SHALL load the chain from
  `baml_src/_shared/provider_router_config.yaml`
- **AND** SHALL fall back to the env-var chain
  (`UNSLOTH_STUDIO_BASE_URL`, `LITELLM_BASE_URL`, etc.) if the
  YAML file is missing

#### Scenario: Per-force overrides take precedence

- **WHEN** the operator invokes `router.invoke(prompt, force_id="metropolitan")`
  and the YAML config has a `metropolitan` override
- **THEN** the router SHALL honour the override (e.g. force
  `gemini_api` as Tier 1 if the override specifies it)
- **AND** SHALL emit a Langfuse span attribute `per_force_override_applied: true`
