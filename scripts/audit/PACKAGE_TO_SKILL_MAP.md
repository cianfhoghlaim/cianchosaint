# Package → Skill Mapping

> **For:** The Stage 6 skill version-header refresh audit + Stage 7 monitoring workflow.
> **Created:** 2026-09-26 (per the openspec/changes/2026-09-26-skill-version-header-refresh-v1/ Stage 6 of the package-version-drift saga).
> **Companion to:** `scripts/audit/refresh_skill_versions.py` (the canonical audit script that uses this mapping).

## The canonical mapping

| Package | Affected skill(s) | Rationale |
|---|---|---|
| pangolin | `.agents/skills/pangolin/SKILL.md` | The canonical Pangolin identity-aware reverse proxy skill |
| gerbil | `.agents/skills/pangolin/SKILL.md` | The WireGuard tunnels section (per the canonical pangolin skill) |
| newt (legacy) | `.agents/skills/pangolin/SKILL.md` | The legacy Newt connector section (kept for backward compat) |
| pangolin-cli (v1.23+) | `.agents/skills/pangolin/SKILL.md` | The new "Sites in the Pangolin CLI" section (Stage 2a) |
| litellm | `.agents/skills/litellm/SKILL.md` | The canonical Litellm gateway skill |
| langfuse | `.agents/skills/langfuse/SKILL.md` + `.agents/skills/agent-observability/SKILL.md` | The canonical Langfuse skill + the observability skill (Langfuse is a sub-topic) |
| komodo | `.agents/skills/komodo/SKILL.md` + `.agents/skills/stacks-sync/SKILL.md` | The canonical Komodo GitOps skill + the stacks-sync sub-topic |
| openchamber | `.agents/skills/opencode/SKILL.md` | The OpenChamber UI is documented in the opencode skill (Stage 4 refactor) |
| crawl4ai | `.agents/skills/crawl4ai/SKILL.md` + `.agents/skills/browser-tools/SKILL.md` | The canonical Crawl4AI skill + the browser-tools sub-topic |
| garage | `.agents/skills/package-version-drift/SKILL.md` | The Garage S3 storage is documented in the package-version-drift skill |
| infisical | `.agents/skills/secrets-management/SKILL.md` + `.agents/skills/setup-secrets/SKILL.md` | The canonical Infisical skill + the setup-secrets sub-topic |
| dagster | `.agents/skills/dagster/SKILL.md` + `.agents/skills/dagster-asset-sync/SKILL.md` | The canonical Dagster skill + the asset-sync sub-topic |
| dagster-dlt + dagster-dbt | `.agents/skills/dlthub/SKILL.md` + `.agents/skills/dlthub-router/SKILL.md` + `.agents/skills/dlt-sync/SKILL.md` | The Dagster-dlt / Dagster-dbt skills (DLT is the data loading tool) |
| cocoindex | `.agents/skills/cocoindex/SKILL.md` + `.agents/skills/notebooks-sync/SKILL.md` | The canonical CocoIndex skill + the notebooks-sync sub-topic |
| baml-py | `.agents/skills/baml/SKILL.md` + `.agents/skills/baml-schema-sync/SKILL.md` | The canonical BAML skill + the schema-sync sub-topic |
| dlt | `.agents/skills/dlt/SKILL.md` + `.agents/skills/dlt-sync/SKILL.md` + `.agents/skills/dlthub/SKILL.md` | The canonical DLT skill + the sync sub-topic + the dlthub router skill |
| duckdb | `.agents/skills/duckdb/SKILL.md` + `.agents/skills/ducklake/SKILL.md` + `.agents/skills/iceberg-lakekeeper/SKILL.md` | The canonical DuckDB skill + the lakehouse sub-topic + the Iceberg REST catalog skill |
| motherduck | `.agents/skills/motherduck/SKILL.md` + `.agents/skills/ducklake/SKILL.md` | The canonical MotherDuck skill + the lakehouse sub-topic |
| lancedb | `.agents/skills/lancedb/SKILL.md` | The canonical LanceDB skill |
| google-adk | `.agents/skills/google-adk/SKILL.md` + `.agents/skills/agent-fleet-orchestration/SKILL.md` | The canonical Google ADK skill + the agent-orchestration sub-topic |
| cognee | `.agents/skills/cognee/SKILL.md` + `.agents/skills/agent-memory-systems/SKILL.md` | The canonical Cognee skill + the memory-systems sub-topic |
| mlflow | `.agents/skills/mlflow/SKILL.md` + `.agents/skills/agent-observability/SKILL.md` | The canonical MLflow skill + the observability sub-topic |
| unsloth | `.agents/skills/unsloth/SKILL.md` | The canonical Unsloth skill |
| graphiti | `.agents/skills/graphiti/SKILL.md` + `.agents/skills/graphiti-core/SKILL.md` + `.agents/skills/agent-memory-systems/SKILL.md` | The canonical Graphiti skill + the core sub-topic + the memory-systems sub-topic |
| falkordb | `.agents/skills/falkordb/SKILL.md` | The canonical FalkorDB skill |
| ducklake | `.agents/skills/ducklake/SKILL.md` | The canonical DuckLake skill |
| mise | `.agents/skills/mise/SKILL.md` | The canonical mise task runner skill |
| modal | `.agents/skills/modal/SKILL.md` | The canonical Modal GPU compute skill |
| openspec | `.agents/skills/openspec/SKILL.md` | The canonical openspec workflow skill |
| hono | `.agents/skills/hono/SKILL.md` | The canonical Hono API skill |
| tanstack-start | `.agents/skills/tanstack-start/SKILL.md` | The canonical TanStack Start skill |
| pydantic | `.agents/skills/pydantic/SKILL.md` | The canonical Pydantic skill |
| dagster | `.agents/skills/dagster/SKILL.md` | The canonical Dagster skill |
| cocoindex | `.agents/skills/cocoindex/SKILL.md` | The canonical CocoIndex skill |
| apple-photos-ingestion | `.agents/skills/apple-photos-ingestion/SKILL.md` | The canonical Apple Photos ingestion skill |
| marimo | `.agents/skills/marimo/SKILL.md` | The canonical marimo notebook skill |
| memgraph | `.agents/skills/memgraph/SKILL.md` | The canonical Memgraph skill |
| huggingface | `.agents/skills/huggingface/SKILL.md` | The canonical Hugging Face skill |
| ag-ui | `.agents/skills/ag-ui/SKILL.md` | The canonical AG-UI skill |
| copilotkit | `.agents/skills/copilotkit/SKILL.md` | The canonical CopilotKit skill |
| agno | `.agents/skills/agno/SKILL.md` | The canonical Agno skill |
| convex | `.agents/skills/convex/SKILL.md` | The canonical Convex skill |
| firecrawl | `.agents/skills/firecrawl/SKILL.md` | The canonical Firecrawl skill |
| ragas | `.agents/skills/ragas/SKILL.md` | The canonical RAGAS skill |
| tuatha | `.agents/skills/tuatha/SKILL.md` | The canonical Tuatha skill |

