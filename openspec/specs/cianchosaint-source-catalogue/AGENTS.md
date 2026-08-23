# `cianchosaint-source-catalogue` — Agent Routing

> `cianchosaint-source-catalogue` is the capability that provides the canonical catalogue of British Isles public-sector bodies at `docs/source-catalogue/`. Covers the 12 UK intelligence + oversight bodies, the 45 UK police forces, the 2 ROI police forces, the 3 Crown Dependencies forces, the UK + Irish armed forces, the 12 UK + devolved + Crown Dependencies departments, the 12 court systems, the 24 political parties, and the ~15 other bodies (ICO / NAO / C&AG / HoC Library / Senedd / Electoral Commission).

## Routing

Load this AGENTS.md when an operator asks "which bodies does
cianchosaint cover?", "what is the URL for body X?", "is body Y
wired?", or "what gaps remain?".

## Quick start

```bash
# 1. Read the master catalogue
xdg-open docs/source-catalogue/README.md     # or: open docs/source-catalogue/README.md

# 2. Validate the umbrella spec
openspec validate cianchosaint-source-catalogue --strict

# 3. Verify the catalogue's numbers match ground truth
mise run lint:drift-docs

# 4. Verify the catalogue's URL claims match the OSINT allowlist
mise run lint:license

# 5. Check which bodies are NOT yet wired (the gap inventory)
ls docs/source-catalogue/*.md | xargs grep -l 'NOT YET WIRED'
```

## Key sources

- `docs/source-catalogue/README.md` — the master catalogue
- `docs/source-catalogue/01..10-*.md` — the 10 topic files
- `LICENSE.md` (repo root) — the load-bearing legal document (BUSL-1.1 — British Isles bodies only)
- `AGENTS.md` (repo root) — the canonical agent routing
- `openspec/AGENTS.md` — the openspec workflow
- `dlt_sources/cianchosaint/common/osint_allowlist.yaml` — the OSINT allowlist

## Adjacent specs

- `openspec/specs/cianchosaint-pipeline/spec.md` — the data pipeline umbrella
- `openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md` — the per-constituency DLT sources
- `openspec/specs/cianchosaint-intelligence-agency-pipeline/spec.md` — the intelligence agency pipeline
- `openspec/specs/cianchosaint-political-party-pipeline/spec.md` — the political party pipeline

## DO NOT

- Add a body from outside the British Isles — the BUSL-1.1 licence explicitly bans them
- Add a body without an `**OSINT allowlist**` field — `mise run lint:license` will fail CI
- Add a body without a `## Gaps` annotation if the DLT source is `NOT YET WIRED`
- Edit `dlt_sources/cianchosaint/common/osint_allowlist.yaml` directly — use `mise run lint:license` + the allowlist curator
- Bypass the openspec validation gate — `openspec validate --strict` MUST pass before commit

## Skill pointers

- `ccc` — for semantic code search across the catalogue + the registries
- `openspec` — for the spec change workflow
- `motherduck` — for the storage layer
- `firecrawl` — for live web scraping of OSINT sources

<!-- generated: 2026-08-23; do not hand-edit -->
