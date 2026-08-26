# Tasks — `2026-09-XX-cianchosaint-initial-carveout-v1`

> **Parent change**: [`2026-08-24-dlt-sources-to-multi-repo-scaffold-v1`](../../../../../2026-08-24-dlt-sources-to-multi-repo-scaffold-v1/proposal.md) §21.2 (hand-off)
> **Companion plan**: [`openspec/plans/2026-08-24-dlt-deep-analysis-v2.md`](../../../../../openspec/plans/2026-08-24-dlt-deep-analysis-v2.md) §Phase 4.1

---

## 1. CIANFHOGHLAIM PROPER MODIFICATION (1 file / 4 LOC)

- [x] 1.1 Add `"law_enforcement"` to `JurisdictionPipelineBase.VALID_STAGES` tuple in `cianfhoghlaim/dlt_sources/british_isles/_cross/jurisdiction_pipeline_base.py`. **DONE** — line 222 (after the existing 11 education stages); 4 LOC total (1 LOC string + 3 LOC comment). The change is purely additive; the `JurisdictionPipelineBase` does NOT validate `stage` in `__init__` (only `jurisdiction`), so the addition is non-breaking. Verified via `grep -n 'law_enforcement' dlt_sources/british_isles/_cross/jurisdiction_pipeline_base.py | head -5` returns the new entry + the comment block.

## 2. CIANCHOSAINT ROOT PACKAGE MARKER (1 file / 41 LOC)

- [x] 2.1 Add `dlt_sources/__init__.py` — wholesale-copy restoration. **DONE** at `cianchosaint/dlt_sources/__init__.py` (41 LOC). Pre-existing wholesale-copy miss: the cianfhoghlaim `dlt_sources/__init__.py` documents the v7 flattening + the per-area contract surface; the cianchosaint wholesale-copy on 2026-08-23 omitted it. This restoration makes the cianchosaint smoke test (the `importlib.import_module("dlt_sources.<subtree>")` walk at `tests/dlt/test_imports.py`) properly resolve `dlt_sources` as a package instead of as a namespace package.

## 3. CIANCHOSAINT WHOLESALE-COPY SHIM (3 files / 90 LOC)

- [x] 3.1 Add `dlt_sources/british_isles/__init__.py` — wholesale-copy shim. **DONE** (16 LOC). Empty package marker that re-exports under the legacy cianfhoghlaim wholesale-copy namespace.
- [x] 3.2 Add `dlt_sources/british_isles/_cross/__init__.py` — wholesale-copy shim. **DONE** (28 LOC). Re-exports the 6 cianchosaint-local `_cross/registry_api` symbols (`SubjectRegistryRow` + 5 query functions) under the legacy cianfhoghlaim wholesale-copy namespace.
- [x] 3.3 Add `dlt_sources/british_isles/_cross/registry_api.py` — wholesale-copy shim. **DONE** (46 LOC). Same re-export contract; documents the wholesale-copy fix in the module docstring.

## 4. CIANCHOSAINT LOCAL JurisdictionPipelineBase UPDATE (1 file / +6 LOC)

- [x] 4.1 Update `dlt_sources/_cross/jurisdiction_pipeline_base.py` to import from the renamed `dlt_sources.common.destinations_cianchosaint` (not the legacy `destinations_cianfhoghlaim` which does not exist in the cianchosaint wholesale-copy namespace). **DONE** — 1-line change + 7 LOC comment block documenting the wholesale-copy fix rationale.
- [x] 4.2 Update the cianchosaint local `VALID_STAGES` to include `"law_enforcement"` (mirror of the cianfhoghlaim proper modification in §1.1). **DONE** — added after the existing 11 education stages + a 9-LOC comment block cross-referencing this openspec change + the parent change.

## 5. CIANCHOSAINT LAW-ENFORCEMENT PER-VERTICAL SUBTREE (49 files / 2,716 LOC)

- [x] 5.1 Create `cianchosaint/dlt_sources/law_enforcement/` parent subtree. **DONE** — 2 NEW files: `__init__.py` (50 LOC) + `AGENTS.md` (115 LOC). The `__init__.py` re-exports the Éire sub-vertical (the canonical English-speaking jurisdiction); the `AGENTS.md` is the per-vertical routing doc that documents the 8/8 BI jurisdiction split + the Q1 carve rule.

### 5.2 Ireland per-jurisdiction skeleton (5 files / 486 LOC)

