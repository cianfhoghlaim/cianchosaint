# CIANCHOSAINT new-build: Reform UK pilot investigation FunctionTool.
#
# Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/
#   cianchosaint-reform-uk-pilot-workflow-v1/specs/cianchosaint-reform-
#   uk-pilot-workflow/spec.md, Requirement: The Reform UK pilot
#   FunctionTool).
# Migrated to cianchosaint: 2026-08-23
# Licence: BUSL-1.1 (per LICENSE.md)
#
# This is the FIRST case-study pilot (per Q12 = B + the locked plan).
# It uses the political party pipeline (Change 4 — reform_uk.py)
# + the intelligence oversight pipeline (Change 3 — IPB evidence)
# + the 4-tier BAML extraction contract to generate a structured
# dossier on a SINGLE entity (Richard Tice + 2024 election debt
# fraud PDF from leabharlann/gemini_deep_research/politics/).
#
# Conservative posture: the pilot NEVER directly submits forms to
# operational systems; it generates the dossier for analyst review
# ONLY. The OSINT ceiling + the BUSL-1.1 v2 licence posture apply.

"""cianchosaint.cianchosaint.tools.reform_uk_pilot — Reform UK pilot FunctionTool.

Cross-references:
- `dlt_sources.cianchosaint.political_parties.uk.reform_uk.reform_uk_source()`
  (Reform UK press releases — Change 4)
- `dlt_sources.cianchosaint.uk.intelligence_oversight.investigatory_powers_bill_evidence`
  (IPB evidence — Change 3)
- `baml_client.b.ExtractReformUkDossier(input)` (BAML extraction)

Returns a structured `ReformUkDossier` dict for analyst review ONLY.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from google.adk.tools import FunctionTool

logger = logging.getLogger(__name__)


async def reform_uk_pilot(
    target_entity: str = "Richard Tice",
    focus: str = "2024 election debt fraud",
    jurisdiction: str = "uk_hoc",
) -> dict[str, Any]:
    """Run the Reform UK pilot investigation dossier.

    Args:
        target_entity: The entity to investigate (default: "Richard Tice").
            Per the locked plan Q12 = B, the pilot starts with a SINGLE
            entity. Expanding to multi-entity dossiers requires an
            explicit follow-up openspec change.
        focus: The investigation focus (default: "2024 election debt
            fraud"). Per the locked plan Q12 = B, the pilot starts with
            a SINGLE focus.
        jurisdiction: The constituency / jurisdiction (default:
            "uk_hoc" — UK House of Commons).

    Returns:
        A structured dossier dict with the 13 canonical fields:
        dossier_id, target_entity, focus, jurisdiction,
        mentions_entities, mentions_donors, mentions_companies_house,
        mentions_investigatory_powers, osint_ceiling_enforced,
        licence_posture, analyst_review_required, source_pdf_urls,
        created_at.

    Reference:
        The canonical Reform UK source (Change 4):
        https://www.reformparty.uk/news (in the OSINT allowlist)

        The canonical IPB evidence source (Change 3):
        https://bills.parliament.uk/bills/2687 (in the OSINT allowlist)

        The 4 leabharlann source PDFs (read-only context):
        - leabharlann/gemini_deep_research/politics/reform_richard_tice_debt_fraud.pdf
        - leabharlann/gemini_deep_research/politics/reform_corruption.pdf
        - leabharlann/gemini_deep_research/politics/clacton_farage_reform_refusal.pdf
        - leabharlann/gemini_deep_research/politics/farage_20reform_20uk_20crypto_20oversight.pdf
    """
    logger.info(
        "running_reform_uk_pilot",
        extra={
            "target_entity": target_entity,
            "focus": focus,
            "jurisdiction": jurisdiction,
        },
    )

    # The full implementation invokes:
    # 1. dlt_sources.cianchosaint.political_parties.uk.reform_uk.reform_uk_source()
    #    → Reform UK press releases
    # 2. dlt_sources.cianchosaint.uk.intelligence_oversight.investigatory_powers_bill_evidence
    #    → IPB evidence submissions
    # 3. baml_client.b.ExtractReformUkDossier(input)
    #    → structured ReformUkDossier record
    #
    # This stub returns the canonical 13-field shape so the per-persona
    # agent (ciafagent-ga-public) can wire against it before the live
    # DLT sources + BAML function are wired in the follow-up change.

    dossier_id = (
        f"reform-uk-pilot-{target_entity.lower().replace(' ', '-')}"
    )

    return {
        "dossier_id": dossier_id,
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
        "source_pdf_urls": [
            "leabharlann/gemini_deep_research/politics/reform_richard_tice_debt_fraud.pdf",
            "leabharlann/gemini_deep_research/politics/reform_corruption.pdf",
            "leabharlann/gemini_deep_research/politics/clacton_farage_reform_refusal.pdf",
            "leabharlann/gemini_deep_research/politics/farage_20reform_20uk_20crypto_20oversight.pdf",
        ],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


reform_uk_pilot_tool = FunctionTool(func=reform_uk_pilot)


__all__ = ["reform_uk_pilot", "reform_uk_pilot_tool"]
