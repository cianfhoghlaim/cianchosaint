# 07 — Key Government Departments (UK + Devolved + Crown Dependencies)

> Per the [`openspec/changes/cianchosaint-british-isles-source-catalogue-v1/`](../../../openspec/changes/cianchosaint-british-isles-source-catalogue-v1/specs/cianchosaint-source-catalogue/spec.md) spec.

## Overview

This file documents the **key government departments** that cianchosaint
relates to across all 4 UK jurisdictions (England + Wales + Scotland +
Northern Ireland) + the 3 Crown Dependencies (Jersey + Guernsey + Isle
of Man) + the Republic of Ireland.

The 12 departments are grouped into:

- **7 UK central government departments** (Home Office, MoJ, FCDO, MoD,
  HMRC, Cabinet Office, DSIT)
- **3 devolved legislatures + executives** (NI Executive, Welsh
  Government, Scottish Government)
- **3 Crown Dependencies governments** (States of Jersey, States of
  Guernsey, Isle of Man Government)
- Plus: the **ROI Department of Defence** (covered in
  [`06-armed-forces-ireland.md`](06-armed-forces-ireland.md))

## Sources

### UK Central Government Departments

#### Home Office

- **URL**: https://www.gov.uk/government/organisations/home-office
- **DLT source**: `dlt_sources/cianchosaint/uk/government/home_office_statistics.py`
- **OSINT allowlist**: yes
- **Coverage**: Home Office statistics (knife crime, drug offences,
  police powers, immigration), policy papers, press releases
- **Update cadence**: quarterly (statistics)
- **Notes**: The lead UK department for policing + counter-terrorism +
  immigration

#### Ministry of Justice (MoJ)

- **URL**: https://www.gov.uk/government/organisations/ministry-of-justice
- **DLT source**: `dlt_sources/cianchosaint/uk/government/moj_statistics.py`
- **OSINT allowlist**: yes
- **Coverage**: MoJ statistics (prison population, court caseload,
  reoffending), policy papers, press releases
- **Update cadence**: quarterly (statistics)
- **Notes**: The lead UK department for the courts + prisons + probation

#### Foreign, Commonwealth & Development Office (FCDO)

- **URL**: https://www.gov.uk/government/organisations/foreign-commonwealth-development-office
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: FCDO press releases (UK political statements on
  international affairs), policy papers, treaties
- **Update cadence**: daily
- **Notes**: NOT YET WIRED — the BIPP v1 + BIDP v1 milestones are
  primarily UK-domestic, so FCDO is de-prioritised. Follow-up
  `cianchosaint-fcdo-pipeline-v1`.

#### Ministry of Defence (MoD)

- **URL**: https://www.gov.uk/government/organisations/ministry-of-defence
- **DLT source**: covered by `uk/military/mod_press_releases.py` (see
  [`05-armed-forces-uk.md`](05-armed-forces-uk.md))
- **OSINT allowlist**: yes
- **Coverage**: MoD press releases, defence policy papers, defence
  procurement
- **Update cadence**: daily
- **Notes**: Cross-referenced in [`05-armed-forces-uk.md`](05-armed-forces-uk.md)

#### HM Revenue & Customs (HMRC)

- **URL**: https://www.gov.uk/government/organisations/hm-revenue-customs
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: HMRC statistics + policy papers
- **Update cadence**: quarterly (statistics)
- **Notes**: NOT YET WIRED — relevant for the financial-crime
  investigation use cases. Follow-up `cianchosaint-hmrc-pipeline-v1`.

#### Cabinet Office

- **URL**: https://www.gov.uk/government/organisations/cabinet-office
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: Cabinet Office policy papers, civil service reform
  papers, Crown Commercial Service notices
- **Update cadence**: monthly
- **Notes**: NOT YET WIRED — relevant for the procurement + governance
  use cases. Follow-up `cianchosaint-cabinet-office-pipeline-v1`.

#### Department for Science, Innovation and Technology (DSIT)

- **URL**: https://www.gov.uk/government/organisations/department-for-science-innovation-and-technology
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: DSIT policy papers (AI safety, online safety, cyber
  security)
- **Update cadence**: monthly
- **Notes**: NOT YET WIRED — relevant for the AI safety + cyber
  security verticals. Follow-up `cianchosaint-dsit-pipeline-v1`.

### Devolved Legislatures + Executives

#### Northern Ireland Executive

- **URL**: https://www.northernireland.gov.uk/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: NI Executive press releases, programme for government,
  budget papers
