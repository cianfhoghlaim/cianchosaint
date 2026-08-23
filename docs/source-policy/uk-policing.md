# UK Policing — Per-Source Policy

> Per the
> [`openspec/changes/cianchosaint-source-policy-v1/`](../../openspec/changes/cianchosaint-source-policy-v1/specs/cianchosaint-source-policy/spec.md)
> spec. Covers the 5 UK policing DLT sources that ship under the
> [`cianchosaint-per-constituency-dlt-sources`](../../openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md)
> spec, Scenario: UK Policing sources.

## Overview

The 5 UK policing DLT sources form the BIPP v1 m2 milestone gate
(British Isles Policing Pipeline, milestone 2 — UK-wide). Together
they cover the 43 territorial England + Wales police forces + the 2
special forces (British Transport Police + Ministry of Defence
Police) + the Metropolitan Police.

## Sources

### data_police_uk — `data.police.uk` master API

- **DLT source file**: `dlt_sources/cianchosaint/uk/policing/data_police_uk.py`
- **OSINT allowlist**: yes (entry: `ig_username=uk_home_office_open_data`)
- **Source URL**: https://data.police.uk/docs/
- **Category**: `policing`
- **Body**: `UK Home Office (data.police.uk portal)`
- **Jurisdiction**: `uk`
- **OSINT ceiling**: `Public-facing open data only; personal data of officers and members of the public excluded beyond what's already in the published datasets`
- **Gaps**:
  - Northern Ireland forces (PSNI) are NOT covered by data.police.uk
    — separate source in `ni/policing/psni_press_releases.py`
  - Crown Dependencies forces (Jersey / Guernsey / Isle of Man) are NOT
    covered — separate sources under `crown_dependencies/policing/`
  - Scottish forces (Police Scotland) are NOT covered — handled by
    Police Scotland's own data portal (out of scope for cianchosaint v1)
  - Real-time / live crime data is NOT covered (the API only publishes
    data with a ~1-month lag)
- **BAML function**: `ExtractCrimeStatistics`
  (defined in
  `baml_src/cianchosaint/processing/met_police_extraction.baml`)
- **Milestone gate**: `BIPP v1 m2`

### metropolitan_police_press_releases — MET press releases

- **DLT source file**: `dlt_sources/cianchosaint/uk/policing/metropolitan_police_press_releases.py`
- **OSINT allowlist**: yes (entry: `ig_username=uk_metropolitan_police`)
- **Source URL**: https://www.met.police.uk/news/
- **Category**: `policing`
- **Body**: `Metropolitan Police Service (MET)`
- **Jurisdiction**: `uk`
- **OSINT ceiling**: `Public-facing press releases only; ongoing investigations and victim identities excluded`
- **Gaps**:
  - Internal MET briefings / operational orders are NOT covered
  - Historical press releases (>5 years) are NOT covered unless they
    are flagged as historically significant
  - Personal data of suspects / victims / officers is NOT processed
- **BAML function**: `ExtractPressRelease`
- **Milestone gate**: `BIPP v1 m2`

### stop_and_search_uk — Stop and search records

- **DLT source file**: `dlt_sources/cianchosaint/uk/policing/stop_and_search_uk.py`
- **OSINT allowlist**: yes (entry: `ig_username=uk_data_police_uk_api`)
- **Source URL**: https://data.police.uk/docs/method/stops-street/
- **Category**: `policing`
- **Body**: `UK Home Office (data.police.uk stop-and-search API)`
- **Jurisdiction**: `uk`
- **OSINT ceiling**: `Public-facing aggregate data only; PII of stopped individuals excluded by the Home Office's pre-publication redaction`
- **Gaps**:
  - Stop-and-search outcomes (arrest / no further action) are NOT
    separately recorded in the public API
  - Body-worn-camera footage is NOT in scope
  - Real-time / live stop-and-search data is NOT available
  - Per-officer stop-and-search patterns are NOT computed (would
    require joining with the workforce data, which is a v2 follow-up)
- **BAML function**: `ExtractStopAndSearchRecord`
  (defined in
  `baml_src/cianchosaint/processing/met_police_extraction.baml`)
- **Milestone gate**: `BIPP v1 m2`

### crime_statistics_uk — Force-level crime statistics

- **DLT source file**: `dlt_sources/cianchosaint/uk/policing/crime_statistics_uk.py`
- **OSINT allowlist**: yes (entry: `ig_username=uk_data_police_uk_api`)
- **Source URL**: https://data.police.uk/docs/method/crime-data/
- **Category**: `policing`
- **Body**: `UK Home Office (data.police.uk crime data API)`
- **Jurisdiction**: `uk`
- **OSINT ceiling**: `Public-facing aggregate data only; victim / suspect PII excluded by the API's response shape`
- **Gaps**:
  - Crime outcomes (charged / cautioned / etc.) are NOT included
    (separate API endpoint — v2 follow-up)
  - Victim / suspect demographics are NOT available
  - Reported vs unreported crime comparison is NOT computed
  - Historical crime data (>2 years) is NOT stored (only the rolling
    24-month window)
- **BAML function**: `ExtractCrimeStatistics`
- **Milestone gate**: `BIPP v1 m2`

### police_workforce_uk — Force-level workforce stats

- **DLT source file**: `dlt_sources/cianchosaint/uk/policing/police_workforce_uk.py`
- **OSINT allowlist**: yes (entry: `ig_username=uk_data_police_uk_api`)
- **Source URL**: https://data.police.uk/docs/method/workforce/
- **Category**: `policing`
- **Body**: `UK Home Office (data.police.uk workforce API)`
- **Jurisdiction**: `uk`
- **OSINT ceiling**: `Public-facing aggregate workforce data only; identifiable officer data excluded`
- **Gaps**:
  - Per-officer performance / disciplinary records are NOT covered
    (subject to FOI exemptions under the Police Act 1996)
  - Pay / grade detail beyond the published aggregate bands is NOT
    covered
  - Real-time workforce data is NOT available
- **BAML function**: `ExtractWorkforceStatistic`
- **Milestone gate**: `BIPP v1 m2`

## Cross-references

- The per-constituency DLT sources spec:
  [`openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md`](../../openspec/specs/cianchosaint-per-constituency-dlt-sources/spec.md)
- The CocoIndex v1 App:
  [`cocoindex_flows/cianchosaint/source_policy_aggregator.py`](../../cocoindex_flows/cianchosaint/source_policy_aggregator.py)
- The BAML extraction function catalog:
  [`baml_src/cianchosaint/processing/met_police_extraction.baml`](../../baml_src/cianchosaint/processing/met_police_extraction.baml)
- The cohort registry:
  [`dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`](../../dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py)
- The source-catalogue entry:
  [`docs/source-catalogue/02-police-forces-uk.md`](../source-catalogue/02-police-forces-uk.md)
- The OSINT allowlist:
  [`dlt_sources/cianchosaint/common/osint_allowlist.yaml`](../../dlt_sources/cianchosaint/common/osint_allowlist.yaml)
- The master per-source policy index:
  [`docs/source-policy/README.md`](README.md)

## Licence

BUSL-1.1 v2 (British-Isles-only) — see [`LICENSE.md`](../../LICENSE.md).
