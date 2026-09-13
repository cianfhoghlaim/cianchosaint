# Change: cianchosaint-politician-schema-v1

## Why

Five problems converged on 2026-09-06:

1. **The 87 leabharlann politics PDFs are referenced by the BIPP v2 cohort registry** (per `openspec/specs/cianchosaint-bipp-v2/spec.md`) but no BAML function systematically harvests the politicians named within them. The `ExtractPartyPressRelease` function (`baml_src/cianchosaint/processing/party.baml`) only extracts *party*-level metadata; nothing currently extracts *politician*-level metadata. This means: when an analyst queries "show me every politician connected to Sinn Féin funding across the 87 PDFs", we cannot answer.

2. **The `PoliticalGraphStore` entity model** (per `agents/cianchosaint/tools/political_graph_store.py` + `openspec/specs/cianchosaint-political-graph/spec.md`) supports 13 entity types including `politician` + `donor` + `company` + `agency` + `court` + `media_outlet` — but there is no canonical `Politician` BAML record, no per-politician DLT source, and no Google ADK FunctionTool that resolves a politician's website + social handles + Hansard record + Wikidata QID via the browser stack.

3. **The user explicitly requested the per-politician schema with the following 7 case studies** (verbatim): *"nigel farage and zack polanski and john o dowd mla northern ireland and gordon lyons paulgivan gavin robinson dup and lara bird snp"*. The case studies span 3 jurisdictions (UK HoC, NI Assembly, Holyrood) and 4 parties (Reform UK, Green Party of England and Wales, Sinn Féin NI, DUP, SNP). Plus the user requested *"adjacent relevant topics relevant to the userbase of cianchosaint and the associated project priorities like their advisors and funding and historic associations and relevant existing political wikipedia archives"*.

4. **The existing `reform_uk_pilot` FunctionTool** (`agents/cianchosaint/tools/reform_uk_pilot.py`) is a single-entity, hardcoded stub targeting Richard Tice + Reform UK. It is not generalisable. A general `politician_account_resolver` FunctionTool is the canonical extension.

5. **The user's prompt request explicitly cites the browser stack**: *"develop a google adk prompt to use such things as the tools found in our browser stack to systematically gather information like the public follower and following of such case studies"*. The browser stack = the Firecrawl MCP (`agents/meaisinfhoghlaim/firecrawl_mcp/client.py` — 12-tool wrapper) + the existing platform resolvers (`dlt_sources/official_media_cianchosaint/fediverse.py` handles Mastodon + Bluesky; X / Facebook / Instagram / YouTube / TikTok / Threads / Truth Social / LinkedIn / GB News / TalkTV / Hansard / TheyWorkForYou need new resolvers).

## What changes

### BAML extraction layer (4 new functions + 8 new classes)

- **NEW file** `baml_src/cianchosaint/politics/politician_extraction.baml` (~400 LOC) with:
  - 3 new schema classes: `SocialHandle`, `PublicFollowerMetrics`, `Politician` (the core politician record)
  - 4 new extraction functions:
    - `ExtractPoliticianFromPDF(input)` — bulk-harvest every politician named in a leabharlann PDF
    - `ExtractPoliticianFromWebPage(input, party_id, jurisdiction)` — high-confidence extraction from a scraped `/people/<slug>` page
    - `ExtractAdjacentContextFromPDF(input)` — harvest advisors + funders + historic associations + Wikidata references
    - `ExtractAdjacentContextFromWebPage(input, politician_name)` — high-confidence counterpart for the 4 axes

### BAML adjacent schema (5 new classes)

- **Within the same BAML file**: `Advisor`, `Funder`, `Donation`, `HistoricalAssociation`, `WikipediaArchives`
- Wrapped in a `AdjacentContext` container that the harvest script emits as one row per politician

### DLT source tree 1 — `politicians/`

