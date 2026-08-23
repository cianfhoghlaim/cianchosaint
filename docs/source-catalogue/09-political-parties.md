# 09 — Political Parties (the 24 in the OSINT allowlist)

> Per the [`openspec/changes/cianchosaint-british-isles-source-catalogue-v1/`](../../../openspec/changes/cianchosaint-british-isles-source-catalogue-v1/specs/cianchosaint-source-catalogue/spec.md) spec.

## Overview

The cianchosaint platform ingests from **24 active political parties**
across the British Isles, per the
[`cianchosaint-political-party-pipeline`](../../../openspec/specs/cianchosaint-political-party-pipeline/spec.md)
spec. The parties are organised into **6 jurisdictions**:

- **7 UK House of Commons parties** (the 24 active parties minus the
  devolved-only ones)
- **12 Republic of Ireland parties** (Dáil + Seanad)
- **7 Northern Ireland Assembly parties**
- **4 Wales Senedd parties** (the 4 largest — Plaid Cymru also has
  UK HoC representation)
- **5 Scotland Holyrood parties** (the 5 largest — SNP also has UK
  HoC representation)
- **3 Crown Dependencies parties** (Jersey + Guernsey + Isle of Man)

The full per-party cohort grid lives in
[`dlt_sources/cianchosaint/political_parties/_registry.py`](../../../dlt_sources/cianchosaint/political_parties/_registry.py).

The 24 parties are enumerated below. Each party appears under its
primary jurisdiction; parties with representation in multiple
jurisdictions (e.g. Plaid Cymru in UK HoC + Senedd, SNP in UK HoC +
Holyrood, Sinn Féin in ROI + NI) are listed once.

## Sources

### UK House of Commons (7 parties)

#### Conservative and Unionist Party

- **URL**: https://www.conservatives.com/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/uk/conservative_party_uk.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, leadership statements
- **Update cadence**: daily
- **Notes**: Electoral Commission ID PP-10125

#### Labour Party

- **URL**: https://labour.org.uk/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/uk/labour_party_uk.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, leadership statements
- **Update cadence**: daily
- **Notes**: Electoral Commission ID PP-10123

#### Liberal Democrats

- **URL**: https://www.libdems.org.uk/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/uk/liberal_democrats_uk.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, leadership statements
- **Update cadence**: daily
- **Notes**: Electoral Commission ID PP-10124

#### Reform UK (the canonical pilot)

- **URL**: https://www.reformparty.uk/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/uk/reform_uk.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, leadership statements
- **Update cadence**: daily
- **Notes**: The canonical pilot source for the reform-uk-pilot-workflow
  use case (per the Q12 = B decision). Electoral Commission ID
  (to be verified — PP-12345 placeholder)

#### Green Party of England and Wales

- **URL**: https://www.greenparty.org.uk/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/uk/green_party_ew.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, conference motions
- **Update cadence**: weekly
- **Notes**: Distinct from the Scottish Greens (who are a separate
  party). Electoral Commission ID PP-10128

#### Plaid Cymru (UK HoC)

- **URL**: https://www.partyofwales.org/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/uk/plaid_cymru.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, leadership statements
- **Update cadence**: daily
- **Notes**: Plaid Cymru has BOTH UK HoC representation AND Senedd
  representation — they share the party_id but ship different scope
  files (`plaid_cymru.py` vs `plaid_cymru_senedd.py`)

#### Scottish National Party (UK HoC)

- **URL**: https://www.snp.org/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/uk/snp.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, leadership statements
- **Update cadence**: daily
- **Notes**: SNP has BOTH UK HoC representation AND Holyrood
  representation — they share the party_id but ship different scope
  files (`snp.py` vs `snp_scottish.py`)

### Republic of Ireland (12 parties)

#### Fianna Fáil

- **URL**: https://www.fiannafail.ie/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/roi/fianna_fail.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Dáil statements
- **Update cadence**: daily
- **Notes**: Irish Electoral Commission ID (to be verified)

#### Fine Gael

- **URL**: https://www.finegael.ie/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/roi/fine_gael.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Dáil statements
- **Update cadence**: daily
- **Notes**: Irish Electoral Commission ID (to be verified)

#### Sinn Féin (ROI)

