# CIANCHOSAINT — Metropolitan Police non-emergency form filler tool.
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
MET Form Fill Tool.

Generates the contents of a Metropolitan Police non-emergency
report form. Does NOT submit — the citizen reviews and submits
at met.police.uk themselves.
"""

from google.adk.tools import FunctionTool


async def met_form_fill(
    incident_type: str,
    location: str,
    time: str,
    description: str,
    suspect_description: str | None = None,
    vehicle_details: str | None = None,
    reporter_name: str | None = None,
    reporter_contact: str | None = None,
) -> dict:
    """Generate the contents of a Met non-emergency report form.

    Args:
        incident_type: One of the Met's published categories
            ("asb", "crime", "road_incident", "lost_found",
            "suspicious_activity", "other").
        location: Where the incident occurred.
        time: When the incident occurred.
        description: Free-text description.
        suspect_description: Optional suspect description.
        vehicle_details: Optional vehicle make/model/colour.
        reporter_name: Optional reporter name.
        reporter_contact: Optional reporter contact.

    Returns:
        A dict with the form contents ready for the citizen to
        review and submit at met.police.uk.

    Reference:
        https://www.met.police.uk/contact/af/contact-us/
    """
    valid_categories = {
        "asb",
        "crime",
        "road_incident",
        "lost_found",
        "suspicious_activity",
        "other",
    }
    if incident_type not in valid_categories:
        incident_type = "other"

    form = {
        "form_type": "MET_NON_EMERGENCY_REPORT",
        "submission_url": "https://www.met.police.uk/contact/af/contact-us/",
        "fields": {
            "incident_type": incident_type,
            "incident_location": location,
            "incident_time": time,
            "incident_description": description,
            "suspect_description": suspect_description,
            "vehicle_details": vehicle_details,
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
                "and submit at met.police.uk yourself."
            ),
        ],
    }
    return form


met_form_fill_tool = FunctionTool(func=met_form_fill)


__all__ = ["met_form_fill", "met_form_fill_tool"]
