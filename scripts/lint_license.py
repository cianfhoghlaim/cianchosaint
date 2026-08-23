# cianchosaint — `scripts/lint_license.py`
#
# Original (this file): new-build by Cian Mhac An Deisigh on 2026-08-23
# Licence: BUSL-1.1 (CIANCHOSAINT edition, per LICENSE.md)
#
# This file is part of cianchosaint (the British Isles defence / policing /
# intelligence-oversight open-source data platform). See LICENSE.md for
# the full Additional Use Grant + the 3-step foreign-use gate + the
# warrant-to-enforce clause.
#
# AST-based license lint for cianchosaint. Walks
#   - dlt_sources/cianchosaint/**
#   - agents/cianchosaint/**
# looking for @dlt.source / @dlt.resource / Google ADK agent declarations
# that reference a source URL. For each URL found:
#   1. verifies the URL is in
#      dlt_sources/cianchosaint/common/osint_allowlist.yaml
#   2. verifies the URL points at a British Isles body
#      (.gov.uk / .police.uk / .mod.uk / .parliament.uk / .judiciary.uk
#       / .nhs.uk / .gov.ie / .garda.ie / .defenceforces.ie / .dfa.ie
#       / .courts.ie / .irishstatutebook.ie / .citizensinformation.ie
#       / .gov.je / .gov.gg / .gov.im)
#
# Exits 0 on success, 1 on any violation. Emits structlog-style errors to
# stderr. Mirrors the cianchosaint-pipeline spec § Requirement: OSINT
# source URL allowlist + § Scenario: Allowlist entry must reference a
# British Isles body.

from __future__ import annotations

import argparse
import ast
import sys
from collections.abc import Iterable
from pathlib import Path
from urllib.parse import urlparse

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DLT_DIR = REPO_ROOT / "dlt_sources" / "cianchosaint"
AGENTS_DIR = REPO_ROOT / "agents" / "cianchosaint"
ALLOWLIST_PATH = REPO_ROOT / "dlt_sources" / "cianchosaint" / "common" / "osint_allowlist.yaml"

BRITISH_ISLES_DOMAINS: frozenset[str] = frozenset(
    {
        # United Kingdom
        "gov.uk",
        "police.uk",
        "mod.uk",
        "judiciary.uk",
        "parliament.uk",
        "nhs.uk",
        "bbc.co.uk",
        "metoffice.gov.uk",
        "caa.co.uk",
        "ons.gov.uk",
        "hmrc.gov.uk",
        # Crown Dependencies
        "gov.je",
        "gov.gg",
        "gov.im",
        # Republic of Ireland
        "gov.ie",
        "garda.ie",
        "defenceforces.ie",
        "military.ie",
        "dfa.ie",
        "hse.ie",
        "courts.ie",
        "irishstatutebook.ie",
        "citizensinformation.ie",
        "revenue.ie",
        "cso.ie",
        "met.ie",
        "rte.ie",
    }
)


def load_allowlist() -> set[str]:
    """Return the set of allowlisted source URLs."""
    if not ALLOWLIST_PATH.exists():
        return set()
    data = yaml.safe_load(ALLOWLIST_PATH.read_text(encoding="utf-8")) or {}
    return {
        entry["source_url"]
        for entry in data.get("entries", [])
        if isinstance(entry, dict) and entry.get("source_url")
    }


def is_british_isles_url(url: str) -> bool:
    """Return True iff the URL's host is a British Isles public-sector body."""
    host = (urlparse(url).hostname or "").lower()
    if not host:
        return False
    for domain in BRITISH_ISLES_DOMAINS:
        if host == domain or host.endswith(f".{domain}"):
            return True
    return False


def extract_urls_from_ast(tree: ast.AST) -> Iterable[tuple[str, int]]:
    """Yield (url, lineno) pairs for every HTTP(S) string constant in the tree."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = node.value
            if value.startswith(("http://", "https://")):
                yield value, node.lineno


def has_dlt_or_adk_decorator(tree: ast.AST) -> bool:
    """Return True iff the module declares a @dlt.source / @dlt.resource / ADK agent."""
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Attribute):
                    if decorator.attr in {"source", "resource"}:
                        return True
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                    if decorator.func.attr in {"source", "resource"}:
                        return True
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in {"root_agent", "LlmAgent", "Agent"}:
                return True
    return False


def walk_python_files(roots: Iterable[Path]) -> Iterable[Path]:
    """Yield every .py file under each existing root directory."""
    for root in roots:
        if not root.exists():
            continue
        yield from root.rglob("*.py")


def lint_file(py_path: Path, allowlist: set[str]) -> list[str]:
    """Return a list of violation strings for the given Python file."""
    try:
        tree = ast.parse(py_path.read_text(encoding="utf-8"))
    except SyntaxError as exc:
        return [f"{py_path}:{exc.lineno}: syntax error: {exc.msg}"]

    if not has_dlt_or_adk_decorator(tree):
        return []

    violations: list[str] = []
    for url, lineno in extract_urls_from_ast(tree):
        if url not in allowlist:
            violations.append(
                f"{py_path}:{lineno}: URL not in OSINT allowlist: {url}"
            )
        if not is_british_isles_url(url):
            violations.append(
                f"{py_path}:{lineno}: URL is not a British Isles body: {url}"
            )
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="cianchosaint OSINT allowlist lint")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 on any violation (default behaviour; flag is explicit).",
    )
    args = parser.parse_args()

    if not ALLOWLIST_PATH.exists():
        print(
            f"FAIL: OSINT allowlist not found at {ALLOWLIST_PATH}; "
            "create it before running the lint",
            file=sys.stderr,
        )
        return 1

    allowlist = load_allowlist()
    if not allowlist:
        print(
            f"FAIL: OSINT allowlist at {ALLOWLIST_PATH} contains 0 entries; "
            "populate it from the wholesale-copied "
            "dlt_sources/official_media_cianchosaint/fixtures/ allowlists",
            file=sys.stderr,
        )
        return 1

    all_violations: list[str] = []
    file_count = 0
    for py_path in walk_python_files([DLT_DIR, AGENTS_DIR]):
        file_count += 1
        all_violations.extend(lint_file(py_path, allowlist))

    if all_violations:
        for violation in all_violations:
            print(f"FAIL: {violation}", file=sys.stderr)
        print(
            f"\n{len(all_violations)} violation(s) across {file_count} file(s); "
            "see cianchosaint-pipeline spec § Requirement: OSINT source URL allowlist",
            file=sys.stderr,
        )
        return 1

    print(
        f"OK: {file_count} file(s) scanned; "
        f"{len(allowlist)} allowlist entries; 0 violations"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())