- **URL**: https://www.sinnfein.ie/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/roi/sinn_fein_roi.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Dáil statements
- **Update cadence**: daily
- **Notes**: Sinn Féin has BOTH ROI representation AND NI Assembly
  representation — they share the party_id but ship different scope
  files (`sinn_fein_roi.py` vs `sinn_fein_ni.py`)

#### Labour Party (ROI)

- **URL**: https://www.labour.ie/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/roi/labour_roi.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Dáil statements
- **Update cadence**: daily
- **Notes**: Irish Electoral Commission ID (to be verified)

#### Social Democrats

- **URL**: https://www.socialdemocrats.ie/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/roi/social_democrats.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers
- **Update cadence**: weekly
- **Notes**: Irish Electoral Commission ID (to be verified)

#### People Before Profit–Solidarity

- **URL**: https://www.pbp.ie/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/roi/pbp_solidarity.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers
- **Update cadence**: weekly
- **Notes**: Irish Electoral Commission ID (to be verified)

#### Green Party / Comhaontas Glas

- **URL**: https://www.greenparty.ie/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/roi/green_party_roi.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers
- **Update cadence**: weekly
- **Notes**: Distinct from the Green Party of England and Wales

#### Aontú

- **URL**: https://aontu.ie/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/roi/aontu.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers
- **Update cadence**: weekly
- **Notes**: Irish Electoral Commission ID (to be verified)

#### Independent Ireland

- **URL**: https://independentireland.ie/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/roi/independent_ireland.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers
- **Update cadence**: weekly
- **Notes**: Irish Electoral Commission ID (to be verified)

#### Irish Freedom Party

- **URL**: https://irishfreedomparty.ie/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/roi/irish_freedom_party.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers
- **Update cadence**: weekly
- **Notes**: Irish Electoral Commission ID (to be verified)

#### National Party

- **URL**: https://www.thenationalparty.ie/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/roi/national_party_roi.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers
- **Update cadence**: weekly
- **Notes**: Irish Electoral Commission ID (to be verified)

#### RISE

- **URL**: https://www.risepartyireland.ie/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/roi/rise_roi.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers
- **Update cadence**: weekly
- **Notes**: Irish Electoral Commission ID (to be verified)

### Northern Ireland Assembly (7 parties)

#### Democratic Unionist Party (DUP)

- **URL**: https://www.mydup.com/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/ni/dup.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Assembly statements
- **Update cadence**: daily
- **Notes**: Electoral Commission ID (to be verified — NI parties are
  registered with the UK Electoral Commission)

#### Sinn Féin (NI)

- **URL**: https://sinnfein.ie/ni/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/ni/sinn_fein_ni.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Assembly statements
- **Update cadence**: daily
- **Notes**: Sinn Féin NI shares the party_id with Sinn Féin ROI

#### Alliance Party

- **URL**: https://www.allianceparty.org/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/ni/alliance_ni.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Assembly statements
- **Update cadence**: weekly
- **Notes**: Electoral Commission ID (to be verified)

#### Ulster Unionist Party (UUP)

- **URL**: https://www.uup.org/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/ni/uup.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Assembly statements
- **Update cadence**: weekly
- **Notes**: Electoral Commission ID (to be verified)

#### Social Democratic and Labour Party (SDLP)

- **URL**: https://www.sdlp.ie/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/ni/sdlp.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Assembly statements
- **Update cadence**: weekly
- **Notes**: Electoral Commission ID (to be verified)

#### Traditional Unionist Voice (TUV)

- **URL**: https://www.tuvni.com/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/ni/tuv_ni.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Assembly statements
- **Update cadence**: weekly
- **Notes**: Electoral Commission ID (to be verified)

#### People Before Profit (NI)

- **URL**: https://www.pbpni.com/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/ni/pbp_ni.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Assembly statements
- **Update cadence**: weekly
- **Notes**: PBP NI is distinct from PBP–Solidarity in the ROI

### Wales Senedd (4 parties)

#### Plaid Cymru (Senedd)

- **URL**: https://www.partyofwales.org/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/wales/plaid_cymru_senedd.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Senedd statements
- **Update cadence**: daily
- **Notes**: Plaid Cymru Senedd shares the party_id with Plaid Cymru
  UK HoC

#### Welsh Labour

- **URL**: https://www.welshlabour.wales/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/wales/labour_wales.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Senedd statements
- **Update cadence**: daily
- **Notes**: Welsh Labour shares the party_id with UK Labour

#### Welsh Conservatives

