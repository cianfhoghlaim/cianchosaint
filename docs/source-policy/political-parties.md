# Political Parties — Per-Source Policy

> Per the
> [`openspec/changes/cianchosaint-source-policy-v1/`](../../openspec/changes/cianchosaint-source-policy-v1/specs/cianchosaint-source-policy/spec.md)
> spec. Covers the 24 political party DLT sources that ship under the
> [`cianchosaint-political-party-pipeline`](../../openspec/specs/cianchosaint-political-party-pipeline/spec.md)
> spec.

## Overview

The 24 political party DLT sources cover the 24 active British Isles
political parties, split across 8 jurisdictions (UK HoC + ROI Dáil +
NI Assembly + Senedd + Holyrood + Jersey + Guernsey + Isle of Man).
Every party uses the shared `ExtractPartyPressRelease` BAML extraction
function defined in `baml_src/cianchosaint/processing/party.baml`.

The political party pipeline is the canonical input layer for the
`reform-uk-pilot-workflow` (per the
[`cianchosaint-reform-uk-pilot-workflow`](../../openspec/specs/cianchosaint-reform-uk-pilot-workflow/spec.md)
spec).

## Sources

### UK House of Commons (7 parties)

#### conservative_party_uk — Conservative and Unionist Party

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/uk/conservative_party_uk.py`
- **OSINT allowlist**: yes (entry: `ig_username=conservative_party_uk`)
- **Source URL**: https://www.conservatives.com/
- **Category**: `political_party`
- **Body**: `Conservative and Unionist Party`
- **Jurisdiction**: `uk_hoc`
- **OSINT ceiling**: `Public-facing press releases + policy papers; internal party documents excluded`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
  (defined in
  `baml_src/cianchosaint/processing/party.baml`)
- **Milestone gate**: `reform-uk-pilot-workflow`

#### labour_party_uk — Labour Party

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/uk/labour_party_uk.py`
- **OSINT allowlist**: yes (entry: `ig_username=labour_party_uk`)
- **Source URL**: https://labour.org.uk/
- **Category**: `political_party`
- **Body**: `Labour Party`
- **Jurisdiction**: `uk_hoc`
- **OSINT ceiling**: `Public-facing press releases + policy papers; internal party documents excluded`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### liberal_democrats_uk — Liberal Democrats

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/uk/liberal_democrats_uk.py`
- **OSINT allowlist**: yes (entry: `ig_username=liberal_democrats_uk`)
- **Source URL**: https://www.libdems.org.uk/
- **Category**: `political_party`
- **Body**: `Liberal Democrats`
- **Jurisdiction**: `uk_hoc`
- **OSINT ceiling**: `Public-facing press releases + policy papers; internal party documents excluded`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### reform_uk — Reform UK (the canonical pilot source)

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/uk/reform_uk.py`
- **OSINT allowlist**: yes (entry: `ig_username=reform_uk`)
- **Source URL**: https://www.reformparty.uk/news
- **Category**: `political_party`
- **Body**: `Reform UK`
- **Jurisdiction**: `uk_hoc`
- **OSINT ceiling**: `Public-facing press releases; Companies House donor data + Electoral Commission returns included via bulk ingest (follow-up change)`
- **Gaps**: Internal party communications / membership data excluded;
  donor PII redacted per UK GDPR + ICO guidance
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### green_party_ew — Green Party of England and Wales

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/uk/green_party_ew.py`
- **OSINT allowlist**: yes (entry: `ig_username=green_party_ew`)
- **Source URL**: https://greenparty.org.uk/
- **Category**: `political_party`
- **Body**: `Green Party of England and Wales`
- **Jurisdiction**: `uk_hoc`
- **OSINT ceiling**: `Public-facing press releases + policy papers; internal party documents excluded`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### snp — Scottish National Party

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/uk/snp.py`
- **OSINT allowlist**: yes (entry: `ig_username=snp`)
- **Source URL**: https://www.snp.org/
- **Category**: `political_party`
- **Body**: `Scottish National Party`
- **Jurisdiction**: `uk_hoc` + `scotland_holyrood`
- **OSINT ceiling**: `Public-facing press releases + policy papers; internal party documents excluded`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### plaid_cymru — Plaid Cymru

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/uk/plaid_cymru.py`
- **OSINT allowlist**: yes (entry: `ig_username=plaid_cymru`)
- **Source URL**: https://www.partyof.wales/
- **Category**: `political_party`
- **Body**: `Plaid Cymru`
- **Jurisdiction**: `uk_hoc` + `wales_senedd`
- **OSINT ceiling**: `Public-facing press releases + policy papers; Welsh-language summaries preserved verbatim`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

### Republic of Ireland (12 parties)

#### fianna_fail — Fianna Fáil

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/roi/fianna_fail.py`
- **OSINT allowlist**: yes (entry: `ig_username=fianna_fail`)
- **Source URL**: https://www.fiannafail.ie/
- **Category**: `political_party`
- **Body**: `Fianna Fáil`
- **Jurisdiction**: `roi_dail`
- **OSINT ceiling**: `Public-facing press releases + policy papers; Irish-language summaries preserved verbatim`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### fine_gael — Fine Gael

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/roi/fine_gael.py`
- **OSINT allowlist**: yes (entry: `ig_username=fine_gael`)
- **Source URL**: https://www.finegael.ie/
- **Category**: `political_party`
- **Body**: `Fine Gael`
- **Jurisdiction**: `roi_dail`
- **OSINT ceiling**: `Public-facing press releases + policy papers`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### sinn_fein_roi — Sinn Féin (ROI)

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/roi/sinn_fein_roi.py`
- **OSINT allowlist**: yes (entry: `ig_username=sinn_fein_roi`)
- **Source URL**: https://www.sinnfein.ie/
- **Category**: `political_party`
- **Body**: `Sinn Féin (Republic of Ireland)`
- **Jurisdiction**: `roi_dail` + `ni_assembly` (cross-listed; see also `ni/sinn_fein_ni.py`)
- **OSINT ceiling**: `Public-facing press releases + policy papers; Irish-language summaries preserved verbatim`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### labour_roi — Irish Labour Party

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/roi/labour_roi.py`
- **OSINT allowlist**: yes (entry: `ig_username=labour_roi`)
- **Source URL**: https://www.labour.ie/
- **Category**: `political_party`
- **Body**: `Irish Labour Party`
- **Jurisdiction**: `roi_dail`
- **OSINT ceiling**: `Public-facing press releases + policy papers`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### social_democrats — Social Democrats

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/roi/social_democrats.py`
- **OSINT allowlist**: yes (entry: `ig_username=social_democrats`)
- **Source URL**: https://www.socialdemocrats.ie/
- **Category**: `political_party`
- **Body**: `Social Democrats`
- **Jurisdiction**: `roi_dail`
- **OSINT ceiling**: `Public-facing press releases + policy papers`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### green_party_roi — Green Party / Comhaontas Glas

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/roi/green_party_roi.py`
- **OSINT allowlist**: yes (entry: `ig_username=green_party_roi`)
- **Source URL**: https://www.greenparty.ie/
- **Category**: `political_party`
- **Body**: `Green Party / Comhaontas Glas`
- **Jurisdiction**: `roi_dail`
- **OSINT ceiling**: `Public-facing press releases + policy papers; Irish-language summaries preserved verbatim`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### pbp_solidarity — People Before Profit–Solidarity

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/roi/pbp_solidarity.py`
- **OSINT allowlist**: yes (entry: `ig_username=pbp_solidarity`)
- **Source URL**: https://www.pbp.ie/
- **Category**: `political_party`
- **Body**: `People Before Profit–Solidarity`
- **Jurisdiction**: `roi_dail`
- **OSINT ceiling**: `Public-facing press releases + policy papers`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### aontu — Aontú

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/roi/aontu.py`
- **OSINT allowlist**: yes (entry: `ig_username=aontu`)
- **Source URL**: https://aontu.ie/
- **Category**: `political_party`
- **Body**: `Aontú`
- **Jurisdiction**: `roi_dail`
- **OSINT ceiling**: `Public-facing press releases + policy papers; Irish-language summaries preserved verbatim`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### irish_freedom_party — Irish Freedom Party

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/roi/irish_freedom_party.py`
- **OSINT allowlist**: yes (entry: `ig_username=irish_freedom_party`)
- **Source URL**: https://irishfreedomparty.ie/
- **Category**: `political_party`
- **Body**: `Irish Freedom Party`
- **Jurisdiction**: `roi_dail`
- **OSINT ceiling**: `Public-facing press releases + policy papers`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### national_party_roi — National Party

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/roi/national_party_roi.py`
- **OSINT allowlist**: yes (entry: `ig_username=national_party_roi`)
- **Source URL**: https://nationalparty.ie/
- **Category**: `political_party`
- **Body**: `National Party`
- **Jurisdiction**: `roi_dail`
- **OSINT ceiling**: `Public-facing press releases + policy papers`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### independent_ireland — Independent Ireland

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/roi/independent_ireland.py`
- **OSINT allowlist**: yes (entry: `ig_username=independent_ireland`)
- **Source URL**: https://independentireland.ie/
- **Category**: `political_party`
- **Body**: `Independent Ireland`
- **Jurisdiction**: `roi_dail`
- **OSINT ceiling**: `Public-facing press releases + policy papers`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### rise_roi — Rise / Republican Party

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/roi/rise_roi.py`
- **OSINT allowlist**: yes (entry: `ig_username=rise_roi`)
- **Source URL**: https://riseparty.ie/
- **Category**: `political_party`
- **Body**: `Rise / Republican Party`
- **Jurisdiction**: `roi_dail`
- **OSINT ceiling**: `Public-facing press releases + policy papers`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

### Northern Ireland Assembly (7 parties)

#### dup — Democratic Unionist Party

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/ni/dup.py`
- **OSINT allowlist**: yes (entry: `ig_username=dup`)
- **Source URL**: https://mydup.com/
- **Category**: `political_party`
- **Body**: `Democratic Unionist Party`
- **Jurisdiction**: `ni_assembly`
- **OSINT ceiling**: `Public-facing press releases + policy papers`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### sinn_fein_ni — Sinn Féin (NI)

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/ni/sinn_fein_ni.py`
- **OSINT allowlist**: yes (entry: `ig_username=sinn_fein_ni`)
- **Source URL**: https://sinnfein.ie/ni/
- **Category**: `political_party`
- **Body**: `Sinn Féin (Northern Ireland)`
- **Jurisdiction**: `ni_assembly`
- **OSINT ceiling**: `Public-facing press releases + policy papers; Irish-language summaries preserved verbatim`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### alliance_ni — Alliance Party

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/ni/alliance_ni.py`
- **OSINT allowlist**: yes (entry: `ig_username=alliance_ni`)
- **Source URL**: https://www.allianceparty.org/
- **Category**: `political_party`
- **Body**: `Alliance Party of Northern Ireland`
- **Jurisdiction**: `ni_assembly`
- **OSINT ceiling**: `Public-facing press releases + policy papers`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### uup — Ulster Unionist Party

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/ni/uup.py`
- **OSINT allowlist**: yes (entry: `ig_username=uup`)
- **Source URL**: https://uup.org/
- **Category**: `political_party`
- **Body**: `Ulster Unionist Party`
- **Jurisdiction**: `ni_assembly`
- **OSINT ceiling**: `Public-facing press releases + policy papers`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### sdlp — Social Democratic and Labour Party

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/ni/sdlp.py`
- **OSINT allowlist**: yes (entry: `ig_username=sdlp`)
- **Source URL**: https://sdlp.ie/
- **Category**: `political_party`
- **Body**: `Social Democratic and Labour Party`
- **Jurisdiction**: `ni_assembly`
- **OSINT ceiling**: `Public-facing press releases + policy papers; Irish-language summaries preserved verbatim`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### tuv_ni — Traditional Unionist Voice

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/ni/tuv_ni.py`
- **OSINT allowlist**: yes (entry: `ig_username=tuv_ni`)
- **Source URL**: https://tuvni.com/
- **Category**: `political_party`
- **Body**: `Traditional Unionist Voice`
- **Jurisdiction**: `ni_assembly`
- **OSINT ceiling**: `Public-facing press releases + policy papers`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### pbp_ni — People Before Profit (NI)

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/ni/pbp_ni.py`
- **OSINT allowlist**: yes (entry: `ig_username=pbp_ni`)
- **Source URL**: https://pbpni.com/
- **Category**: `political_party`
- **Body**: `People Before Profit (Northern Ireland)`
- **Jurisdiction**: `ni_assembly`
- **OSINT ceiling**: `Public-facing press releases + policy papers`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

