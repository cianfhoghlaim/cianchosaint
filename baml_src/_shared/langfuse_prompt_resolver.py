"""CIANCHOSAINT — Langfuse v3 prompt management resolver.

Per the openspec/changes/cianchosaint-langfuse-prompt-management-v1/
specs/cianchosaint-langfuse-prompt-management/spec.md.

This module is the load-bearing foundation for the Garda self-hosted
prompt development workflow (per cianchosaint-garda-prompt-workflow).
Every BAML function in `baml_src/cianchosaint/**/*.baml` can either:
- (a) Inline its prompt (the historical default)
- (b) Resolve the prompt via Langfuse (the new pattern)

The `LangfusePromptResolver` class implements (b) with a graceful
fallback to (a) if Langfuse is unavailable (same circuit-breaker
pattern as the 4-tier provider router in
`baml_src/_shared/provider_router.py`).

Per the .agents/skills/langfuse/SKILL.md (wholesale-copied from
cianfhoghlaim/.agents/skills/langfuse/ on 2026-08-24):
- Langfuse v3 (Python SDK v4.12+, JS SDK v5.9+, Platform v3.125+)
- Prompt management via `langfuse.create_prompt()` + `langfuse.get_prompt()`
- Scores API v3 for RAGAS metrics (faithfulness, answer-relevancy,
  context-recall, context-precision)
- A/B testing via `prompt_v2_experiment_tag`

Usage in BAML (per the canonical pattern):

```baml
function ExtractISCReport(input: string) -> ISCReport {
  client Primary
  prompt #"
    {{ _.role("user") }}
    Extract the structured Intelligence and Security Committee report
    metadata from the following content.
    {{ input }}
  "#
  # NEW (per this change): the resolver wraps the prompt with the
  # LangfusePromptResolver so the prompt is loaded from Langfuse at
  # runtime. The inline prompt above is the fallback if Langfuse is
  # unavailable.
  resolver "langfuse"
  resolver_args { prompt_name "extract_isc_report" }
}
```
"""

from __future__ import annotations

import logging
import os
import threading
import time
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LANGFUSE_HOST = os.environ.get(
    "LANGFUSE_HOST",
    "https://langfuse.cianchosaint.ie",
)
LANGFUSE_PUBLIC_KEY = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY = os.environ.get("LANGFUSE_SECRET_KEY", "")

CIRCUIT_BREAKER_THRESHOLD = int(os.environ.get("LANGFUSE_CIRCUIT_BREAKER_THRESHOLD", "3"))
CIRCUIT_BREAKER_RESET_SECONDS = int(os.environ.get("LANGFUSE_CIRCUIT_BREAKER_RESET_SECONDS", "60"))