- **Update cadence**: weekly
- **Notes**: NOT YET WIRED — relevant for the devolved-policing +
  devolved-justice verticals. Follow-up
  `cianchosaint-ni-executive-pipeline-v1`.

#### Northern Ireland Assembly

- **URL**: https://www.niassembly.gov.uk/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: NI Assembly debates, Hansard, committee reports
- **Update cadence**: daily
- **Notes**: NOT YET WIRED — relevant for the devolved-justice
  vertical. Follow-up `cianchosaint-ni-assembly-pipeline-v1`.

#### Welsh Government

- **URL**: https://www.gov.wales/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: Welsh Government press releases, policy papers,
  legislation
- **Update cadence**: weekly
- **Notes**: NOT YET WIRED — follow-up
  `cianchosaint-welsh-gov-pipeline-v1`.

#### Senedd (Welsh Parliament)

- **URL**: https://senedd.wales/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: Senedd debates, Members statements, committee reports
- **Update cadence**: daily
- **Notes**: NOT YET WIRED — covered separately in
  [`10-other-bodies.md`](10-other-bodies.md) under Senedd Research

#### Scottish Government

- **URL**: https://www.gov.scot/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: Scottish Government press releases, policy papers,
  legislation
- **Update cadence**: weekly
- **Notes**: NOT YET WIRED — follow-up
  `cianchosaint-scottish-gov-pipeline-v1`.

#### Scottish Parliament

- **URL**: https://www.parliament.scot/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: Holyrood debates, Members statements, committee reports
- **Update cadence**: daily
- **Notes**: NOT YET WIRED — follow-up
  `cianchosaint-holyrood-pipeline-v1`.

### Crown Dependencies Governments

#### States of Jersey

- **URL**: https://www.gov.je/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: States of Jersey government press releases, legislation
- **Update cadence**: weekly
- **Notes**: NOT YET WIRED — follow-up
  `cianchosaint-crown-deps-extra-v1`

#### States of Guernsey

- **URL**: https://www.gov.gg/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: States of Guernsey government press releases,
  legislation
- **Update cadence**: weekly
- **Notes**: NOT YET WIRED — follow-up
  `cianchosaint-crown-deps-extra-v1`

#### Isle of Man Government

- **URL**: https://www.gov.im/
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: Isle of Man Government press releases, legislation,
  Tynwald proceedings
- **Update cadence**: weekly
- **Notes**: NOT YET WIRED — follow-up
  `cianchosaint-crown-deps-extra-v1`

### Republic of Ireland

#### Department of Defence (ROI)

- **URL**: https://www.gov.ie/en/organisation/department-of-defence/
- **DLT source**: covered by
  `ireland/defence_forces/idf_press_releases.py` (see
  [`06-armed-forces-ireland.md`](06-armed-forces-ireland.md))
- **OSINT allowlist**: yes
- **Coverage**: ROI Department of Defence press releases, policy
  papers, White Paper on Defence
- **Update cadence**: weekly
- **Notes**: The ROI parent department for the Defence Forces

## Gaps

The **majority** of UK + devolved + Crown Dependencies government
departments are NOT YET WIRED. The follow-up changes:

- `cianchosaint-fcdo-pipeline-v1` — FCDO
- `cianchosaint-hmrc-pipeline-v1` — HMRC
- `cianchosaint-cabinet-office-pipeline-v1` — Cabinet Office
- `cianchosaint-dsit-pipeline-v1` — DSIT
- `cianchosaint-ni-executive-pipeline-v1` — NI Executive
- `cianchosaint-ni-assembly-pipeline-v1` — NI Assembly
- `cianchosaint-welsh-gov-pipeline-v1` — Welsh Government
- `cianchosaint-scottish-gov-pipeline-v1` — Scottish Government
- `cianchosaint-holyrood-pipeline-v1` — Scottish Parliament
- `cianchosaint-crown-deps-extra-v1` — States of Jersey + States of
  Guernsey + Isle of Man Government

## References

- The canonical openspec spec:
  [`openspec/specs/cianchosaint-source-catalogue/spec.md`](../../../openspec/specs/cianchosaint-source-catalogue/spec.md)
- The per-constituency DLT sources spec:
  [`openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md`](../../../openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md)
- The OSINT allowlist:
  [`dlt_sources/cianchosaint/common/osint_allowlist.yaml`](../../../dlt_sources/cianchosaint/common/osint_allowlist.yaml)
- The per-constituency cohort registry:
  [`dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`](../../../dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py)
