# CIANCHOSAINT — PSNI non-emergency form filler tool.
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
PSNI Form Fill Tool.

Generates the contents of a PSNI non-emergency report form.
Does NOT submit — the citizen reviews and submits at
psni.police.uk themselves.
"""

from google.adk.tools import FunctionTool


async def psni_form_fill(
    incident_type: str,
    location: str,
    time: str,
    description: str,
    suspect_description: str | None = None,
    vehicle_details: str | None = None,
    reporter_name: str | None = None,
    reporter_contact: str | None = None,
    near_border: bool = False,
) -> dict:
    """Generate the contents of a PSNI non-emergency report form.

    Args:
        incident_type: One of the PSNI's published categories
            ("asb", "crime", "road_incident", "lost_found",
            "suspicious_activity", "domestic", "other").
        location: Where the incident occurred.
        time: When the incident occurred.
        description: Free-text description.
        suspect_description: Optional suspect description.
        vehicle_details: Optional vehicle make/model/colour.
        reporter_name: Optional reporter name.
        reporter_contact: Optional reporter contact.
        near_border: True if the incident is near the NI / ROI
            border (flag for cross-jurisdiction routing).

    Returns:
        A dict with the form contents ready for the citizen to
        review and submit at psni.police.uk.

    Reference:
        https://www.psni.police.uk/contact-us/
    """
    valid_categories = {
        "asb",
        "crime",
        "road_incident",
        "lost_found",
        "suspicious_activity",
        "domestic",
        "other",
    }
    if incident_type not in valid_categories:
        incident_type = "other"

    form = {
        "form_type": "PSNI_NON_EMERGENCY_REPORT",
        "submission_url": "https://www.psni.police.uk/contact-us/",
        "fields": {
            "incident_type": incident_type,
            "incident_location": location,
            "incident_time": time,
            "incident_description": description,
            "suspect_description": suspect_description,
            "vehicle_details": vehicle_details,
            "reporter_name": reporter_name,
            "reporter_contact": reporter_contact,
            "near_border": near_border,
        },
        "warnings": [
            (
                "DO NOT SUBMIT THIS FORM IF THE INCIDENT IS AN "
                "EMERGENCY. Call 999 immediately."
            ),
            (
                "This form generates the contents only — review "
                "and submit at psni.police.uk yourself."
            ),
        ],
        "border_warning": (
            "If the incident is near the border, An Garda Síochána "
            "(ROI) may also have jurisdiction — consider a separate "
            "report to garda.ie."
            if near_border
            else None
        ),
    }
    return form


psni_form_fill_tool = FunctionTool(func=psni_form_fill)


__all__ = ["psni_form_fill", "psni_form_fill_tool"]
