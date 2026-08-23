# 10 — Other Bodies (ICO, NAO, C&AG, HoC Library, Senedd Research, Electoral Commission, etc.)

> Per the [`openspec/changes/cianchosaint-british-isles-source-catalogue-v1/`](../../../openspec/changes/cianchosaint-british-isles-source-catalogue-v1/specs/cianchosaint-source-catalogue/spec.md) spec.

## Overview

This file documents the **~15 other British Isles public-sector bodies**
that cianchosaint relates to but which don't fit neatly into the other
9 categories. These are:

- **3 audit / accountability bodies**: NAO, C&AG (ROI), Audit NI
- **2 information-rights bodies**: ICO, plus the Information
  Commissioner for Scotland (separate from the ICO)
- **2 ombudsman bodies**: Police Ombudsman for Northern Ireland, Office
  of the Police Ombudsman for Scotland
- **2 library / research services**: House of Commons Library, Senedd
  Research
- **1 election regulator**: Electoral Commission (UK)
- **1 press regulator**: IPSO (Independent Press Standards Organisation)
- **1 policing inspectorate**: HM Inspectorate of Constabulary (HMICFRS)
- **2 standards bodies**: Committee on Standards in Public Life (CSPL),
  Public Standards Board for Scotland
- **1 inspector of prosecution**: Crown Prosecution Service Inspectorate

The cianchosaint platform documents these bodies here but most of the
DLT source implementations are NOT YET WIRED. They are listed in the
`## Gaps` section of each entry, with the follow-up openspec change
that would close the gap.

## Sources

### National Audit Office (NAO)

- **URL**: https://www.nao.org.uk/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: NAO value-for-money reports, investigations, briefings
- **Update cadence**: weekly
- **Notes**: NOT YET WIRED — follow-up `cianchosaint-nao-pipeline-v1`

### Comptroller and Auditor General (C&AG, ROI)

- **URL**: https://www.audit.gov.ie/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: C&AG annual reports, value-for-money reviews
- **Update cadence**: annually
- **Notes**: NOT YET WIRED — follow-up
  `cianchosaint-cag-pipeline-v1`

### Northern Ireland Audit Office (NIAO)

- **URL**: https://www.niauditoffice.gov.uk/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: NIAO value-for-money reports
- **Update cadence**: annually
- **Notes**: NOT YET WIRED — follow-up
  `cianchosaint-niao-pipeline-v1`

### Information Commissioner's Office (ICO)

- **URL**: https://ico.org.uk/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: ICO enforcement notices, FOI decision notices, data
  protection guidance
- **Update cadence**: weekly
- **Notes**: NOT YET WIRED — relevant for the FOIA / data protection
  investigation use cases. Follow-up `cianchosaint-ico-pipeline-v1`

### Information Commissioner for Scotland (ICS)

- **URL**: https://www.itspublicknowledge.info/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: ICS enforcement notices, FOI decision notices
- **Update cadence**: weekly
- **Notes**: NOT YET WIRED — Scotland has its own FOI regime

### Police Ombudsman for Northern Ireland

- **URL**: https://www.policeombudsman.org/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: Police Ombudsman investigation outcomes, annual
  reports
- **Update cadence**: monthly
- **Notes**: NOT YET WIRED — the NI counterpart to the IOPC

### Office of the Police Ombudsman for Scotland

- **URL**: https://www.pescad.org/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: Police Ombudsman investigation outcomes, annual
  reports
- **Update cadence**: monthly
- **Notes**: NOT YET WIRED — the Scottish counterpart to the IOPC

### House of Commons Library

- **URL**: https://commonslibrary.parliament.uk/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: HoC Library research briefings, debate packs,
  insight articles
- **Update cadence**: daily
- **Notes**: NOT YET WIRED — the authoritative source of UK
  parliamentary research

### Senedd Research

