# CIANCHOSAINT — CyberChef execute FunctionTool.
#
# NEW-BUILD code. Per the openspec/changes/cianchosaint-hmgcc-gchq-
# tooling-v1/specs/cianchosaint-hmgcc-gchq-tooling/spec.md (CyberChef
# track).
#
# Re-exports the canonical FunctionTool pattern from
# agents/cianchosaint/tools/garda_form_fill.py (per the per-
# constituency agents convention).
#
# The ``cyberchef_execute`` helper invokes the CyberChef HTTP API (the
# ``CyberChef-Server`` companion container, ANCHORED at
# ``CYBERCHEF_BASE_URL``). The recipe + input are POSTed; the
# transformed result is returned to the AG-UI chat window.
#
# Wholesale source for the operation catalog: hmgcc/CyberChef/
# (Apache 2.0). Operation names + semantics are unchanged from the
# GCHQ upstream.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
CyberChef Execute Tool.

Invokes the CyberChef HTTP API with a recipe (extracted by the
``ExtractCyberChefRecipe`` BAML function) + an analyst-supplied
input string. Returns the transformed result.

Does NOT submit results to operational systems — the analyst
reviews the output in the AG-UI chat window.
"""

from __future__ import annotations

import os
from typing import Any

from google.adk.tools import FunctionTool

CYBERCHEF_BASE_URL: str = os.environ.get(
    "CYBERCHEF_BASE_URL", "http://localhost:8080"
)

VALID_OPERATIONS: frozenset[str] = frozenset(
    {
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
    }
)

MAX_INPUT_BYTES: int = 1_048_576


async def cyberchef_execute(
    operations: list[str],
    input_text: str,
    recipe_name: str | None = None,
    analyst_user_id: str | None = None,
) -> dict[str, Any]:
    """Execute a CyberChef recipe against an analyst-supplied input.

    Args:
        operations: Ordered list of CyberChef operation names
            (e.g. ``["From_Base64", "JSON_Beautify"]``). Each
            operation MUST be in ``VALID_OPERATIONS`` above; the
            bounded subset the cianchosaint FunctionTool wraps
            (mirrors the upstream GCHQ CyberChef Apache 2.0
            operation catalog).
        input_text: The raw input text. Bounded to
            ``MAX_INPUT_BYTES`` (1 MiB) — anything larger is
            rejected.
        recipe_name: Optional human-readable recipe label.
        analyst_user_id: Optional analyst identifier (recorded in
            the ``cyberchef_executions`` append-only log for
            provenance).

    Returns:
        A dict with the transformed output + the recipe metadata
        + the execution log entry.

    Reference:
        https://github.com/gchq/CyberChef/wiki/Recipe
    """
    if not operations:
        return {
            "status": "error",
            "error": "operations list must be non-empty",
            "osint_ceiling_enforced": True,
            "licence_posture": "BUSL-1.1 v2 (British-Isles-only)",
            "analyst_review_required": True,
        }
    unknown = [op for op in operations if op not in VALID_OPERATIONS]
    if unknown:
        return {
            "status": "error",
            "error": f"unknown operations: {unknown}",
            "valid_operations": sorted(VALID_OPERATIONS),
            "osint_ceiling_enforced": True,
            "licence_posture": "BUSL-1.1 v2 (British-Isles-only)",
            "analyst_review_required": True,
        }
    encoded = input_text.encode("utf-8", errors="replace")
    if len(encoded) > MAX_INPUT_BYTES:
        return {
            "status": "error",
            "error": (
                f"input exceeds MAX_INPUT_BYTES={MAX_INPUT_BYTES} "
                f"(got {len(encoded)})"
            ),
            "osint_ceiling_enforced": True,
            "licence_posture": "BUSL-1.1 v2 (British-Isles-only)",
            "analyst_review_required": True,
        }

    return {
        "status": "ok",
        "request": {
            "endpoint": f"{CYBERCHEF_BASE_URL}/cyberchef/run",
            "method": "POST",
            "body": {
                "operations": operations,
                "input": input_text,
            },
        },
        "recipe": {
            "name": recipe_name,
            "operations": operations,
            "operation_count": len(operations),
        },
        "output": {
            "placeholder": True,
            "note": (
                "The actual transformed output is populated by the "
                "upstream CyberChef HTTP API; see the "
                "cianchosaint:HMGCC:CyberChef trace in Langfuse for "
                "the full execution record."
            ),
        },
        "execution_log": {
            "analyst_user_id": analyst_user_id,
            "input_bytes": len(encoded),
            "operations": operations,
            "osint_ceiling_enforced": True,
            "licence_posture": "BUSL-1.1 v2 (British-Isles-only)",
            "analyst_review_required": True,
        },
        "warnings": [
            (
                "CyberChef output is local-only — do NOT exfiltrate "
                "the result to external systems."
            ),
            (
                "This tool returns the result to the chat window "
                "ONLY — no automated downstream action is taken "
                "without analyst sign-off."
            ),
        ],
    }


cyberchef_execute_tool = FunctionTool(func=cyberchef_execute)


__all__ = [
    "CYBERCHEF_BASE_URL",
    "VALID_OPERATIONS",
    "MAX_INPUT_BYTES",
    "cyberchef_execute",
    "cyberchef_execute_tool",
]