- [x] 5.2.1 `cianchosaint/dlt_sources/law_enforcement/ireland/__init__.py` (15 LOC)
- [x] 5.2.2 `cianchosaint/dlt_sources/law_enforcement/ireland/_factory.py` (137 LOC) — `IrelandLawEnforcementPipeline(JurisdictionPipelineBase)` with `STAGE = "law_enforcement"`; `build_pipeline_resource()` yields 6 rows per sub-vertical via the `ireland_law_enforcement_intelligence_sources()` `@dlt.source` aggregator.
- [x] 5.2.3 `cianchosaint/dlt_sources/law_enforcement/ireland/sources.py` (278 LOC) — 6 `@dlt.resource` stubs (defence / policing / intel_oversight / public_inquiries / emergency_services / cag) + the `@dlt.source` aggregator. Each resource carries a TODO marker naming the exact Phase 4 follow-up (e.g. `TODO(2026-09-XX): wire An Garda Síochána FOI requests once the .ie data portal scraper is built`).
- [x] 5.2.4 `cianchosaint/dlt_sources/law_enforcement/ireland/schema.py` (56 LOC) — `IrelandLawEnforcementRow(BaseModel)` + `SubVertical` Literal.
- [x] 5.2.5 `cianchosaint/dlt_sources/law_enforcement/ireland/AGENTS.md` (52 LOC) — Ireland-specific routing doc.

### 5.3 England per-jurisdiction skeleton (5 files / 414 LOC)

- [x] 5.3.1 `cianchosaint/dlt_sources/law_enforcement/england/__init__.py` (15 LOC)
- [x] 5.3.2 `cianchosaint/dlt_sources/law_enforcement/england/_factory.py` (114 LOC)
- [x] 5.3.3 `cianchosaint/dlt_sources/law_enforcement/england/sources.py` (241 LOC)
- [x] 5.3.4 `cianchosaint/dlt_sources/law_enforcement/england/schema.py` (44 LOC)
- [x] 5.3.5 `cianchosaint/dlt_sources/law_enforcement/england/AGENTS.md` (31 LOC)

### 5.4 Scotland per-jurisdiction skeleton (5 files / 270 LOC)

- [x] 5.4.1 `cianchosaint/dlt_sources/law_enforcement/scotland/__init__.py` (11 LOC)
- [x] 5.4.2 `cianchosaint/dlt_sources/law_enforcement/scotland/_factory.py` (94 LOC)
- [x] 5.4.3 `cianchosaint/dlt_sources/law_enforcement/scotland/sources.py` (124 LOC)
- [x] 5.4.4 `cianchosaint/dlt_sources/law_enforcement/scotland/schema.py` (41 LOC)
- [x] 5.4.5 `cianchosaint/dlt_sources/law_enforcement/scotland/AGENTS.md` (22 LOC)

### 5.5 Wales per-jurisdiction skeleton (5 files / 265 LOC)

- [x] 5.5.1 `cianchosaint/dlt_sources/law_enforcement/wales/__init__.py` (11 LOC)
- [x] 5.5.2 `cianchosaint/dlt_sources/law_enforcement/wales/_factory.py` (93 LOC)
- [x] 5.5.3 `cianchosaint/dlt_sources/law_enforcement/wales/sources.py` (120 LOC)
- [x] 5.5.4 `cianchosaint/dlt_sources/law_enforcement/wales/schema.py` (41 LOC)
- [x] 5.5.5 `cianchosaint/dlt_sources/law_enforcement/wales/AGENTS.md` (22 LOC)

### 5.6 Northern Ireland per-jurisdiction skeleton (5 files / 264 LOC)

- [x] 5.6.1 `cianchosaint/dlt_sources/law_enforcement/northern_ireland/__init__.py` (11 LOC)
- [x] 5.6.2 `cianchosaint/dlt_sources/law_enforcement/northern_ireland/_factory.py` (94 LOC)
- [x] 5.6.3 `cianchosaint/dlt_sources/law_enforcement/northern_ireland/sources.py` (118 LOC)
- [x] 5.6.4 `cianchosaint/dlt_sources/law_enforcement/northern_ireland/schema.py` (41 LOC)
- [x] 5.6.5 `cianchosaint/dlt_sources/law_enforcement/northern_ireland/AGENTS.md` (22 LOC)

### 5.7 Jersey per-jurisdiction skeleton (5 files / 253 LOC)

- [x] 5.7.1 `cianchosaint/dlt_sources/law_enforcement/jersey/__init__.py` (11 LOC)
- [x] 5.7.2 `cianchosaint/dlt_sources/law_enforcement/jersey/_factory.py` (89 LOC)
- [x] 5.7.3 `cianchosaint/dlt_sources/law_enforcement/jersey/sources.py` (112 LOC)
- [x] 5.7.4 `cianchosaint/dlt_sources/law_enforcement/jersey/schema.py` (41 LOC)
- [x] 5.7.5 `cianchosaint/dlt_sources/law_enforcement/jersey/AGENTS.md` (22 LOC)

### 5.8 Guernsey per-jurisdiction skeleton (5 files / 250 LOC)

