# AGENTS.md — cianchosaint-baml-schemas

## Routing

Per-vertical BAML extraction schemas for the 7 Q3 verticals.
Authored by `cianchosaint-baml-schemas-v1`.

## Quick start

```bash
# Inspect the 4-tier client chain (wholesale-copied from Cianfhoghlaim)
head -90 baml_src/clients.baml

# Validate the 8 NEW BAML files
openspec validate cianchosaint-baml-schemas-v1 --strict

# Re-run the BAML runtime (requires baml-cli)
baml-cli validate baml_src/cianchosaint/
```

## Key sources

- `baml_src/clients.baml` — the canonical 4-tier client chain
- `baml_src/cianchosaint/processing/` — 6 NEW BAML files
- `baml_src/cianchosaint/political_parties/political_party_extraction.baml` — shared
- `baml_src/cianchosaint/politics/reform_uk_dossier_extraction.baml` — pilot

## Adjacent specs

- `cianchosaint-bootstrap-v2` — the wholesale-copy umbrella
- `cianchosaint-pipeline` — the pipeline umbrella
- `cianchosaint-source-catalogue` — the 17-domain catalogue
- `cianchosaint-reform-uk-pilot-workflow` — uses `ExtractReformUkDossier`

## DO NOT

- DO NOT introduce new BAML clients outside the 4-tier chain.
- DO NOT omit the conservative-posture fields
  (`osint_ceiling_enforced` / `licence_posture` / `analyst_review_required`).
- DO NOT cite source URLs that are NOT on the OSINT allowlist.

## Skill pointers

- `.agents/skills/baml/SKILL.md` — BAML schema authoring