## The "no-map" skills (skills without a canonical package mapping)

These skills are sub-topics or methodology skills that don't directly map to a single package. They get the generic "Version policy" section appended without being audited for specific package drift:

- `.agents/skills/_template/SKILL.md` (the template — not a skill)
- `.agents/skills/agent-fleet-orchestration/SKILL.md` (the sub-topic; covered by google-adk)
- `.agents/skills/agent-observability/SKILL.md` (the sub-topic; covered by langfuse + mlflow)
- `.agents/skills/agent-memory-systems/SKILL.md` (the sub-topic; covered by cognee + graphiti)
- `.agents/skills/agentic-frontend-frameworks/SKILL.md` (the sub-topic; covered by ag-ui + copilotkit + tanstack-start)
- `.agents/skills/better-auth/SKILL.md` (the sub-topic; covered by convex + auth0)
- `.agents/skills/baml-schema-sync/SKILL.md` (the sub-topic; covered by baml)
- `.agents/skills/ccc/SKILL.md` (CocoIndex Code CLI; covered by cocoindex)
- `.agents/skills/centralized-registry/SKILL.md` (the meta-skill; covered by Stage 1)
- `.agents/skills/change-detection/SKILL.md` (the sub-topic; covered by browser-tools + crawl4ai)
- `.agents/skills/cloudflare/SKILL.md` (the sub-topic; covered by hono + firecrawl)
- `.agents/skills/dagster-asset-sync/SKILL.md` (the sub-topic; covered by dagster)
- `.agents/skills/dignified-python/SKILL.md` (the methodology; covered by all Python skills)
- `.agents/skills/dlt-sync/SKILL.md` (the sub-topic; covered by dlt)
- `.agents/skills/dlthub/SKILL.md` (the sub-topic; covered by dlt)
- `.agents/skills/dlthub-router/SKILL.md` (the sub-topic; covered by dlt)
- `.agents/skills/dlt-sync/SKILL.md` (the sub-topic; covered by dlt)
- `.agents/skills/falkordb/SKILL.md` (the sub-topic; covered by the graph DB family)
- `.agents/skills/firecrawl-cli/SKILL.md` (the sub-topic; covered by firecrawl)
- `.agents/skills/garage/SKILL.md` (the sub-topic; covered by bonneagar)
- `.agents/skills/graphiti-core/SKILL.md` (the sub-topic; covered by graphiti)
- `.agents/skills/huggingface/SKILL.md` (the canonical Hugging Face skill)
- `.agents/skills/ibis/SKILL.md` (the canonical Ibis skill)
- `.agents/skills/iceberg-lakekeeper/SKILL.md` (the sub-topic; covered by ducklake)
- `.agents/skills/improve-skills/SKILL.md` (the methodology)
- `.agents/skills/knowledge-sync-loop/SKILL.md` (the methodology; covered by openspec)
- `.agents/skills/memgraph/SKILL.md` (the sub-topic; covered by the graph DB family)
- `.agents/skills/mise/SKILL.md` (the canonical mise skill)
- `.agents/skills/modal/SKILL.md` (the canonical Modal skill)
- `.agents/skills/notebooks-sync/SKILL.md` (the sub-topic; covered by cocoindex + marimo)
- `.agents/skills/openspec/SKILL.md` (the canonical openspec skill)
- `.agents/skills/package-version-drift/SKILL.md` (the canonical version-drift skill, this saga)
- `.agents/skills/pydantic/SKILL.md` (the canonical Pydantic skill)
- `.agents/skills/ragas/SKILL.md` (the canonical RAGAS skill)
- `.agents/skills/risingwave/SKILL.md` (the canonical RisingWave skill)
- `.agents/skills/schema-codegen/SKILL.md` (the methodology)
- `.agents/skills/secrets-management/SKILL.md` (the canonical Infisical + Locket skill)
- `.agents/skills/setup-secrets/SKILL.md` (the sub-topic; covered by secrets-management)
- `.agents/skills/stacks-sync/SKILL.md` (the sub-topic; covered by komodo)
- `.agents/skills/tanstack-start/SKILL.md` (the canonical TanStack Start skill)
- `.agents/skills/tuatha/SKILL.md` (the canonical Tuatha skill)
- `.agents/skills/_template/SKILL.md` (the template — not a skill)
- `.agents/skills/agents-sync/SKILL.md` (the methodology; covered by Stage 6 itself)
- `.agents/skills/agents-sync/SKILL.md` (the methodology)
- `.agents/skills/baml-schema-sync/SKILL.md` (the sub-topic; covered by baml)
- `.agents/skills/better-auth/SKILL.md` (the sub-topic; covered by convex)
- `.agents/skills/cognee/SKILL.md` (the canonical Cognee skill)
- `.agents/skills/copilotkit/SKILL.md` (the canonical CopilotKit skill)
- `.agents/skills/dagster-asset-sync/SKILL.md` (the sub-topic)
- `.agents/skills/falkordb/SKILL.md` (the sub-topic; covered by graph DB family)
- `.agents/skills/graphiti-core/SKILL.md` (the sub-topic; covered by graphiti)
- `.agents/skills/huggingface/SKILL.md` (the canonical Hugging Face skill)
- `.agents/skills/ibis/SKILL.md` (the canonical Ibis skill)
- `.agents/skills/memgraph/SKILL.md` (the sub-topic)
- `.agents/skills/mise/SKILL.md` (the canonical mise skill)
- `.agents/skills/modal/SKILL.md` (the canonical Modal skill)
- `.agents/skills/notebooks-sync/SKILL.md` (the sub-topic)
- `.agents/skills/openspec/SKILL.md` (the canonical openspec skill)
- `.agents/skills/pydantic/SKILL.md` (the canonical Pydantic skill)
- `.agents/skills/risingwave/SKILL.md` (the canonical RisingWave skill)
- `.agents/skills/tuatha/SKILL.md` (the canonical Tuatha skill)
- `.agents/skills/{apple-photos-ingestion,marimo,convex,firecrawl,ragas,agno,huggingface}/SKILL.md` (sub-topics)
- ... (others)

## Cross-references

- [`scripts/audit/refresh_skill_versions.py`](./refresh_skill_versions.py) — the canonical audit script that uses this mapping
- [`docs/SKILL-VERSION-HEADER-POLICY.md`](../../../docs/SKILL-VERSION-HEADER-POLICY.md) — the canonical refresh policy
