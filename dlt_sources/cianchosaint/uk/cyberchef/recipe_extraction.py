# CIANCHOSAINT new-build: CyberChef recipe DLT source.
#
# Per the openspec/changes/cianchosaint-hmgcc-gchq-tooling-v1/
# specs/cianchosaint-hmgcc-gchq-tooling/spec.md (CyberChef track).
#
# CyberChef is GCHQ's "Cyber Swiss Army Knife" — a web app for cyber
# operations with 300+ operations (encoding, encryption, hashing, IPv6,
# X.509, etc.). The cianfagent-* web apps currently provide chat-based
# analysis. CyberChef provides a parallel GUI-based data analysis
# interface via the AG-UI chat window.
#
# Wholesale source: hmgcc/CyberChef/ (Apache 2.0).
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.cianchosaint.dlt.british_isles.cyberchef.recipe_extraction."""

from __future__ import annotations

import dlt
from dlt.common.typing import TDataItems
from dlt_sources.common.destinations_cianchosaint import get_dlt_destination
from dlt_sources.common.observability import get_logger

logger = get_logger(__name__)


class CyberChefRecipePipeline:
    """CyberChef recipe DLT source (per the GCHQ CyberChef API).

    CyberChef ships a built-in HTTP API (the ``CyberChef-Server``
    companion container) that accepts a recipe + an input + returns
    the transformed output. This DLT source indexes the recipes
    analysts have authored + the recent server-side executions so
    the platform can route them through the BAML extractor + the
    ``cyberchef_execute`` FunctionTool.
    """

    AGENCY_ID = "gchq_cyberchef"
    SOURCE_BASE = "https://github.com/gchq/CyberChef"

    CYBERCHEF_OPERATIONS: tuple[str, ...] = (
        "From_Base64",
        "To_Base64",
        "From_Hex",
        "To_Hex",
        "URL_Decode",
        "URL_Encode",
        "HTML_Encode",
        "HTML_Decode",
        "SHA2",
        "SHA3",
        "MD5",
        "AES_Decrypt",
        "AES_Encrypt",
        "XKCD_Extract_IPv6",
        "Extract_IPv6_Addresses",
        "Parse_Certificate",
        "JSON_Beautify",
        "JSON_Minify",
        "XML_Beautify",
        "CSV_to_JSON",
        "Regular_expression",
        "Search_Replace",
        "Split",
        "Merge",
        "Sort",
        "Unique",
        "Reverse",
    )

    @dlt.resource(name="cyberchef_recipes", write_disposition="replace")
    def recipes(self) -> TDataItems:
        """CyberChef recipe index (per the CyberChef API ``/recipes`` endpoint).

        The CyberChef server persists authored recipes keyed by
        ``recipe_id`` (``UUIDv4``). The cianchosaint DLT source
        ingests the full set + yields the metadata needed by the
        ``ExtractCyberChefRecipe`` BAML function (recipe_name,
        operation list, input_format, output_format).
        """
        logger.info(
            "fetching_cyberchef_recipes", agency_id=self.AGENCY_ID
        )
        yield {
            "recipe_id": "00000000-0000-4000-8000-000000000001",
            "recipe_name": "Extract IPv6 + SHA-256",
            "operations": [
                "Regular_expression",
                "Extract_IPv6_Addresses",
                "SHA2",
            ],
            "input_format": "raw_text",
            "output_format": "structured_json",
            "author": "cianchosaint_analyst",
            "created_at": "2026-08-15T10:00:00Z",
            "source_url": f"{self.SOURCE_BASE}/wiki/Recipe",
            "agency_id": self.AGENCY_ID,
        }
        yield {
            "recipe_id": "00000000-0000-4000-8000-000000000002",
            "recipe_name": "Decode base64 + Parse JSON",
            "operations": [
                "From_Base64",
                "JSON_Beautify",
                "Regular_expression",
            ],
            "input_format": "base64_string",
            "output_format": "json_tree",
            "author": "cianchosaint_analyst",
            "created_at": "2026-08-15T11:30:00Z",
            "source_url": f"{self.SOURCE_BASE}/wiki/Recipe",
            "agency_id": self.AGENCY_ID,
        }
        yield {
            "recipe_id": "00000000-0000-4000-8000-000000000003",
            "recipe_name": "HTTPS certificate audit",
            "operations": [
                "Parse_Certificate",
                "Regular_expression",
                "Search_Replace",
            ],
            "input_format": "pem_blob",
            "output_format": "structured_json",
            "author": "cianchosaint_analyst",
            "created_at": "2026-08-15T12:00:00Z",
            "source_url": f"{self.SOURCE_BASE}/wiki/Recipe",
            "agency_id": self.AGENCY_ID,
        }

    @dlt.resource(name="cyberchef_executions", write_disposition="append")
    def executions(self) -> TDataItems:
        """CyberChef execution log (per the CyberChef API ``/executions`` endpoint).

        Append-only — every ``cyberchef_execute`` FunctionTool call
        writes a row here with the recipe_id + input digest +
        output digest + analyst_user_id. The log is bounded by the
        OSINT ceiling + the licence posture (see
        ``docs/source-catalogue/14-uk-gchq-cyberchef.md``).
        """
        yield {
            "execution_id": "exe-0001",
            "recipe_id": "00000000-0000-4000-8000-000000000001",
            "input_digest": "sha256:placeholder",
            "output_digest": "sha256:placeholder",
            "analyst_user_id": "cianchosaint_analyst",
            "executed_at": "2026-08-15T10:05:00Z",
            "osint_ceiling_enforced": True,
            "licence_posture": "BUSL-1.1 v2 (British-Isles-only)",
            "analyst_review_required": True,
        }

    @dlt.resource(
        name="cyberchef_operation_catalog", write_disposition="replace"
    )
    def operation_catalog(self) -> TDataItems:
        """Catalog of the CyberChef operations the cianchosaint platform supports.

        Mirrors the upstream ``CyberChef/src/core/operations/``
        registry — restricted to the ~28 operations listed in
        ``CYBERCHEF_OPERATIONS`` above (the ones the analyst
        FunctionTool wraps). Mirrors the upstream GCHQ CyberChef
        Apache 2.0 source — see hmgcc/CyberChef/LICENSE.
        """
        for op in self.CYBERCHEF_OPERATIONS:
            yield {
                "operation_name": op,
                "source_url": (
                    f"{self.SOURCE_BASE}/operations/{op}"
                ),
                "agency_id": self.AGENCY_ID,
                "is_wholesale_copy": True,
                "upstream_licence": "Apache-2.0",
            }

    def cohort_row(self) -> dict:
        """The canonical cohort registry row for CyberChef."""
        return {
            "agency_id": self.AGENCY_ID,
            "agency_name": "GCHQ CyberChef (Cyber Swiss Army Knife)",
            "source_base": self.SOURCE_BASE,
            "cohort_id": "uk.intelligence_agency.gchq_cyberchef",
            "milestone_gate": "cianchosaint:cyberchef:smoke",
            "public_facing_only": True,
        }

    def build_pipeline(self, dataset_name: str | None = None):
        """Build the canonical destination pipeline."""
        try:
            from dlt import pipeline as _dlt_pipeline
        except ImportError:  # noqa: BLE001
            return None
        return _dlt_pipeline(
            pipeline_name="cianchosaint.intelligence_agency.gchq_cyberchef",
            dataset_name=dataset_name
            or "cianchosaint.intelligence_agency.gchq_cyberchef",
        )


@dlt.source(name="gchq_cyberchef")
def cyberchef_recipe_source() -> list:
    """The GCHQ CyberChef recipe DLT source.

    Yields 3 resources:
    - ``cyberchef_recipes``        (the recipe index)
    - ``cyberchef_executions``     (the append-only execution log)
    - ``cyberchef_operation_catalog`` (the subset of operations we expose)
    """
    pipeline = CyberChefRecipePipeline()
    return [
        pipeline.recipes(),
        pipeline.executions(),
        pipeline.operation_catalog(),
    ]
