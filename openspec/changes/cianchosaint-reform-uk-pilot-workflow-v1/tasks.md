# Tasks: cianchosaint-reform-uk-pilot-workflow-v1

## 0. Pre-flight

- [x] Verify `cianchosaint-political-party-pipeline-v1` is archived (it is — 2026-08-23)
- [x] Verify `cianchosaint-intelligence-agency-pipeline-v1` is archived (it is — 2026-08-23)
- [x] Verify `cianchosaint-per-constituency-dlt-sources-v1` is archived (it is — 2026-08-23)
- [x] Verify the 2 input DLT sources exist on disk:
  - `dlt_sources/cianchosaint/political_parties/uk/reform_uk.py` (exists)
  - `dlt_sources/cianchosaint/uk/intelligence_oversight/investigatory_powers_bill_evidence.py` (exists)
- [x] Verify the 4 leabharlann source PDFs exist on disk:
  - `leabharlann/gemini_deep_research/politics/reform_richard_tice_debt_fraud.pdf`
  - `leabharlann/gemini_deep_research/politics/reform_corruption.pdf`
  - `leabharlann/gemini_deep_research/politics/clacton_farage_reform_refusal.pdf`
  - `leabharlann/gemini_deep_research/politics/farage_20reform_20uk_20crypto_20oversight.pdf`
- [x] Verify `baml_src/clients.baml` exposes the 4-tier client chain
  (Primary / Fallback / Emergency / Gemini)

## 1. OpenSpec artifacts

- [ ] Author `openspec/changes/cianchosaint-reform-uk-pilot-workflow-v1/proposal.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-reform-uk-pilot-workflow-v1/tasks.md` (this file) — DONE
- [ ] Author `openspec/changes/cianchosaint-reform-uk-pilot-workflow-v1/specs/cianchosaint-reform-uk-pilot-workflow/spec.md` (the 3 ADDED Requirements delta) — DONE
- [ ] Author `openspec/specs/cianchosaint-reform-uk-pilot-workflow/spec.md` (canonical END-STATE spec) — DONE
- [ ] Author `openspec/specs/cianchosaint-reform-uk-pilot-workflow/AGENTS.md` (per-spec routing) — DONE

## 2. Validation gates

- [ ] Run `openspec validate cianchosaint-reform-uk-pilot-workflow-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-reform-uk-pilot-workflow --strict` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL pass
- [ ] Run `python3.13 -c "import ast; ast.parse(open('agents/cianchosaint/tools/reform_uk_pilot.py').read())"` and verify exit code 0

## 3. Implementation: 1 FunctionTool + 1 BAML + 1 case study

### FunctionTool (1 file at `agents/cianchosaint/tools/`)
- [ ] `reform_uk_pilot.py` — the `reform_uk_pilot_tool = FunctionTool(func=reform_uk_pilot)` that consumes the 2 DLT sources + the BAML extraction

### BAML extraction (1 file at `baml_src/cianchosaint/politics/`)
- [ ] `reform_uk_pilot_extraction.baml` — the `ReformUkDossier` schema + the `ExtractReformUkDossier` extraction function

### Case study (1 file at `docs/case-study/`)
- [ ] `reform-uk-pilot.md` — the canonical case study document (~2,000-3,000 words)

## 4. Per-file pattern (FunctionTool usage)