- **NEW base** `dlt_sources/cianchosaint/politicians/_base.py` (~150 LOC) — `PoliticianPipelineBase` (mirrors `political_parties/_base.py`)
- **NEW registry** `dlt_sources/cianchosaint/politicians/_registry.py` (~200 LOC) — `POLITICIAN_REGISTRY` enumerating the 7 case studies + the harvested names
- **NEW seed** `dlt_sources/cianchosaint/politicians/_registry_seed.json` — auto-generated from `harvest_politicians_from_leabharlann.py`
- **NEW 7 case-study DLT sources** (~100 LOC each):
  - `dlt_sources/cianchosaint/politicians/uk/nigel_farage.py`
  - `dlt_sources/cianchosaint/politicians/uk/zack_polanski.py`
  - `dlt_sources/cianchosaint/politicians/ni/john_o_dowd.py`
  - `dlt_sources/cianchosaint/politicians/ni/gordon_lyons.py`
  - `dlt_sources/cianchosaint/politicians/ni/paul_givan.py`
  - `dlt_sources/cianchosaint/politicians/ni/gavin_robinson.py`
  - `dlt_sources/cianchosaint/politicians/scotland/lara_bird.py`

### DLT source tree 2 — `advisors/`

- **NEW base** `dlt_sources/cianchosaint/advisors/_base.py` (~150 LOC) — `AdvisorPipelineBase`
- **NEW registry** `dlt_sources/cianchosaint/advisors/_registry.py` (~100 LOC) — `ADVISOR_REGISTRY` enumerating the 4 jurisdictional SpAd registers
- **NEW 4 DLT sources**:
  - `dlt_sources/cianchosaint/advisors/uk_hoc_spad_register.py` — UK Cabinet Office SpAd register
  - `dlt_sources/cianchosaint/advisors/ni_assembly_spad_register.py` — NI Assembly SpAd register
  - `dlt_sources/cianchosaint/advisors/oireachtas_advisors.py` — ROI Oireachtas advisors
  - `dlt_sources/cianchosaint/advisors/holyrood_spad_register.py` — Scottish Government SpAd register

### DLT source tree 3 — `funders/`

- **NEW base** `dlt_sources/cianchosaint/funders/_base.py` (~150 LOC) — `FunderPipelineBase`
- **NEW registry** `dlt_sources/cianchosaint/funders/_registry.py` (~200 LOC) — `FUNDER_REGISTRY` enumerating the 9 funder surfaces
- **NEW 9 DLT sources**:
  - `dlt_sources/cianchosaint/funders/electoral_commission_uk.py`
  - `dlt_sources/cianchosaint/funders/electoral_commission_ie.py`
  - `dlt_sources/cianchosaint/funders/electoral_office_ni.py`
  - `dlt_sources/cianchosaint/funders/companies_house_psc.py`
  - `dlt_sources/cianchosaint/funders/register_of_interests_uk_hoc.py`
  - `dlt_sources/cianchosaint/funders/register_of_interests_ni_assembly.py`
  - `dlt_sources/cianchosaint/funders/register_of_interests_oireachtas.py`
  - `dlt_sources/cianchosaint/funders/register_of_interests_holyrood.py`
  - `dlt_sources/cianchosaint/funders/register_of_interests_senedd.py`

### DLT source tree 4 — `historical_associations/`

- **NEW base** `dlt_sources/cianchosaint/historical_associations/_base.py` (~150 LOC) — `HistoricalAssociationPipelineBase`
- **NEW registry** `dlt_sources/cianchosaint/historical_associations/_registry.py` (~100 LOC)
- **NEW 5 DLT sources**:
  - `dlt_sources/cianchosaint/historical_associations/wikidata_politician.py`
  - `dlt_sources/cianchosaint/historical_associations/ni_courts_service.py`
  - `dlt_sources/cianchosaint/historical_associations/oireachtas_courts.py`
  - `dlt_sources/cianchosaint/historical_associations/scot_courts.py`
  - `dlt_sources/cianchosaint/historical_associations/companies_house_officer_history.py`
  - `dlt_sources/cianchosaint/historical_associations/insolvency_service.py`

