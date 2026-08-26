# cianchosaint — Architecture Overview (1-page)

> **Per the repo-hygiene-agent-routing spec**, this 1-page architecture overview is the entry point for the per-sister canonical spec at [`../openspec/specs/cianchosaint-architecture/spec.md`](../openspec/specs/cianchosaint-architecture/spec.md).

## What is cianchosaint?

**Cianchosaint** = Irish Gaelic "cian" (long/far/longing) + "chosaint" (defence/protection) → "distant defence / far protection". Mirrors *Cianfhoghlaim* = "cian" + "fhoghlaim" (learning).

**Scope (per `LICENSE.md`)**: OSINT-only British Isles defence / policing / intelligence-oversight data platform. Strictly restricted to public-sector bodies of the Republic of Ireland, the United Kingdom of Great Britain and Northern Ireland, the Crown Dependencies (Jersey, Guernsey, Isle of Man), and their respective defence, security, intelligence, and policing bodies. Foreign use requires satisfaction of the 3-step gate (Explain → Do us a favour → Maybe).

## Sister-repo position (per the multi-repo scaffold)

Per the `2026-08-24-dlt-sources-to-multi-repo-scaffold-v1` parent change, cianchosaint is the BI law-enforcement + civil protection sister repo:

| Repo | Owns |
|---|---|
| `cianfhoghlaim` | Cross-cutting hub (`common/`, `lakehouse/`, `jobs/`) + the BIEP flagship (`british_isles/_cross/`, `british_isles/ireland/education/`) |
| `tuatha` | BI Educational MMO — 8 NCCA subject agents + 40 per-subject tools + 3 educational + 4 BIEP hackathon + 1 media_intel pipeline |
| `ciandlithe` | BI legal-system vertical — courts + tribunals + regulators + ombudsmen + law societies + bar councils + legal-aid bodies + coroners + health-service complaints bodies + claimant-representation clinics |
| **`cianchosaint`** | **BI law-enforcement + civil protection vertical — defence forces + policing bodies + intelligence oversight + public inquiries + emergency services + NAO/C&AG reports** |
| `ciancheiltis` | Pure Irish-language datasets + non-educational Celtic-language pipelines (deferred — Phase 4) |

## The 6 cascade contracts (per parent change §15-§19)

1. **`dlt-sister-sync-reusable-workflow`** — `.github/workflows/dlt-sister-sync-call.yml` calls cianfhoghlaim's reusable workflow
2. **`cognee-twin-clusters`** — 6 cianchosaint_* Cognee clusters
3. **`dlt-nightly-mirror-merge`** — cianchosaint emits `_sister_refs/cianchosaint/...` diffs
4. **`dlt-destination-versioning-contract`** — pins `cianfhoghlaim >=<minor>,<<next-minor`
5. **`agent-observability-cianchosaint`** — `cianchosaint_*` Langfuse project + project-scoped API key
6. **`openspec-per-sister-sync`** — per-sister `openspec/AGENTS.md` + `openspec/specs/`

## Skeleton shape

```
cianchosaint/
├── pyproject.toml          # uv workspace member, depends on cianfhoghlaim (FUTURE)
├── mise.toml               # cianchosaint:<verb>:* task namespace
├── README.md
├── AGENTS.md
├── LICENSE.md              # BUSL-1.1
├── openspec/
│   ├── AGENTS.md           # per-repo openspec conventions
│   ├── specs/
│   │   ├── cianchosaint-architecture.md  # per-sister canonical spec (NEW)
│   │   ├── cianchosaint-bootstrap-v2/    # the bootstrap-v2 umbrella spec
│   │   └── ...
│   └── changes/
│       └── 2026-08-24-cianchosaint-init-v1/   # this init change
├── dlt_sources/
│   ├── _cross/             # JurisdictionPipelineBase re-export + cross-repo helpers
│   ├── common/             # 4 canonical helpers + the per-sister destinations_cianchosaint
│   ├── official_media_cianchosaint/   # the legacy media-intel sub-tree (HARD-ARCHIVED per consolidation)
│   └── cianchosaint/       # the BI law-enforcement + civil protection vertical
│       ├── ireland/        # An Garda Síochána + Defence Forces + Oireachtas + DoD + DoJ + DFA
│       ├── uk/             # Met Police + BTP + PSNI + MoD + RAF + RN + Army + Home Office + FCDO + MoJ + DoH
│       ├── ni/             # PSNI + NI Policing Board
│       ├── crown_dependencies/   # IoM Constabulary + States of Jersey Police + Guernsey Police
│       └── common/         # the per-sister OSINT allowlist
├── baml_src/               # the BAML extraction contracts (per-sister schemas)
├── orchestration/          # the Dagster asset groups
├── cocoindex_flows/        # the CocoIndex v1 Apps
├── notebooks/              # the per-jurisdiction marimo dives
├── ci/                     # the CI conventions README
└── docs/
    ├── AGENTS.md           # per-directory conventions
    └── architecture.md     # this file
```

## Cross-references

- [`../openspec/specs/cianchosaint-architecture/spec.md`](../openspec/specs/cianchosaint-architecture/spec.md) — the per-sister canonical spec
- [`../openspec/specs/cianchosaint-bootstrap-v2/spec.md`](../openspec/specs/cianchosaint-bootstrap-v2/spec.md) — the bootstrap-v2 umbrella spec
- [`../openspec/changes/2026-08-24-cianchosaint-init-v1/proposal.md`](../openspec/changes/2026-08-24-cianchosaint-init-v1/proposal.md) — the init change
- [`../openspec/AGENTS.md`](../openspec/AGENTS.md) — the per-repo openspec conventions
- [`../AGENTS.md`](../AGENTS.md) — the canonical agent routing
- [`../LICENSE.md`](../LICENSE.md) — the load-bearing legal document