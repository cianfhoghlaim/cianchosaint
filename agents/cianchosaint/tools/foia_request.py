# CIANCHOSAINT — FOIA request tool (UK FOIA + ROI FOI Act).
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
FOIA Request Tool.

Drafts Freedom of Information requests for UK (Freedom of
Information Act 2000) and ROI (Freedom of Information Act
2014) public bodies.
"""

from google.adk.tools import FunctionTool


async def foia_request(
    public_body: str,
    jurisdiction: str,
    request_text: str,
    applicant_name: str | None = None,
    applicant_email: str | None = None,
) -> dict:
    """Draft a Freedom of Information request.

    Args:
        public_body: The target public body (e.g. "An Garda
            Síochána", "Metropolitan Police Service",
            "Police Service of Northern Ireland").
        jurisdiction: One of "uk" (Freedom of Information Act
            2000), "ireland" (Freedom of Information Act 2014).
        request_text: The specific information being requested.
        applicant_name: Optional applicant name.
        applicant_email: Optional applicant email.

    Returns:
        A dict with the drafted FOI letter + standard fees +
        response deadlines.

    Reference:
        - UK FOIA 2000: https://www.legislation.gov.uk/ukpga/2000/36
        - ROI FOI Act 2014: https://www.irishstatutebook.ie/eli/2014/act/30
    """
    if jurisdiction == "uk":
        fees_note = "Standard UK FOIA fee: free (no fee for requests)."
        deadline = "20 working days (s.10)."
        act_name = "Freedom of Information Act 2000"
    elif jurisdiction == "ireland":
        fees_note = "ROI FOI fee: EUR 15 (non-personal), EUR 0 (personal)."
        deadline = "20 working days (s.13)."
        act_name = "Freedom of Information Act 2014"
    else:
        fees_note = "Unknown jurisdiction."
        deadline = "N/A"
        act_name = "Unknown"

    letter = {
        "form_type": "FOIA_REQUEST_LETTER",
        "jurisdiction": jurisdiction,
        "act_name": act_name,
        "public_body": public_body,
        "applicant_name": applicant_name,
        "applicant_email": applicant_email,
        "request_text": request_text,
        "fees_note": fees_note,
        "response_deadline": deadline,
        "warnings": [
            (
                "This tool drafts the FOI letter; the citizen "
                "reviews and sends it themselves."
            ),
        ],
    }
    return letter


foia_request_tool = FunctionTool(func=foia_request)


__all__ = ["foia_request", "foia_request_tool"]