```python
"""Reform UK pilot investigation FunctionTool.

Per the openspec/changes/cianchosaint-reform-uk-pilot-workflow-v1/
specs/cianchosaint-reform-uk-pilot-workflow/spec.md.

This is the FIRST case-study pilot (per Q12 = B + the locked plan).
It uses the political party pipeline (Change 4 — reform_uk.py)
+ the intelligence oversight pipeline (Change 3 — IPB evidence)
+ the 4-tier BAML extraction contract to generate a structured
dossier on a SINGLE entity (Richard Tice + 2024 election debt
fraud PDF from leabharlann/gemini_deep_research/politics/).

Conservative posture: the pilot NEVER directly submits forms to
operational systems; it generates the dossier for analyst review
ONLY. The OSINT ceiling + the BUSL-1.1 v2 licence posture apply.
"""
from __future__ import annotations

import logging
from google.adk.tools import FunctionTool

logger = logging.getLogger(__name__)


async def reform_uk_pilot(
    target_entity: str = "Richard Tice",
    focus: str = "2024 election debt fraud",
    jurisdiction: str = "uk_hoc",
) -> dict:
    """Run the Reform UK pilot investigation dossier.

    Args:
        target_entity: The entity to investigate (default: "Richard Tice").
        focus: The investigation focus (default: "2024 election debt fraud").
        jurisdiction: The constituency (default: "uk_hoc").

    Returns:
        A structured dossier dict with dossier_id, target_entity, focus,
        jurisdiction, mentions_entities, mentions_donors,
        mentions_companies_house, mentions_investigatory_powers,
        osint_ceiling_enforced, licence_posture, analyst_review_required,
        source_pdf_urls, created_at.
    """
    logger.info("running_reform_uk_pilot", target_entity=target_entity, focus=focus)

    # Real implementation uses:
    # - dlt_sources.cianchosaint.political_parties.uk.reform_uk.reform_uk_source()
    # - dlt_sources.cianchosaint.uk.intelligence_oversight.investigatory_powers_bill_evidence
    # - baml_client.b.ExtractReformUkDossier(input)

    return {
        "dossier_id": f"reform-uk-pilot-{target_entity.lower().replace(' ', '-')}",
        "target_entity": target_entity,
        "focus": focus,
        "jurisdiction": jurisdiction,
        "mentions_entities": [target_entity],
        "mentions_donors": [],
        "mentions_companies_house": [],
        "mentions_investigatory_powers": [],
        "osint_ceiling_enforced": True,
        "licence_posture": "BUSL-1.1 v2 (British-Isles-only)",
        "analyst_review_required": True,
        "source_pdf_urls": [],
        "created_at": "",
    }


reform_uk_pilot_tool = FunctionTool(func=reform_uk_pilot)
```

## 5. Per-file pattern (BAML extraction)

```baml
class ReformUkDossier {
  dossier_id string
  target_entity string
  focus string
  jurisdiction enum<UK_HOC, ROI_DAIL, NI_ASSEMBLY, SENEDD, HOLYROOD>
  mentions_entities string[]
  mentions_donors string[]
  mentions_companies_house string[]
  mentions_investigatory_powers string[]
  osint_ceiling_enforced bool
  licence_posture string  // "BUSL-1.1 v2 (British-Isles-only)"
  analyst_review_required bool
  source_pdf_urls string[]  // links to the leabharlann PDFs
  created_at string  // ISO 8601 timestamp
}

function ExtractReformUkDossier(input: string) -> ReformUkDossier {
  client Primary
  prompt #"
    Extract the structured Reform UK pilot investigation dossier
    from the following content.
    {{ input }}
  "#
}
```

## 6. CI gates + commit + push

- [ ] Run `mise run lint:license` and verify exit code 0 (the 2 input DLT sources are already in the OSINT allowlist; this change adds no new source URLs)
- [ ] Run `python3.13 -c "import ast; ast.parse(open('agents/cianchosaint/tools/reform_uk_pilot.py').read())"` and verify
- [ ] Run `openspec validate --all --strict` and verify ALL pass
- [ ] Commit on `cianchosaint:main` with message: `feat(pilot): Reform UK pilot workflow (Richard Tice + 2024 election debt fraud) — Change 7`
- [ ] Push to `github.com/cianfhoghlaim/cianchosaint`

## 7. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-reform-uk-pilot-workflow-v2` — multi-entity dossier expansion (deferred until the v1 pilot has been validated by a public-sector analyst)
- [ ] `cianchosaint-companies-house-bulk-pipeline-v1` — the Companies House bulk data cross-reference (the donor analysis layer)
- [ ] `cianchosaint-per-constituency-agents-v2` — the cross-jurisdiction linking (NI ↔ ROI)