### DLT source tree 5 — `wikipedia_archives/`

- **NEW base** `dlt_sources/cianchosaint/wikipedia_archives/_base.py` (~150 LOC) — `WikipediaArchivesPipelineBase`
- **NEW registry** `dlt_sources/cianchosaint/wikipedia_archives/_registry.py` (~100 LOC)
- **NEW 5 DLT sources**:
  - `dlt_sources/cianchosaint/wikipedia_archives/wikipedia_en.py`
  - `dlt_sources/cianchosaint/wikipedia_archives/wikipedia_ga.py`
  - `dlt_sources/cianchosaint/wikipedia_archives/wikipedia_cy.py`
  - `dlt_sources/cianchosaint/wikipedia_archives/wikipedia_gd.py`
  - `dlt_sources/cianchosaint/wikipedia_archives/wikidata.py`

### Platform resolvers

- **NEW file** `dlt_sources/official_media_cianchosaint/platforms.py` (~400 LOC) — `resolve_x`, `resolve_facebook`, `resolve_instagram`, `resolve_youtube`, `resolve_tiktok`, `resolve_threads`, `resolve_truth_social`, `resolve_linkedin`, `resolve_gb_news_appearances`, `resolve_talktv_appearances`, `resolve_hansard_url`, `resolve_twfy_url` (mirrors the existing `fediverse.py` pattern)

### FunctionTool layer (4 new tools)

- **NEW** `agents/cianchosaint/tools/politician_account_resolver.py` (~250 LOC) — the Google ADK FunctionTool that systematically gathers the politician schema
- **NEW** `agents/cianchosaint/tools/adjacent_context_resolver.py` (~200 LOC) — umbrella FunctionTool returning the 5-axis context (politician + advisors + funders + historic + wikipedia)
- **NEW** `agents/cianchosaint/tools/funder_network_graph.py` (~150 LOC) — Cognee/Graphiti donor network visualizer
- **NEW** `agents/cianchosaint/tools/wikipedia_bridge.py` (~150 LOC) — Wikidata QID ↔ Politician reconciliation

### `PoliticalGraphStore` extension

- **MODIFIED** `agents/cianchosaint/tools/political_graph_store.py` — extended `EntityType` (4 new: `advisor`, `funder`, `historical_association`, `wikipedia_archives`) + extended `RelationshipType` (4 new: `advises`, `advised_by`, `was_member_of`, `holds_wikidata_qid`)

### OpenSpec artifacts (this change)

- **NEW** `proposal.md` (this file)
- **NEW** `tasks.md`
- **NEW** `cross-repo-sync.md`
- **NEW** `specs/cianchosaint-baml-schemas/spec.md` — the BAML extraction delta
- **NEW** `specs/cianchosaint-bipp-v2/spec.md` — the BIPP v2 cohort cross-reference delta
- **NEW** `specs/cianchosaint-political-graph/spec.md` — the political graph entity-type delta
- **NEW** `specs/cianchosaint-dlt-sources-carveout/spec.md` — the 5 new DLT source-tree deltas
- **NEW** `specs/cianchosaint-agents-sync/spec.md` — the agent-fleet registry delta

### Scripts + CI gates

- **NEW** `scripts/harvest_politicians_from_leabharlann.py` (~250 LOC) — bulk PDF extraction across all 87 PDFs + the 1 .md file
- **NEW** `scripts/lint_politician_schema.py` (~100 LOC) — CI gate: every politician DLT source URL is in the OSINT allowlist; every BAML function declares a Langfuse resolver; every FunctionTool is wired to `PoliticalGraphStore`

### OSINT allowlist