- **URL**: https://research.senedd.wales/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: Senedd Research briefings, infographics
- **Update cadence**: weekly
- **Notes**: NOT YET WIRED — the Senedd counterpart to the HoC
  Library

### Electoral Commission (UK)

- **URL**: https://www.electoralcommission.org.uk/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: Electoral Commission registers (political parties,
  donations, campaign spending), guidance
- **Update cadence**: weekly
- **Notes**: NOT YET WIRED — relevant for the donor-filings use
  cases. Follow-up `cianchosaint-electoral-commission-v1`

### Independent Press Standards Organisation (IPSO)

- **URL**: https://www.ipso.co.uk/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: IPSO rulings on press complaints
- **Update cadence**: weekly
- **Notes**: NOT YET WIRED — the UK press regulator (covers most
  major UK newspapers + magazines)

### HM Inspectorate of Constabulary (HMICFRS)

- **URL**: https://hmicfrs.justiceinspectorates.gov.uk/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: HMICFRS inspection reports (force-level + thematic),
  annual State of Policing report
- **Update cadence**: monthly
- **Notes**: NOT YET WIRED — the independent inspector of police
  forces in England + Wales (now covers fire + rescue too)

### Committee on Standards in Public Life (CSPL)

- **URL**: https://www.gov.uk/government/organisations/committee-on-standards-in-public-life
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: CSPL reports on standards in public life,
  consultations
- **Update cadence**: annually
- **Notes**: NOT YET WIRED — relevant for the standards / ethics
  investigation use cases

### Public Standards Board for Scotland

- **URL**: https://www.ethicalstandards.org.uk/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: Public Standards Board reports on standards in public
  life in Scotland
- **Update cadence**: annually
- **Notes**: NOT YET WIRED — the Scottish counterpart to the CSPL

### Crown Prosecution Service Inspectorate (CPSI)

- **URL**: https://www.justiceinspectorates.gov.uk/cpsi/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: CPSI inspection reports on the CPS
- **Update cadence**: annually
- **Notes**: NOT YET WIRED — the inspector of the CPS

## Gaps

The **majority** of `10-other-bodies.md` is NOT YET WIRED. The
follow-up changes:

- `cianchosaint-nao-pipeline-v1` — National Audit Office
- `cianchosaint-cag-pipeline-v1` — C&AG (ROI)
- `cianchosaint-niao-pipeline-v1` — NIAO
- `cianchosaint-ico-pipeline-v1` — ICO + ICS
- `cianchosaint-police-ombudsman-v1` — PONI + OPOS
- `cianchosaint-parliamentary-library-v1` — HoC Library + Senedd
  Research + Holyroad Research
- `cianchosaint-electoral-commission-v1` — Electoral Commission
- `cianchosaint-ipso-pipeline-v1` — IPSO
- `cianchosaint-hmicfrs-pipeline-v1` — HMICFRS
- `cianchosaint-standards-v1` — CSPL + Public Standards Board for
  Scotland
- `cianchosaint-cpsi-pipeline-v1` — CPSI

## References

- The canonical openspec spec:
  [`openspec/specs/cianchosaint-source-catalogue/spec.md`](../../../openspec/specs/cianchosaint-source-catalogue/spec.md)
- The per-constituency DLT sources spec:
  [`openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md`](../../../openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md)
- The political-party pipeline spec:
  [`openspec/specs/cianchosaint-political-party-pipeline/spec.md`](../../../openspec/specs/cianchosaint-political-party-pipeline/spec.md)
- The OSINT allowlist:
  [`dlt_sources/cianchosaint/common/osint_allowlist.yaml`](../../../dlt_sources/cianchosaint/common/osint_allowlist.yaml)
- The per-constituency cohort registry:
  [`dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`](../../../dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py)
- The per-political-party registry:
  [`dlt_sources/cianchosaint/political_parties/_registry.py`](../../../dlt_sources/cianchosaint/political_parties/_registry.py)
