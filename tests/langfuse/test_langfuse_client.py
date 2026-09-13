"""Smoke tests for the Langfuse v3 client wrapper.

Per `openspec/changes/cianchosaint-langfuse-prompt-management-v1/`
these tests verify the thin client wrapper at
`baml_src/_shared/langfuse_client.py` connects + authenticates
correctly in the no-credentials CI mode and returns the expected
`not_configured` health surface.

The tests are READ-ONLY on `baml_src/_shared/langfuse_client.py`
and assert the public contract documented in the spec delta at
`openspec/changes/cianchosaint-langfuse-prompt-management-v1/
specs/cianchosaint-langfuse-prompt-management/spec.md`.

This file is intended to be invoked by the
`mise run cianchosaint:langfuse:smoke` task and by the
`.github/workflows/langfuse-prompt-management.yml` CI gate.
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SHARED_DIR = REPO_ROOT / "baml_src" / "_shared"

# Ensure the project root is on sys.path so `baml_src._shared.*` imports resolve.
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture(scope="module")
def langfuse_client_module():
    """Reload the langfuse_client module to pick up env-var-only config."""
    import baml_src._shared.langfuse_client as mod

    importlib.reload(mod)
    return mod


class TestLangfuseConfig:
    """The LangfuseConfig dataclass reads env vars at construction time."""

    def test_default_host_is_local_canary(
        self, langfuse_client_module, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("LANGFUSE_HOST", raising=False)
        monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
        monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
        cfg = langfuse_client_module.LangfuseConfig()
        assert cfg.host == "https://langfuse.cianchosaint.ie"
        assert cfg.public_key == ""
        assert cfg.secret_key == ""
        assert cfg.environment == "production"

    def test_is_configured_false_when_no_creds(
        self, langfuse_client_module, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
        monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
        cfg = langfuse_client_module.LangfuseConfig()
        assert cfg.is_configured is False

    def test_is_configured_true_when_both_creds_set(
        self, langfuse_client_module, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-test-123")
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test-456")
        cfg = langfuse_client_module.LangfuseConfig()
        assert cfg.is_configured is True

    def test_host_override_respected(
        self, langfuse_client_module, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("LANGFUSE_HOST", "https://langfuse.staging.example.com")
        cfg = langfuse_client_module.LangfuseConfig()
        assert cfg.host == "https://langfuse.staging.example.com"


class TestHealthCheck:
    """The `health_check()` helper returns the canonical CI status surface."""

    def test_returns_not_configured_when_no_creds(
        self, langfuse_client_module, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
        monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
        result = langfuse_client_module.health_check()
        assert result["status"] == "not_configured"
        assert result["is_configured"] is False
        assert "host" in result
        assert "environment" in result
        assert "release" in result

    def test_returns_json_serialisable_dict(
        self, langfuse_client_module, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
        monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
        result = langfuse_client_module.health_check()
        # `json.dumps` must not raise — the field types must be JSON-native.
        json.dumps(result)


class TestGetLangfuseClientSingleton:
    """The `get_langfuse_client()` singleton raises when unconfigured."""

    def test_raises_runtime_error_when_not_configured(
        self, langfuse_client_module, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
        monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
        # Reset the singleton so the test sees the new env.
        langfuse_client_module._CLIENT = None
        with pytest.raises(RuntimeError, match="not configured"):
            langfuse_client_module.get_langfuse_client()


class TestRagasMetrics:
    """The RAGAS_METRICS constant is the canonical RAGAS metric list."""

    def test_contains_the_five_canonical_metrics(self, langfuse_client_module) -> None:
        canonical = {
            "ragas.faithfulness",
            "ragas.answer_relevancy",
            "ragas.context_recall",
            "ragas.context_precision",
            "ragas.context_entity_recall",
        }
        assert canonical.issubset(set(langfuse_client_module.RAGAS_METRICS))

    def test_no_duplicate_metric_names(self, langfuse_client_module) -> None:
        metrics = langfuse_client_module.RAGAS_METRICS
        assert len(metrics) == len(set(metrics))


class TestReportRagasScores:
    """The `report_ragas_scores()` helper ignores empty inputs."""

    def test_returns_zero_for_empty_scores(
        self, langfuse_client_module, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
        monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
        assert langfuse_client_module.report_ragas_scores("trace-x", {}) == 0

    def test_returns_zero_for_unknown_metrics(
        self, langfuse_client_module, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
        monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
        # Unknown metrics are filtered silently when no client is configured
        # (the helper catches the no-client RuntimeError). The point is that
        # we don't crash with KeyError or TypeError on unknown metric names.
        result = langfuse_client_module.report_ragas_scores(
            "trace-x", {"not.a.real.metric": 0.5}
        )
        assert result == 0


class TestTagExperiment:
    """The `tag_experiment()` helper tolerates the not-configured case."""

    def test_does_not_raise_when_not_configured(
        self, langfuse_client_module, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
        monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
        # The helper must log-and-swallow the RuntimeError, not propagate it.
        langfuse_client_module.tag_experiment(
            trace_id="trace-x",
            experiment_name="ci_smoke",
            variant="baseline",
        )


class TestModuleExports:
    """The module's `__all__` exports the documented public surface."""

    def test_all_exports(self, langfuse_client_module) -> None:
        expected = {
            "LangfuseConfig",
            "RAGAS_METRICS",
            "get_langfuse_client",
            "health_check",
            "report_ragas_scores",
            "tag_experiment",
        }
        assert set(langfuse_client_module.__all__) == expected

    def test_shared_dir_layout(self) -> None:
        assert (SHARED_DIR / "langfuse_client.py").is_file()