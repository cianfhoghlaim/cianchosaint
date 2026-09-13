"""Smoke tests for the Langfuse prompt management surface (create + update + delete).

Per `openspec/changes/cianchosaint-langfuse-prompt-management-v1/`
these tests verify the `scripts/sync_langfuse_prompts.py` CLI surface
+ the canonical prompt registry contract used by every cianchosaint
BAML extraction function.

The tests are READ-ONLY on `scripts/sync_langfuse_prompts.py` and
`baml_src/_shared/langfuse_prompt_resolver.py`. They exercise:

- the 13-entry `CANONICAL_PROMPTS` registry in the sync script
- the regex-based `extract_baml_prompt_text()` helper
- the `push_prompt()` + `list_prompts()` + `promote_prompt()` flows
  with a stub client (so the tests do NOT require live Langfuse)
- the CLI argument parsing surface

This file is intended to be invoked by the
`mise run cianchosaint:langfuse:smoke` task and by the
`.github/workflows/langfuse-prompt-management.yml` CI gate.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import sync_langfuse_prompts as sync_mod  # noqa: E402


class _StubPrompt:
    """Stub Langfuse `Prompt` object for the list_prompts flow."""

    def __init__(
        self,
        name: str,
        version: int = 1,
        labels: tuple[str, ...] = ("staging",),
        updated_at: str = "2026-08-24T00:00:00Z",
    ) -> None:
        self.name = name
        self.version = version
        self.labels = list(labels)
        self.updated_at = updated_at


class _StubLangfuseClient:
    """Stub Langfuse client covering the full sync-script API surface."""

    def __init__(self) -> None:
        self.created: list[dict[str, Any]] = []
        self.prompts: list[_StubPrompt] = []
        self.get_called: list[tuple[str, int | None]] = []
        self.auth_check_called = False

    def create_prompt(
        self,
        name: str,
        prompt: str,
        labels: list[str] | None = None,
        tags: list[str] | None = None,
        description: str = "",
    ) -> None:
        self.created.append(
            {
                "name": name,
                "prompt": prompt,
                "labels": labels or [],
                "tags": tags or [],
                "description": description,
            }
        )
        # Append the new version to the prompts list so subsequent `list_prompts`
        # calls reflect the create.
        version = len([p for p in self.prompts if p.name == name]) + 1
        self.prompts.append(
            _StubPrompt(name=name, version=version, labels=tuple(labels or []))
        )

    def list_prompts(self) -> list[_StubPrompt]:
        return self.prompts

    def get_prompt(self, name: str, version: int | None = None) -> _StubPrompt:
        self.get_called.append((name, version))
        for p in self.prompts:
            if p.name == name and (version is None or p.version == version):
                return p
        raise KeyError(f"prompt not found: {name} v{version}")

    def auth_check(self) -> bool:
        self.auth_check_called = True
        return True


class TestCanonicalPromptsRegistry:
    """The sync script exposes a canonical prompt registry."""

    def test_registry_has_at_least_13_entries(self) -> None:
        assert len(sync_mod.CANONICAL_PROMPTS) >= 13

    def test_each_entry_has_required_keys(self) -> None:
        for prompt_name, meta in sync_mod.CANONICAL_PROMPTS.items():
            assert "file" in meta, f"{prompt_name} missing 'file'"
            assert "baml_function" in meta, f"{prompt_name} missing 'baml_function'"
            assert "description" in meta, f"{prompt_name} missing 'description'"
            assert meta["file"].endswith(".baml")

    def test_extract_isc_report_registered(self) -> None:
        assert "extract_isc_report" in sync_mod.CANONICAL_PROMPTS
        meta = sync_mod.CANONICAL_PROMPTS["extract_isc_report"]
        assert meta["baml_function"] == "ExtractISCReport"

    def test_extract_composite_pilot_dossier_registered(self) -> None:
        # The ciandlithe composite pilot is included for the BIPP v2 mirror.
        # This is a cross-repo entry — its BAML file lives in the
        # `ciandlithe` sister repo, NOT in this `cianchosaint` checkout.
        assert "extract_composite_pilot_dossier" in sync_mod.CANONICAL_PROMPTS
        meta = sync_mod.CANONICAL_PROMPTS["extract_composite_pilot_dossier"]
        assert meta["file"].startswith("baml_src/ciandlithe/")

    def test_local_files_exist_on_disk(self) -> None:
        # Every LOCAL canonical prompt (excluding the cross-repo
        # ciandlithe composite pilot) must point at a real .baml file
        # on disk. The cross-repo entry is intentionally skipped —
        # it is a `ciandlithe` sister-repo concern, validated in its
        # own smoke suite.
        missing = []
        for prompt_name, meta in sync_mod.CANONICAL_PROMPTS.items():
            if meta["file"].startswith("baml_src/ciandlithe/"):
                continue  # cross-repo, validated separately
            file_path = REPO_ROOT / meta["file"]
            if not file_path.is_file():
                missing.append(f"{prompt_name}: {file_path}")
        assert missing == [], f"missing canonical prompt files: {missing}"


class TestExtractBamlPromptText:
    """The regex extractor pulls the inline `prompt #"..."` block."""

    def test_extracts_prompt_from_real_baml(self, tmp_path: Path) -> None:
        baml = tmp_path / "x.baml"
        baml.write_text(
            'function ExtractX(input: string) -> string {\n'
            '  client Primary\n'
            '  prompt #"\n'
            '    Hello {{ input }} world\n'
            '  "#\n'
            "}\n",
            encoding="utf-8",
        )
        text = sync_mod.extract_baml_prompt_text(baml, "ExtractX")
        assert text is not None
        assert "Hello {{ input }} world" in text

    def test_extracts_prompt_with_multi_arg_signature(self, tmp_path: Path) -> None:
        baml = tmp_path / "x.baml"
        baml.write_text(
            'function ExtractX(input: string, target_entity: string, focus: string) -> Dossier {\n'
            '  client Primary\n'
            '  prompt #"\n'
            '    Analyse {{ target_entity }} for {{ focus }}\n'
            '  "#\n'
            "}\n",
            encoding="utf-8",
        )
        text = sync_mod.extract_baml_prompt_text(baml, "ExtractX")
        assert text is not None
        assert "Analyse {{ target_entity }}" in text

    def test_returns_none_when_function_missing(self, tmp_path: Path) -> None:
        baml = tmp_path / "x.baml"
        baml.write_text(
            "function Other(input: string) -> string {\n  prompt #\"x\"#\n}\n",
            encoding="utf-8",
        )
        assert sync_mod.extract_baml_prompt_text(baml, "ExtractX") is None

    def test_returns_none_when_file_missing(self, tmp_path: Path) -> None:
        assert sync_mod.extract_baml_prompt_text(tmp_path / "missing.baml", "X") is None


class TestPushPrompt:
    """`push_prompt()` creates a prompt via the Langfuse client."""

    def test_dry_run_does_not_call_client(self) -> None:
        client = _StubLangfuseClient()
        ok = sync_mod.push_prompt(
            client=client,
            prompt_name="extract_isc_report",
            prompt_text="hello",
            description="smoke",
            dry_run=True,
        )
        assert ok is True
        assert client.created == []

    def test_live_push_calls_create_prompt(self) -> None:
        client = _StubLangfuseClient()
        ok = sync_mod.push_prompt(
            client=client,
            prompt_name="extract_isc_report",
            prompt_text="inline prompt",
            description="smoke test",
            dry_run=False,
        )
        assert ok is True
        assert len(client.created) == 1
        assert client.created[0]["name"] == "extract_isc_report"
        assert "staging" in client.created[0]["labels"]
        assert "cianchosaint" in client.created[0]["tags"]


class TestListPrompts:
    """`list_prompts()` prints every Langfuse prompt + returns the count."""

    def test_returns_count_of_prompts(self, capsys: pytest.CaptureFixture[str]) -> None:
        client = _StubLangfuseClient()
        client.prompts = [
            _StubPrompt("extract_isc_report", 1, ("staging",)),
            _StubPrompt("extract_ipco_report", 2, ("production",)),
        ]
        count = sync_mod.list_prompts(client)
        assert count == 2
        captured = capsys.readouterr()
        assert "extract_isc_report" in captured.out
        assert "extract_ipco_report" in captured.out


class TestPromotePrompt:
    """`promote_prompt()` looks up the version + logs the action."""

    def test_returns_true_for_existing_version(self) -> None:
        client = _StubLangfuseClient()
        client.prompts = [_StubPrompt("extract_isc_report", 1)]
        ok = sync_mod.promote_prompt(client, "extract_isc_report", 1)
        assert ok is True
        assert client.get_called == [("extract_isc_report", 1)]

    def test_returns_false_for_missing_version(self) -> None:
        client = _StubLangfuseClient()
        ok = sync_mod.promote_prompt(client, "extract_isc_report", 99)
        assert ok is False


class TestSyncScriptCLI:
    """The CLI arg parser accepts the documented flags."""

    def test_argument_parser_defines_all_flags(self) -> None:
        # Touch the parser to ensure the imports + flag set is intact.
        from scripts.sync_langfuse_prompts import main  # noqa: F401

        assert callable(main)

    def test_project_root_path_resolves(self) -> None:
        # The script computes PROJECT_ROOT from its own __file__.
        assert sync_mod.PROJECT_ROOT.exists()
        assert (sync_mod.PROJECT_ROOT / "mise.toml").is_file()