### Wales Senedd (4 parties — Plaid Cymru already counted above)

#### labour_wales — Welsh Labour

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/wales/labour_wales.py`
- **OSINT allowlist**: yes (entry: `ig_username=labour_wales`)
- **Source URL**: https://www.welshlabour.wales/
- **Category**: `political_party`
- **Body**: `Welsh Labour`
- **Jurisdiction**: `wales_senedd`
- **OSINT ceiling**: `Public-facing press releases + policy papers; Welsh-language summaries preserved verbatim`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### conservative_wales — Welsh Conservatives

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/wales/conservative_wales.py`
- **OSINT allowlist**: yes (entry: `ig_username=conservative_wales`)
- **Source URL**: https://www.conservatives.wales/
- **Category**: `political_party`
- **Body**: `Welsh Conservatives`
- **Jurisdiction**: `wales_senedd`
- **OSINT ceiling**: `Public-facing press releases + policy papers; Welsh-language summaries preserved verbatim`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### liberal_democrats_wales — Welsh Liberal Democrats

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/wales/liberal_democrats_wales.py`
- **OSINT allowlist**: yes (entry: `ig_username=liberal_democrats_wales`)
- **Source URL**: https://www.welshlibdems.wales/
- **Category**: `political_party`
- **Body**: `Welsh Liberal Democrats`
- **Jurisdiction**: `wales_senedd`
- **OSINT ceiling**: `Public-facing press releases + policy papers; Welsh-language summaries preserved verbatim`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### plaid_cymru_senedd — Plaid Cymru (Senedd)

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/wales/plaid_cymru_senedd.py`
- **OSINT allowlist**: yes (entry: `ig_username=plaid_cymru_senedd`)
- **Source URL**: https://www.partyof.wales/senedd/
- **Category**: `political_party`
- **Body**: `Plaid Cymru (Senedd delegation)`
- **Jurisdiction**: `wales_senedd`
- **OSINT ceiling**: `Public-facing press releases + policy papers; Welsh-language summaries preserved verbatim`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

