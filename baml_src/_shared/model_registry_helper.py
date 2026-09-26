# CIANCHOSAINT model_registry_helper — the runtime BAML ClientRegistry wrapper.
#
# Per the openspec/changes/cianchosaint-baml-centralised-model-registry-v1/spec.md,
# Requirement: Centralised model choice via MODEL_REGISTRY (not hardcoded strings).
#
# This module is the canonical bridge between:
#   - The declarative BAML clients (baml_src/clients.baml) — 4 named clients (Primary,
#     Fallback, Emergency, LastResort) with hardcoded model placeholders that get
#     resolved at runtime via env vars
#   - The centralised MODEL_REGISTRY (meaisinfhoghlaim/models/model_registry.py) —
#     52 entries across 7 families (ocr_vision / text_llm / embedder / rerank /
#     image_gen / voice / translation)
#   - The provider router config (baml_src/_shared/provider_router_config.yaml) —
#     YAML-driven per-deployment model overrides with `{{ registry.<family>.<role> }}`
#     Jinja-style placeholders
#
# Per the BAML best-practices research (2026-09-26, via Firecrawl MCP), the canonical
# BAML pattern for runtime model overrides is the `ClientRegistry` API from `baml_py`
# (NOT the `{{ registry.<family>.<role> }}` template-string syntax that the previous
# plan v3 had guessed at). The ClientRegistry pattern lets you `add_llm_client()` at
# runtime with the resolved model + base_url + api_key, then `set_primary()` per
# function.
#
# Licence: BUSL-1.1 (per LICENSE.md)
"""CIANCHOSAINT model_registry_helper — the runtime BAML ClientRegistry wrapper.

Canonical bridge between:
- The declarative BAML clients (baml_src/clients.baml) — 4 named clients with hardcoded
  model placeholders that get resolved at runtime via env vars.
- The centralised MODEL_REGISTRY (meaisinfhoghlaim/models/model_registry.py) — 52 entries
  across 7 families.
- The provider router config (baml_src/_shared/provider_router_config.yaml) — YAML-driven
  per-deployment model overrides with `{{ registry.<family>.<role> }}` Jinja-style
  placeholders.

Per the BAML best-practices research (2026-09-26), the canonical BAML pattern for runtime
model overrides is the `ClientRegistry` API from `baml_py`, NOT template-string syntax.
The ClientRegistry pattern lets you `add_llm_client()` at runtime with the resolved model
+ base_url + api_key, then `set_primary()` per function.

Usage:
    from baml_src._shared.model_registry_helper import configure_client_registry

    registry = configure_client_registry()
    # Use the registry in your BAML function calls
    result = b.ExtractDefencePublication(input, baml_options={"client_registry": registry})

Or, in cianchosaint's specific case:
    from baml_src._shared.model_registry_helper import configure_client_registry

    registry = configure_client_registry()
    # baml_client.b calls now use the registry-resolved model for each function
    b = baml_client.with_client_registry(registry)
    defence = b.ExtractDefencePublication(input)
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from baml_py import ClientRegistry

logger = logging.getLogger(__name__)


# The canonical YAML config path (same file the provider_router uses)
PROVIDER_ROUTER_CONFIG_PATH = Path(__file__).parent / "provider_router_config.yaml"

# The BAML client names (must match baml_src/clients.baml)
CLIENT_PRIMARY = "Primary"
CLIENT_FALLBACK = "Fallback"
CLIENT_EMERGENCY = "Emergency"
CLIENT_LAST_RESORT = "LastResort"

# Map client name → provider name in the YAML config
CLIENT_TO_PROVIDER = {
    CLIENT_PRIMARY: "unsloth_studio",
    CLIENT_FALLBACK: "litellm",
    CLIENT_EMERGENCY: "minimax_token_plan",
    CLIENT_LAST_RESORT: "gemini_api",
}

# Jinja-style registry placeholder pattern: {{ registry.<family>.<role> }}
_REGISTRY_PATTERN = re.compile(r"\{\{\s*registry\.([a-z_]+)\.([a-z_]+)\s*\}\}")


@dataclass
class ResolvedProviderConfig:
    """Resolved config for one provider in the chain (after MODEL_REGISTRY lookup)."""

    name: str  # "unsloth_studio" | "litellm" | "minimax_token_plan" | "gemini_api"
    client_name: str  # BAML client name (Primary | Fallback | Emergency | LastResort)
    base_url: str
    api_key: str  # resolved from env at runtime
    model: str  # resolved via MODEL_REGISTRY (was {{ registry.text_llm.default }} etc.)
    timeout_seconds: float = 30.0
    enabled: bool = True


def _resolve_registry_placeholder(family: str, role: str) -> str:
    """Resolve a `{{ registry.<family>.<role> }}` placeholder via MODEL_REGISTRY.

    Args:
        family: One of the 7 model families (text_llm, embedder, ocr_vision, etc.)
        role: The canonical role within the family (default, primary, tts, etc.)

    Returns:
        The resolved model key (e.g. "minimax-m3", "BAAI/bge-m3", "gemma-4-26b-a4b").

    Raises:
        ImportError: If meaisinfhoghlaim.models is not available.
        KeyError: If the (family, role) lookup returns no entry.
    """
    from meaisinfhoghlaim.models import model_for

    return model_for(family, role)


def _substitute_registry_placeholders(value: str) -> str:
    """Substitute all `{{ registry.<family>.<role> }}` placeholders in a string.

    Example:
        "minimax-m3" stays "minimax-m3" (no placeholders)
        "{{ registry.text_llm.default }}" becomes "minimax-m3"
        "https://{{ registry.embedder.default }}/api" becomes the embedder's URL
    """
    def _replace(match: re.Match[str]) -> str:
        family = match.group(1)
        role = match.group(2)
        return _resolve_registry_placeholder(family, role)

    return _REGISTRY_PATTERN.sub(_replace, value)


def _parse_yaml_simple(path: Path) -> dict[str, Any]:
    """Minimal YAML parser (avoids PyYAML dependency).

    Supports the subset we need: top-level dicts + nested dicts + lists of strings.
    """
    import yaml  # PyYAML is a runtime dep of litellm, so it's always available

    with open(path) as f:
        return yaml.safe_load(f)


def load_resolved_provider_configs(
    config_path: Path | None = None,
) -> list[ResolvedProviderConfig]:
    """Load provider_router_config.yaml + resolve all MODEL_REGISTRY placeholders.

    This is the canonical entrypoint for the cianchosaint app startup. It returns
    a list of ResolvedProviderConfig with all `{{ registry.<family>.<role> }}`
    placeholders replaced by their MODEL_REGISTRY-resolved values.

    Args:
        config_path: Defaults to PROVIDER_ROUTER_CONFIG_PATH (the cianchosaint
            baml_src/_shared/provider_router_config.yaml file).

    Returns:
        List of 4 ResolvedProviderConfig (unsloth_studio + litellm +
        minimax_token_plan + gemini_api) in the canonical provider_order.

    Raises:
        ImportError: If meaisinfhoghlaim.models is not available.
        KeyError: If a placeholder references a non-existent (family, role) entry.
        FileNotFoundError: If config_path doesn't exist.
    """
    if config_path is None:
        config_path = PROVIDER_ROUTER_CONFIG_PATH

    cfg = _parse_yaml_simple(config_path)
    provider_order = cfg.get("provider_order", [])
    provider_overrides = cfg.get("provider_overrides", {})

    resolved: list[ResolvedProviderConfig] = []
    for provider_name in provider_order:
        if provider_name not in provider_overrides:
            logger.warning(f"provider {provider_name} not in provider_overrides; skipping")
            continue
        overrides = provider_overrides[provider_name]
        # Resolve the model placeholder via MODEL_REGISTRY
        raw_model = overrides.get("model", "")
        resolved_model = _substitute_registry_placeholders(raw_model)
        # Find the matching BAML client name
        client_name = next(
            (cn for cn, pn in CLIENT_TO_PROVIDER.items() if pn == provider_name),
            provider_name,
        )
        # Resolve the api_key from env (was left empty in YAML per the secrets contract)
        api_key_env = f"{provider_name.upper()}_API_KEY"
        api_key = os.environ.get(api_key_env, "")
        resolved.append(
            ResolvedProviderConfig(
                name=provider_name,
                client_name=client_name,
                base_url=overrides.get("base_url", ""),
                api_key=api_key,
                model=resolved_model,
                timeout_seconds=overrides.get("timeout_seconds", 30.0),
                enabled=overrides.get("enabled", True),
            )
        )
    return resolved


def configure_client_registry(
    config_path: Path | None = None,
) -> "ClientRegistry":
    """Build a BAML ClientRegistry from the resolved provider configs.

    Per the BAML best-practices research (2026-09-26), this is the canonical way
    to override BAML client model choices at runtime. The resulting ClientRegistry
    can be passed to `baml_client.with_client_registry()` or via the `baml_options`
    kwarg on any BAML function call.

    Example:
        from baml_src._shared.model_registry_helper import configure_client_registry
        registry = configure_client_registry()
        result = b.ExtractDefencePublication(input, baml_options={"client_registry": registry})

    Args:
        config_path: Defaults to PROVIDER_ROUTER_CONFIG_PATH.

    Returns:
        A baml_py.ClientRegistry configured with the 4 named clients (Primary,
        Fallback, Emergency, LastResort), each pointing at the MODEL_REGISTRY-
        resolved model.

    Raises:
        ImportError: If baml_py is not installed.
    """
    try:
        from baml_py import ClientRegistry
    except ImportError as e:
        raise ImportError(
            "baml_py is required for the centralised model registry. "
            "Install via: pip install baml-py (or uv pip install baml-py)"
        ) from e

    resolved_configs = load_resolved_provider_configs(config_path)
    registry = ClientRegistry()

    for config in resolved_configs:
        if not config.enabled:
            logger.info(f"provider {config.name} disabled; skipping")
            continue
        # Map provider name → BAML provider string
        # unsloth_studio + litellm + minimax_token_plan all use openai-generic
        # (OpenAI-compatible /chat/completions endpoint)
        # gemini_api uses google-ai (the Gemini generateContent endpoint)
        if config.name == "gemini_api":
            provider = "google-ai"
        else:
            provider = "openai-generic"

        registry.add_llm_client(
            name=config.client_name,
            provider=provider,
            options={
                "base_url": config.base_url,
                "api_key": config.api_key,
                "model": config.model,
                "temperature": 0.0,
                "max_tokens": 8192,
                "timeout": int(config.timeout_seconds),
            },
        )
        logger.info(
            "configured baml client",
            extra={
                "client_name": config.client_name,
                "provider": config.name,
                "model": config.model,
                "base_url": config.base_url,
            },
        )

    return registry


def get_model_for_tier(tier: str) -> str:
    """Convenience: return the model key for a given provider tier name.

    Args:
        tier: One of "unsloth_studio", "litellm", "minimax_token_plan", "gemini_api"

    Returns:
        The MODEL_REGISTRY-resolved model key for that tier.
    """
    configs = load_resolved_provider_configs()
    for config in configs:
        if config.name == tier:
            return config.model
    raise KeyError(f"Unknown tier: {tier}")


# Self-test (run via `python -m baml_src._shared.model_registry_helper`)
if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO)
    try:
        configs = load_resolved_provider_configs()
        for c in configs:
            print(f"{c.name}: model={c.model} base_url={c.base_url}")
        print("\nAll MODEL_REGISTRY placeholders resolved successfully.")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