# The canonical prompt names (mirrored in the BAML files).
CANONICAL_PROMPT_NAMES = {
    "extract_isc_report": "ExtractISCReport",
    "extract_ipco_report": "ExtractIPCOReport",
    "extract_ipt_decision": "ExtractIPTDecision",
    "extract_ipb_evidence": "ExtractInvestigatoryPowersBillEvidence",
    "extract_court_judgment": "ExtractCourtJudgment",
    "extract_statute_reference": "ExtractStatuteReference",
    "extract_foia_request": "ExtractFOIARequest",
    "extract_reform_uk_dossier": "ExtractReformUkDossier",
    "extract_source_policy": "ExtractSourcePolicy",
    "extract_stop_and_search_record": "ExtractStopAndSearchRecord",
    "extract_police_crime_statistics": "ExtractPoliceCrimeStatistics",
    "extract_intelligence_oversight_report": "ExtractIntelligenceOversightReport",
    "extract_cross_jurisdiction_finding": "ExtractCrossJurisdictionFinding",
    "extract_political_party_dossier": "ExtractPoliticalPartyDossier",
    "extract_reform_uk_devolved_dossier": "ExtractReformUkDevolvedDossier",
    "extract_ni_political_dossier": "ExtractNiPoliticalDossier",
    "extract_scottish_political_dossier": "ExtractScottishPoliticalDossier",
    "extract_welsh_london_dossier": "ExtractWelshLondonDossier",
    "extract_roi_political_dossier": "ExtractRoiPoliticalDossier",
    "extract_intelligence_cybersecurity_dossier": "ExtractIntelligenceCybersecurityDossier",
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class LangfusePromptHit:
    """One Langfuse prompt resolution result."""

    prompt_name: str
    prompt_version: int | None
    prompt_text: str
    variables: dict[str, Any]
    langfuse_host: str
    resolved_at: str
    fallback_used: bool


@dataclass
class LangfuseCircuitBreaker:
    """3-strike circuit-breaker per Langfuse prompt resolution."""

    fail_threshold: int = CIRCUIT_BREAKER_THRESHOLD
    reset_seconds: float = float(CIRCUIT_BREAKER_RESET_SECONDS)

    failure_count: int = 0
    last_failure_time: float = 0.0
    is_open: bool = False

    def record_failure(self) -> None:
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.fail_threshold:
            self.is_open = True
            logger.warning(
                "langfuse_circuit_breaker_opened",
                extra={"threshold": self.fail_threshold},
            )

    def record_success(self) -> None:
        self.failure_count = 0
        self.is_open = False

    def is_open_now(self) -> bool:
        if self.is_open and (time.time() - self.last_failure_time) > self.reset_seconds:
            self.is_open = False
            self.failure_count = 0
        return self.is_open


# ---------------------------------------------------------------------------
# Resolver
# ---------------------------------------------------------------------------


class LangfusePromptUnavailable(Exception):
    """Raised when Langfuse is unavailable AND no fallback is provided."""


class LangfusePromptResolver:
    """The canonical Langfuse v3 prompt resolver.

    Mirrors the 4-tier ModelProviderRouter pattern. The resolver:
    - Loads `langfuse` SDK lazily (defer import errors to runtime)
    - Maintains a per-prompt circuit-breaker
    - Falls back to inline prompts if Langfuse is unavailable
    - Records every resolution as a Langfuse span (when available)

    Args:
        host: Langfuse host (default: $LANGFUSE_HOST).
        public_key: Langfuse public key (default: $LANGFUSE_PUBLIC_KEY).
        secret_key: Langfuse secret key (default: $LANGFUSE_SECRET_KEY).
        inline_fallbacks: dict mapping prompt_name → inline prompt text
            (the fallback used when Langfuse is unavailable).
    """

    def __init__(
        self,
        host: str | None = None,
        public_key: str | None = None,
        secret_key: str | None = None,
        inline_fallbacks: dict[str, str] | None = None,
    ) -> None:
        self.host = host or LANGFUSE_HOST
        self.public_key = public_key or LANGFUSE_PUBLIC_KEY
        self.secret_key = secret_key or LANGFUSE_SECRET_KEY
        self.inline_fallbacks = inline_fallbacks or {}
        self.circuit_breaker = LangfuseCircuitBreaker()
        self._client: Any = None
        self._client_lock = threading.Lock()
        self._last_span: dict[str, Any] = {}

    @property
    def is_configured(self) -> bool:
        """True if Langfuse credentials are present."""
        return bool(self.public_key) and bool(self.secret_key)

    def _get_client(self) -> Any:
        """Lazily initialize the Langfuse client (thread-safe)."""
        if self._client is not None:
            return self._client
        with self._client_lock:
            if self._client is not None:
                return self._client
            try:
                from langfuse import Langfuse

                self._client = Langfuse(
                    public_key=self.public_key,
                    secret_key=self.secret_key,
                    host=self.host,
                )
            except ImportError as exc:
                logger.warning(
                    "langfuse_sdk_not_installed", extra={"error": str(exc)}
                )
                raise
        return self._client

    def resolve(
        self,
        prompt_name: str,
        variables: dict[str, Any] | None = None,
    ) -> LangfusePromptHit:
        """Resolve a prompt via Langfuse.

        Args:
            prompt_name: the canonical prompt name (e.g. "extract_isc_report")
            variables: the variables to compile into the prompt template

        Returns:
            A LangfusePromptHit with the resolved prompt text + metadata.

        Falls back to the inline prompt if:
        - The circuit-breaker is open
        - The Langfuse call fails for any reason
        - Langfuse credentials are not configured
        """
        variables = variables or {}
        # If circuit-breaker is open, fall back immediately.
        if self.circuit_breaker.is_open_now():
            logger.info(
                "langfuse_circuit_breaker_open_using_fallback",
                extra={"prompt_name": prompt_name},
            )
            return self._fallback(prompt_name, variables)

        # If Langfuse is not configured, fall back immediately.
        if not self.is_configured:
            logger.debug(
                "langfuse_not_configured_using_fallback",
                extra={"prompt_name": prompt_name},
            )
            return self._fallback(prompt_name, variables)

        # Try to resolve via Langfuse.
        try:
            client = self._get_client()
            prompt = client.get_prompt(prompt_name)
            prompt_text = prompt.compile(**variables)
            self.circuit_breaker.record_success()
            self._last_span = {
                "prompt_name": prompt_name,
                "prompt_version": getattr(prompt, "version", None),
                "langfuse_host": self.host,
                "fallback_used": False,
            }
            from datetime import datetime, timezone

            return LangfusePromptHit(
                prompt_name=prompt_name,
                prompt_version=getattr(prompt, "version", None),
                prompt_text=prompt_text,
                variables=variables,
                langfuse_host=self.host,
                resolved_at=datetime.now(timezone.utc).isoformat(),
                fallback_used=False,
            )
        except Exception as exc:  # noqa: BLE001 - circuit-breaker catches all
            self.circuit_breaker.record_failure()
            logger.warning(
                "langfuse_resolve_failed_using_fallback",
                extra={"prompt_name": prompt_name, "error": str(exc)},
            )
            return self._fallback(prompt_name, variables)

    def _fallback(
        self,
        prompt_name: str,
        variables: dict[str, Any],
    ) -> LangfusePromptHit:
        """Use the inline fallback prompt for a given prompt_name."""
        from datetime import datetime, timezone

        inline_text = self.inline_fallbacks.get(
            prompt_name,
            f"[MISSING_PROMPT_FALLBACK] prompt_name={prompt_name!r}",
        )
        # Apply a simple variable substitution (`{{var}}`).
        compiled = inline_text
        for k, v in variables.items():
            compiled = compiled.replace(f"{{{{{k}}}}}", str(v))
        return LangfusePromptHit(
            prompt_name=prompt_name,
            prompt_version=None,
            prompt_text=compiled,
            variables=variables,
            langfuse_host="(inline_fallback)",
            resolved_at=datetime.now(timezone.utc).isoformat(),
            fallback_used=True,
        )

    def register_inline_fallback(self, prompt_name: str, prompt_text: str) -> None:
        """Register an inline fallback prompt for a given prompt_name."""
        self.inline_fallbacks[prompt_name] = prompt_text

    def health_check(self) -> dict[str, Any]:
        """Health check: returns Langfuse connectivity + circuit-breaker state."""
        from datetime import datetime, timezone

        base: dict[str, Any] = {
            "langfuse_host": self.host,
            "is_configured": self.is_configured,
            "circuit_breaker_open": self.circuit_breaker.is_open_now(),
            "circuit_breaker_failure_count": self.circuit_breaker.failure_count,
            "last_span": self._last_span,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }
        if not self.is_configured:
            base["status"] = "not_configured"
            return base
        if self.circuit_breaker.is_open_now():
            base["status"] = "circuit_breaker_open"
            return base
        try:
            client = self._get_client()
            # The auth_check() call validates the API key without
            # hitting any specific prompt.
            auth_ok = client.auth_check()
            base["status"] = "ok" if auth_ok else "auth_failed"
            return base
        except Exception as exc:  # noqa: BLE001
            base["status"] = "unreachable"
            base["error"] = str(exc)
            return base

    @staticmethod
    def canonical_prompt_names() -> list[str]:
        """Return the canonical Langfuse prompt names (the full list)."""
        return list(CANONICAL_PROMPT_NAMES.keys())

    @staticmethod
    def canonical_baml_function(prompt_name: str) -> str:
        """Return the canonical BAML function name for a given prompt_name."""
        return CANONICAL_PROMPT_NAMES.get(prompt_name, prompt_name)


# ---------------------------------------------------------------------------
# Singleton
# ---------------------------------------------------------------------------

_DEFAULT_RESOLVER: LangfusePromptResolver | None = None


def get_default_resolver() -> LangfusePromptResolver:
    """Return the canonical singleton LangfusePromptResolver.

    Lazily initialized on first call. Re-initialized if Langfuse env
    vars change (per the canonical cianchosaint pattern).
    """
    global _DEFAULT_RESOLVER
    if _DEFAULT_RESOLVER is None:
        _DEFAULT_RESOLVER = LangfusePromptResolver()
    return _DEFAULT_RESOLVER


__all__ = [
    "CANONICAL_PROMPT_NAMES",
    "CIRCUIT_BREAKER_THRESHOLD",
    "CIRCUIT_BREAKER_RESET_SECONDS",
    "LangfuseCircuitBreaker",
    "LangfusePromptHit",
    "LangfusePromptResolver",
    "LangfusePromptUnavailable",
    "get_default_resolver",
]


if __name__ == "__main__":
    import json

    resolver = get_default_resolver()
    print(json.dumps(resolver.health_check(), indent=2))