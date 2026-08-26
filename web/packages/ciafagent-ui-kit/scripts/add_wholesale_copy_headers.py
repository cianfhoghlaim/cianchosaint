#!/usr/bin/env python3
# cianchosaint — `web/packages/ciafagent-ui-kit/scripts/add_wholesale_copy_headers.py`
#
# Prepends the cianchosaint wholesale-copy licence attribution header to
# every .tsx and .ts file under
# `web/packages/ciafagent-ui-kit/src/ic-web-components/` and
# `web/packages/ciafagent-ui-kit/src/ic-react/`.
#
# The header follows the
# openspec/changes/archive/2026-08-23-cianchosaint-repo-bootstrap-v2/
# specs/cianchosaint-bootstrap-v2/spec.md "Data platform wholesale-copy"
# requirement pattern.
#
# The ic-ui-kit is dual-licensed OGL-3.0 + MIT (per its source repo at
# hmgcc/ic-ui-kit/LICENSE). The wholesale-copy preserves both upstream
# licences AND adds the cianchosaint BUSL-1.1 v2 attribution.
#
# Idempotent: skips files that already carry the header marker.

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
PKG_SRC = REPO_ROOT / "web" / "packages" / "ciafagent-ui-kit" / "src"

HEADER_MARKER = "CIANCHOSAINT wholesale-copy of mi6/ic-ui-kit"

HEADER = """/**
 * {MARKER}.
 *
 * Original: mi6/ic-ui-kit (https://github.com/mi6/ic-ui-kit, MIT + OGL-3.0).
 * Wholesale-copied into cianchosaint: 2026-08-26 per
 * openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md.
 *
 * Upstream licences (preserved):
 *   - MIT (https://github.com/mi6/ic-ui-kit/blob/main/LICENSE)
 *   - Open Government Licence v3.0 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)
 *
 * Cianchosaint licence:
 *   - BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md) — British-Isles-only.
 *   - This file is part of the ciafagent UI kit that wraps the IC Design System
 *     for British-Isles defence / policing / intelligence-oversight analysts.
 *
 * Namespace: cianchosaint (every reference is renamed from the upstream
 * `ukic` / `@ukic` package scope to the `cianchosaint` workspace scope
 * during build via the cianchosaint @ukic/* package aliases).
 */
"""

PATTERNS = ("*.ts", "*.tsx")


def already_has_header(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8") as f:
            head = f.read(2048)
        return HEADER_MARKER in head
    except (UnicodeDecodeError, OSError):
        return False


def prepend_header(path: Path) -> bool:
    if already_has_header(path):
        return False
    original = path.read_text(encoding="utf-8")
    path.write_text(HEADER.format(MARKER=HEADER_MARKER) + original, encoding="utf-8")
    return True


def walk_and_prepend(root: Path) -> tuple[int, int]:
    """Returns (files_modified, files_skipped)."""
    modified = 0
    skipped = 0
    for pattern in PATTERNS:
        for file in root.rglob(pattern):
            if "node_modules" in file.parts or "dist" in file.parts:
                continue
            if file.name == "*.d.ts":
                continue
            if prepend_header(file):
                modified += 1
            else:
                skipped += 1
    return modified, skipped


def main(argv: list[str]) -> int:
    targets = [PKG_SRC / "ic-web-components", PKG_SRC / "ic-react"]
    total_modified = 0
    total_skipped = 0
    for target in targets:
        if not target.exists():
            print(f"skip: missing target {target}", file=sys.stderr)
            continue
        modified, skipped = walk_and_prepend(target)
        total_modified += modified
        total_skipped += skipped
        print(f"{target.relative_to(REPO_ROOT)}: modified={modified} skipped={skipped}", file=sys.stderr)
    print(f"total: modified={total_modified} skipped={total_skipped}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
