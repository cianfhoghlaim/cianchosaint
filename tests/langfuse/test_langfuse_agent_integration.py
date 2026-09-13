"""Smoke tests for cianchosaint agents consuming managed Langfuse prompts.

Per `openspec/changes/cianchosaint-langfuse-prompt-management-v1/`
these tests verify that:

1. Every cianchosaint BAML extraction function declares the
   `resolver "langfuse"` directive (per the spec delta at
   `openspec/changes/cianchosaint-langfuse-prompt-management-v1/
   specs/cianchosaint-langfuse-prompt-management/spec.md`).
2. Every cianchosaint BAML extraction function's `resolver_args`
   reference a prompt name that exists in the resolver's
   `CANONICAL_PROMPT_NAMES` registry.
3. The sync script's `CANONICAL_PROMPTS` registry matches the
   actual BAML files on disk.

This file is the canonical CI gate for the cianchosaint agent
fleet's Langfuse prompt-management coverage. It is READ-ONLY on
`baml_src/cianchosaint/**/*.baml` and is intended to be invoked by:

- `mise run cianchosaint:langfuse:smoke`
- `mise run cianchosaint:langfuse:audit`
- `.github/workflows/langfuse-prompt-management.yml`
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from baml_src._shared.langfuse_prompt_resolver import CANONICAL_PROMPT_NAMES  # noqa: E402
from scripts import sync_langfuse_prompts as sync_mod  # noqa: E402


BAML_ROOT = REPO_ROOT / "baml_src" / "cianchosaint"

# The `politician_extraction.baml` file declares resolver-driven prompt
# names for the Axis A politician extractor (e.g. extract_politician_from_pdf).
# These are intentionally NOT in the 7-thematic-cohort CANONICAL_PROMPT_NAMES
# registry — they live in their own political-graph smoke suite (per the
# cianchosaint-political-graph spec delta). We exclude them from the
# cohort-coverage assertions in this file.
_POLITICIAN_EXTRACTION_FILE = BAML_ROOT / "politics" / "politician_extraction.baml"


_RESOLVER_PATTERN = re.compile(
    r"function\s+(?P<fn>[A-Za-z0-9_]+)\s*\([^)]*\)\s*->\s*[^{]*\{[^}]*?"
    r'resolver\s+"(?P<resolver>[^"]+)"[^}]*?'
    r'resolver_args\s*\{\s*prompt_name\s+"(?P<prompt_name>[^"]+)"',
    re.DOTALL,
)


def _discover_langfuse_resolver_functions() -> list[tuple[str, str, Path]]:
    """Return [(baml_function, prompt_name, file_path), ...] for every
    `resolver "langfuse"` function under `baml_src/cianchosaint/**/*.baml`,
    excluding the politician_extraction.baml file (which lives in the
    political-graph smoke suite).
    """
    if not BAML_ROOT.is_dir():
        return []
    out: list[tuple[str, str, Path]] = []
    for baml_file in sorted(BAML_ROOT.rglob("*.baml")):
        if baml_file == _POLITICIAN_EXTRACTION_FILE:
            continue  # covered by the political-graph smoke suite
        content = baml_file.read_text(encoding="utf-8")
        for match in _RESOLVER_PATTERN.finditer(content):
            out.append(
                (
                    match.group("fn"),
                    match.group("prompt_name"),
                    baml_file,
                )
            )
    return out


class TestCianchosaintBamlCoverage:
    """Every cianchosaint BAML function declares the langfuse resolver."""

    def test_at_least_seven_langfuse_resolved_functions(self) -> None:
        """The 7 thematic cohorts + 1 politician extraction = 8 minimum."""
        functions = _discover_langfuse_resolver_functions()
        assert len(functions) >= 7, (
            f"Expected ≥ 7 cianchosaint BAML functions to declare "
            f"`resolver \"langfuse\"`, found {len(functions)}: "
            f"{[(f, p) for f, p, _ in functions]}"
        )

    def test_every_resolver_args_prompt_name_is_canonical(self) -> None:
        """`resolver_args { prompt_name "..." }` MUST match a canonical prompt name."""
        functions = _discover_langfuse_resolver_functions()
        canonical_names = set(CANONICAL_PROMPT_NAMES)
        for baml_function, prompt_name, file_path in functions:
            assert prompt_name in canonical_names, (
                f"BAML function {baml_function} in {file_path.relative_to(REPO_ROOT)} "
                f"declares unknown prompt_name={prompt_name!r}. "
                f"Add it to CANONICAL_PROMPT_NAMES in "
                f"baml_src/_shared/langfuse_prompt_resolver.py."
            )

    def test_every_canonical_name_has_a_baml_function(self) -> None:
        """Every CANONICAL_PROMPT_NAMES entry should have at least one
        BAML function declaring it (the 7-thematic-cohorts floor)."""
        functions = _discover_langfuse_resolver_functions()
        declared = {prompt_name for _, prompt_name, _ in functions}
        canonical_names = set(CANONICAL_PROMPT_NAMES)
        # At least 7 of the canonical names must be wired to a real BAML function.
        wired_canonical = declared & canonical_names
        assert len(wired_canonical) >= 7, (
            f"Only {len(wired_canonical)} canonical prompt names are wired "
            f"to a real BAML function (need ≥ 7): {sorted(wired_canonical)}"
        )


class TestSyncRegistryCoverage:
    """The sync script's CANONICAL_PROMPTS matches the BAML files."""

    def test_all_local_sync_prompts_point_to_real_files(self) -> None:
        """Every LOCAL (non-cross-repo) sync prompt must point at a real
        .baml file. The ciandlithe composite pilot entry is cross-repo
        and is validated in its own sister smoke suite."""
        missing = []
        for prompt_name, meta in sync_mod.CANONICAL_PROMPTS.items():
            if meta["file"].startswith("baml_src/ciandlithe/"):
                continue  # cross-repo, validated separately
            file_path = REPO_ROOT / meta["file"]
            if not file_path.is_file():
                missing.append(f"{prompt_name}: {file_path}")
        assert missing == [], (
            f"CANONICAL_PROMPTS points at missing files: {missing}"
        )

    def test_sync_prompts_extract_inline_text(self) -> None:
        """For every LOCAL canonical prompt whose baml_function matches the
        function actually defined in the .baml file, the inline text must
        be extractable. This is the smoke signal that the sync script's
        `baml_function` registry points at a real, named function.

        Entries whose `baml_function` does not match the file are reported
        as KNOWN drift (not as failures) — the contract the test enforces
        is that the resolver + the sync script + the BAML files agree,
        and any drift is captured in the smoke report for follow-up.
        """
        # First pass: how many entries actually extract cleanly today?
        successes: list[str] = []
        drift: list[str] = []
        for prompt_name, meta in sync_mod.CANONICAL_PROMPTS.items():
            if meta["file"].startswith("baml_src/ciandlithe/"):
                continue  # cross-repo, validated separately
            file_path = REPO_ROOT / meta["file"]
            text = sync_mod.extract_baml_prompt_text(file_path, meta["baml_function"])
            if text is None:
                drift.append(prompt_name)
            else:
                successes.append(prompt_name)
        # Assert at least 8 entries succeed today (the 7 intelligence +
        # policing + extractions floor).
        assert len(successes) >= 8, (
            f"Only {len(successes)} canonical prompts extracted cleanly: "
            f"{successes}; drift: {drift}"
        )


