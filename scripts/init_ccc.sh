#!/usr/bin/env bash
# cianchosaint — `scripts/init_ccc.sh`
#
# Original (this file): new-build by Cian Mhac An Deisigh on 2026-08-23
# Licence: BUSL-1.1 (CIANCHOSAINT edition, per LICENSE.md)
#
# This file is part of cianchosaint (the British Isles defence / policing /
# intelligence-oversight open-source data platform). See LICENSE.md for
# the full Additional Use Grant + the 3-step foreign-use gate + the
# warrant-to-enforce clause.
#
# First-time CCC (CocoIndex Code) setup for the cianchosaint repo.
# Creates the per-project semantic index at .cocoindex_code/ for the
# ccc CLI to consume. Idempotent — safe to run multiple times.
#
# Usage:
#   bash scripts/init_ccc.sh
#   # or
#   mise run ccc:init

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CCC_DIR="${REPO_ROOT}/.cocoindex_code"

if [[ ! -d "${CCC_DIR}" ]]; then
  echo "FAIL: ${CCC_DIR} does not exist; settings.yml + guides.yml must be in place first" >&2
  exit 1
fi

if [[ ! -f "${CCC_DIR}/settings.yml" ]]; then
  echo "FAIL: ${CCC_DIR}/settings.yml missing — copy from cianfhoghlaim reference first" >&2
  exit 1
fi

if [[ ! -f "${CCC_DIR}/guides.yml" ]]; then
  echo "FAIL: ${CCC_DIR}/guides.yml missing — copy from cianfhoghlaim reference first" >&2
  exit 1
fi

echo "cianchosaint — initialising CCC semantic index..."
echo "  settings.yml: ${CCC_DIR}/settings.yml"
echo "  guides.yml:   ${CCC_DIR}/guides.yml (12 guides)"

# The ccc CLI is invoked through bun (per the cianfhoghlaim mise.toml convention).
# Falls back to a direct ccc invocation if bun is unavailable.
if command -v bun >/dev/null 2>&1; then
  bun run ccc:init
else
  if command -v ccc >/dev/null 2>&1; then
    ccc init
  else
    echo "FAIL: neither 'bun' nor 'ccc' is on PATH; install bun first (mise install)" >&2
    exit 1
  fi
fi

echo "OK: CCC initialised at ${CCC_DIR}"
echo "    next: bash scripts/lint_ccc_freshness.sh   # verify the index is fresh"
echo "    next: bun run ccc:search '<query>'         # semantic search"