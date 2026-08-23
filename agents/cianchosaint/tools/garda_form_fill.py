# CIANCHOSAINT — Garda non-emergency form filler tool.
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
GA Form Fill Tool.

Generates the contents of a Garda non-emergency report form.
Does NOT submit — the citizen reviews and submits at garda.ie
themselves.
"""

from google.adk.tools import FunctionTool


async def garda_form_fill(
    location: str,
    time: str,
    description: str,
    vehicle_reg: str | None = None,
    reporter_name: str | None = None,
    reporter_contact: str | None = None,
) -> dict:
    """Generate the contents of a Garda non-emergency report form.

    Args:
        location: Where the incident occurred (address or area).
        time: When the incident occurred (ISO 8601 datetime or
            human-readable string).
        description: Free-text description of the incident.
        vehicle_reg: Vehicle registration if applicable (ROI format).
        reporter_name: Optional reporter name.
        reporter_contact: Optional reporter contact (email/phone).

    Returns:
        A dict with the form contents ready for the citizen to
        review and submit at garda.ie.

    Reference:
        https://www.garda.ie/en/about-us/contact-us/
    """
    form = {
        "form_type": "GA_NON_EMERGENCY_REPORT",
        "submission_url": "https://www.garda.ie/en/about-us/contact-us/",
        "fields": {
            "incident_location": location,
            "incident_time": time,
            "incident_description": description,
            "vehicle_registration": vehicle_reg,
            "reporter_name": reporter_name,
            "reporter_contact": reporter_contact,
        },
        "warnings": [
            (
                "DO NOT SUBMIT THIS FORM IF THE INCIDENT IS AN "
                "EMERGENCY. Call 999 or 112 immediately."
            ),
            (
                "This form generates the contents only — review "
                "and submit at garda.ie yourself."
            ),
        ],
    }
    return form


garda_form_fill_tool = FunctionTool(func=garda_form_fill)


__all__ = ["garda_form_fill", "garda_form_fill_tool"]
