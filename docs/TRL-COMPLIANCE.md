# CIANCHOSAINT — TRL Compliance (UKRI / STFC Technology Readiness Level)

> **Audience:** Anyone authoring an openspec change for `cianchosaint` who needs to demonstrate Technology Readiness Level (TRL) maturity to a UKRI / STFC funding body, an HMGCC supplier, or an MoD / NAO evaluator.
>
> **Companion docs:** openspec/AGENTS.md · README.md · LICENSE.md · docs/USAGE-GUIDELINES.md · docs/DEPLOYMENT.md · docs/HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md
>
> **Licence:** BUSL-1.1 v2 — CIANCHOSAINT edition (British-Isles-only Additional Use Grant + 3-step foreign-use gate + warrant-to-enforce clause)
>
> **Canonical TRL reference:** hmgcc/Eligibility of technology readiness levels (TRL).md — wholesale-copied verbatim from the UKRI / STFC eligibility-of-technology-readiness-levels-trl reference page on 2026-08-26.

## §1 — Why TRL assessment matters

The UK Intelligence Community + the UK Ministry of Defence + the Royal Navy / RAF / British Army + the Royal Navy + HMGCC + the Defence Forces of Ireland all use Technology Readiness Levels (TRLs) when evaluating new software + hardware + integration + observability + intelligence workflows. The CIANCHOSAINT project uses openspec to track every change — and so it makes sense to:

1. **Map every openspec change to a TRL pair** (`current_trl` + `target_trl`)
2. **Prove the gap** between the two via concrete evidence (proposal.md + tasks.md + spec deltas + implementation PRs)
3. **Provide a recommendation** for the next change that closes the gap

## §2 — The 9 UKRI / STFC TRL definitions (verbatim)

Per hmgcc/Eligibility of technology readiness levels (TRL).md:

| TRL | Definition |
|--:|:--|
| TRL 1 | basic principles observed and reported |
| TRL 2 | technology concept or application formulated |
| TRL 3 | analytical and experimental critical function or characteristic proof-of-concept |
| TRL 4 | technology basic validation in a laboratory environment |
| TRL 5 | technology basic validation in a relevant environment |
| TRL 6 | technology model or prototype demonstration in a relevant environment |
| TRL 7 | technology prototype demonstration in an operational environment |
| TRL 8 | actual technology completed and qualified through test and demonstration |
| TRL 9 | actual technology qualified through successful mission operations. |

## §3 — How openspec changes map to TRL

Every CIANCHOSAINT openspec change SHOULD carry a TRL pair (`current_trl` + `target_trl` + `gap_analysis` + `evidence` + `recommendation`). The CIANCHOSAINT TRL assessment tooling produces these automatically:

| OpenSpec artefact | TRL band | Notes |
|---|--:|---|
| No proposal.md, no tasks.md, no spec.md | TRL 1 | basic principles observed and reported — the change is barely a sketch |
| proposal.md present, no spec.md | TRL 2 | technology concept or application formulated — the change has a clear "why" + "what" but not yet a typed specification |
| spec.md present, no implementation PR | TRL 3 | analytical / experimental proof-of-concept — the requirement is fully typed but no code exists yet |
| spec.md + implementation PR + openspec validate passes | TRL 4 | basic validation in a laboratory environment — the change has its code in the repo and the openspec suite accepts it |
| Implementation merged + CI smoke test passes | TRL 5 | basic validation in a relevant environment — the change is in a real git branch and the CI considers it safe |
| Implementation deployed to per-persona dev environment | TRL 6 | prototype demonstration in a relevant environment — the change is deployed somewhere an analyst can poke |
| Implementation deployed to per-persona staging environment | TRL 7 | prototype demonstration in an operational environment — the change is deployed somewhere an analyst uses for real work |
| Implementation deployed to per-persona prod environment + acceptance test passes | TRL 8 | qualified through test and demonstration — the change is in production |
| Implementation audited + signed-off by IAO + supervisor body (CPCAB / IPCO / ISC) | TRL 9 | qualified through successful mission operations — the change has been used in real cases |

## §4 — The CIANCHOSAINT TRL assessment tooling

### §4.1 — The BAML ExtractTRLAssessment function

The canonical TRL extraction lives at
baml_src/cianchosaint/processing/trl_assessment.baml and exposes the
`ExtractTRLAssessment` BAML function with the `TRLAssessment` schema
(`change_id` + `title` + `current_trl` + `target_trl` + `gap_analysis` +
`evidence` + `recommendation` + `trl_definitions_inline` + the
conservative-posture fields). Every extraction is forced to respect:

