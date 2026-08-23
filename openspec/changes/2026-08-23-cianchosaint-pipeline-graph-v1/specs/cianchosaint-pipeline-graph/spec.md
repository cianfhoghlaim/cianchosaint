# Spec Delta: cianchosaint-pipeline-graph

This delta is applied by the openspec change
[`cianchosaint-pipeline-graph-v1`](../proposal.md). It describes the
ADDED Requirements to the canonical
[`openspec/specs/cianchosaint-pipeline-graph/spec.md`](../../../../specs/cianchosaint-pipeline-graph/spec.md)
that this change adds.

## ADDED Requirements

### Requirement: The hand-rolled React + d3.js `PipelineGraph` component

The system SHALL provide a React + d3.js pipeline graph component at
`web/packages/ui-kit/components/PipelineGraph.tsx` that visualises
the 5-stage Cianchosaint pipeline for a given persona.

The component SHALL satisfy:

1. Read the per-source VLM extraction results + per-source cost +
   per-source latency + per-source extraction pass-rate from the
   Convex `vlmPipelineDashboard` table via `useQuery` from
   `convex/react` (the wholesale-copied Cianfhoghlaim pattern).
2. Render 5 stage nodes (DLT source → BAML extraction → CocoIndex v1
   embedding → LanceDB / DuckLake target → AG-UI consumer) with
   per-source labels attached to each stage.
3. Render per-source VLM model + OCR confidence + extraction
   pass-rate + cost (Unsloth Studio credits) on hover (via the
   wholesale-copied Radix UI HoverCard primitive).
4. Render per-stage cost + latency badges on the edges connecting
   adjacent stages.
5. Use `d3-force` for layout so the graph auto-arranges for any
   number of sources (no hand-tuned positions).
6. Support a `persona: 'analyst' | 'lawyer' | 'judge' | 'oversight'`
   prop that switches the highlight colour (per the per-persona
   colour scheme in the wholesale-copied Cianfhoghlaim pattern).
7. Export `PipelineGraph` as the named export from the component
   file (the wholesale-copied Cianfhoghlaim `data-slot="pipeline-graph"`
   convention).

The component file SHALL be valid TypeScript parseable by
`tsc --noEmit --strict` with the wholesale-copied
`web/packages/ui-kit/tsconfig.json` settings.

#### Scenario: The component renders 5 stage nodes

- **WHEN** the operator mounts `<PipelineGraph persona="analyst" />`
  in any of the 8 per-persona web apps
- **THEN** the component SHALL render exactly 5 stage nodes with
  the per-stage labels (`DLT source`, `BAML extraction`,
  `CocoIndex v1 embedding`, `LanceDB / DuckLake target`,
  `AG-UI consumer`)

#### Scenario: The component reads from vlmPipelineDashboard

- **WHEN** the operator mounts the component with a populated
  `vlmPipelineDashboard` Convex table
- **THEN** the component SHALL render per-source hover cards with
  the VLM model + OCR confidence + extraction pass-rate + cost
  pulled from the table

#### Scenario: The component switches persona colour

- **WHEN** the operator mounts the component with
  `persona="judge"`
- **THEN** the highlight colour SHALL switch from the analyst
  default to the judge colour scheme
- **AND** the per-stage edges SHALL still render the cost + latency
  badges regardless of persona

### Requirement: The static SVG/PNG generator

The system SHALL provide a static SVG/PNG generator at
`scripts/pipeline_graph_generator.py` that produces a
docs-embeddable pipeline graph image for use in the README, the
governance docs, and the case-study pages.

The generator SHALL satisfy:

1. Read the same per-source metadata as `PipelineGraph.tsx`
   (hard-coded at module scope for offline generation).
3. Produce `docs/figures/pipeline-graph-{YYYY-MM-DD}.svg` and
   `docs/figures/pipeline-graph-{YYYY-MM-DD}.png` where
   `{YYYY-MM-DD}` is `datetime.now(UTC).strftime('%Y-%m-%d')`.
4. Use the `cairosvg` library (already in the wholesale-copied
   Cianfhoghlaim pattern at `pyproject.toml`) for SVG → PNG
   conversion.
5. Exit 0 on success, exit 1 on missing deps with a clear error
   message pointing at `pip install cairosvg`.
6. Be invokable via `python scripts/pipeline_graph_generator.py`
   (no CLI args required — uses defaults) or
   `python scripts/pipeline_graph_generator.py --output-dir ./out`
   (CLI args via the wholesale-copied Cianfhoghlaim `click` pattern).

The Python file SHALL be valid Python 3.13 parseable by
`python3 -c "import ast; ast.parse(open('scripts/pipeline_graph_generator.py').read())"`.

#### Scenario: The generator produces an SVG + PNG pair

- **WHEN** the operator runs
  `python scripts/pipeline_graph_generator.py`
- **THEN** the generator SHALL produce exactly 2 files in
  `docs/figures/`: one `.svg` and one `.png`
- **AND** both files SHALL be non-empty

#### Scenario: The generator exits 1 on missing cairosvg

- **WHEN** the operator uninstalls `cairosvg` (or the import fails
  for any reason) and runs the generator
- **THEN** the generator SHALL exit with code 1
- **AND** SHALL print a clear error message pointing at
  `pip install cairosvg`

### Requirement: The CocoInsight future-swap-in note

The system SHALL document (in the canonical spec's Background
section + in `docs/research/cocoinsight-v0-research.md`) that if
CocoIndex V1 ever ships a stable CocoInsight-compatible HTTP server
API (tracked upstream as
[cocoindex-io/cocoindex#1351](https://github.com/cocoindex-io/cocoindex/issues/1351)),
the React + d3.js component SHALL be replaceable with a one-line
swap (`<PipelineGraph>` → `<CocoInsightEmbed url="..." />`) without
any other code change.

The swap-in SHALL satisfy:

1. The component interface (`props: { persona: ... }`) SHALL remain
   stable across the swap.
2. The Convex `vlmPipelineDashboard` table schema SHALL remain
   unchanged (CocoInsight already shows per-step data preview,
   which is functionally equivalent to the per-source hover cards).
3. The per-persona view layer SHALL remain a Cianchosaint-specific
   concern (CocoInsight's spreadsheet UX is unsuitable for
   case-file presentation; cianchosaint's per-persona view is).

#### Scenario: The swap-in note is present in both locations

- **WHEN** the operator reads
  `openspec/specs/cianchosaint-pipeline-graph/spec.md` Background
  section
- **THEN** the operator SHALL find the CocoInsight swap-in note
- **AND WHEN** the operator reads
  `docs/research/cocoinsight-v0-research.md`
- **THEN** the operator SHALL find the same swap-in note (in the
  Decision matrix section)

#### Scenario: The swap-in is one component replacement

- **WHEN** the operator wants to enable CocoInsight
- **THEN** the operator SHALL set the `COCOINSIGHT_ENABLED=true`
  env var
- **AND** replace `<PipelineGraph persona={...} />` with
  `<CocoInsightEmbed url="https://cocoindex.io/cocoinsight" />`
  in the consuming app
- **AND** no other code change SHALL be required