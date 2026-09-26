"""Smoke test for the centralised MODEL_REGISTRY BAML client surface.

Per the openspec/changes/cianchosaint-baml-centralised-model-registry-v1/
specs/cianchosaint-baml-centralised-model-registry/spec.md, this test verifies:

- The 4 providers load with the correct MODEL_REGISTRY-resolved models
- The 4 provider names match the canonical chain order
- The {{ registry.<family>.<role> }} placeholders are substituted correctly
- The Tier 4 provider uses google-ai (not openai-generic)
- The helper exposes configure_client_registry() returning a baml_py.ClientRegistry

Run: PYTHONPATH=. python3 tests/baml/test_centralised_model_registry.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the repo root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from baml_src._shared.model_registry_helper import (  # noqa: E402
    CLIENT_EMERGENCY,
    CLIENT_FALLBACK,
    CLIENT_LAST_RESORT,
    CLIENT_PRIMARY,
    _REGISTRY_PATTERN,
    _substitute_registry_placeholders,
    get_model_for_tier,
    load_resolved_provider_configs,
)


def assert_eq(actual, expected, label: str) -> bool:
    if actual == expected:
        print(f"  PASS: {label} == {expected!r}")
        return True
    print(f"  FAIL: {label}: expected {expected!r}, got {actual!r}")
    return False


def assert_in(item, container, label: str) -> bool:
    if item in container:
        print(f"  PASS: {label}: {item!r} in container")
        return True
    print(f"  FAIL: {label}: {item!r} not in container")
    return False


def assert_truthy(value, label: str) -> bool:
    if value:
        print(f"  PASS: {label} is truthy")
        return True
    print(f"  FAIL: {label} is falsy")
    return False


def main() -> int:
    print("=" * 60)
    print("cianchosaint-baml-centralised-model-registry smoke test")
    print("=" * 60)

    all_pass = True

    print("\n[1] The 4 providers load with the correct MODEL_REGISTRY-resolved models")
    configs = load_resolved_provider_configs()
    print(f"  Loaded {len(configs)} provider configs")
    expected_models = {
        "unsloth_studio": "minimax-m3",
        "litellm": "minimax-m3",
        "minimax_token_plan": "qwen3.7-plus",
        "gemini_api": "gemini-2.5-pro",
    }
    for cfg in configs:
        all_pass &= assert_eq(
            cfg.model,
            expected_models[cfg.name],
            f"{cfg.name} resolved model",
        )

    print("\n[2] The 4 provider names match the canonical chain order")
    expected_order = ["unsloth_studio", "litellm", "minimax_token_plan", "gemini_api"]
    actual_order = [c.name for c in configs]
    all_pass &= assert_eq(
        actual_order,
        expected_order,
        "canonical provider chain order",
    )

    print("\n[3] The {{ registry.<family>.<role> }} placeholders are substituted correctly")
    test_cases = [
        ("{{ registry.text_llm.default }}", "minimax-m3"),
        ("{{ registry.text_llm.token_plan_primary }}", "qwen3.7-plus"),
        ("{{ registry.text_llm.strong_hosted }}", "gemini-2.5-pro"),
        ("{{ registry.embedder.default }}", "BAAI/bge-m3"),
        ("model is {{ registry.text_llm.default }} (canonical chokepoint)", "model is minimax-m3 (canonical chokepoint)"),
        ("minimax-m3", "minimax-m3"),  # no substitution
    ]
    for template, expected in test_cases:
        all_pass &= assert_eq(
            _substitute_registry_placeholders(template),
            expected,
            f"template {template!r}",
        )

    print("\n[4] The Tier 4 provider uses google-ai (not openai-generic)")
    # Verify by reading the baml_src/clients.baml file directly
    clients_baml_path = Path(__file__).resolve().parents[2] / "baml_src" / "clients.baml"
    clients_baml = clients_baml_path.read_text()
    # Find the LastResort client block
    last_resort_start = clients_baml.find("client<llm> LastResort")
    last_resort_end = clients_baml.find("\n}\n", last_resort_start)
    last_resort_block = clients_baml[last_resort_start:last_resort_end]
    all_pass &= assert_in(
        'provider "google-ai"',
        last_resort_block,
        "LastResort uses google-ai provider",
    )
    all_pass &= assert_truthy(
        "openai-generic" not in last_resort_block,
        "LastResort does NOT use openai-generic",
    )

    print("\n[5] The helper exposes configure_client_registry() returning a baml_py.ClientRegistry")
    try:
        from baml_src._shared.model_registry_helper import configure_client_registry
    except ImportError:
        print("  FAIL: configure_client_registry() not importable")
        all_pass = False
    else:
        try:
            registry = configure_client_registry()
        except ImportError as e:
            # baml_py may not be installed in this CI env; treat as a soft pass
            print(f"  SKIP: configure_client_registry() requires baml_py: {e}")
            print("  (The runtime ClientRegistry is wired up via baml_client.with_client_registry() at app startup)")
        except Exception as e:
            print(f"  FAIL: configure_client_registry() raised: {e}")
            all_pass = False
        else:
            try:
                from baml_py import ClientRegistry
            except ImportError:
                print("  SKIP: baml_py not installed; the ClientRegistry type can't be checked")
            else:
                all_pass &= assert_truthy(
                    isinstance(registry, ClientRegistry),
                    "configure_client_registry() returns a baml_py.ClientRegistry",
                )
                # Verify the 4 client names are present
                all_pass &= assert_eq(
                    registry.list_clients() if hasattr(registry, "list_clients") else sorted(dir(registry)),
                    sorted([CLIENT_PRIMARY, CLIENT_FALLBACK, CLIENT_EMERGENCY, CLIENT_LAST_RESORT]),
                    "ClientRegistry has 4 named clients",
                )

    print("\n" + "=" * 60)
    if all_pass:
        print("ALL ASSERTIONS PASSED ✓")
        return 0
    print("SOME ASSERTIONS FAILED ✗")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
