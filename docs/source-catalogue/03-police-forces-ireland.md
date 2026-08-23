# 03 — Police Forces of Ireland (Republic of Ireland + Northern Ireland)

> Per the [`openspec/changes/cianchosaint-british-isles-source-catalogue-v1/`](../../../openspec/changes/cianchosaint-british-isles-source-catalogue-v1/specs/cianchosaint-source-catalogue/spec.md) spec.

## Overview

The island of Ireland has **2 police bodies** that cianchosaint covers:

- **An Garda Síochána** (Republic of Ireland's national police)
- **Police Service of Northern Ireland** (PSNI)

The UK territorial forces (43 + BTP) are in
[`02-police-forces-uk.md`](02-police-forces-uk.md). The Crown
Dependencies forces (3) are in
[`04-police-forces-crown-dependencies.md`](04-police-forces-crown-dependencies.md).

## Sources

### An Garda Síochána (Ireland's national police)

- **URL**: https://www.garda.ie/
- **DLT source**: `dlt_sources/cianchosaint/ireland/policing/garda_press_releases.py` (planned, BIPP v1 m1)
- **OSINT allowlist**: yes
- **Coverage**: Garda press releases, Garda crime statistics, An
  Garda Síochána annual reports, recruitment
- **Update cadence**: daily (press releases)
- **Notes**: The canonical Irish police source. The BIPP v1 m1
  milestone unblocks once this DLT source is implemented.

### An Garda Síochána — CSO Ireland crime statistics

- **URL**: https://www.cso.ie/en/statistics/crimeandjustice/
- **DLT source**: `dlt_sources/cianchosaint/ireland/policing/cso_crime_ireland.py` (planned)
- **OSINT allowlist**: yes
- **Coverage**: Quarterly CSO Ireland crime + justice statistics
- **Update cadence**: quarterly
- **Notes**: The Irish counterpart to ONS crime statistics for England
  + Wales

### An Garda Síochána — Courts Service of Ireland

- **URL**: https://www.courts.ie/
- **DLT source**: `dlt_sources/cianchosaint/ireland/law/courts_ie.py` (wholesale-copied from Cianfhoghlaim)
- **OSINT allowlist**: yes
- **Coverage**: Court judgments, court lists, forms
- **Update cadence**: daily
- **Notes**: The Courts Service is the canonical Irish court source;
  also documented in [`08-courts-and-tribunals.md`](08-courts-and-tribunals.md)

### Irish Statute Book

- **URL**: https://www.irishstatutebook.ie/
- **DLT source**: `dlt_sources/cianchosaint/ireland/law/irish_statute_book.py` (wholesale-copied from Cianfhoghlaim)
- **OSINT allowlist**: yes
- **Coverage**: Every Act of the Oireachtas + every statutory instrument
- **Update cadence**: weekly
- **Notes**: The canonical Irish statutory source

### Police Service of Northern Ireland (PSNI)

- **URL**: https://www.psni.police.uk/
- **DLT source**: `dlt_sources/cianchosaint/ni/psni_press_releases.py`
- **OSINT allowlist**: yes
- **Coverage**: PSNI press releases, crime statistics, annual reports
- **Update cadence**: daily
- **Notes**: The PSNI is the only UK police force that is NOT in the
  data.police.uk API (separate jurisdiction + separate governance)

### NI Department of Justice

- **URL**: https://www.justice-ni.gov.uk/
- **DLT source**: `dlt_sources/cianchosaint/ni/justice_ni.py`
- **OSINT allowlist**: yes
- **Coverage**: NI Department of Justice publications, legislation,
  statistics
- **Update cadence**: weekly
- **Notes**: The devolved NI counterpart to the UK Ministry of Justice

### NI Policing Board

- **URL**: https://www.nipolicingboard.org.uk/
- **DLT source**: `dlt_sources/cianchosaint/ni/policing_board_ni.py`
- **OSINT allowlist**: yes
- **Coverage**: NI Policing Board oversight reports, annual reports,
  public meeting minutes
- **Update cadence**: monthly
- **Notes**: The independent oversight body for the PSNI (NI-specific)

## Gaps

- **Garda Inspectorate** (the body that inspects the Garda) is NOT YET
  WIRED. Follow-up `cianchosaint-garda-inspectorate-pipeline-v1`.
- **Police Ombudsman for Northern Ireland** (the independent complaints
  body for the PSNI) is NOT YET WIRED — covered in
  [`10-other-bodies.md`](10-other-bodies.md).
- **Garda Síochána Inspectorate annual reports** (separate from CSO
  stats) are NOT YET WIRED.

## References

- The canonical openspec spec:
  [`openspec/specs/cianchosaint-source-catalogue/spec.md`](../../../openspec/specs/cianchosaint-source-catalogue/spec.md)
- The per-constituency DLT sources spec:
  [`openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md`](../../../openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md)
- The OSINT allowlist:
  [`dlt_sources/cianchosaint/common/osint_allowlist.yaml`](../../../dlt_sources/cianchosaint/common/osint_allowlist.yaml)
- The per-constituency cohort registry:
  [`dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`](../../../dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py)
- The 5 GA + 5 PSNI specialist agents:
  [`agents/cianchosaint/ga_specialists/`](../../../agents/cianchosaint/ga_specialists/) +
  [`agents/cianchosaint/psni_specialists/`](../../../agents/cianchosaint/psni_specialists/)