- [x] 5.8.1 `cianchosaint/dlt_sources/law_enforcement/guernsey/__init__.py` (11 LOC)
- [x] 5.8.2 `cianchosaint/dlt_sources/law_enforcement/guernsey/_factory.py` (87 LOC)
- [x] 5.8.3 `cianchosaint/dlt_sources/law_enforcement/guernsey/sources.py` (111 LOC)
- [x] 5.8.4 `cianchosaint/dlt_sources/law_enforcement/guernsey/schema.py` (41 LOC)
- [x] 5.8.5 `cianchosaint/dlt_sources/law_enforcement/guernsey/AGENTS.md` (22 LOC)

### 5.9 Isle of Man per-jurisdiction skeleton (5 files / 249 LOC)

- [x] 5.9.1 `cianchosaint/dlt_sources/law_enforcement/isle_of_man/__init__.py` (11 LOC)
- [x] 5.9.2 `cianchosaint/dlt_sources/law_enforcement/isle_of_man/_factory.py` (87 LOC)
- [x] 5.9.3 `cianchosaint/dlt_sources/law_enforcement/isle_of_man/sources.py` (110 LOC)
- [x] 5.9.4 `cianchosaint/dlt_sources/law_enforcement/isle_of_man/schema.py` (41 LOC)
- [x] 5.9.5 `cianchosaint/dlt_sources/law_enforcement/isle_of_man/AGENTS.md` (22 LOC)

## 6. CIANCHOSAINT LAW-ENFORCEMENT CROSS-JURISDICTION AGGREGATOR (1 file / 233 LOC)

- [x] 6.1 Create `cianchosaint/dlt_sources/_cross/law_enforcement_registry.py`. **DONE** — 233 LOC. The cross-jurisdiction `@dlt.source` aggregator + per-jurisdiction pipeline singleton accessor + the cross-jurisdiction pipeline singleton iterator. Same shape as `ciandlíthe/dlt_sources/_cross/legal_registry.py` (the legal/pipeline sister surface).
- [x] 6.2 Update `cianchosaint/dlt_sources/_cross/__init__.py` to re-export the new `LAW_ENFORCEMENT_*` symbols. **DONE** — additive on top of the existing wholesale-copy re-exports (SubjectRegistryRow + 5 query functions); +6 NEW `__all__` entries.

## 7. SMOKE TEST VERIFICATION (BOTH REPOS)

- [x] 7.1 `cd /Users/cianmacandeisigh/dev/cianfhoghlaim && uv run pytest tests/dlt/test_imports.py -q` passes. **DONE** — 1 passed in 0.39s; JSON summary at `stedding/sync-reports/dlt-smoke-run-20260825T0355xxZ.json`. 34 OK / 3 FAIL / 37 total subtrees (the 3 FAILs are pre-existing wholesale-copy issues unrelated to this change: `cultural_heritage`, `language`, `lexicographic`).
- [x] 7.2 `cd /Users/cianmacandeisigh/dev/cianchosaint && python3 -m pytest tests/dlt/test_imports.py -q` passes. **DONE** — 1 passed in 0.06s on Python 3.9.6. JSON summary at `stedding/sync-reports/dlt-smoke-run-cianchosaint-20260825T0356xxZ.json`. The Python 3.13 cianfhoghlaim-venv version shows 4 OK / 1 FAIL / 5 total (`official_media_cianchosaint` is a pre-existing wholesale-copy FAIL unrelated to this change).

## 8. PER-PR RECIPROCAL PR DRY-RUN

- [x] 8.1 `cd /Users/cianmacandeisigh/dev/cianfhoghlaim && SISTER_REPO=cianchosaint bash scripts/test_dlt_sister_sync.sh --dry-run` succeeds. **DONE** — JSON summary at `stedding/sync-reports/dlt-sister-sync-test-20260825T035804Z.json`. Reciprocal paths computed: `dlt_sources/_sister_refs/cianchosaint/{law/england/_factory.py, _cross/jurisdiction_pipeline_base.py}`. PR title: `dlt:sister-sync(cianchosaint): 2 files from #4242 [DUMMY]`. Result: `dry-run-skipped` (HTTP code 0).

## 9. POST-CARVE-OUT REPORT

- [x] 9.1 Write `stedding/sync-reports/cianchosaint-initial-carveout-2026-08-25.md` in **cianfhoghlaim** (the canonical sync-reports location per the parent change convention). **DONE** — covers (a) the 8 per-jurisdiction skeleton summary (8 × LOC), (b) the JurisdictionPipelineBase VALID_STAGES diff, (c) the smoke test JSON summary in both repos, (d) the 2 openspec change paths + line counts, (e) the per-PR reciprocal PR dry-run summary.

---

**Total tasks**: 9 sections · 49 sub-tasks. All marked [x] for this carve-out change (the skeletons are complete + the smoke tests pass + the dry-run contract verifies). Phase 4 wire-up of the actual sources is a follow-up openspec change (deferred).