#!/usr/bin/env bash
# cianchosaint — `web/packages/ciafagent-ui-kit/scripts/ic_ui_kit_smoke.sh`
#
# The cianchosaint:ic-ui-kit:smoke mise task. Verifies the
# ciafagent-ui-kit wholesale-copy is intact + the licence attribution
# headers are present on every TypeScript file.
#
# Per the openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
# specs/cianchosaint-ic-ui-kit-integration/spec.md Requirement:
# The cianchosaint:ic-ui-kit:smoke mise task.
#
# Exits 0 on success, 1 on any violation.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PKG_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$PKG_ROOT/../.." && pwd)"

IC_WC="$PKG_ROOT/src/ic-web-components"
IC_REACT="$PKG_ROOT/src/ic-react"
INDEX_TS="$PKG_ROOT/src/index.ts"
LICENCE_FILE="$PKG_ROOT/LICENCE-ic_ui_kit.md"
HEADER_MARKER="CIANCHOSAINT wholesale-copy of mi6/ic-ui-kit"

FAIL=0

echo "=== cianchosaint:ic-ui-kit:smoke ==="
echo "repo_root:  $REPO_ROOT"
echo "pkg_root:   $PKG_ROOT"

step() {
  local label="$1"
  local cmd="$2"
  echo -n "  $label: "
  if eval "$cmd" > /tmp/ic_ui_kit_smoke.$$ 2>&1; then
    echo "OK ($(cat /tmp/ic_ui_kit_smoke.$$ | head -1))"
  else
    echo "FAIL"
    cat /tmp/ic_ui_kit_smoke.$$ >&2
    FAIL=1
  fi
  rm -f /tmp/ic_ui_kit_smoke.$$
}

# 1) wholesale-copy directories exist
[ -d "$IC_WC" ] || { echo "FAIL: missing $IC_WC" >&2; FAIL=1; }
[ -d "$IC_REACT" ] || { echo "FAIL: missing $IC_REACT" >&2; FAIL=1; }

# 2) ≥60 ic-* component directories wholesale-copied
WC_COUNT="$(find "$IC_WC" -maxdepth 1 -mindepth 1 -type d -name 'ic-*' 2>/dev/null | wc -l | tr -d ' ')"
if [ "$WC_COUNT" -ge 60 ]; then
  echo "  ic-* component dirs wholesale-copied: OK ($WC_COUNT)"
else
  echo "FAIL: only $WC_COUNT ic-* wholesale-copied component dirs (expected >= 60)" >&2
  FAIL=1
fi

# 3) index.ts present
[ -f "$INDEX_TS" ] && echo "  src/index.ts: OK" || { echo "FAIL: missing $INDEX_TS" >&2; FAIL=1; }

# 4) LICENCE-ic_ui_kit.md attribution present
[ -f "$LICENCE_FILE" ] && echo "  LICENCE-ic_ui_kit.md: OK" || { echo "FAIL: missing $LICENCE_FILE" >&2; FAIL=1; }

# 5) Wholesale-copied .ts/.tsx files all have the licence attribution header
MISSING_HEADER_COUNT="$(python3 - <<PY
import os
marker = "$HEADER_MARKER"
count = 0
for root in ("$IC_WC", "$IC_REACT"):
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if not (filename.endswith(".ts") or filename.endswith(".tsx")):
                continue
            if filename.endswith(".d.ts"):
                continue
            full_path = os.path.join(dirpath, filename)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    head = f.read(2048)
            except (UnicodeDecodeError, OSError):
                continue
            if marker not in head:
                count += 1
print(count)
PY
)"
if [ "$MISSING_HEADER_COUNT" -eq 0 ]; then
  echo "  wholesale-copy headers: OK (every .ts/.tsx has the CIANCHOSAINT attribution)"
else
  echo "FAIL: $MISSING_HEADER_COUNT wholesale-copied .ts/.tsx files missing the licence attribution header" >&2
  FAIL=1
fi

# 6) The 9 ciafagent integration wrappers exist
EXPECTED_WRAPPERS=(
  "ic-ic-classification-banner"
  "ic-ic-top-navigation"
  "ic-ic-search-bar"
  "ic-ic-data-table"
  "ic-ic-tab-group"
  "ic-ic-drawer"
  "ic-ic-card-vertical"
  "ic-ic-footer"
  "ic-privacy-disclaimer"
)
for wrapper in "${EXPECTED_WRAPPERS[@]}"; do
  if [ -f "$PKG_ROOT/src/${wrapper}.tsx" ]; then
    echo "  wrapper $wrapper.tsx: OK"
  else
    echo "FAIL: missing ciafagent integration wrapper $wrapper.tsx" >&2
    FAIL=1
  fi
done

if [ "$FAIL" -eq 0 ]; then
  echo "=== cianchosaint:ic-ui-kit:smoke PASS ==="
  exit 0
else
  echo "=== cianchosaint:ic-ui-kit:smoke FAIL ===" >&2
  exit 1
fi
