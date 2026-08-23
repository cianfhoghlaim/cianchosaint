# CIANCHOSAINT — UK force lookup tool (43 UK forces via data.police.uk).
#
# NEW-BUILD code. Per `cianchosaint-per-constituency-agents-v1`.
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""
Force Lookup Tool.

Resolves a UK territorial force by name or region. Provides
metadata for all 43 UK forces (England + Wales) + the
Metropolitan Police Service.
"""

from google.adk.tools import FunctionTool


# The canonical 43 UK territorial forces (England + Wales).
UK_FORCES: list[dict[str, str]] = [
    {"id": "metropolitan", "name": "Metropolitan Police Service", "region": "London"},
    {"id": "city-of-london", "name": "City of London Police", "region": "London"},
    {"id": "bedfordshire", "name": "Bedfordshire Police", "region": "East"},
    {"id": "cambridgeshire", "name": "Cambridgeshire Constabulary", "region": "East"},
    {"id": "essex", "name": "Essex Police", "region": "East"},
    {"id": "hertfordshire", "name": "Hertfordshire Constabulary", "region": "East"},
    {"id": "norfolk", "name": "Norfolk Constabulary", "region": "East"},
    {"id": "suffolk", "name": "Suffolk Constabulary", "region": "East"},
    {"id": "avon-and-somerset", "name": "Avon and Somerset Constabulary", "region": "South West"},
    {"id": "devon-and-cornwall", "name": "Devon and Cornwall Police", "region": "South West"},
    {"id": "dorset", "name": "Dorset Police", "region": "South West"},
    {"id": "gloucestershire", "name": "Gloucestershire Constabulary", "region": "South West"},
    {"id": "wiltshire", "name": "Wiltshire Police", "region": "South West"},
    {"id": "hampshire", "name": "Hampshire Constabulary", "region": "South East"},
    {"id": "kent", "name": "Kent Police", "region": "South East"},
    {"id": "surrey", "name": "Surrey Police", "region": "South East"},
    {"id": "sussex", "name": "Sussex Police", "region": "South East"},
    {"id": "thames-valley", "name": "Thames Valley Police", "region": "South East"},
    {"id": "lancashire", "name": "Lancashire Constabulary", "region": "North West"},
    {"id": "merseyside", "name": "Merseyside Police", "region": "North West"},
    {"id": "cheshire", "name": "Cheshire Constabulary", "region": "North West"},
    {"id": "cumbria", "name": "Cumbria Constabulary", "region": "North West"},
    {"id": "greater-manchester", "name": "Greater Manchester Police", "region": "North West"},
    {"id": "northumbria", "name": "Northumbria Police", "region": "North East"},
    {"id": "durham", "name": "Durham Constabulary", "region": "North East"},
    {"id": "north-yorkshire", "name": "North Yorkshire Police", "region": "North East"},
    {"id": "west-yorkshire", "name": "West Yorkshire Police", "region": "North East"},
    {"id": "south-yorkshire", "name": "South Yorkshire Police", "region": "North East"},
    {"id": "cleveland", "name": "Cleveland Police", "region": "North East"},
    {"id": "west-midlands", "name": "West Midlands Police", "region": "West Midlands"},
    {"id": "staffordshire", "name": "Staffordshire Police", "region": "West Midlands"},
    {"id": "west-mercia", "name": "West Mercia Police", "region": "West Midlands"},
    {"id": "warwickshire", "name": "Warwickshire Police", "region": "West Midlands"},
    {"id": "shropshire", "name": "Shropshire Police", "region": "West Midlands"},
    {"id": "dyfed-powys", "name": "Dyfed-Powys Police", "region": "Wales"},
    {"id": "gwent", "name": "Gwent Police", "region": "Wales"},
    {"id": "north-wales", "name": "North Wales Police", "region": "Wales"},
    {"id": "south-wales", "name": "South Wales Police", "region": "Wales"},
    {"id": "leicestershire", "name": "Leicestershire Police", "region": "East Midlands"},
    {"id": "lincolnshire", "name": "Lincolnshire Police", "region": "East Midlands"},
    {"id": "northamptonshire", "name": "Northamptonshire Police", "region": "East Midlands"},
    {"id": "nottinghamshire", "name": "Nottinghamshire Police", "region": "East Midlands"},
    {"id": "derbyshire", "name": "Derbyshire Constabulary", "region": "East Midlands"},
]


async def force_lookup(query: str) -> dict:
    """Look up a UK territorial force by name or region.

    Args:
        query: The force name (e.g. "Metropolitan", "West Midlands")
            or region (e.g. "Wales", "London").

    Returns:
        A dict with the matching force(s) + data.police.uk URLs.

    Reference:
        https://data.police.uk/docs/method/force-list/
    """
    query_lower = query.lower()
    matches = [
        f
        for f in UK_FORCES
        if query_lower in f["name"].lower()
        or query_lower in f["region"].lower()
        or query_lower in f["id"]
    ]

    return {
        "query": query,
        "matches": matches,
        "data_police_url": "https://data.police.uk/docs/method/force-list/",
        "total_uk_forces": len(UK_FORCES),
    }


force_lookup_tool = FunctionTool(func=force_lookup)


__all__ = ["force_lookup", "force_lookup_tool", "UK_FORCES"]
