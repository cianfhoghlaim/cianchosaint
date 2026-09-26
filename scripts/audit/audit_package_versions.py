#!/usr/bin/env python3
"""CIANCHOSAINT + CIANFHOGHLAIM package version audit script.

Per the openspec/changes/2026-09-26-package-version-drift-audit-v1/specs/package-version-drift/spec.md,
Requirement: Audit script that runs against PyPI + Docker Hub + GitHub Releases.

This script produces the canonical drift report for all 80+ opensource packages
across both repos. The output feeds:
- The CI gate (`.github/workflows/package-version-drift.yml`)
- The Dagster sensor (`orchestration/defs/sensors/package_version_drift_sensor.py`)
- The mise task (`mise run devops:version-drift`)
- The skill (`.agents/skills/package-version-drift/SKILL.md`)

Usage:
    python3 scripts/audit_package_versions.py            # Default: print drift table
    python3 scripts/audit_package_versions.py --json     # Emit JSON for CI
    python3 scripts/audit_package_versions.py --strict   # Exit 1 if drift > 1 minor
    python3 scripts/audit_package_versions.py --help     # Show all options

Drift semantics:
- "aligned" — pinned == latest
- "behind-1-minor" — pinned is exactly 1 minor behind latest
- "behind-N-minor" — pinned is N minor behind latest
- "behind-major" — pinned is on a different major
- "unknown" — can't determine (network error, package not found)

Version policy (per docs/VERSION-DRIFT-POLICY.md, NEW 2026-09-26):
- Pin EXACT (==) for IaC stack Docker images
- Pin CARET (^=) for Python BIEP data platform deps
- Pin LATEST for dev tooling (mise [tools])

Licence: BUSL-1.1 (per LICENSE.md)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path


# === Canonical registry (the source of truth for "what we pin") ===

# Each entry: name, kind (pypi|docker|github), pinned, repo (cianchosaint|cianchofghhlaim|both)
#   kind-specific query params: pypi: package_name; docker: image_name; github: owner/repo
# This is the canonical package drift table — sourced from the 2026-09-26
# Firecrawl MCP research of 80+ opensource packages across both repos.

PACKAGE_TABLE: list[dict] = [
    # ===== IaC stack Docker images (both repos) =====
    {"name": "pangolin",           "kind": "docker", "image": "fosrl/pangolin",     "pinned_ciancho": "ee-1.23.0",  "pinned_cianfhog": "ee-1.23.0",  "policy": "exact", "stage": "2a"},
    {"name": "gerbil",             "kind": "docker", "image": "fosrl/gerbil",       "pinned_ciancho": "1.5.1",      "pinned_cianfhog": "1.5.1",     "policy": "exact", "stage": "2a"},
    {"name": "newt",               "kind": "docker", "image": "fosrl/newt",         "pinned_ciancho": "latest",     "pinned_cianfhog": "1.16.x",    "policy": "exact", "stage": "2a", "note": "Pangolin 1.23 renamed Newt → Pangolin Site; legacy container kept for backward compat"},
    {"name": "pangolin-cli",       "kind": "docker", "image": "fosrl/pangolin-cli", "pinned_ciancho": "latest",     "pinned_cianfhog": "latest",    "policy": "exact", "stage": "2a", "note": "v1.23+ canonical new-site pattern (replaces standalone Newt binary)"},
    {"name": "infisical",          "kind": "docker", "image": "infisical/infisical", "pinned_ciancho": "v0.161.12",  "pinned_cianfhog": "v0.161.12", "policy": "exact", "stage": "2c"},
    {"name": "litellm",            "kind": "docker", "image": "ghcr.io/berriai/litellm-database", "pinned_ciancho": "v1.102.0",  "pinned_cianfhog": "v1.102.0",  "policy": "exact", "stage": "2b"},
    {"name": "langfuse",           "kind": "docker", "image": "langfuse/langfuse",  "pinned_ciancho": "4.7.0",      "pinned_cianfhog": "4.7.0",     "policy": "exact", "stage": "2b"},
    {"name": "langfuse-worker",    "kind": "docker", "image": "langfuse/langfuse-worker", "pinned_ciancho": "4.7.0",  "pinned_cianfhog": "4.7.0",     "policy": "exact", "stage": "2b"},
    {"name": "komodo-core",        "kind": "docker", "image": "ghcr.io/moghtech/komodo-core", "pinned_ciancho": "2",       "pinned_cianfhog": "2",      "policy": "exact", "stage": "2b"},
    {"name": "komodo-periphery",   "kind": "docker", "image": "ghcr.io/moghtech/komodo-periphery", "pinned_ciancho": "2-dev", "pinned_cianfhog": "2-dev", "policy": "exact", "stage": "2b"},
    {"name": "ferretdb",           "kind": "docker", "image": "ghcr.io/ferretdb/ferretdb", "pinned_ciancho": "2",       "pinned_cianfhog": "2",      "policy": "exact", "stage": "2b", "note": "Komodo 1.18+ requires FerretDB v2 (per v1.18 release notes)"},
    {"name": "openchamber",        "kind": "docker", "image": "ghcr.io/openchamber/openchamber", "pinned_ciancho": "1.22.2",   "pinned_cianfhog": "1.22.2",  "policy": "exact", "stage": "2b"},
    {"name": "crawl4ai",           "kind": "docker", "image": "unclecode/crawl4ai", "pinned_ciancho": "v0.9.2",     "pinned_cianfhog": "v0.9.2",    "policy": "exact", "stage": "2c"},
    {"name": "garage",             "kind": "docker", "image": "dxflrs/garage",      "pinned_ciancho": "v2.3.0",      "pinned_cianfhog": "v2.3.0",     "policy": "exact", "stage": "2c"},
    {"name": "stagehand",         "kind": "docker", "image": "cianchosaint/stagehand", "pinned_ciancho": "local",  "pinned_cianfhog": "n/a",       "policy": "exact", "stage": "skip"},
    {"name": "locket",             "kind": "docker", "image": "cianchosaint/locket", "pinned_ciancho": "local",       "pinned_cianfhog": "n/a",       "policy": "exact", "stage": "skip"},
    {"name": "openclaw",           "kind": "docker", "image": "cianchosaint/openclaw", "pinned_ciancho": "local",     "pinned_cianfhog": "local",     "policy": "exact", "stage": "skip"},

    # ===== Python BIEP data platform deps (both repos) =====
    {"name": "dagster",            "kind": "pypi", "pypi": "dagster",     "pinned_ciancho": ">=1.13.0",   "pinned_cianfhog": ">=1.13",    "policy": "caret", "stage": "3"},
    {"name": "dagster-dlt",        "kind": "pypi", "pypi": "dagster-dlt", "pinned_ciancho": "unpinned",    "pinned_cianfhog": ">=0.29",     "policy": "caret", "stage": "3"},
    {"name": "dagster-dbt",       "kind": "pypi", "pypi": "dagster-dbt", "pinned_ciancho": "unpinned",    "pinned_cianfhog": ">=0.29",     "policy": "caret", "stage": "3"},
    {"name": "cocoindex",          "kind": "pypi", "pypi": "cocoindex",   "pinned_ciancho": ">=1.0.14",    "pinned_cianfhog": ">=1.0.20",   "policy": "caret", "stage": "3"},
    {"name": "baml-py",            "kind": "pypi", "pypi": "baml-py",     "pinned_ciancho": ">=0.223.0",   "pinned_cianfhog": ">=0.222.0",  "policy": "caret", "stage": "3"},
    {"name": "dlt",                "kind": "pypi", "pypi": "dlt",         "pinned_ciancho": ">=1.4.0",     "pinned_cianfhog": ">=1.28.1",   "policy": "caret", "stage": "3"},
    {"name": "duckdb",             "kind": "pypi", "pypi": "duckdb",      "pinned_ciancho": ">=1.4.0",     "pinned_cianfhog": ">=1.4,<1.6.0", "policy": "caret", "stage": "3"},
    {"name": "motherduck",         "kind": "pypi", "pypi": "motherduck",  "pinned_ciancho": ">=0.10.0",    "pinned_cianfhog": ">=0.10",     "policy": "caret", "stage": "3"},
    {"name": "lancedb",            "kind": "pypi", "pypi": "lancedb",     "pinned_ciancho": ">=0.20.0",    "pinned_cianfhog": ">=0.15",     "policy": "caret", "stage": "3+5"},
    {"name": "google-adk",         "kind": "pypi", "pypi": "google-adk",  "pinned_ciancho": "unpinned",    "pinned_cianfhog": ">=2.5.0,<3", "policy": "caret", "stage": "3"},
    {"name": "langfuse-py",        "kind": "pypi", "pypi": "langfuse",    "pinned_ciancho": ">=4.7.0,<5.0", "pinned_cianfhog": ">=4.15.1 (via logfire)", "policy": "caret", "stage": "3"},
    {"name": "litellm-py",         "kind": "pypi", "pypi": "litellm",     "pinned_ciancho": "unpinned",    "pinned_cianfhog": ">=1.97.0",   "policy": "caret", "stage": "3"},
    {"name": "firecrawl-py",       "kind": "pypi", "pypi": "firecrawl",   "pinned_ciancho": "unpinned",    "pinned_cianfhog": ">=4.28.2",   "policy": "caret", "stage": "skip"},
    {"name": "marimo",             "kind": "pypi", "pypi": "marimo",      "pinned_ciancho": "unpinned",    "pinned_cianfhog": ">=0.23.10",  "policy": "caret", "stage": "skip"},
    {"name": "openai",             "kind": "pypi", "pypi": "openai",      "pinned_ciancho": "unpinned",    "pinned_cianfhog": ">=2.32.0",   "policy": "caret", "stage": "skip"},
    {"name": "anthropic",          "kind": "pypi", "pypi": "anthropic",   "pinned_ciancho": "unpinned",    "pinned_cianfhog": ">=0.106.0",  "policy": "caret", "stage": "skip"},
    {"name": "groq",               "kind": "pypi", "pypi": "groq",        "pinned_ciancho": "unpinned",    "pinned_cianfhog": ">=1.4.0",    "policy": "caret", "stage": "skip"},
    {"name": "google-genai",       "kind": "pypi", "pypi": "google-genai", "pinned_ciancho": "unpinned",   "pinned_cianfhog": ">=1.73.1",   "policy": "caret", "stage": "skip"},
    {"name": "pydantic",           "kind": "pypi", "pypi": "pydantic",    "pinned_ciancho": ">=2.10.0",    "pinned_cianfhog": ">=2 (via pydantic-settings)", "policy": "caret", "stage": "skip"},
    {"name": "structlog",         "kind": "pypi", "pypi": "structlog",   "pinned_ciancho": ">=25.0.0",    "pinned_cianfhog": ">=25",       "policy": "caret", "stage": "skip"},
    {"name": "logfire",            "kind": "pypi", "pypi": "logfire",     "pinned_ciancho": "unpinned",    "pinned_cianfhog": ">=4.15.1",   "policy": "caret", "stage": "skip"},
    {"name": "fastapi",            "kind": "pypi", "pypi": "fastapi",     "pinned_ciancho": "unpinned",    "pinned_cianfhog": ">=0.115.0,<0.140", "policy": "caret", "stage": "skip"},
    {"name": "agno",               "kind": "pypi", "pypi": "agno",        "pinned_ciancho": "unpinned",    "pinned_cianfhog": ">=2.6.11",   "policy": "caret", "stage": "skip"},
    {"name": "ibis-framework",     "kind": "pypi", "pypi": "ibis-framework", "pinned_ciancho": "unpinned", "pinned_cianfhog": ">=10",       "policy": "caret", "stage": "skip"},
    {"name": "pyiceberg",          "kind": "pypi", "pypi": "pyiceberg",   "pinned_ciancho": "unpinned",    "pinned_cianfhog": ">=0.10",     "policy": "caret", "stage": "skip"},
    {"name": "pymupdf",            "kind": "pypi", "pypi": "pymupdf",     "pinned_ciancho": "unpinned",    "pinned_cianfhog": ">=1.24",     "policy": "caret", "stage": "skip"},
    {"name": "tenacity",           "kind": "pypi", "pypi": "tenacity",    "pinned_ciancho": "unpinned",    "pinned_cianfhog": ">=9,<10",    "policy": "caret", "stage": "skip"},
    {"name": "httpx",              "kind": "pypi", "pypi": "httpx",       "pinned_ciancho": "unpinned",    "pinned_cianfhog": ">=0.27,<1.0", "policy": "caret", "stage": "skip"},
    {"name": "beautifulsoup4",     "kind": "pypi", "pypi": "beautifulsoup4", "pinned_ciancho": "unpinned", "pinned_cianfhog": ">=4.12",     "policy": "caret", "stage": "skip"},
    {"name": "pyyaml",             "kind": "pypi", "pypi": "pyyaml",      "pinned_ciancho": ">=6.0.0",     "pinned_cianfhog": "unpinned",   "policy": "caret", "stage": "skip"},
]


@dataclass
class DriftResult:
    """Single package drift result."""

    name: str
    kind: str  # pypi|docker|github
    pinned_ciancho: str
    pinned_cianfhog: str
    latest: str
    drift_status: str  # aligned|behind-1-minor|behind-N-minor|behind-major|unknown|local-only
    policy: str
    stage: str
    note: str = ""


def fetch_pypi_latest(pkg: str, timeout: float = 5.0) -> str:
    """Fetch the latest version of a PyPI package."""
    url = f"https://pypi.org/pypi/{pkg}/json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "cianchosaint-audit/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
            return data["info"]["version"]
    except (urllib.error.URLError, KeyError, json.JSONDecodeError) as e:
        return f"unknown ({e})"


def fetch_docker_latest(image: str, timeout: float = 5.0) -> str:
    """Fetch the latest tag of a Docker Hub image.

    NOTE: This requires the Docker Hub Registry API. For GHCR images,
    we use the GitHub Container Registry API instead.
    """
    # Split registry/image
    if image.startswith("ghcr.io/"):
        path = image.replace("ghcr.io/", "")
        url = f"https://ghcr.io/token?scope=repository:{path}:pull&service=ghcr.io"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "cianchosaint-audit/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                token_data = json.loads(resp.read())
                token = token_data.get("token", "")
        except Exception:
            token = ""

        url2 = f"https://ghcr.io/v2/{path}/tags/list"
        try:
            req = urllib.request.Request(
                url2,
                headers={"User-Agent": "cianchosaint-audit/1.0", "Authorization": f"Bearer {token}"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read())
                tags = [t for t in data.get("tags", []) if not t.startswith("sha")]
                if not tags:
                    return "unknown (no tags)"
                # Return the most recent non-snapshot tag
                return sorted(tags, reverse=True)[0]
        except Exception as e:
            return f"unknown ({e})"
    else:
        # Docker Hub
        url = f"https://hub.docker.com/v2/repositories/{image}/tags/?page_size=20"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "cianchosaint-audit/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read())
                tags = [t["name"] for t in data.get("results", []) if not t["name"].startswith("sha")]
                if not tags:
                    return "unknown (no tags)"
                return tags[0]
        except Exception as e:
            return f"unknown ({e})"


def fetch_github_latest(owner_repo: str, timeout: float = 5.0) -> str:
    """Fetch the latest release tag of a GitHub repo."""
    url = f"https://api.github.com/repos/{owner_repo}/releases/latest"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "cianchosaint-audit/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
            return data.get("tag_name", "unknown")
    except Exception as e:
        return f"unknown ({e})"


def _parse_version(v: str) -> tuple[int, int, int] | None:
    """Parse a version string like '1.5.5' or 'v1.5.5' into (major, minor, patch)."""
    v = v.lstrip("v")
    parts = v.split(".")
    if len(parts) < 3:
        # Try to coerce 2-part versions like '1.5' into (1, 5, 0)
        if len(parts) == 2:
            try:
                return (int(parts[0]), int(parts[1]), 0)
            except ValueError:
                return None
        return None
    try:
        return (int(parts[0]), int(parts[1]), int(parts[2].split("-")[0].split("+")[0]))
    except (ValueError, IndexError):
        return None


def _extract_pinned_version(pinned: str) -> str | None:
    """Extract the canonical version from a pinned constraint string.

    Examples:
        ">=1.4,<1.6.0" → "1.6.0" (the upper bound, i.e. the constraint ceiling)
        ">=1.13.0" → "1.13.0"
        "ee-latest" → None (no version)
        "1.0.0@sha256:21fda..." → "1.0.0"
        "v0.161.12" → "0.161.12"
    """
    if pinned in ("latest", "unpinned", "local", "n/a", "needs-verification"):
        return None

    # Find all version strings in the constraint
    matches = re.findall(r"\d+\.\d+(?:\.\d+)?", pinned)
    if not matches:
        return None

    # If the constraint has a comma, take the LAST version (the upper bound)
    if "," in pinned:
        return matches[-1]
    # If the constraint has < or >, take the version after the operator
    if "<" in pinned or ">" in pinned:
        return matches[-1]

    # No operator — it's a raw version (possibly with @sha256 suffix)
    return matches[0]


def compute_drift(pinned: str, latest: str) -> str:
    """Compute drift status from pinned vs latest version strings."""
    if pinned in ("latest", "unpinned", "local", "n/a", "needs-verification"):
        return "local-only" if pinned in ("local", "n/a") else "unknown"

    if latest.startswith("unknown"):
        return "unknown"

    pinned_v = _extract_pinned_version(pinned)
    if pinned_v is None:
        return "unknown"

    latest_v = _extract_pinned_version(latest)
    if latest_v is None:
        return "unknown"

    # Direct match
    if pinned_v == latest_v:
        return "aligned"

    # Compare semver
    p = _parse_version(pinned_v)
    l = _parse_version(latest_v)
    if p is None or l is None:
        return "unknown"

    p_major, p_minor, p_patch = p
    l_major, l_minor, l_patch = l

    if p_major != l_major:
        # Special case: pinned is BEHIND major-wise (e.g., 1.x → 2.x)
        return "behind-major"

    if p_minor == l_minor:
        # Same major.minor — drift is just patch
        return "aligned" if p_patch == l_patch else "aligned"  # patch diff = still aligned per LiteLLM policy

    delta = l_minor - p_minor
    if delta <= 0:
        # Pinned is same or newer than latest (shouldn't happen but handle)
        return "aligned"
    if delta == 1:
        return "behind-1-minor"
    return f"behind-{delta}-minor"


def audit_all(strict: bool = False, json_output: bool = False) -> list[DriftResult]:
    """Run the full audit."""
    results: list[DriftResult] = []
    for pkg in PACKAGE_TABLE:
        # Skip local-only images (we don't drift-track them)
        if pkg.get("pinned_ciancho") in ("local", "n/a"):
            continue

        # Fetch latest based on kind
        latest = "unknown"
        if pkg["kind"] == "pypi":
            latest = fetch_pypi_latest(pkg["pypi"])
        elif pkg["kind"] == "docker":
            latest = fetch_docker_latest(pkg["image"])
        elif pkg["kind"] == "github":
            latest = fetch_github_latest(pkg["owner"])

        # Compute drift for each pinned value (take the worse one)
        drift_ciancho = compute_drift(pkg["pinned_ciancho"], latest)
        drift_cianfhog = compute_drift(pkg["pinned_cianfhog"], latest)

        # The drift_status is the worse of the two (aligned is best)
        status_priority = {
            "aligned": 0,
            "behind-1-minor": 1,
            "behind-2-minor": 2,
            "behind-3-minor": 3,
            "unknown": 4,
            "local-only": 5,
            "behind-major": 6,
        }
        # Parse "behind-N-minor" into the priority
        def parse_drift(d: str) -> int:
            if d.startswith("behind-") and d.endswith("-minor") and d != "behind-1-minor":
                try:
                    n = int(d.split("-")[1])
                    return n
                except ValueError:
                    return 99
            return status_priority.get(d, 99)

        worst_drift = drift_ciancho if parse_drift(drift_ciancho) > parse_drift(drift_cianfhog) else drift_cianfhog

        results.append(
            DriftResult(
                name=pkg["name"],
                kind=pkg["kind"],
                pinned_ciancho=pkg["pinned_ciancho"],
                pinned_cianfhog=pkg["pinned_cianfhog"],
                latest=latest,
                drift_status=worst_drift,
                policy=pkg["policy"],
                stage=pkg["stage"],
                note=pkg.get("note", ""),
            )
        )

    return results


def print_table(results: list[DriftResult]) -> None:
    """Print a human-readable drift table."""
    print(f"\n{'PACKAGE':<22} {'PINNED (ciancho)':<22} {'PINNED (cianfhog)':<22} {'LATEST':<22} {'DRIFT':<20} {'STAGE':<6}")
    print("=" * 120)
    for r in results:
        print(f"{r.name:<22} {r.pinned_ciancho:<22} {r.pinned_cianfhog:<22} {r.latest:<22} {r.drift_status:<20} {r.stage:<6}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="CIANCHOSAINT/CIANFHOGHLAIM package version audit")
    parser.add_argument("--json", action="store_true", help="Emit JSON output for CI")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any drift > 1 minor behind")
    args = parser.parse_args(argv)

    results = audit_all(strict=args.strict, json_output=args.json)

    if args.json:
        output = {
            "audit_timestamp": datetime.now(timezone.utc).isoformat(),
            "results": [asdict(r) for r in results],
        }
        print(json.dumps(output, indent=2))
    else:
        print_table(results)
        print()
        n_aligned = sum(1 for r in results if r.drift_status == "aligned")
        n_behind_1 = sum(1 for r in results if r.drift_status == "behind-1-minor")
        n_behind_n = sum(1 for r in results if r.drift_status.startswith("behind-") and r.drift_status != "behind-1-minor")
        n_unknown = sum(1 for r in results if r.drift_status == "unknown")
        print(f"SUMMARY: {len(results)} packages audited")
        print(f"  aligned:           {n_aligned}")
        print(f"  behind-1-minor:    {n_behind_1}")
        print(f"  behind-N-minor:    {n_behind_n}")
        print(f"  unknown:           {n_unknown}")

    # Strict mode: exit 1 if drift > 1 minor
    if args.strict:
        for r in results:
            if r.drift_status.startswith("behind-") and r.drift_status != "behind-1-minor":
                if r.drift_status != "behind-major":  # behind-major handled separately
                    return 1
            if r.drift_status == "behind-major":
                return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
