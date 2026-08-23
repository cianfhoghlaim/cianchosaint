#!/usr/bin/env bash
# cianchosaint — `scripts/lint_ccc_freshness.sh`
#
# Original (this file): new-build by Cian Mhac An Deisigh on 2026-08-23
# Licence: BUSL-1.1 (CIANCHOSAINT edition, per LICENSE.md)
#
# This file is part of cianchosaint (the British Isles defence / policing /
# intelligence-oversight open-source data platform). See LICENSE.md for
# the full Additional Use Grant + the 3-step foreign-use gate + the
# warrant-to-enforce clause.
#
# CI gate for the CCC (CocoIndex Code) semantic index freshness.
# Exits 1 if the index is older than the threshold (default 7 days),
# 0 otherwise. Mirrors the cianfhoghlaim convention of validating the
# ccc index freshness in CI to keep semantic search results accurate.
#
# Usage:
#   bash scripts/lint_ccc_freshness.sh                 # default 7-day threshold
#   bash scripts/lint_ccc_freshness.sh --max-age-days=3 # override threshold

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CCC_DIR="${REPO_ROOT}/.cocoindex_code"
INDEX_DB="${CCC_DIR}/target_sqlite.db"
MAX_AGE_DAYS=7

for arg in "$@"; do
  case "${arg}" in
    --max-age-days=*)
      MAX_AGE_DAYS="${arg#*=}"
      ;;
    *)
      echo "FAIL: unknown argument ${arg}" >&2
      exit 1
      ;;
  esac
done

if [[ ! -f "${INDEX_DB}" ]]; then
  echo "FAIL: CCC index not found at ${INDEX_DB}; run scripts/init_ccc.sh first" >&2
  exit 1
fi

# Compute the age of the index in whole days.
INDEX_MTIME_EPOCH="$(stat -f %m "${INDEX_DB}" 2>/dev/null || stat -c %Y "${INDEX_DB}" 2>/dev/null || echo 0)"
NOW_EPOCH="$(date +%s)"
AGE_SECONDS=$((NOW_EPOCH - INDEX_MTIME_EPOCH))
AGE_DAYS=$((AGE_SECONDS / 86400))

if (( AGE_DAYS > MAX_AGE_DAYS )); then
  echo "FAIL: CCC index is ${AGE_DAYS} days old (threshold: ${MAX_AGE_DAYS} days)" >&2
  echo "      rebuild with: bun run ccc:index" >&2
  exit 1
fi

echo "OK: CCC index is ${AGE_DAYS} day(s) old (threshold: ${MAX_AGE_DAYS} days)"