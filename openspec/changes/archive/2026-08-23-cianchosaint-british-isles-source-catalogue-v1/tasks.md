# Tasks: cianchosaint-british-isles-source-catalogue-v1

## 0. Pre-flight (preconditions)

- [ ] Verify the 26 per-constituency DLT sources are present at
      `dlt_sources/cianchosaint/<jurisdiction>/<vertical>/`
- [ ] Verify the 24 political-party DLT sources are present at
      `dlt_sources/cianchosaint/political_parties/<jurisdiction>/`
- [ ] Verify the 5 intelligence-agency DLT sources are present at
      `dlt_sources/cianchosaint/uk/intelligence_agencies/`
- [ ] Verify the cohort registries are present:
      `_cross/per_constituency_cohort_registry.py` +
      `political_parties/_registry.py`
- [ ] Verify the OSINT allowlist is at
      `dlt_sources/cianchosaint/common/osint_allowlist.yaml`

## 1. OpenSpec artifacts

- [ ] Author `openspec/changes/cianchosaint-british-isles-source-catalogue-v1/proposal.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-british-isles-source-catalogue-v1/tasks.md` — this file
- [ ] Author `openspec/changes/cianchosaint-british-isles-source-catalogue-v1/cross-repo-sync.md` — Cianfhoghlaim unchanged
- [ ] Author `openspec/changes/cianchosaint-british-isles-source-catalogue-v1/specs/cianchosaint-source-catalogue/spec.md` (delta — 4 ADDED Requirements)
- [ ] Author `openspec/specs/cianchosaint-source-catalogue/spec.md` (canonical END-STATE spec, 4 Requirements + Scenarios)
- [ ] Author `openspec/specs/cianchosaint-source-catalogue/AGENTS.md` (≤30 lines per the repo-hygiene convention)

## 2. The catalogue

- [ ] Author `docs/source-catalogue/README.md` (the master catalogue — overview + how to use + cross-cutting references)
- [ ] Author `docs/source-catalogue/01-intelligence-agencies.md` (12 bodies: MI5, MI6, GCHQ, DI, HMGCC, NCA, NPCC, IOPC, ISC, IPCO, IPT, IPB)
- [ ] Author `docs/source-catalogue/02-police-forces-uk.md` (45 bodies: 43 territorial + BTP + MDP)
- [ ] Author `docs/source-catalogue/03-police-forces-ireland.md` (2 bodies: An Garda Síochána, PSNI)
- [ ] Author `docs/source-catalogue/04-police-forces-crown-dependencies.md` (3 bodies: States of Jersey, Bailiwick of Guernsey, Isle of Man)
- [ ] Author `docs/source-catalogue/05-armed-forces-uk.md` (UK MoD + RAF + Royal Navy + British Army)
- [ ] Author `docs/source-catalogue/06-armed-forces-ireland.md` (Defence Forces of Ireland: Army, Naval Service, Air Corps)
- [ ] Author `docs/source-catalogue/07-key-government-departments.md` (Home Office / MoJ / FCDO / MoD / HMRC / Cabinet Office / DSIT + NI Executive + devolved + Crown Dependencies)
- [ ] Author `docs/source-catalogue/08-courts-and-tribunals.md` (12 court systems: UK Supreme + Court of Appeal + High Court + Crown Court + Magistrates' Courts + Tribunals + ROI Courts + NICTS + SCTS + Jersey + Guernsey + IoM)
- [ ] Author `docs/source-catalogue/09-political-parties.md` (24 parties across 6 jurisdictions)
- [ ] Author `docs/source-catalogue/10-other-bodies.md` (ICO, NAO, C&AG, HoC Library, Senedd Research, Electoral Commission, etc.)

## 3. Validation gates

- [ ] Run `openspec validate cianchosaint-british-isles-source-catalogue-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-source-catalogue --strict` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL changes + ALL specs pass
- [ ] Run `mise run lint:license` and verify the catalogue's URL claims match the OSINT allowlist
- [ ] Run `mise run lint:drift-docs` and verify the catalogue's number claims (43 forces, 24 parties, etc.) match ground truth
- [ ] Verify all internal links in `docs/source-catalogue/*.md` resolve (no broken links)

## 4. CI gates + commit + push

- [ ] Commit on `cianchosaint:main` with message: `docs(openspec): cianchosaint-british-isles-source-catalogue-v1 — the canonical catalogue of British Isles public-sector bodies`
- [ ] Push to `github.com:cianfhoghlaim/cianchosaint`
- [ ] Archive `cianchosaint-british-isles-source-catalogue-v1` (no blockers)

## 5. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-nao-pipeline-v1` — wire the NAO / C&AG / HoC Library bodies to DLT sources
- [ ] `cianchosaint-crown-dependencies-extra-v1` — wire the devolved Northern Ireland + Crown Dependencies legislatures + audit bodies
- [ ] `cianchosaint-ico-pipeline-v1` — wire the Information Commissioner's Office + the 3 ombudsman bodies
- [ ] `cianchosaint-armed-forces-extra-v1` — wire the British doctrine series (JSP/JDP/AP/BR) + the Irish Defence Forces white paper

## Verification

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint

openspec list --specs
# Expected: 10 specs (the 9 existing + cianchosaint-source-catalogue)

openspec list
# Expected: at least 3 pending changes (foundation + bootstrap-v2 + deployment-runbook-v1 + this catalogue)

openspec validate --all --strict
# Expected: ALL pass

ls docs/source-catalogue/
# Expected: 11 files (README.md + 01..10 topic files)

wc -w docs/source-catalogue/*.md | tail -1
# Expected: ~8,000-12,000 words total

# Verify the catalogue numbers match ground truth
grep -c '^- \*\*Body' docs/source-catalogue/01-intelligence-agencies.md
# Expected: ~12 (the 12 UK intelligence + oversight bodies)

grep -c '^- \*\*Body' docs/source-catalogue/02-police-forces-uk.md
# Expected: ~45 (43 territorial + BTP + MDP)

grep -c '^- \*\*Body' docs/source-catalogue/09-political-parties.md
# Expected: ~24 (the 24 parties in the OSINT allowlist)
```
