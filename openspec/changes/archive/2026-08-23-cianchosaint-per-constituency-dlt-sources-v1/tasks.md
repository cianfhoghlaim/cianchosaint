# Tasks: cianchosaint-per-constituency-dlt-sources-v1

## 0. Pre-flight

- [ ] Verify `cianchosaint-repo-bootstrap-v2` is archived (it is, as of `f8c72d5`)
- [ ] Verify openspec CLI: `openspec --version` (expected 1.4.1)

## 1. OpenSpec artifacts

- [ ] Author `openspec/changes/cianchosaint-per-constituency-dlt-sources-v1/proposal.md` (this file's purpose) — DONE
- [ ] Author `openspec/changes/cianchosaint-per-constituency-dlt-sources-v1/tasks.md` (this file) — DONE
- [ ] Author `openspec/changes/cianchosaint-per-constituency-dlt-sources-v1/cross-repo-sync.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-per-constituency-dlt-sources-v1/specs/cianchosaint-per-constituency-dlt-sources/spec.md` (the ADDED Requirements delta) — DONE
- [ ] Author `openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md` (canonical END-STATE spec) — DONE
- [ ] Author `openspec/specs/cianchosaint-per-constituency-dlt-sources/AGENTS.md` (per-spec routing) — DONE

## 2. Validation gates

- [ ] Run `openspec validate cianchosaint-per-constituency-dlt-sources-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-per-constituency-dlt-sources --strict` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL pass

## 3. Implementation: ~30 DLT source files

### UK Policing (5 files at `dlt_sources/cianchosaint/uk/policing/`)
- [ ] `data_police_uk.py` — 43 UK forces via `data.police.uk` API
- [ ] `metropolitan_police_press_releases.py` — MET press releases from `met.police.uk`
- [ ] `stop_and_search_uk.py` — stop & search records
- [ ] `crime_statistics_uk.py` — force-level crime statistics
- [ ] `police_workforce_uk.py` — force-level workforce statistics

### NI Policing (3 files at `dlt_sources/cianchosaint/ni/`)
- [ ] `psni_press_releases.py` — PSNI press releases from `psni.police.uk`
- [ ] `justice_ni.py` — NI Department of Justice
- [ ] `policing_board_ni.py` — NI Policing Board oversight reports

### UK Military (6 files at `dlt_sources/cianchosaint/uk/military/`)
- [ ] `mod_press_releases.py` — UK MoD corporate press releases from `gov.uk/government/organisations/ministry-of-defence`
- [ ] `raf_press_releases.py` — Royal Air Force press releases from `raf.mod.uk`
- [ ] `royal_navy_press_releases.py` — Royal Navy press releases from `royalnavy.mod.uk`
- [ ] `british_army_press_releases.py` — British Army press releases from `army.mod.uk`
- [ ] `jsp_doctrine.py` — Joint Service Publications (JSP) from `gov.uk/government/collections/jsp-`
- [ ] `jdp_doctrine.py` — Joint Doctrine Publications (JDP) from `gov.uk/government/collections/jdp-`

### Ireland Defence (2 files at `dlt_sources/cianchosaint/ireland/defence_forces/`)
- [ ] `idf_press_releases.py` — Defence Forces of Ireland press releases from `defence.ie`
- [ ] `idf_white_paper.py` — White Paper on Defence from `defence.ie`

### Crown Dependencies (3 files at `dlt_sources/cianchosaint/crown_dependencies/`)
- [ ] `jersey_policing.py` — States of Jersey Police from `police.je`
- [ ] `guernsey_policing.py` — Bailiwick of Guernsey Police from `guernseypolice.com`
- [ ] `isle_of_man_policing.py` — Isle of Man Constabulary from `iompolice.im`

### Intelligence Oversight (4 files at `dlt_sources/cianchosaint/uk/intelligence_oversight/`)
- [ ] `isc_annual_reports.py` — Intelligence and Security Committee annual reports from `isc.independent.gov.uk`
- [ ] `ipco_reports.py` — Investigatory Powers Commissioner reports from `ipco.org.uk`
- [ ] `ipt_decisions.py` — Investigatory Powers Tribunal decisions from `investigatorypowerstribunal.org.uk`
- [ ] `investigatory_powers_bill_evidence.py` — Investigatory Powers Bill evidence submissions

### UK Government (3 files at `dlt_sources/cianchosaint/uk/government/`)
- [ ] `nca_threat_assessments.py` — National Crime Agency threat assessments
- [ ] `home_office_statistics.py` — Home Office statistical bulletins
- [ ] `moj_statistics.py` — Ministry of Justice statistics

### Each file pattern:
```python
"""<Source name> — <jurisdiction> <vertical> DLT source.

Per the openspec/changes/cianchosaint-per-constituency-dlt-sources-v1/
specs/cianchosaint-per-constituency-dlt-sources/spec.md, Requirement:
The per-constituency DLT source manifest.

Sources data from <URL> via <method>.
Per the cianchosaint OSINT allowlist (dlt_sources/cianchosaint/common/
osint_allowlist.yaml), this source falls within the British Isles
public-sector OSINT ceiling.

The wholesale-copied cianchosaint DLT common helpers (per the
cianchosaint-repo-bootstrap-v2 change, Phase 3.1) provide:
- destinations_cianchosaint.py (the md:cianchosaint destination factory)
- endpoint_recovery.py (URL allowlist helpers)
- observability.py (structlog + Langfuse)
- safety.py (input validation)
"""
from __future__ import annotations
import dlt
from dlt.common.typing import TDataItems
from dlt_sources.common.destinations_cianchosaint import get_dlt_destination
from dlt_sources.common.observability import get_logger

logger = get_logger(__name__)

SOURCE_BASE = "<URL>"

@dlt.resource(name="<resource_name>", write_disposition="replace")
def <resource_name>(...) -> TDataItems:
    """<Description>."""
    # ... implementation

@dlt.source(name="<source_name>")
def <source_name>(...) -> list:
    return [<resource_name>(...), ...]
```

## 4. CI gates + commit + push

- [ ] Run `mise run lint:license` and verify exit code 0 (every new URL is in the OSINT allowlist)
- [ ] Run `python3 -c "import ast; ast.parse(open('dlt_sources/cianchosaint/uk/policing/data_police_uk.py').read())"` and verify Python 3.13 syntax
- [ ] Run `openspec validate --all --strict` and verify ALL pass
- [ ] Commit on `cianchosaint:main` with message: `feat(dlt): per-constituency DLT sources (Phase Q1 — UK + NI + Crown Dependencies + military + intel oversight)`
- [ ] Push to `github.com/cianfhoghlaim/cianchosaint`
- [ ] Archive `cianchosaint-per-constituency-dlt-sources-v1` after all validations pass

## 5. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-baml-schemas-v1` — the 12 BAML extraction functions for these DLT sources
- [ ] `cianchosaint-cocoindex-flows-v1` — the CocoIndex flows that consume these DLT sources
- [ ] `cianchosaint-source-catalogue-v1` — the British Isles source catalogue (document-only) that documents every source
