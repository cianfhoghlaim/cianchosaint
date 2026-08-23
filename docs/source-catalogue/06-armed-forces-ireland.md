# 06 — Defence Forces of Ireland (Army / Naval Service / Air Corps)

> Per the [`openspec/changes/cianchosaint-british-isles-source-catalogue-v1/`](../../../openspec/changes/cianchosaint-british-isles-source-catalogue-v1/specs/cianchosaint-source-catalogue/spec.md) spec.

## Overview

The **Defence Forces of Ireland** (Óglaigh na hÉireann) are Ireland's
military. They comprise **3 single-service branches**:

- **Army** (an tArm)
- **Naval Service** (an tSeirbhís Chabhlaigh)
- **Air Corps** (an tAerfhórsa)

The parent body is the **Department of Defence** (An Roinn Cosanta).
The cianchosaint platform covers the 3 branches + the parent Department
+ the periodic **White Paper on Defence** + the **Commission on the
Defence Forces** reports, per the
[`cianchosaint-per-constituency-dlt-sources`](../../../openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md)
spec (the BIDP v1 m2 milestone).

## Sources

### Department of Defence (Ireland)

- **URL**: https://www.gov.ie/en/organisation/department-of-defence/
- **DLT source**: NOT YET WIRED (the DLT sources below cover the
  individual branches)
- **OSINT allowlist**: yes
- **Coverage**: Department of Defence press releases, defence policy
  papers, annual reports
- **Update cadence**: weekly
- **Notes**: The parent department for all 3 single-service branches.
  The BIDP v1 m2 milestone master source would aggregate from the
  branch DLTs.

### Defence Forces (Ireland) press releases

- **URL**: https://www.military.ie/en/news/
- **DLT source**: `dlt_sources/cianchosaint/ireland/defence_forces/idf_press_releases.py`
- **OSINT allowlist**: yes
- **Coverage**: All 3 branches (Army / Naval Service / Air Corps) press
  releases from the unified Defence Forces news page
- **Update cadence**: daily
- **Notes**: The unified ingest point for all 3 branches

### White Paper on Defence (Ireland)

- **URL**: https://www.gov.ie/en/department-of-defence/publications/white-paper-on-defence/
- **DLT source**: `dlt_sources/cianchosaint/ireland/defence_forces/idf_white_paper.py`
- **OSINT allowlist**: yes
- **Coverage**: The 2015 White Paper on Defence + any subsequent
  updates
- **Update cadence**: on-publication
- **Notes**: The canonical statement of Irish defence policy; the
  most-cited Irish defence document

### Commission on the Defence Forces

- **URL**: https://www.gov.ie/en/department-of-defence/publications/report-of-the-commission-on-the-defence-forces/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: The 1996 Report of the Commission on the Defence Forces
  + any subsequent commission reports
- **Update cadence**: on-publication
- **Notes**: A historical-archive DLT source; not YET WIRED. Follow-up
  `cianchosaint-defence-commission-archive-v1`.

### Army (Ireland)

- **URL**: https://www.military.ie/en/the-army/
- **DLT source**: covered by `idf_press_releases.py` (branch-specific
  filtering)
- **OSINT allowlist**: yes
- **Coverage**: Army press releases, regimental histories, recruitment
- **Update cadence**: daily
- **Notes**: The land branch of the Defence Forces

### Naval Service (Ireland)

- **URL**: https://www.military.ie/en/the-naval-service/
- **DLT source**: covered by `idf_press_releases.py` (branch-specific
  filtering)
- **OSINT allowlist**: yes
- **Coverage**: Naval Service press releases, ship commissioning logs,
  fisheries protection patrol reports
- **Update cadence**: daily
- **Notes**: The maritime branch of the Defence Forces

### Air Corps (Ireland)

- **URL**: https://www.military.ie/en/the-air-corps/
- **DLT source**: covered by `idf_press_releases.py` (branch-specific
  filtering)
- **OSINT allowlist**: yes
- **Coverage**: Air Corps press releases, aircraft deployment logs,
  recruitment
- **Update cadence**: daily
- **Notes**: The air branch of the Defence Forces

## Gaps

- **Department of Defence** itself does NOT have its own dedicated DLT
  source (covered via the branch DLTs). Follow-up
  `cianchosaint-ireland-defence-dept-v1` if needed.
- **Commission on the Defence Forces** archive is NOT YET WIRED.
- **Overseas deployments** (UNIFIL / UNDOF / EUTM / KFOR) are partially
  captured via the branch press releases but NOT yet extracted as a
  dedicated deployment-tracker source.
- **Defence Forces Reserve** (the RDF — Reserve Defence Force) is
  partially captured via the branch press releases but NOT yet
  extracted as a dedicated source.

## References

- The canonical openspec spec:
  [`openspec/specs/cianchosaint-source-catalogue/spec.md`](../../../openspec/specs/cianchosaint-source-catalogue/spec.md)
- The per-constituency DLT sources spec:
  [`openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md`](../../../openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md)
- The OSINT allowlist:
  [`dlt_sources/cianchosaint/common/osint_allowlist.yaml`](../../../dlt_sources/cianchosaint/common/osint_allowlist.yaml)
- The per-constituency cohort registry:
  [`dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`](../../../dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py)
- The 4 UK Armed Forces branches:
  [`05-armed-forces-uk.md`](05-armed-forces-uk.md)
