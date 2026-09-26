#!/usr/bin/env python3
"""CIANCHOSAINT — Skill version-header refresh audit script.

Per the openspec/changes/2026-09-26-skill-version-header-refresh-v1/
specs/skill-refresh/spec.md.

Scans all 79 `.agents/skills/*/SKILL.md` files + compares each
skill's version header against the canonical PACKAGE-VERSIONS.md
entry for its corresponding package.

Usage:
    python3 scripts/audit/refresh_skill_versions.py            # default: print drift table
    python3 scripts/audit/refresh_skill_versions.py --strict  # exit 1 if any drift
    python3 scripts/audit/refresh_skill_versions.py --help    # show help

Licence: BUSL-1.1 (per LICENSE.md)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# The canonical package→skill mapping (per scripts/audit/PACKAGE_TO_SKILL_MAP.md)
PACKAGE_TO_SKILL_MAP: dict[str, list[str]] = {
    "pangolin": ["pangolin"],
    "gerbil": ["pangolin"],
    "newt": ["pangolin"],
    "pangolin-cli": ["pangolin"],
    "litellm": ["litellm"],
    "langfuse": ["langfuse", "agent-observability"],
    "komodo": ["komodo", "stacks-sync"],
    "openchamber": ["opencode"],
    "crawl4ai": ["crawl4ai", "browser-tools"],
    "garage": ["package-version-drift"],
    "infisical": ["secrets-management", "setup-secrets"],
    "dagster": ["dagster", "dagster-asset-sync"],
    "dagster-dlt": ["dlthub", "dlthub-router", "dlt-sync"],
    "dagster-dbt": ["dlthub", "dlthub-router", "dlt-sync"],
    "cocoindex": ["cocoindex", "notebooks-sync"],
    "baml-py": ["baml", "baml-schema-sync"],
    "dlt": ["dlt", "dlt-sync", "dlthub"],
    "duckdb": ["duckdb", "ducklake", "iceberg-lakekeeper"],
    "motherduck": ["motherduck", "ducklake"],
    "lancedb": ["lancedb"],
    "google-adk": ["google-adk", "agent-fleet-orchestration"],
    "cognee": ["cognee", "agent-memory-systems"],
    "mlflow": ["mlflow", "agent-observability"],
    "unsloth": ["unsloth"],
    "graphiti": ["graphiti", "graphiti-core", "agent-memory-systems"],
    "falkordb": ["falkordb"],
    "ducklake": ["ducklake"],
}

# The canonical PACKAGE-VERSIONS.md entries (the canonical "latest" for each)
# Sourced from the canonical PACKAGE-VERSIONS.md table (per Stage 1 audit + Stages 2-5 bumps)
CANONICAL_LATEST: dict[str, str] = {
    "pangolin": "1.23.0",
    "gerbil": "1.5.1",
    "newt": "1.16.x",
    "pangolin-cli": "latest",
    "litellm": "1.102.0",
    "langfuse": "4.7.0",
    "komodo": "2",
    "openchamber": "1.22.2",
    "crawl4ai": "v0.9.4",
    "garage": "v2.4.1",
    "infisical": "v0.165.15",
    "dagster": ">=1.13,<2.0",
    "dagster-dlt": ">=0.29,<1.0",
    "dagster-dbt": ">=0.29,<1.0",
    "cocoindex": ">=1.0.20,<2.0",
    "baml-py": ">=0.223,<1.0",
    "dlt": ">=1.30,<2.0",
    "duckdb": ">=1.5.5,<1.6.0",
    "motherduck": ">=0.10,<1.0",
    "lancedb": ">=0.39,<1.0",
    "google-adk": ">=2.9.0,<3",
    "cognee": ">=1.0.0,<2",
    "mlflow": "3.x",
    "unsloth": ">=2026.6.9",
    "graphiti": "graphiti-core 0.29.2+",
    "falkordb": "4.18.11+",
    "ducklake": "0.3+",
}


def parse_version_header(skill_md: Path) -> tuple[str | None, str | None]:
    """Parse the **Version:** | **Last Updated:** header from a SKILL.md file."""
    version = None
    last_updated = None
    try:
        content = skill_md.read_text()
    except Exception:
        return None, None
    for line in content.splitlines():
        m_version = re.search(r"\*\*Version:\*\*\s*(.+?)(?:\s*\||\s*$)", line)
        if m_version:
            version = m_version.group(1).strip()
        m_updated = re.search(r"\*\*Last Updated:\*\*\s*(\d{4}-\d{2}-\d{2})", line)
        if m_updated:
            last_updated = m_updated.group(1)
    return version, last_updated


def audit_skills(strict: bool = False) -> int:
    """Run the audit + print the per-skill status table."""
    skills_dir = Path(__file__).resolve().parents[2] / ".agents" / "skills"
    if not skills_dir.exists():
        print(f"ERROR: skills directory not found: {skills_dir}", file=sys.stderr)
        return 1

    skill_dirs = sorted([d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()])

    print(f"Auditing {len(skill_dirs)} skills for version-header drift...")
    print()
    print(f"{'SKILL':<35} {'VERSION':<40} {'LAST UPDATED':<15} {'PACKAGE':<20} {'CANONICAL':<30} {'STATUS':<10}")
    print("=" * 150)

    stale_count = 0
    unknown_count = 0
    for skill_dir in skill_dirs:
        skill_name = skill_dir.name
        skill_md = skill_dir / "SKILL.md"
        version, last_updated = parse_version_header(skill_md)

        # Find the canonical package for this skill
        package = None
        canonical = None
        for pkg, skills in PACKAGE_TO_SKILL_MAP.items():
            if skill_name in skills:
                package = pkg
                canonical = CANONICAL_LATEST.get(pkg, "unknown")
                break

        if not package:
            status = "no-map"
            unknown_count += 1
        elif version is None:
            status = "no-header"
            unknown_count += 1
        elif version == canonical:
            status = "aligned"
        else:
            # Simple drift detection (substring match)
            status = "drift"
            stale_count += 1

        print(f"{skill_name:<35} {version or 'NONE':<40} {last_updated or 'NONE':<15} {package or 'unknown':<20} {canonical or 'unknown':<30} {status:<10}")

    print()
    print(f"SUMMARY: {len(skill_dirs)} skills audited")
    print(f"  aligned:           {len(skill_dirs) - stale_count - unknown_count}")
    print(f"  drift (stale):     {stale_count}")
    print(f"  unknown (no-map or no-header): {unknown_count}")

    if strict and stale_count > 0:
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="CIANCHOSAINT — Skill version-header refresh audit script"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any skill has a stale version header",
    )
    args = parser.parse_args()
    return audit_skills(strict=args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