### Scotland Holyrood (5 parties — SNP already counted above)

#### scottish_labour — Scottish Labour

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/scotland/scottish_labour.py`
- **OSINT allowlist**: yes (entry: `ig_username=scottish_labour`)
- **Source URL**: https://www.scottishlabour.org.uk/
- **Category**: `political_party`
- **Body**: `Scottish Labour`
- **Jurisdiction**: `scotland_holyrood`
- **OSINT ceiling**: `Public-facing press releases + policy papers`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### scottish_conservatives — Scottish Conservatives

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/scotland/scottish_conservatives.py`
- **OSINT allowlist**: yes (entry: `ig_username=scottish_conservatives`)
- **Source URL**: https://www.scottishconservatives.com/
- **Category**: `political_party`
- **Body**: `Scottish Conservatives`
- **Jurisdiction**: `scotland_holyrood`
- **OSINT ceiling**: `Public-facing press releases + policy papers`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### scottish_liberal_democrats — Scottish Liberal Democrats

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/scotland/scottish_liberal_democrats.py`
- **OSINT allowlist**: yes (entry: `ig_username=scottish_liberal_democrats`)
- **Source URL**: https://www.scotlibdems.org.uk/
- **Category**: `political_party`
- **Body**: `Scottish Liberal Democrats`
- **Jurisdiction**: `scotland_holyrood`
- **OSINT ceiling**: `Public-facing press releases + policy papers`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### scottish_greens — Scottish Greens

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/scotland/scottish_greens.py`
- **OSINT allowlist**: yes (entry: `ig_username=scottish_greens`)
- **Source URL**: https://greens.scot/
- **Category**: `political_party`
- **Body**: `Scottish Greens`
- **Jurisdiction**: `scotland_holyrood`
- **OSINT ceiling**: `Public-facing press releases + policy papers`
- **Gaps**: Internal party communications / membership data excluded
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

