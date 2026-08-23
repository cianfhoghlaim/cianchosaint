# 02 — UK Police Forces (England + Wales + Scotland)

> Per the [`openspec/changes/cianchosaint-british-isles-source-catalogue-v1/`](../../../openspec/changes/cianchosaint-british-isles-source-catalogue-v1/specs/cianchosaint-source-catalogue/spec.md) spec.

## Overview

The UK has 43 territorial police forces (England + Wales + Scotland) +
2 special forces (British Transport Police + Ministry of Defence Police) =
**45 police bodies**. The cianchosaint platform covers all 45 via the
`data.police.uk` API (the master API for all 43 territorial + BTP), plus
dedicated DLT sources for the Metropolitan Police press releases.

Northern Ireland is handled separately in
[`03-police-forces-ireland.md`](03-police-forces-ireland.md) (PSNI), and
the Crown Dependencies in
[`04-police-forces-crown-dependencies.md`](04-police-forces-crown-dependencies.md).

## Sources

### data.police.uk API (master — covers all 43 territorial + BTP)

- **URL**: https://data.police.uk/docs/
- **DLT source**: `dlt_sources/cianchosaint/uk/policing/data_police_uk.py`
- **OSINT allowlist**: yes
- **Coverage**: crime data, stop-and-search data, police workforce
  data, neighbourhood-level data for all 43 territorial forces + BTP
- **Update cadence**: monthly (the API is updated monthly with the
  previous month's data)
- **Notes**: The master ingest for the BIPP v1 m2 milestone; one API
  call covers all 43 forces

### Stop and search UK

- **URL**: https://data.police.uk/docs/method/stops-street/
- **DLT source**: `dlt_sources/cianchosaint/uk/policing/stop_and_search_uk.py`
- **OSINT allowlist**: yes
- **Coverage**: Stop and search records, with ethnicity flags + location
  data, for all 43 forces + BTP
- **Update cadence**: monthly
- **Notes**: Highly sensitive data; subject to consent gates in the
  citizen-facing surfaces

### Crime statistics UK (force-level)

- **URL**: https://data.police.uk/docs/method/crime-data/
- **DLT source**: `dlt_sources/cianchosaint/uk/policing/crime_statistics_uk.py`
- **OSINT allowlist**: yes
- **Coverage**: Force-level crime statistics, broken down by category
  (violence / burglary / vehicle crime / etc.) and by neighbourhood
- **Update cadence**: monthly
- **Notes**: Sub-resource of the data.police.uk API but elevated to its
  own DLT source for per-force indexing

### Police workforce UK

- **URL**: https://data.police.uk/docs/method/workforce/
- **DLT source**: `dlt_sources/cianchosaint/uk/policing/police_workforce_uk.py`
- **OSINT allowlist**: yes
- **Coverage**: Officer numbers + officer rank + diversity breakdown +
  leaver/starter rates per force
- **Update cadence**: quarterly
- **Notes**: Useful for the BIPP v1 workforce-trend analyses

### Metropolitan Police (MET) press releases

- **URL**: https://www.met.police.uk/news/
- **DLT source**: `dlt_sources/cianchosaint/uk/policing/metropolitan_police_press_releases.py`
- **OSINT allowlist**: yes
- **Coverage**: MET press releases (high volume — ~5-10 per week)
- **Update cadence**: daily
- **Notes**: The MET is the largest UK force; gets its own DLT source
  in addition to the data.police.uk coverage

### The 43 Territorial Forces (England + Wales)

The following 43 forces are all covered by the `data.police_uk.py`
master DLT source (one API, 43 forces):

#### England (39 forces)

- Avon and Somerset
- Bedfordshire
- Cambridgeshire
- Cheshire
- City of London
- Cleveland
- Cumbria
- Derbyshire
- Devon and Cornwall
- Dorset
- Durham
- Essex
- Gloucestershire
- Greater Manchester
- Hampshire
- Hertfordshire
- Humberside
- Kent
- Lancashire
- Leicestershire
- Lincolnshire
- Merseyside
- Metropolitan Police (separate DLT for press releases)
- Norfolk
- North Yorkshire
- Northamptonshire
- Northumbria
- Nottinghamshire
- South Yorkshire
- Staffordshire
- Suffolk
- Surrey
- Sussex
- Thames Valley
- Warwickshire
- West Mercia
- West Midlands
- West Yorkshire
- Wiltshire

#### Wales (4 forces)

- Dyfed-Powys
- Gwent
- North Wales
- South Wales

### British Transport Police (BTP)

- **URL**: https://www.btp.police.uk/
- **DLT source**: covered by `data_police_uk.py` (one API, BTP included)
- **OSINT allowlist**: yes
- **Coverage**: Crime data on the rail / London Underground network
- **Update cadence**: monthly
- **Notes**: Statutory special police force; not territorial but
  covered by data.police.uk

### Ministry of Defence Police (MDP)

- **URL**: https://www.gov.uk/government/organisations/ministry-of-defence-police
- **DLT source**: NOT YET WIRED
- **OSINT allowlist**: yes
- **Coverage**: MOD base security data; statutory special police force
- **Update cadence**: monthly
- **Notes**: NOT in the data.police.uk API; needs its own DLT source
  (planned: `ministry_of_defence_police.py`). Follow-up
  `cianchosaint-mdp-pipeline-v1`

### Scottish Police (single national force)

- **URL**: https://www.scotland.police.uk/
- **DLT source**: NOT YET WIRED (data.police.uk does not cover Scotland)
- **OSINT allowlist**: yes
- **Coverage**: Crime + stop-and-search data for Police Scotland (the
  single national Scottish force since 2013)
- **Update cadence**: monthly
- **Notes**: NOT in the data.police.uk API; needs its own DLT source
  via the Scottish Government open data portal. Follow-up
  `cianchosaint-scotland-policing-pipeline-v1`

## Gaps

- **Ministry of Defence Police** is NOT YET WIRED (no data.police.uk
  coverage). Follow-up `cianchosaint-mdp-pipeline-v1`.
- **Police Scotland** is NOT YET WIRED (data.police.uk is England + Wales
  only). Follow-up `cianchosaint-scotland-policing-pipeline-v1`.
- **Police Service of Northern Ireland (PSNI)** is in
  [`03-police-forces-ireland.md`](03-police-forces-ireland.md) (separate
  jurisdiction).

## References

- The canonical openspec spec:
  [`openspec/specs/cianchosaint-source-catalogue/spec.md`](../../../openspec/specs/cianchosaint-source-catalogue/spec.md)
- The per-constituency DLT sources spec:
  [`openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md`](../../../openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md)
- The OSINT allowlist:
  [`dlt_sources/cianchosaint/common/osint_allowlist.yaml`](../../../dlt_sources/cianchosaint/common/osint_allowlist.yaml)
- The per-constituency cohort registry:
  [`dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`](../../../dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py)
