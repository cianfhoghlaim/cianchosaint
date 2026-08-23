# CIANCHOSAINT — cross-jurisdiction statute lookup tool.
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
Statute Lookup Tool.

Cross-jurisdiction statute lookup for ROI (irishstatutebook.ie),
NI (justice-ni.gov.uk), and UK (legislation.gov.uk).
"""

from google.adk.tools import FunctionTool


async def statute_lookup(
    query: str,
    jurisdiction: str = "ireland",
) -> dict:
    """Look up a statute across the British Isles jurisdictions.

    Args:
        query: The statute name or topic (e.g. "Criminal Justice
            (Theft and Fraud Offences) Act 2001").
        jurisdiction: One of "ireland" (ROI), "northern_ireland"
            (NI), "uk" (UK-wide), "all" (cross-jurisdiction).

    Returns:
        A dict with the matched statute(s) + canonical URLs.

    Reference:
        https://www.irishstatutebook.ie/
        https://www.legislation.gov.uk/
        https://www.justice-ni.gov.uk/
    """
    endpoints = {
        "ireland": "https://www.irishstatutebook.ie/",
        "northern_ireland": "https://www.legislation.gov.uk/uksi",
        "uk": "https://www.legislation.gov.uk/",
        "all": "cross_jurisdiction",
    }

    if jurisdiction not in endpoints:
        jurisdiction = "ireland"

    return {
        "query": query,
        "jurisdiction": jurisdiction,
        "endpoints": endpoints,
        "status": "lookup_initiated",
        "note": (
            "The actual lookup is performed by the calling agent "
            "via the cianchosaint BAML function "
            "`baml_src.cianchosaint.common.statute_lookup`. This "
            "tool returns the routing metadata."
        ),
    }


statute_lookup_tool = FunctionTool(func=statute_lookup)


__all__ = ["statute_lookup", "statute_lookup_tool"]
