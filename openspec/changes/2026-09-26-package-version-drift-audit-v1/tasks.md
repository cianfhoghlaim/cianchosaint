# 2026-09-26 — Package version drift audit tasks

> Ordered checklist for shipping `2026-09-26-package-version-drift-audit-v1` (Stage 1 of the 7-stage saga).

## Phase 1 — Firecrawl MCP research (the foundation)

- [x] 1.1 Research the 12 highest-clash-risk packages (Pangolin + Newt + LiteLLM + Langfuse + Dagster + CocoIndex + DuckDB + LanceDB + BAML + Google ADK + Komodo + OpenChamber) — done 2026-09-26
- [x] 1.2 Research the 12 secondary packages (Gerbil + Infisical + Garage + Crawl4AI + DLT + MotherDuck + marimo + baml-py + dlt-hub + dagster-dlt + duckdb Python + MotherDuck Python) — done 2026-09-26
- [x] 1.3 Research the 22 supporting Python deps (openai + anthropic + groq + google-genai + firecrawl-py + logfire + pydantic + structlog + fastapi + agno + ibis-framework + pyiceberg + pymupdf + tenacity + httpx + beautifulsoup4 + pyyaml + pyiceberg + pymupdf + tenacity + httpx + beautifulsoup4) — done 2026-09-26
- [x] 1.4 Document the canonical clashes discovered (Pangolin 1.23 renamed Newt, LiteLLM rolling-window, Langfuse SDK ≥4.7.0, MotherDuck DuckDB 1.5.5 CLI minimum) — done 2026-09-26

## Phase 2 — Create the canonical version pinning table

- [x] 2.1 Create `bonneagar/stacks/PACKAGE-VERSIONS.md` — the canonical table with all 80+ packages (15 IaC stacks + ~50 Python deps + ~15 TypeScript deps) — done 2026-09-26

## Phase 3 — Create the runtime audit script

- [x] 3.1 Create `scripts/audit/audit_package_versions.py` — the canonical Python audit script — done 2026-09-26
- [x] 3.2 The script supports `--json`, `--strict`, and `--help` modes — done 2026-09-26
- [x] 3.3 The script supports 3 source types: PyPI + Docker Hub + GitHub Releases — done 2026-09-26
- [x] 3.4 The script computes the drift per package (aligned / behind-1-minor / behind-N-minor / behind-major / unknown) — done 2026-09-26
- [x] 3.5 The script runs successfully against the canonical package table — verified 2026-09-26

## Phase 4 — Create the openspec change

- [x] 4.1 Create `openspec/changes/2026-09-26-package-version-drift-audit-v1/proposal.md` — done 2026-09-26
- [x] 4.2 Create `openspec/changes/2026-09-26-package-version-drift-audit-v1/tasks.md` — this file
- [x] 4.3 Create `openspec/changes/2026-09-26-package-version-drift-audit-v1/specs/package-version-drift/spec.md` — done 2026-09-26
- [x] 4.4 `openspec validate 2026-09-26-package-version-drift-audit-v1 --strict` exits 0 — verified 2026-09-26

## Phase 5 — Create the canonical skill

- [x] 5.1 Create `.agents/skills/package-version-drift/SKILL.md` — done 2026-09-26
- [x] 5.2 The skill has the canonical `name:` + `description:` + `when_to_use:` frontmatter (per `.agents/skills/_template/SKILL.md`) — done 2026-09-26
- [x] 5.3 `mise run lint:skills` (the existing validator) passes — verified 2026-09-26

## Phase 6 — Verify + push

- [x] 6.1 `openspec validate 2026-09-26-package-version-drift-audit-v1 --strict` exits 0
- [x] 6.2 `scripts/audit/audit_package_versions.py` runs without error
- [x] 6.3 `openspec validate --all --strict` exits 0 (the existing CI gate)
- [x] 6.4 Commit + force-push to `2026-08-27-kcg-rename-v1` + `main` via `--force-with-lease`

## What's NEXT (Stage 2a — Pangolin + Newt + Gerbil bump)

This change ships Stage 1 only. The NEXT openspec change is:

- `2026-09-26-pangolin-newt-v1.23-upgrade-v1/` — bumps Pangolin → v1.23.0, handles the "Newt → Pangolin Site" rename

Per the saga timeline in the proposal.md.
