# Tasks: cianchosaint-political-party-pipeline-v1

## 0. Pre-flight

- [ ] Verify `cianchosaint-repo-bootstrap-v2` is archived (it is)
- [ ] Verify `cianchosaint-per-constituency-dlt-sources-v1` is committed (it is, as `01f6eb6`)

## 1. OpenSpec artifacts

- [ ] Author `openspec/changes/cianchosaint-political-party-pipeline-v1/proposal.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-political-party-pipeline-v1/tasks.md` (this file) — DONE
- [ ] Author `openspec/changes/cianchosaint-political-party-pipeline-v1/cross-repo-sync.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-political-party-pipeline-v1/specs/cianchosaint-political-party-pipeline/spec.md` (the 3 ADDED Requirements delta) — DONE
- [ ] Author `openspec/specs/cianchosaint-political-party-pipeline/spec.md` (canonical END-STATE spec) — DONE
- [ ] Author `openspec/specs/cianchosaint-political-party-pipeline/AGENTS.md` (per-spec routing) — DONE

## 2. Validation gates

- [ ] Run `openspec validate cianchosaint-political-party-pipeline-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-political-party-pipeline --strict` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL pass

## 3. Implementation: 24 political party DLT sources

### Pipeline base (1 file at `dlt_sources/cianchosaint/political_parties/`)
- [ ] `_base.py` — the `PoliticalPartyPipelineBase` class
- [ ] `_registry.py` — the per-party cohort registry
- [ ] `__init__.py`

### UK HoC (7 parties at `dlt_sources/cianchosaint/political_parties/uk/`)
- [ ] `conservative_party_uk.py`
- [ ] `labour_party_uk.py`
- [ ] `liberal_democrats_uk.py`
- [ ] `reform_uk.py` ⭐ (the canonical Reform UK source — used by the reform-uk-pilot-workflow)
- [ ] `green_party_ew.py`
- [ ] `plaid_cymru.py`
- [ ] `snp.py` (shared UK HoC + Scotland Holyrood)

### ROI (12 parties at `dlt_sources/cianchosaint/political_parties/roi/`)
- [ ] `fianna_fail.py`
- [ ] `fine_gael.py`
- [ ] `sinn_fein_roi.py`
- [ ] `labour_roi.py`
- [ ] `social_democrats.py`
- [ ] `pbp_solidarity.py`
- [ ] `green_party_roi.py`
- [ ] `aontu.py`
- [ ] `independent_ireland.py`
- [ ] `irish_freedom_party.py`
- [ ] `national_party_roi.py`
- [ ] `rise_roi.py`

### NI Assembly (7 parties at `dlt_sources/cianchosaint/political_parties/ni/`)
- [ ] `dup.py`
- [ ] `sinn_fein_ni.py`
- [ ] `alliance_ni.py`
- [ ] `uup.py`
- [ ] `sdlp.py`
- [ ] `tuv_ni.py`
- [ ] `pbp_ni.py`

### Wales Senedd (5 parties at `dlt_sources/cianchosaint/political_parties/wales/`)
- [ ] `plaid_cymru_senedd.py`
- [ ] `labour_wales.py`
- [ ] `conservative_wales.py`
- [ ] `liberal_democrats_wales.py`
- [ ] `plaid_cymru_voice.py`

### Scotland Holyrood (5 parties at `dlt_sources/cianchosaint/political_parties/scotland/`)
- [ ] `snp_scottish.py`
- [ ] `scottish_labour.py`
- [ ] `scottish_conservatives.py`
- [ ] `scottish_liberal_democrats.py`
- [ ] `scottish_greens.py`

### Crown Dependencies (3 parties at `dlt_sources/cianchosaint/political_parties/crown_dependencies/`)
- [ ] `jersey_party.py`
- [ ] `guernsey_party.py`
- [ ] `iom_party.py`

### OSINT allowlist extension
- [ ] Extend `dlt_sources/official_media_cianchosaint/fixtures/allowlist_parties.yaml` with 24 per-party source URLs

## 4. Per-file pattern (PoliticalPartyPipelineBase usage)

```python
"""Reform UK political party DLT source.

Per the openspec/changes/cianchosaint-political-party-pipeline-v1/
specs/cianchosaint-political-party-pipeline/spec.md, Requirement:
The 24 per-party DLT source modules.

This is the canonical Reform UK source — used by the reform-uk-pilot-
workflow (per Q12 = B + the locked plan). It is the FIRST party source
authored in this change and serves as the PATTERN for the other 23.

Sources data from:
- Reform UK official website: https://www.reformparty.uk/news
- Reform UK Companies House filings: bulk data via data.police.uk-style
  bulk endpoints
- Reform UK Electoral Commission returns: bulk data via the Electoral
  Commission Register of Political Parties API

Per the cianchosaint OSINT allowlist (dlt_sources/cianchosaint/common/
osint_allowlist.yaml + dlt_sources/official_media_cianchosaint/fixtures/
allowlist_parties.yaml), this source falls within the British Isles
public-sector OSINT ceiling.
"""
from __future__ import annotations

import dlt
from dlt.common.typing import TDataItems
from dlt_sources.common.destinations_cianchosaint import get_dlt_destination
from dlt_sources.common.observability import get_logger
from dlt_sources.cianchosaint.political_parties._base import PoliticalPartyPipelineBase

logger = get_logger(__name__)


class ReformUKPipeline(PoliticalPartyPipelineBase):
    """Reform UK party pipeline.
    
    Canonical sources (per Q12 = B — Reform UK pilot case study):
    - https://www.reformparty.uk/news (press releases)
    - Companies House bulk data (donor analysis)
    - Electoral Commission returns (voting records)
    """
    
    PARTY_ID = "reform-uk"
    PARTY_NAME = "Reform UK"
    JURISDICTION = "uk_hoc"
    SOURCE_BASE = "https://www.reformparty.uk/news"
    ELECTORAL_COMMISSION_ID = "PP-12345"  # Reform UK's Electoral Commission ID
    
    @dlt.resource(name="reform_uk_press_releases", write_disposition="replace")
    def press_releases(self) -> TDataItems:
        """Reform UK press releases."""
        # ...
        yield {
            "title": "...",
            "published_at": "...",
            "source_url": "...",
            "electoral_commission_id": self.ELECTORAL_COMMISSION_ID,
        }


@dlt.source(name="reform_uk")
def reform_uk_source() -> list:
    pipeline = ReformUKPipeline()
    return [pipeline.press_releases()]
```

## 5. CI gates + commit + push

- [ ] Run `mise run lint:license` and verify exit code 0
- [ ] Run `python3.13 -c "import ast; ast.parse(open('dlt_sources/cianchosaint/political_parties/reform_uk.py').read())"` and verify
- [ ] Run `openspec validate --all --strict` and verify ALL pass
- [ ] Commit on `cianchosaint:main` with message: `feat(political-parties): 24-party pipeline + Reform UK pilot source (Change 4)`
- [ ] Push to `github.com/cianfhoghlaim/cianchosaint`
- [ ] Archive `cianchosaint-political-party-pipeline-v1` after the reform-uk-pilot-workflow (Change 7) has been authored

## 6. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-reform-uk-pilot-workflow-v1` — the Reform UK pilot case study (Change 7, per Q12 = B)
- [ ] `cianchosaint-baml-schemas-v1` — the 24-party BAML extraction (shared `ExtractPartyPressRelease` schema)
- [ ] `cianchosaint-cocoindex-flows-v1` — the CocoIndex flows that consume these party sources
