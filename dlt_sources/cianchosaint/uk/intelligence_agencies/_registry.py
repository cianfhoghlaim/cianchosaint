# CIANCHOSAINT new-build: the 5 UK intelligence agency cohort registry.
#
# Per the openspec/changes/cianchosaint-intelligence-agency-pipeline-v1/
# specs/cianchosaint-intelligence-agency-pipeline/spec.md, Requirement:
# The IntelligenceAgencyPipelineBase class + the cross-agency cohort
# registry, Scenario: The cohort registry cross-references the
# intelligence OVERSIGHT sources.

"""cianchosaint.cianchosaint.dlt.british_isles.intelligence_agencies._registry.

The cohort registry enumerates every (agency_id, source_url,
cohort_id) tuple + the cross-reference to the intelligence OVERSIGHT
sources (ISC + IPCO + IPT — shipped in
cianchosaint-per-constituency-dlt-sources-v1 Change 3) + the
companion IntelligenceAgencyPipelineBase classes.

Run with::

    python -m dlt_sources.cianchosaint.uk.intelligence_agencies._registry

Output::

    === UK intelligence ecosystem cohort registry ===
    agency_id             agency_name                        cohort_id
    --------------------- ----------------------------------- ---------------------------
    mi5                   MI5 (Security Service)             uk.intelligence_agency.mi5
    mi6                   MI6 (Secret Intelligence Service)  uk.intelligence_agency.mi6
    gchq                  GCHQ (signals intelligence)         uk.intelligence_agency.gchq
    defence_intelligence  Defence Intelligence (DI)          uk.intelligence_agency.defence_intelligence
    hmgcc                 HMGCC (12-week rolling window)      uk.intelligence_agency.hmgcc

    Cross-reference to intelligence OVERSIGHT sources (Change 3):
    - isc_annual_reports        (Intelligence and Security Committee)
    - ipco_reports              (Investigatory Powers Commissioner)
    - ipt_decisions             (Investigatory Powers Tribunal)
    - investigatory_powers_bill_evidence

    Milestone gate: cianchosaint:biip:v1:m1
"""

from __future__ import annotations

from ._base import IntelligenceAgencyPipelineBase

# Cross-reference to intelligence OVERSIGHT sources (Change 3)
OVERSIGHT_CROSS_REFERENCE: tuple[str, ...] = (
    "isc_annual_reports",
    "ipco_reports",
    "ipt_decisions",
    "investigatory_powers_bill_evidence",
)

# The 5 intelligence agencies with their metadata
AGENCY_REGISTRY: tuple[dict[str, str], ...] = (
    {
        "agency_id": "mi5",
        "agency_name": "MI5 (Security Service)",
        "source_base": "https://www.mi5.gov.uk/",
        "role": "Domestic counter-intelligence and security",
    },
    {
        "agency_id": "mi6",
        "agency_name": "MI6 (Secret Intelligence Service)",
        "source_base": "https://www.sis.gov.uk/",
        "role": "Foreign intelligence",
    },
    {
        "agency_id": "gchq",
        "agency_name": "GCHQ (Government Communications Headquarters)",
        "source_base": "https://www.gchq.gov.uk/",
        "role": "Signals intelligence",
    },
    {
        "agency_id": "defence_intelligence",
        "agency_name": "Defence Intelligence (DI)",
        "source_base": "https://www.gov.uk/government/organisations/defence-intelligence",
        "role": "Military intelligence",
    },
    {
        "agency_id": "hmgcc",
        "agency_name": "HMGCC (His Majesty's Government Communications Centre)",
        "source_base": "https://www.hmgcc.gov.uk/",
        "role": "Government communications + 12-week rolling window",
    },
)


def get_agency_pipeline(agency_id: str) -> IntelligenceAgencyPipelineBase | None:
    """Return the IntelligenceAgencyPipelineBase subclass for an agency."""
    for entry in AGENCY_REGISTRY:
        if entry["agency_id"] == agency_id:
            # Lazy import to avoid circular dependency
            from . import mi5, mi6, gchq, defence_intelligence, hmgcc_rolling_window

            module_map = {
                "mi5": mi5,
                "mi6": mi6,
                "gchq": gchq,
                "defence_intelligence": defence_intelligence,
                "hmgcc": hmgcc_rolling_window,
            }
            module = module_map.get(agency_id)
            if module is None:
                return None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, IntelligenceAgencyPipelineBase)
                    and attr is not IntelligenceAgencyPipelineBase
                ):
                    return attr()
    return None


def print_cohort_registry() -> None:
    """Print the canonical cohort registry table."""
    print("=== UK intelligence ecosystem cohort registry ===")
    print(f"{'agency_id':<25} {'agency_name':<35} {'cohort_id'}")
    print(f"{'-'*25} {'-'*35} {'-'*40}")
    for entry in AGENCY_REGISTRY:
        print(
            f"{entry['agency_id']:<25} {entry['agency_name']:<35} "
            f"uk.intelligence_agency.{entry['agency_id']}"
        )
    print()
    print("Cross-reference to intelligence OVERSIGHT sources (Change 3):")
    for oversight_source in OVERSIGHT_CROSS_REFERENCE:
        print(f"  - {oversight_source}")
    print()
    print("Milestone gate: cianchosaint:biip:v1:m1")


if __name__ == "__main__":
    print_cohort_registry()