- `osint_ceiling_enforced: true` (always)
- `licence_posture: "BUSL-1.1 v2 (British-Isles-only)"` (always)
- `analyst_review_required: true` (always)
- `current_trl >= 1` and `current_trl <= 9`
- `target_trl - current_trl >= 2` (conservative gap; not simply 1)
- `target_trl >= current_trl` (the change must advance the platform)

The BAML function returns the TRL definitions inline so the downstream
analysts never have to track a moving definition.

### §4.2 — The trl_assess.py script

The heuristic TRL assessment lives at scripts/trl_assess.py and
implements the same schema as a static analyser (no LLM required). The
script:

1. Walks `openspec/changes/` (excluding `archive/`)
2. Inspects each change's `proposal.md` + `tasks.md` + `specs/<spec>/spec.md`
3. Maps the artefacts to a heuristic `current_trl` (per §3)
4. Computes a `target_trl = clamp(current_trl + 3, 1, 9)`
5. Derives a `gap_analysis` string describing the remaining work
6. Recommends the next follow-up change to advance the TRL
7. Writes the per-day JSON report to `stedding/trl-assessments/<YYYY-MM-DD>.json`

Run it via:

```bash
mise run cianchosaint:trl:assess          # summary table + JSON file
mise run cianchosaint:trl:assess-json     # JSON to stdout (for CI)
mise run cianchosaint:trl:assess-one <change-id>  # one change
```

### §4.3 — The mise.toml registration

The TRL assessment is registered in mise.toml under §17:

```toml
[tasks."cianchosaint:trl:assess"]
description = "Assess every pending openspec change against the 9 UKRI/STFC TRL definitions"
run = "python3 scripts/trl_assess.py"
```

## §5 — Worked examples

The following table shows TRL pairs for representative openspec changes
(per the latest `stedding/trl-assessments/<date>.json`):

| OpenSpec change | current_trl | target_trl | Recommended follow-up |
|---|--:|--:|---|
| 2026-08-24-cianchosaint-init-v1 | 5 | 8 | open a follow-up change advancing to TRL 6 (technology model or prototype demonstration in a relevant environment) |
| cianchosaint-bipp-v2-baml-v1 | 4 | 7 | open a follow-up change advancing to TRL 5 (technology basic validation in a relevant environment) |
| cianchosaint-cognee-graphiti-political-v1 | 5 | 8 | open a follow-up change advancing to TRL 6 |
| cianchosaint-collaboration-workspace-v1 | 5 | 8 | open a follow-up change advancing to TRL 6 |
| cianchosaint-garda-prompt-workflow-v1 | 4 | 7 | open a follow-up change advancing to TRL 5 |
| cianchosaint-generative-ui-kit-v1 | 4 | 7 | open a follow-up change advancing to TRL 5 |
| cianchosaint-langfuse-dashboard-v1 | 1 | 4 | open a follow-up change advancing to TRL 2 |
| cianchosaint-langfuse-prompt-management-v1 | 4 | 7 | open a follow-up change advancing to TRL 5 |
| cianchosaint-ragas-eval-pipeline-v1 | 5 | 8 | open a follow-up change advancing to TRL 6 |
| cianchosaint-bipp-v2-political-party-v2-v1 | 4 | 7 | open a follow-up change advancing to TRL 5 |
| cianchosaint-bipp-v2-spec-v1 | 4 | 7 | open a follow-up change advancing to TRL 5 |

## §6 — When to re-assess TRL

Re-run the TRL assessment:

1. After every successful CI run (i.e. on every merged PR)
2. After every openspec archive (the change is now in production and may
   advance to TRL 6, 7, 8, or 9)
3. Before submitting the change to UKRI / STFC / HMGCC / MoD / NAO for
   funding or audit
4. As part of the quarterly licence-enforcement review (per the
   cianchosaint-licence-enforcement-v1 change)

## §7 — Cross-references

- hmgcc/Eligibility of technology readiness levels (TRL).md — the
  canonical UKRI / STFC TRL definitions (wholesale-copied verbatim)
- baml_src/cianchosaint/processing/trl_assessment.baml — the BAML
  function
- scripts/trl_assess.py — the heuristic TRL assessment script
- openspec/AGENTS.md — the TRL compliance section (added 2026-08-26)
- openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
  specs/cianchosaint-ic-ui-kit-integration/spec.md — the canonical spec

## §8 — Final note

The TRL assessment is intentionally conservative. CIANCHOSAINT values
honest engineering over impressive-looking TRL numbers — the platform's
mission-critical surfaces (per the OSINT ceiling + the BUSL-1.1 v2
licence posture) require demonstrated maturity, not inflated slideware.
The `analyst_review_required: true` + `osint_ceiling_enforced: true`
flags on every TRL assessment reflect this posture.

End of TRL-COMPLIANCE.md.