- **MODIFIED** `dlt_sources/cianchosaint/common/osint_allowlist.yaml` — +34 entries covering:
  - 7 personal politician websites (Farage, Polanski, O'Dowd, Lyons, Givan, Robinson, Bird)
  - 7 party `/people/<slug>` URLs
  - 4 SpAd registers (UK / NI / ROI / Holyrood)
  - 3 Electoral Commission registers (UK / ROI / NI)
  - 5 Registers of Members' Interests (UK HoC / NI / ROI / Holyrood / Senedd)
  - Companies House PSC + officer history
  - 4 court services (UK / NI / ROI / Scottish)
  - 4 Wikipedia surfaces (en / ga / cy / gd) + Wikidata Query Service
  - Insolvency Service determinations

### Mise tasks

- **MODIFIED** `mise.toml` — 7 new tasks:
  - `cianchosaint:politician:harvest-leabharlann`
  - `cianchosaint:politician:resolve`
  - `cianchosaint:politician:bulk-resolve`
  - `cianchosaint:adjacent:harvest`
  - `cianchosaint:adjacent:resolve`
  - `cianchosaint:adjacent:bulk-resolve`
  - `cianchosaint:funder-network`

## Impact

- **Affected specs**: 5 modified (`cianchosaint-baml-schemas`, `cianchosaint-bipp-v2`, `cianchosaint-political-graph`, `cianchosaint-dlt-sources-carveout`, `cianchosaint-agents-sync`)
- **Affected code/config**: ~30 NEW files (5 scaffolds + ~24 DLT sources + 4 FunctionTools + 2 scripts) + 4 MODIFIED files (`political_graph_store.py`, `osint_allowlist.yaml`, `mise.toml`, `__init__.py` exports)
- **New BAML functions**: 4 (2 politician + 2 adjacent)
- **New BAML classes**: 8 (SocialHandle + PublicFollowerMetrics + Politician + Advisor + Funder + Donation + HistoricalAssociation + WikipediaArchives)
- **New DLT source modules**: 30 (7 politicians + 4 advisors + 9 funders + 6 historical_associations + 5 wikipedia_archives — minus 1 base + 1 registry each)
- **New entity types in PoliticalGraphStore**: 4
- **New FunctionTools**: 4
- **No secret values are written to disk**: all keys resolve via `infisical://dev-baile/cianchosaint/...` template refs hydrated by mise + Locket
- **The leabharlann repo is unaffected**: the 87 PDFs are read-only context
- **The cianfhoghlaim repo is unaffected**: this change ships only inside `cianchosaint`

## Out of scope (follow-up changes)

- The 7 BIPP v2 CocoIndex flows for politicians + adjacent (follow-up `cianchosaint-bipp-v2-cocoindex-v2-v1`)
- The Dagster defs + asset checks + milestone gates (follow-up `cianchosaint-bipp-v2-orchestration-v2-v1`)
- The RAGAS eval dataset for politician extraction (follow-up `cianchosaint-ragas-eval-pipeline-v2-v1`)
- The CocoIndex flows for the 4 adjacent schemas (follow-up `cianchosaint-adjacent-cocoindex-v1`)
- The generative UI components for the 5-axis context view (follow-up `cianchosaint-generative-ui-kit-v2-v1`)
- The collaboration workspace extension (follow-up `cianchosaint-collaboration-workspace-v2-v1`)

## Dependencies

`Blocked by: cianchosaint-bipp-v2-spec-v1` (must archive first; archived 2026-08-24)
`Blocked by: cianchosaint-bipp-v2-political-party-v2-v1` (must archive first; pending archive)
`Blocked by (soft): cianchosaint-langfuse-prompt-management-v1` (archived 2026-08-24)
`Blocked by (soft): cianchosaint-political-graph-v1` (the PoliticalGraphStore is the foundation — already shipped)
`Blocked by (soft): leabharlann/gemini_deep_research/politics/` (read-only context — already shipped)
`Affected repos: cianchosaint only`

## Cross-repo sync

This change touches ONLY the `cianchosaint/cianchosaint` repo. Cianfhoghlaim + leabharlann remain completely unchanged.

## Verification

```bash
cd /Users/cianmacandeisigh/dev/cianchosaint

# Step 1: Spec validation
openspec validate cianchosaint-politician-schema-v1 --strict
# Expected: Validation passes

openspec validate cianchosaint-baml-schemas --strict
openspec validate cianchosaint-bipp-v2 --strict
openspec validate cianchosaint-political-graph --strict
openspec validate cianchosaint-dlt-sources-carveout --strict
openspec validate cianchosaint-agents-sync --strict
# Expected: all pass

# Step 2: DLT registry sanity check
python3 -c "
import sys; sys.path.insert(0, '.')
from dlt_sources.cianchosaint.politicians._registry import POLITICIAN_REGISTRY
print(f'Politician registry: {len(POLITICIAN_REGISTRY)} entries')"
# Expected: 7 entries (the case studies)

python3 -c "
import sys; sys.path.insert(0, '.')
from dlt_sources.cianchosaint.advisors._registry import ADVISOR_REGISTRY
print(f'Advisor registry: {len(ADVISOR_REGISTRY)} entries')"
# Expected: 4 entries

python3 -c "
import sys; sys.path.insert(0, '.')
from dlt_sources.cianchosaint.funders._registry import FUNDER_REGISTRY
print(f'Funder registry: {len(FUNDER_REGISTRY)} entries')"
# Expected: 9 entries

python3 -c "
import sys; sys.path.insert(0, '.')
from dlt_sources.cianchosaint.historical_associations._registry import HISTORICAL_ASSOCIATION_REGISTRY
print(f'Historical association registry: {len(HISTORICAL_ASSOCIATION_REGISTRY)} entries')"
# Expected: 6 entries

python3 -c "
import sys; sys.path.insert(0, '.')
from dlt_sources.cianchosaint.wikipedia_archives._registry import WIKIPEDIA_ARCHIVES_REGISTRY
print(f'Wikipedia archives registry: {len(WIKIPEDIA_ARCHIVES_REGISTRY)} entries')"
# Expected: 5 entries

# Step 3: FunctionTool sanity check
python3 -c "
from agents.cianchosaint.tools.politician_account_resolver import politician_account_resolver_tool
from agents.cianchosaint.tools.adjacent_context_resolver import adjacent_context_resolver_tool
from agents.cianchosaint.tools.funder_network_graph import funder_network_graph_tool
from agents.cianchosaint.tools.wikipedia_bridge import wikipedia_bridge_tool
print(f'4 FunctionTools wired: {[t.name for t in [politician_account_resolver_tool, adjacent_context_resolver_tool, funder_network_graph_tool, wikipedia_bridge_tool]]}')"
# Expected: ['politician_account_resolver', 'adjacent_context_resolver', 'funder_network_graph', 'wikipedia_bridge']

# Step 4: PoliticalGraphStore extension sanity check
python3 -c "
from agents.cianchosaint.tools.political_graph_store import (
    EntityType, RelationshipType, PoliticalGraphStore
)
assert 'advisor' in EntityType.__args__
assert 'funder' in EntityType.__args__
assert 'historical_association' in EntityType.__args__
assert 'wikipedia_archives' in EntityType.__args__
assert 'advises' in RelationshipType.__args__
assert 'advised_by' in RelationshipType.__args__
assert 'was_member_of' in RelationshipType.__args__
assert 'holds_wikidata_qid' in RelationshipType.__args__
print('PoliticalGraphStore extended correctly: +4 entity types, +4 relationship types')"

# Step 5: Leabharlann harvest dry-run (offline path — just list PDFs)
python3 -c "
import os, sys
pdf_dir = os.environ.get('LEABHARLANN_POLITICS_DIR', '/Users/cianmacandeisigh/dev/leabharlann/gemini_deep_research/politics')
files = sorted([f for f in os.listdir(pdf_dir) if f.endswith(('.pdf', '.md'))])
print(f'Leabharlann politics PDFs found: {len(files)}')
print('First 3:', files[:3])"
# Expected: Leabharlann politics PDFs found: 88

# Step 6: CI gates
mise run lint:license
mise run lint:politician-schema
mise run openspec:validate-all
# Expected: all pass
```