### Crown Dependencies (3 parties)

#### jersey_party — Jersey (active parties)

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/crown_dependencies/jersey_party.py`
- **OSINT allowlist**: yes (entry: `ig_username=jersey_party`)
- **Source URL**: https://www.gov.je/government/pages/politicalparties.aspx
- **Category**: `political_party`
- **Body**: `Active Jersey political parties (aggregate)`
- **Jurisdiction**: `jsy`
- **OSINT ceiling**: `Public-facing party press releases; the Jersey OSINT allowlist covers the 3 active parties (Reform Jersey, Jersey Liberal Conservatives, etc.)`
- **Gaps**: Per-party press releases are aggregated at the Jersey
  government level (no per-party DLT source yet)
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### guernsey_party — Guernsey (active parties)

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/crown_dependencies/guernsey_party.py`
- **OSINT allowlist**: yes (entry: `ig_username=guernsey_party`)
- **Source URL**: https://www.gov.gg/politicalparties
- **Category**: `political_party`
- **Body**: `Active Guernsey political parties (aggregate)`
- **Jurisdiction**: `ggy`
- **OSINT ceiling**: `Public-facing party press releases`
- **Gaps**: Per-party press releases are aggregated at the Guernsey
  government level (no per-party DLT source yet)
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

#### iom_party — Isle of Man (active parties)

