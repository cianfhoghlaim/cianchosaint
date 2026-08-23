# Tasks: cianchosaint-baml-schemas-v1

## 1. Canonical spec scaffold

- [ ] 1.1 Create `openspec/specs/cianchosaint-baml-schemas/spec.md`
      (4 ADDED Requirements)
- [ ] 1.2 Create `openspec/specs/cianchosaint-baml-schemas/AGENTS.md`
      (≤30 lines, per the per-spec AGENTS.md convention)
- [ ] 1.3 Create
      `openspec/changes/cianchosaint-baml-schemas-v1/specs/cianchosaint-baml-schemas/spec.md`
      (the spec delta for the change)

## 2. BAML extraction files (8 files at `baml_src/cianchosaint/`)

- [ ] 2.1 `baml_src/cianchosaint/processing/irish_legal_extraction.baml`
      — `ExtractCourtJudgment` + `ExtractStatuteReference` +
      `ExtractFOIARequest`
- [ ] 2.2 `baml_src/cianchosaint/processing/met_police_extraction.baml`
      — `ExtractMETPressRelease` + `ExtractStopAndSearchRecord` +
      `ExtractCrimeStatistics`
- [ ] 2.3 `baml_src/cianchosaint/processing/psni_extraction.baml`
      — `ExtractPSNIPressRelease` + `ExtractNIJustice` +
      `ExtractPolicingBoardReport`
- [ ] 2.4 `baml_src/cianchosaint/processing/uk_military_extraction.baml`
      — `ExtractMODPressRelease` + `ExtractRAFDoctrine` +
      `ExtractRoyalNavyDoctrine` + `ExtractBritishArmyDoctrine` +
      `ExtractJSPDoctrine` + `ExtractJDPDoctrine`
- [ ] 2.5 `baml_src/cianchosaint/processing/ireland_defence_forces_extraction.baml`
      — `ExtractIDFPressRelease` + `ExtractIDFWhitePaper`
- [ ] 2.6 `baml_src/cianchosaint/processing/intelligence_oversight_extraction.baml`
      — `ExtractISCReport` + `ExtractIPCOReport` + `ExtractIPTDecision` +
      `ExtractInvestigatoryPowersBillEvidence`
- [ ] 2.7 `baml_src/cianchosaint/political_parties/political_party_extraction.baml`
      — `ExtractPartyPressRelease` (shared schema for all 24 parties)
- [ ] 2.8 `baml_src/cianchosaint/politics/reform_uk_dossier_extraction.baml`
      — `ExtractReformUkDossier` (refines the wholesale-copied pilot)

## 3. Conservative-posture enforcement

- [ ] 3.1 Every new BAML class includes `osint_ceiling_enforced: bool`
      (default `true`) + `licence_posture: string` (default
      `"BUSL-1.1 v2 (British-Isles-only)"`) + `analyst_review_required: bool`
      (default `true`)
- [ ] 3.2 Every new BAML function prompt explicitly states the
      conservative posture: do not invent factual claims, leave lists
      empty if not in input
- [ ] 3.3 Every new BAML function's prompt references the LICENCE
      attribution header per the wholesale-copy convention

## 4. Validation

- [ ] 4.1 `openspec validate cianchosaint-baml-schemas-v1 --strict`
      passes
- [ ] 4.2 `openspec validate openspec/specs/cianchosaint-baml-schemas/ --strict`
      passes (canonical spec validation)

## 5. Commit + archive

- [ ] 5.1 `git add baml_src/cianchosaint/ openspec/specs/cianchosaint-baml-schemas/
      openspec/changes/cianchosaint-baml-schemas-v1/` only (no
      `git add -A` — concurrent-agent safety per the
      `concurrent-agent-write-safety-v1` convention)
- [ ] 5.2 `git commit -m "feat(q3-track1): BAML schemas for 8 per-vertical extractions (Change 11)"`
- [ ] 5.3 `git push origin main`
- [ ] 5.4 `openspec archive cianchosaint-baml-schemas-v1 --yes`
