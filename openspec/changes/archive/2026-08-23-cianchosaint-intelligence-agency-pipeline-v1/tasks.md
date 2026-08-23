# Tasks: cianchosaint-intelligence-agency-pipeline-v1

## 0. Pre-flight

- [ ] Verify `cianchosaint-repo-bootstrap-v2` is archived (it is)
- [ ] Verify `cianchosaint-per-constituency-dlt-sources-v1` is committed (it is, as `01f6eb6`)

## 1. OpenSpec artifacts

- [ ] Author `openspec/changes/cianchosaint-intelligence-agency-pipeline-v1/proposal.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-intelligence-agency-pipeline-v1/tasks.md` (this file) — DONE
- [ ] Author `openspec/changes/cianchosaint-intelligence-agency-pipeline-v1/cross-repo-sync.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-intelligence-agency-pipeline-v1/specs/cianchosaint-intelligence-agency-pipeline/spec.md` (the 2 ADDED Requirements delta) — DONE
- [ ] Author `openspec/specs/cianchosaint-intelligence-agency-pipeline/spec.md` (canonical END-STATE spec) — DONE
- [ ] Author `openspec/specs/cianchosaint-intelligence-agency-pipeline/AGENTS.md` (per-spec routing) — DONE

## 2. Validation gates

- [ ] Run `openspec validate cianchosaint-intelligence-agency-pipeline-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-intelligence-agency-pipeline --strict` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL pass

## 3. Implementation: 5 UK intelligence agency DLT sources

### Pipeline base (3 files at `dlt_sources/cianchosaint/uk/intelligence_agencies/`)
- [ ] `_base.py` — the `IntelligenceAgencyPipelineBase` class
- [ ] `_registry.py` — the cohort registry
- [ ] `__init__.py`

### The 5 intelligence agencies
- [ ] `mi5.py` — MI5 (Security Service) public-facing content
- [ ] `mi6.py` — MI6 (Secret Intelligence Service) public-facing content
- [ ] `gchq.py` — GCHQ (Government Communications Headquarters) public-facing content
- [ ] `defence_intelligence.py` — Defence Intelligence (DI) public-facing content
- [ ] `hmgcc_rolling_window.py` — HMGCC rolling window (extends the wholesale-copied `official_media_cianchosaint/hmgcc/rolling_window.py`)

### OSINT allowlist extension
- [ ] Extend `dlt_sources/cianchosaint/common/osint_allowlist.yaml` with 5 per-agency source URLs

## 4. Per-file pattern

```python
"""MI5 (Security Service) intelligence agency DLT source.

Per the openspec/changes/cianchosaint-intelligence-agency-pipeline-v1/
specs/cianchosaint-intelligence-agency-pipeline/spec.md.

MI5 is the UK's domestic counter-intelligence and security agency.
Public-facing content is necessarily limited — this pipeline sources
from:
- The official website (https://www.mi5.gov.uk/)
- Public annual reports (sparingly published)
- Public statements / press releases
- Recruitment notices (a key signal of MI5's capability priorities)

Companion to cianchosaint-per-constituency-dlt-sources-v1 Change 3
which ships the intelligence OVERSIGHT ecosystem (ISC + IPCO + IPT +
IPB). Together they form the canonical British Isles intelligence
ecosystem pipeline.

Per the cianchosaint OSINT allowlist, this source falls within the
British Isles public-sector OSINT ceiling.
"""
from __future__ import annotations

import dlt
from dlt.common.typing import TDataItems
from dlt_sources.common.destinations_cianchosaint import get_dlt_destination
from dlt_sources.common.observability import get_logger
from dlt_sources.cianchosaint.uk.intelligence_agencies._base import IntelligenceAgencyPipelineBase

logger = get_logger(__name__)


class MI5Pipeline(IntelligenceAgencyPipelineBase):
    """MI5 (Security Service) intelligence agency pipeline."""
    
    AGENCY_ID = "mi5"
    AGENCY_NAME = "MI5 (Security Service)"
    SOURCE_BASE = "https://www.mi5.gov.uk/"
    
    @dlt.resource(name="mi5_public_statements", write_disposition="replace")
    def public_statements(self) -> TDataItems:
        """MI5 public statements (annual reports + press releases)."""
        yield {
            "title": "...",
            "published_at": "...",
            "source_url": f"{self.SOURCE_BASE}/news/...",
            "agency_id": self.AGENCY_ID,
        }


@dlt.source(name="mi5")
def mi5_source() -> list:
    pipeline = MI5Pipeline()
    return [pipeline.public_statements()]
```

## 5. CI gates + commit + push

- [ ] Run `mise run lint:license` and verify exit code 0
- [ ] Run `python3.13 -c "import ast; ast.parse(open('dlt_sources/cianchosaint/uk/intelligence_agencies/mi5.py').read())"` and verify
- [ ] Run `openspec validate --all --strict` and verify ALL pass
- [ ] Commit on `cianchosaint:main` with message: `feat(intelligence-agencies): 5 UK intelligence agency DLT sources (Change 5)`
- [ ] Push to `github.com/cianfhoghlaim/cianchosaint`
- [ ] Archive `cianchosaint-intelligence-agency-pipeline-v1` after Change 3 + Change 4 have also been archived

## 6. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-baml-schemas-v1` — the BAML extraction functions
- [ ] `cianchosaint-cocoindex-flows-v1` — the CocoIndex flows
- [ ] `cianchosaint-reform-uk-pilot-workflow-v1` — the Reform UK pilot case study (Change 7)
