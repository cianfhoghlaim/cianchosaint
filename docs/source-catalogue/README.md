# CIANCHOSAINT British Isles Source Catalogue

> Per the [`openspec/changes/cianchosaint-british-isles-source-catalogue-v1/`](../../openspec/changes/cianchosaint-british-isles-source-catalogue-v1/specs/cianchosaint-source-catalogue/spec.md) spec.
>
> **Audience:** operators onboarding to cianchosaint, analysts
> building per-constituency agents, the OSINT allowlist curator.
>
> **Scope:** every British Isles public-sector body that cianchosaint
> ingests from or could ingest from, organised into 10 topical files.

## Overview

This catalogue is the canonical reference for the **bodies** (not the
source files) that cianchosaint relates to. The bodies are organised
into 10 topics:

| # | File | Topic | Bodies covered |
|--:|:--|:--|--:|
| 01 | [`01-intelligence-agencies.md`](01-intelligence-agencies.md) | UK intelligence agencies + oversight bodies | 12 |
| 02 | [`02-police-forces-uk.md`](02-police-forces-uk.md) | UK police forces (England + Wales + Scotland) | 45 |
| 03 | [`03-police-forces-ireland.md`](03-police-forces-ireland.md) | Republic of Ireland + Northern Ireland police | 2 |
| 04 | [`04-police-forces-crown-dependencies.md`](04-police-forces-crown-dependencies.md) | Crown Dependencies police forces | 3 |
| 05 | [`05-armed-forces-uk.md`](05-armed-forces-uk.md) | UK MoD + RAF + Royal Navy + British Army | 4 |
| 06 | [`06-armed-forces-ireland.md`](06-armed-forces-ireland.md) | Defence Forces of Ireland | 1 |
| 07 | [`07-key-government-departments.md`](07-key-government-departments.md) | UK + devolved + Crown Dependencies departments | 12 |
| 08 | [`08-courts-and-tribunals.md`](08-courts-and-tribunals.md) | UK + ROI + NI + Scotland + Crown Dependencies courts | 12 |
| 09 | [`09-political-parties.md`](09-political-parties.md) | Active political parties in the OSINT allowlist | 24 |
| 10 | [`10-other-bodies.md`](10-other-bodies.md) | ICO, NAO, C&AG, HoC Library, Senedd, Electoral Commission, etc. | 15 |
| | | **Total** | **~130** |

## How to use this catalogue

### Per-body schema

Every body in this catalogue uses the same 6-field schema:

```markdown
### <Body Name>
- **URL**: <the body's canonical website>
- **DLT source**: <path to the DLT source file or "NOT YET WIRED">
- **OSINT allowlist**: <yes / no>
- **Coverage**: <what the source provides>
- **Update cadence**: <daily / weekly / monthly / on-publication>
- **Notes**: <any caveats>
```

### Where to look

| If you want to... | Look at... |
|:--|:--|
| Find the URL for body X | the `### <Body Name>` heading in the relevant topic file |
| Find which bodies have a DLT source wired | `**DLT source**: dlt_sources/...` (vs `NOT YET WIRED`) |
| Find which bodies are NOT yet wired | the `## Gaps` section at the bottom of each topic file |
| Audit the OSINT allowlist | `dlt_sources/cianchosaint/common/osint_allowlist.yaml` |
| Find the per-constituency cohort | `_cross/per_constituency_cohort_registry.py` (26 cohorts) |
| Find the per-party cohort | `political_parties/_registry.py` (38 cohorts / 24 parties) |

## Cross-cutting references

- **OSINT allowlist**: [`../../dlt_sources/cianchosaint/common/osint_allowlist.yaml`](../../dlt_sources/cianchosaint/common/osint_allowlist.yaml)
  — the canonical URL list. Every DLT source URL MUST appear here.
- **Per-constituency cohort registry**:
  [`../../dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`](../../dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py)
  — the 26 (jurisdiction × vertical × source) tuples.
- **Per-political-party registry**:
  [`../../dlt_sources/cianchosaint/political_parties/_registry.py`](../../dlt_sources/cianchosaint/political_parties/_registry.py)
  — the 38 (party × jurisdiction) tuples.
- **Intelligence-agency DLT sources**:
  [`../../dlt_sources/cianchosaint/uk/intelligence_agencies/`](../../dlt_sources/cianchosaint/uk/intelligence_agencies/)
  — the 5 UK intelligence agencies.
- **Per-persona agents**:
  [`../../agents/cianchosaint/`](../../agents/cianchosaint/) — the 24-agent Google ADK fleet.
- **Canonical openspec spec**:
  [`../../openspec/specs/cianchosaint-source-catalogue/spec.md`](../../openspec/specs/cianchosaint-source-catalogue/spec.md)

## Licence ceiling

Per `LICENSE.md` (BUSL-1.1 v2 — the CIANCHOSAINT edition), the catalogue
covers **only British Isles public-sector bodies** (UK + ROI + NI +
Crown Dependencies). Foreign bodies (FBI / CIA / BND / DGSE / etc.)
are explicitly BANNED and MUST NOT be added to this catalogue or to the
OSINT allowlist. `mise run lint:license` enforces this constraint.

## Gap summary

Across all 10 topic files, the NOT YET WIRED bodies are:

- Most of `10-other-bodies.md` (NAO / C&AG / HoC Library / Senedd /
  Electoral Commission / IPSO / etc. — 15 bodies total, ~12 NOT YET WIRED)
- The devolved legislature + audit bodies in `07-key-government-departments.md`
  (Northern Ireland Assembly + Senedd + Holyrood + Jersey + Guernsey +
  IoM legislatures — 6 bodies, ~4 NOT YET WIRED)
- The doctrine series (JSP / JDP / AP / BR) — 4 series, NOT YET WIRED
- Several court systems in `08-courts-and-tribunals.md` (UK Tribunals,
  SCTS, NICTS, Jersey + Guernsey + IoM courts — 6 systems, 4 NOT YET WIRED)

Each gap has a `## Gaps` section in its topic file with the proposed
follow-up openspec change to close it.
