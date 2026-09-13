## ADDED Requirements

### Requirement: 4 new FunctionTools wired into the per-constituency agent fleet

The system SHALL extend the per-constituency agent fleet registry at `agents/cianchosaint/tools/__init__.py` with 4 new FunctionTools:

1. `politician_account_resolver_tool` — the canonical FunctionTool for systematically gathering the per-politician schema (Axis A — uses Firecrawl + the 13 platform resolvers + the 7 politician DLT sources)
2. `adjacent_context_resolver_tool` — the umbrella FunctionTool returning the 5-axis context (politician + advisors + funders + historic + wikipedia)
3. `funder_network_graph_tool` — the Cognee/Graphiti donor network visualizer
4. `wikipedia_bridge_tool` — the Wikidata QID ↔ Politician reconciliation tool (live SPARQL)

#### Scenario: All 4 tools export via `agents.cianchosaint.tools.__init__`

- **WHEN** the operator runs `python3 -c "from agents.cianchosaint.tools import politician_account_resolver_tool, adjacent_context_resolver_tool, funder_network_graph_tool, wikipedia_bridge_tool"`
- **THEN** the import SHALL succeed
- **AND** each tool SHALL have a `.name` attribute matching the canonical name

#### Scenario: The 7 root agents can dispatch to the new tools

- **WHEN** the operator inspects `agents/cianchosaint/ga_root_agent.py`, `met_root_agent.py`, `psni_root_agent.py`
- **THEN** each root agent's `sub_agents` list SHALL optionally include a `politician_research_agent` that wraps the 4 new tools
- **AND** the `CianchosaintAgentBase.check_osint_source()` gate SHALL be invoked before every external URL access (per the existing pattern)
