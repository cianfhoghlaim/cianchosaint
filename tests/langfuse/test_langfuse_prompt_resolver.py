"""Smoke tests for the Langfuse v3 prompt resolver.

Per `openspec/changes/cianchosaint-langfuse-prompt-management-v1/`
these tests verify the resolver at
`baml_src/_shared/langfuse_prompt_resolver.py` resolves prompts
+ applies the inline fallback + drives the 3-strike circuit-breaker
correctly when Langfuse credentials are absent (the CI mode).

The tests are READ-ONLY on `baml_src/_shared/langfuse_prompt_resolver.py`
and assert the public contract documented in the spec delta at
`openspec/changes/cianchosaint-langfuse-prompt-management-v1/
specs/cianchosaint-langfuse-prompt-management/spec.md`.

This file is intended to be invoked by the
`mise run cianchosaint:langfuse:smoke` task and by the
`.github/workflows/langfuse-prompt-management.yml` CI gate.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from baml_src._shared.langfuse_prompt_resolver import (  # noqa: E402
    CANONICAL_PROMPT_NAMES,
    CIRCUIT_BREAKER_THRESHOLD,
    CIRCUIT_BREAKER_RESET_SECONDS,
    LangfuseCircuitBreaker,
    LangfusePromptHit,
    LangfusePromptResolver,
    get_default_resolver,
)


@pytest.fixture
def unconfigured_resolver(monkeypatch: pytest.MonkeyPatch) -> LangfusePromptResolver:
    """Return a fresh resolver with no Langfuse credentials configured."""
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
    return LangfusePromptResolver()


@pytest.fixture
def configured_resolver(monkeypatch: pytest.MonkeyPatch) -> LangfusePromptResolver:
    """Return a fresh resolver with placeholder Langfuse credentials."""
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-test-123")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test-456")
    return LangfusePromptResolver()


class TestResolverFallback:
    """The resolver falls back to the inline prompt when Langfuse is unconfigured."""

    def test_resolve_returns_langfuse_prompt_hit_with_fallback_used(
        self, unconfigured_resolver: LangfusePromptResolver
    ) -> None:
        unconfigured_resolver.register_inline_fallback(
            "extract_isc_report", "Inline fallback text for {{topic}}"
        )
        hit = unconfigured_resolver.resolve(
            "extract_isc_report", variables={"topic": "ISCR/2023/01"}
        )
        assert isinstance(hit, LangfusePromptHit)
        assert hit.fallback_used is True
        assert hit.prompt_name == "extract_isc_report"
        assert hit.prompt_version is None
        # NOTE: the resolver's `_fallback()` does a literal
        # `.replace("{{var}}", str(v))` — so the variable name must
        # be `{{topic}}` (no spaces) for substitution to fire.
        assert hit.langfuse_host == "(inline_fallback)"

    def test_resolve_returns_missing_prompt_marker_when_no_fallback(
        self, unconfigured_resolver: LangfusePromptResolver
    ) -> None:
        hit = unconfigured_resolver.resolve("extract_unknown_thing")
        assert hit.fallback_used is True
        assert "[MISSING_PROMPT_FALLBACK]" in hit.prompt_text
        assert "extract_unknown_thing" in hit.prompt_text

    def test_health_check_returns_not_configured(
        self, unconfigured_resolver: LangfusePromptResolver
    ) -> None:
        result = unconfigured_resolver.health_check()
        assert result["status"] == "not_configured"
        assert result["is_configured"] is False
        assert result["circuit_breaker_open"] is False
        assert result["circuit_breaker_failure_count"] == 0


class TestResolverInlineRegistration:
    """`register_inline_fallback()` stores prompts keyed by canonical name."""

    def test_register_then_resolve(self, unconfigured_resolver: LangfusePromptResolver) -> None:
        unconfigured_resolver.register_inline_fallback(
            "extract_court_judgment", "Court prompt v1 {{case_id}}"
        )
        hit = unconfigured_resolver.resolve(
            "extract_court_judgment", variables={"case_id": "C-2024-001"}
        )
        # The resolver's `_fallback()` does a literal
        # `.replace("{{case_id}}", str(v))` — variable substitution requires
        # the `{{var}}` form (no spaces) per the BAML convention.
        assert "Court prompt v1 C-2024-001" in hit.prompt_text
        assert hit.fallback_used is True

    def test_register_overwrites_previous(self, unconfigured_resolver: LangfusePromptResolver) -> None:
        unconfigured_resolver.register_inline_fallback("extract_x", "old")
        unconfigured_resolver.register_inline_fallback("extract_x", "new {{var}}")
        hit = unconfigured_resolver.resolve("extract_x", variables={"var": "Z"})
        assert "new Z" in hit.prompt_text
        assert "old" not in hit.prompt_text


class TestCircuitBreaker:
    """The 3-strike circuit-breaker opens after threshold consecutive failures."""

    def test_starts_closed(self) -> None:
        cb = LangfuseCircuitBreaker()
        assert cb.is_open is False
        assert cb.failure_count == 0
        assert cb.is_open_now() is False

    def test_opens_after_threshold_failures(self) -> None:
        cb = LangfuseCircuitBreaker(fail_threshold=3, reset_seconds=60.0)
        cb.record_failure()
        assert cb.is_open is False
        cb.record_failure()
        assert cb.is_open is False
        cb.record_failure()
        assert cb.is_open is True

    def test_is_open_now_returns_true_when_open(self) -> None:
        cb = LangfuseCircuitBreaker(fail_threshold=1)
        cb.record_failure()
        assert cb.is_open_now() is True

    def test_record_success_resets(self) -> None:
        cb = LangfuseCircuitBreaker(fail_threshold=3)
        cb.record_failure()
        cb.record_failure()
        cb.record_success()
        assert cb.failure_count == 0
        assert cb.is_open is False

    def test_resets_after_reset_seconds(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Use a fake monotonic clock via monkeypatched `time.time`.
        import baml_src._shared.langfuse_prompt_resolver as resolver_mod

        monkeypatch.setattr(resolver_mod.time, "time", lambda: 1000.0)
        cb = LangfuseCircuitBreaker(fail_threshold=1, reset_seconds=10.0)
        cb.record_failure()
        assert cb.is_open_now() is True

        # Advance the fake clock past the reset window.
        monkeypatch.setattr(resolver_mod.time, "time", lambda: 2000.0)
        assert cb.is_open_now() is False


class TestCanonicalPromptNames:
    """The canonical 20+ prompt names match every BAML function."""

    def test_at_least_20_canonical_names(self) -> None:
        assert len(CANONICAL_PROMPT_NAMES) >= 20

    def test_extract_isc_report_present(self) -> None:
        assert "extract_isc_report" in CANONICAL_PROMPT_NAMES
        assert CANONICAL_PROMPT_NAMES["extract_isc_report"] == "ExtractISCReport"

    def test_extract_ipco_report_present(self) -> None:
        assert "extract_ipco_report" in CANONICAL_PROMPT_NAMES
        assert CANONICAL_PROMPT_NAMES["extract_ipco_report"] == "ExtractIPCOReport"

    def test_canonical_prompt_names_returns_list(self) -> None:
        names = LangfusePromptResolver.canonical_prompt_names()
        assert isinstance(names, list)
        assert len(names) == len(CANONICAL_PROMPT_NAMES)

    def test_canonical_baml_function_lookup(self) -> None:
        assert (
            LangfusePromptResolver.canonical_baml_function("extract_isc_report")
            == "ExtractISCReport"
        )
        assert (
            LangfusePromptResolver.canonical_baml_function("unknown_name") == "unknown_name"
        )


class TestCircuitBreakerConstants:
    """The default circuit-breaker constants are sane."""

    def test_threshold_is_positive(self) -> None:
        assert CIRCUIT_BREAKER_THRESHOLD >= 1

    def test_reset_seconds_is_positive(self) -> None:
        assert CIRCUIT_BREAKER_RESET_SECONDS >= 1


class TestDefaultResolverSingleton:
    """`get_default_resolver()` returns the canonical singleton."""

    def test_returns_resolver_instance(self) -> None:
        r = get_default_resolver()
        assert isinstance(r, LangfusePromptResolver)

    def test_is_idempotent(self) -> None:
        a = get_default_resolver()
        b = get_default_resolver()
        assert a is b


class TestResolveRecordsSpan:
    """A successful inline-fallback resolution still populates the
    `health_check().last_span` lazily."""

    def test_health_check_last_span_initial_empty(
        self, unconfigured_resolver: LangfusePromptResolver
    ) -> None:
        result = unconfigured_resolver.health_check()
        assert result["last_span"] == {}

    def test_resolve_does_not_populate_last_span_when_fallback(
        self, unconfigured_resolver: LangfusePromptResolver
    ) -> None:
        unconfigured_resolver.register_inline_fallback("extract_x", "fallback text")
        unconfigured_resolver.resolve("extract_x")
        # The `_last_span` is only populated on successful Langfuse hits
        # (so we can detect that a real fetch happened).
        assert unconfigured_resolver._last_span == {}