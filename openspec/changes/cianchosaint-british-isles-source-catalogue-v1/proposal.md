# Change: cianchosaint-british-isles-source-catalogue-v1

## Why

The cianchosaint platform has reached the milestone where the OSINT
allowlist (`dlt_sources/cianchosaint/common/osint_allowlist.yaml`),
the per-constituency DLT source manifest
(`dlt_sources/cianchosaint/<jurisdiction>/<source>.py`), the per-
political-party DLT sources (24 parties across UK HoC + ROI Dáil +
NI Assembly + Wales Senedd + Scotland Holyrood + Crown Dependencies),
the per-intelligence-agency DLT sources (5 UK agencies), the per-
military DLT sources (UK MoD + RAF + RN + Army + 6 doctrine series +
Irish Defence Forces), and the per-court DLT sources (UK + ROI + NI +
Scotland + Crown Dependencies) are all in place. The 26 per-constituency
cohorts are documented in
`dlt_sources/cianchosaint/_cross/per_constituency_cohort_registry.py`
and the 38 political-party cohorts are documented in
`dlt_sources/cianchosaint/political_parties/_registry.py`.

But there is **no canonical, operator-facing document** that enumerates
the **bodies** (not the source files) that cianchosaint ingests from.
Operators and analysts hit these questions repeatedly:

1. **"What UK police forces does cianchosaint cover?"** — the answer
   is "43 territorial forces + BTP + MDP = 45 entries" but that
   number is scattered across `dlt_sources/cianchosaint/uk/policing/`
   + the cohort registry + the political-party registry.
2. **"What intelligence agencies?"** — "the 5 UK agencies" + "the
   3 ROI oversight bodies" + "ISC + IPCO + IPT + IPB" + "NCA + NPCC +
   IOPC" — scattered across 4 different folders.
3. **"What courts?"** — "UK Supreme + Court of Appeal + High Court +
   Crown Court + Magistrates' + Tribunals + ROI + NICTS + SCTS +
   Jersey + Guernsey + IoM" — no single document.
4. **"What political parties?"** — "the 24 parties in the OSINT
   allowlist" but the per-jurisdiction split (7 UK + 12 ROI + 7 NI +
   4 Wales + 5 Scotland + 3 Crown Dependencies) isn't in one place.
5. **"What other bodies?"** — "ICO + NAO + C&AG + HoC Library + Senedd
   + Electoral Commission + Police Ombudsman for Northern Ireland +
   Office of the Police Ombudsman for Scotland + HM Inspectorate of
   Constabulary" — scattered.

This change is a **DOCUMENT-ONLY** change that produces a single
canonical multi-file artefact at `docs/source-catalogue/` — a 11-file
catalogue of every public-sector body (across the 8 legal sub-domains)
that cianchosaint ingests from or could ingest from.

The user explicitly clarified (verified 2026-08-23):
*"explanations of document and website sources of all intelligence
agencies, police forces, armies, air forces, navies, key governmental
departments"* — i.e. the catalogue should cover EVERY British Isles
public-sector body the platform relates to, not just the bodies that
already have a DLT source file.

## What changes

**One openspec change** that adds:

- **1 new spec** (`cianchosaint-source-catalogue/spec.md`) — 4 ADDED
  Requirements capturing the contract that `docs/source-catalogue/`
  MUST cover: the multi-file format (11 files: 1 README + 10 topic
  files), the per-body schema (URL + DLT source linkage + OSINT
  allowlist flag + coverage description + update cadence + notes),
  the gap inventory (what bodies are NOT yet wired), and the licence
  attribution (every British Isles public-sector body is in scope).

- **1 multi-file catalogue** at `docs/source-catalogue/` (11 files:
  - `README.md` — the master catalogue
  - `01-intelligence-agencies.md` — 12 UK intelligence + oversight bodies
  - `02-police-forces-uk.md` — 43 UK territorial + BTP + MDP
  - `03-police-forces-ireland.md` — An Garda Síochána + PSNI
  - `04-police-forces-crown-dependencies.md` — States of Jersey + Bailiwick of Guernsey + IoM
  - `05-armed-forces-uk.md` — UK MoD + RAF + Royal Navy + British Army
  - `06-armed-forces-ireland.md` — Defence Forces of Ireland (Army / Naval Service / Air Corps)
  - `07-key-government-departments.md` — Home Office / MoJ / FCDO / MoD / HMRC / Cabinet Office / DSIT + NI Executive + devolved + Crown Dependencies
  - `08-courts-and-tribunals.md` — 12 court systems
  - `09-political-parties.md` — the 24 parties in the OSINT allowlist
  - `10-other-bodies.md` — ICO / NAO / C&AG / HoC Library / Senedd / Electoral Commission / etc.

- **1 per-spec AGENTS.md** (`openspec/specs/cianchosaint-source-catalogue/AGENTS.md`)
  for the new spec, ≤30 lines per the repo-hygiene convention.

- **NO code changes** — this is a document-only change. The catalogue
  links to the existing DLT source files + the OSINT allowlist +
  the openspec specs — it does NOT introduce new DLT sources or new
  openspec changes.

## Impact

- Affected specs: 1 NEW spec (`cianchosaint-source-catalogue/`).
- Affected code/config: 0 LOC of code. 11 new markdown files at
  `docs/source-catalogue/` (the README + 10 topic files; ~8,000-12,000
  words total).
- Supersedes: nothing.
- No secret values are written to disk: the catalogue describes the
  public-sector body URLs but does NOT materialise any secrets itself.

## Out of scope

- The actual IMPLEMENTATION of new DLT sources for bodies that are NOT
  yet wired (e.g. NAO / C&AG / Senedd are in the catalogue but their
  DLT sources are marked "NOT YET WIRED"). Those follow-up sources
  are tracked in separate `cianchosaint-nao-pipeline-v1` /
  `cianchosaint-crown-dependencies-extra-v1` / etc. changes.
- The Crown Dependencies political-party sources (3 parties —
  Jersey Party / Guernsey Party / IoM Party) — they ARE listed in the
  catalogue (`09-political-parties.md`) per their registry entries,
  but the per-jurisdiction legislature writeup lives separately.
- The ICO + NAO + C&AG + HoC Library bodies — they ARE listed in
  `10-other-bodies.md` but their DLT source implementations are
  marked "NOT YET WIRED" pending a follow-up change.

## Dependencies

`Blocked by: none` (the 26 per-constituency DLT sources + the 24
political-party sources + the 5 intelligence-agency sources + the
OSINT allowlist are all already in place from the bootstrap-v2 +
per-constituency + intelligence-agency + political-party changes).

`Blocked by (soft): cianchosaint-repo-bootstrap-v2` (the umbrella
wholesale-copy spec that defines the data platform + agents + IaC
that the catalogue summarises).

`Blocked by (soft): cianchosaint-per-constituency-dlt-sources-v1`,
`cianchosaint-intelligence-agency-pipeline-v1`,
`cianchosaint-political-party-pipeline-v1` (the 3 sub-pipeline specs
whose sources the catalogue inventories).

`Affected repos: cianchosaint.` (Cianfhoghlaim is NOT modified.)

## Cross-repo sync

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) remains completely
unchanged. The `cross-repo-sync.md` file in this change records this in
the standard format but does NOT require any Cianfhoghlaim action.