- **DLT source file**: `dlt_sources/cianchosaint/political_parties/crown_dependencies/iom_party.py`
- **OSINT allowlist**: yes (entry: `ig_username=iom_party`)
- **Source URL**: https://www.gov.im/categories/political-parties/
- **Category**: `political_party`
- **Body**: `Active Isle of Man political parties (aggregate)`
- **Jurisdiction**: `iom`
- **OSINT ceiling**: `Public-facing party press releases`
- **Gaps**: Per-party press releases are aggregated at the IoM
  government level (no per-party DLT source yet)
- **BAML function**: `ExtractPartyPressRelease`
- **Milestone gate**: `reform-uk-pilot-workflow`

## Cross-references

- The political party pipeline spec:
  [`openspec/specs/cianchosaint-political-party-pipeline/spec.md`](../../openspec/specs/cianchosaint-political-party-pipeline/spec.md)
- The CocoIndex v1 App:
  [`cocoindex_flows/cianchosaint/source_policy_aggregator.py`](../../cocoindex_flows/cianchosaint/source_policy_aggregator.py)
- The shared BAML extraction function:
  [`baml_src/cianchosaint/processing/party.baml`](../../baml_src/cianchosaint/processing/party.baml)
- The political parties cohort registry:
  [`dlt_sources/cianchosaint/political_parties/_registry.py`](../../dlt_sources/cianchosaint/political_parties/_registry.py)
- The Reform UK pilot workflow spec:
  [`openspec/specs/cianchosaint-reform-uk-pilot-workflow/spec.md`](../../openspec/specs/cianchosaint-reform-uk-pilot-workflow/spec.md)
- The source-catalogue entry:
  [`docs/source-catalogue/09-political-parties.md`](../source-catalogue/09-political-parties.md)
- The OSINT allowlist entries:
  [`dlt_sources/official_media_cianchosaint/fixtures/allowlist_parties.yaml`](../../dlt_sources/official_media_cianchosaint/fixtures/allowlist_parties.yaml)
- The master per-source policy index:
  [`docs/source-policy/README.md`](README.md)

## Licence

BUSL-1.1 v2 (British-Isles-only) — see [`LICENSE.md`](../../LICENSE.md).