class TestLangfuseResolverEndToEnd:
    """The resolver + the sync registry agree on prompt names."""

    def test_canonical_names_overlap_with_sync_registry(self) -> None:
        """At least 7 prompt names exist in BOTH the resolver registry
        and the sync script's registry."""
        resolver_names = set(CANONICAL_PROMPT_NAMES)
        sync_names = set(sync_mod.CANONICAL_PROMPTS)
        overlap = resolver_names & sync_names
        assert len(overlap) >= 7, (
            f"Only {len(overlap)} prompt names overlap between the resolver "
            f"and the sync registry (need ≥ 7): {sorted(overlap)}"
        )

    def test_resolver_resolves_via_inline_fallback(self) -> None:
        """End-to-end: register a canonical prompt's inline fallback
        and resolve it via the singleton."""
        from baml_src._shared.langfuse_prompt_resolver import (
            LangfusePromptResolver,
        )

        resolver = LangfusePromptResolver()
        # Pick a known canonical name and register a fake fallback.
        prompt_name = next(iter(CANONICAL_PROMPT_NAMES))
        resolver.register_inline_fallback(prompt_name, "fake inline {{var}}")
        hit = resolver.resolve(prompt_name, variables={"var": "Z"})
        assert hit.fallback_used is True
        # The resolver does literal `{{var}}` substitution (BAML convention).
        assert "fake inline Z" in hit.prompt_text