- **URL**: https://www.welshconservatives.co.uk/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/wales/conservative_wales.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Senedd statements
- **Update cadence**: weekly
- **Notes**: Welsh Conservatives shares the party_id with UK
  Conservative and Unionist Party

#### Welsh Liberal Democrats

- **URL**: https://www.welshlibdems.wales/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/wales/liberal_democrats_wales.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Senedd statements
- **Update cadence**: weekly
- **Notes**: Welsh Lib Dems shares the party_id with UK Liberal
  Democrats

### Scotland Holyrood (5 parties)

#### Scottish National Party (Holyrood)

- **URL**: https://www.snp.org/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/scotland/snp_scottish.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Holyrood statements
- **Update cadence**: daily
- **Notes**: SNP Holyrood shares the party_id with SNP UK HoC

#### Scottish Labour

- **URL**: https://scottishlabour.org.uk/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/scotland/scottish_labour.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Holyrood statements
- **Update cadence**: daily
- **Notes**: Scottish Labour shares the party_id with UK Labour

#### Scottish Conservatives

- **URL**: https://www.scottishconservatives.com/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/scotland/scottish_conservatives.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Holyrood statements
- **Update cadence**: weekly
- **Notes**: Scottish Conservatives shares the party_id with UK
  Conservative and Unionist Party

#### Scottish Liberal Democrats

- **URL**: https://www.scotlibdems.org.uk/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/scotland/scottish_liberal_democrats.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Holyrood statements
- **Update cadence**: weekly
- **Notes**: Scottish Lib Dems shares the party_id with UK Liberal
  Democrats

#### Scottish Greens

- **URL**: https://www.scottishgreens.org.uk/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/scotland/scottish_greens.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Holyrood statements
- **Update cadence**: weekly
- **Notes**: Scottish Greens are a separate party from the Green
  Party of England and Wales

### Crown Dependencies (3 parties)

#### Jersey Party

- **URL**: https://www.jerseyparty.com/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/crown_dependencies/jersey_party.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, States of Jersey
  statements
- **Update cadence**: weekly
- **Notes**: One of the largest Jersey parties

#### Guernsey Party

- **URL**: https://www.guernseyparty.gg/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/crown_dependencies/guernsey_party.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, States of Guernsey
  statements
- **Update cadence**: weekly
- **Notes**: One of the largest Guernsey parties

#### Isle of Man Party

- **URL**: https://www.iomparty.com/
- **DLT source**: `dlt_sources/cianchosaint/political_parties/crown_dependencies/iom_party.py`
- **OSINT allowlist**: yes
- **Coverage**: Press releases, policy papers, Tynwald statements
- **Update cadence**: weekly
- **Notes**: One of the largest Isle of Man parties

## Gaps

- **Electoral Commission IDs** for the 12 ROI parties + the 7 NI parties
  are NOT YET VERIFIED. The UK Electoral Commission IDs (for the 7 UK
  HoC parties + the 4 Welsh + 5 Scottish) are partially verified. The
  Crown Dependencies parties are registered locally (not with the UK
  Electoral Commission). Follow-up
  `cianchosaint-electoral-commission-ids-v1`.
- **Donor filings** (the Electoral Commission / Standards in Public
  Life Commission register of political donations) are NOT yet covered
  by the per-party DLT sources. Follow-up
  `cianchosaint-donor-filings-v1`.
- **Voting records** (the per-MP / per-MEP / per-MLA / per-TD voting
  record) are NOT yet covered. Follow-up `cianchosaint-voting-records-v1`.

## References

- The canonical openspec spec:
  [`openspec/specs/cianchosaint-source-catalogue/spec.md`](../../../openspec/specs/cianchosaint-source-catalogue/spec.md)
- The political-party pipeline spec:
  [`openspec/specs/cianchosaint-political-party-pipeline/spec.md`](../../../openspec/specs/cianchosaint-political-party-pipeline/spec.md)
- The OSINT allowlist:
  [`dlt_sources/cianchosaint/common/osint_allowlist.yaml`](../../../dlt_sources/cianchosaint/common/osint_allowlist.yaml)
- The per-political-party registry:
  [`dlt_sources/cianchosaint/political_parties/_registry.py`](../../../dlt_sources/cianchosaint/political_parties/_registry.py)
- The 4-tier provider chain:
  [`baml_src/_shared/provider_router.py`](../../../baml_src/_shared/provider_router.py)
