# `cianchosaint-reform-uk-pilot-workflow` — Agent Routing

> `cianchosaint-reform-uk-pilot-workflow` is the capability that provides the Reform UK pilot investigation dossier — the FIRST case-study pilot in cianchosaint (per Q12 = B + the locked plan).

## Routing

Load this AGENTS.md when the parent spec (`./spec.md`) is in scope.
Use it to find the most relevant mise tasks + skills + adjacent files
without re-reading the full spec.

## Quick start

```bash
# 1. Validate the Reform UK pilot workflow spec
openspec validate cianchosaint-reform-uk-pilot-workflow --strict

# 2. Inspect the pilot FunctionTool
python3.13 -c "import ast; ast.parse(open('agents/cianchosaint/tools/reform_uk_pilot.py').read())"

# 3. Invoke the pilot from the per-persona agent
# (the ciafagent-ga-public web app calls reform_uk_pilot_tool with
#  target_entity='Richard Tice', focus='2024 election debt fraud')

# 4. Verify the OSINT allowlist covers every input source URL
mise run lint:license
```

## Key sources

- `openspec/specs/cianchosaint-reform-uk-pilot-workflow/spec.md` — the canonical spec
- `agents/cianchosaint/tools/reform_uk_pilot.py` ⭐ — the canonical pilot FunctionTool
- `baml_src/cianchosaint/politics/reform_uk_pilot_extraction.baml` ⭐ — the BAML extraction function + schema
- `docs/case-study/reform-uk-pilot.md` ⭐ — the canonical case-study narrative
- `dlt_sources/cianchosaint/political_parties/uk/reform_uk.py` — the upstream Reform UK DLT source (Change 4)
- `dlt_sources/cianchosaint/uk/intelligence_oversight/investigatory_powers_bill_evidence.py` — the upstream IPB evidence DLT source (Change 3)
- `baml_src/clients.baml` — the 4-tier provider chain (`Primary` / `Fallback` / `Emergency` / `Gemini`)

## Adjacent specs

- `openspec/specs/cianchosaint-political-party-pipeline/spec.md` — upstream (Change 4)
- `openspec/specs/cianchosaint-intelligence-agency-pipeline/spec.md` — upstream (Change 3)
- `openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md` — companion (Change 3)
- `openspec/specs/cianchosaint-per-constituency-agents/spec.md` — downstream consumer (the per-persona agents)

## DO NOT

- Directly submit forms to operational systems (Companies House webhooks, ICO complaint forms, etc.) — the pilot is for analyst review ONLY.
- Bypass the OSINT allowlist check under any circumstances.
- Expand to multi-entity or cross-jurisdiction dossiers without an explicit follow-up openspec change (per the locked plan Q12 = B, the v1 pilot is SINGLE entity + SINGLE focus).
- Treat the leabharlann PDFs as authoritative factual sources — they are read-only context for the `source_pdf_urls` field of the dossier.

## Skill pointers

- `ccc` — for semantic code search across the 24 party DLT sources + the 5 intelligence agency DLT sources
- `openspec` — for the spec change workflow
- `motherduck` — for the storage layer (uses `md:cianchosaint`)
- `baml` — for the BAML extraction schemas + the 4-tier provider chain
- `secrets-management` — for the Infisical + Locket contract

<!-- generated: 2026-08-23; do not hand-edit -->
