# ciafagent-cyberchef

The **GCHQ CyberChef** chat surface — for analysts. Provides a
parallel **GUI-based data analysis interface** alongside the chat-based
analysis the other `ciafagent-*` apps offer, via the AG-UI chat
window.

**RESTRICTED ACCESS** — UK public-sector analyst networks only.

## Stack

- TanStack Start + CopilotKit v2 + AG-UI + Hono + Convex + BetterAuth
- Routes through `ciafagent-api` to `../../agents/cianchosaint/cyberchef_root_agent`

## Surfaces

| Route | Purpose |
|:--|:--|
| `/` | Landing + analyst credentials check |
| `/chat` | AG-UI chat with `cyberchef_root_agent` (recipe generation + execution) |
| `/recipes` | The CyberChef recipe index (per the CyberChef DLT source) |
| `/operation-catalog` | The ~28 operations the FunctionTool wraps (mirrors the upstream GCHQ CyberChef Apache 2.0 catalog) |
| `/executions` | The append-only execution log (per the DLT source) |

## References

- CyberChef wholesale source: `hmgcc/CyberChef/` (Apache 2.0)
- DLT source: `dlt_sources/cianchosaint/uk/cyberchef/recipe_extraction.py`
- BAML extraction: `baml_src/cianchosaint/processing/cyberchef_recipe_extraction.baml`
- FunctionTool: `agents/cianchosaint/tools/cyberchef_execute.py`
- Source catalogue: `docs/source-catalogue/14-uk-gchq-cyberchef.md`
