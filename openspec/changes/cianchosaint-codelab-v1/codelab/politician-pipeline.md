# CIANCHOSAINT politician pipeline — codelab

Per `openspec/changes/cianchosaint-codelab-v1/specs/cianchosaint-codelab/spec.md`.

This codelab walks a new analyst through the full cianchosaint politician pipeline:
the 7 case-study politicians + the BAML extraction + the 4 FunctionTools
+ the 3 workflow graphs + the RAGAS eval + the GEPA optimizer.

It mirrors the cianfhoghlaim codelab convention (`loop-lab-table/codelab/`,
`support-memory-lab/codelab/`, `monstertix/codelab/`):

> "Every codelab follows the same convention: `codelab/<name>.md` is the
> markdown walkthrough, `notebooks/<name>.ipynb` is the buildable notebook,
> `solutions/` has the finished code, `scripts/walk.py` runs every assertion
> as a sentence."

## Setup

```bash
git clone https://github.com/cianfhoghlaim/cianchosaint.git
cd cianchosaint
uv sync --all-groups
cp .env.example .env  # fill in GOOGLE_API_KEY + the optional keys
mise run lint:license
```

## Level 1 — the 7 case-study politicians

**Claim:** the cianchosaint politician pipeline knows about 7 specific politicians
(Nigel Farage, Zack Polanski, John O'Dowd, Gordon Lyons, Paul Givan, Gavin Robinson,
Lara Bird) and can resolve each to a structured record.

```python
from agents.cianchosaint._factory import AGENT_FACTORY_REGISTRY

assert set(AGENT_FACTORY_REGISTRY["ga_root_agent"].sub_agents) is not None
assert len(AGENT_FACTORY_REGISTRY) == 18  # 3 root + 15 specialist
```

**Exercise:** add an 8th case-study politician (e.g. Mary Lou McDonald) to
`tests/evals/politician/world.py::POLITICIANS` + the corresponding
`expected_facts(...)` entry. Run `tests/evals/politician/walk.py`.

## Level 2 — the BAML extraction

**Claim:** the BAML `ExtractPoliticianFromWebPage` function (per
`cianchosaint-politician-schema-v1`) produces a structured record from
the party profile + Wikipedia payload.

```python
from baml_client.async_client import b
result = await b.ExtractPoliticianFromWebPage(
    web_page="Nigel Farage leads Reform UK as of 2024.",
    party_id="reform-uk",
    jurisdiction="uk_hoc",
)
assert result.canonical_name == "Nigel Farage"
```

**Exercise:** change the extraction prompt in
`baml_src/cianchosaint/politics/politician_extraction.baml` and re-run
the eval dataset (per `cianchosaint-ragas-eval-dataset-v1`).

## Level 3 — the 4 FunctionTools

**Claim:** the 4 politician FunctionTools work — `politician_account_resolver`,
`adjacent_context_resolver`, `funder_network_graph`, `wikipedia_bridge`.

```python
from agents.cianchosaint.tools import politician_account_resolver
result = await politician_account_resolver(politician_name="Nigel Farage")
assert result["party_id"] == "reform-uk"
```

**Exercise:** add a 5th FunctionTool — `psni_officer_safety_lookup` — that
queries the PSNI officer welfare data via the cianchosaint OSINT allowlist.

## Level 4 — the 3 workflow graphs

**Claim:** the 3 workflow graphs (`politician_resolver_graph`,
`funder_network_graph`, `wikipedia_bridge_graph`) execute end-to-end.

```python
from agents.cianchosaint.workflows import politician_resolver_graph
graph = politician_resolver_graph()
assert graph is not None
```

**Exercise:** add a 4th workflow graph — `party_dossier_graph` — that bundles
the party profile + the funder network + the wikipedia article into one
ADK Workflow graph for the BIPP v2 cohort.

## Level 5 — RAGAS eval + GEPA optimizer

**Claim:** the RAGAS eval (per `cianchosaint-ragas-eval-dataset-v1`) +
GEPA optimizer (per `cianchosaint-ragas-prompt-optimizer-v1`) measure + improve
the politician extraction quality.

```bash
python3 scripts/politician_optimize.py --budget 100
python3 scripts/politician_reward_hacking_study.py --runs 4
```

**Exercise:** write your own politician agent instruction, then run
`adk optimize` against the canonical eval dataset. Verify the score
improves from ~0.6 to ~1.0.

## The one rule to carry through all five levels

> *The loop is neutral machinery — it pushes up whatever number you hand it.
> Everything here is about which number you hand it.*

If the honest judge scores your agent at 1.0 and the gameable judge at 0.8,
your agent is good. If the honest judge scores your agent at 0.6 and the
gameable judge at 0.9, your agent is gaming the wrong metric — and the
reward-hacking study will tell you so.

## Next steps

- The full web-app adapters (`webapps/politician-pipeline/`) — separate change (T3.4)
- The Dagster integration (T3.3) — uses this codelab but is a separate change
- The narrative-deep-dive (`T4.1`) — extends the codelab with `season_search` + `season_known_issue`

## Where to go next

- Run `python3 openspec/changes/cianchosaint-codelab-v1/scripts/walk.py` to verify every assertion
- Build the Colab notebook: `python3 openspec/changes/cianchosaint-codelab-v1/notebooks/build.py`
- Read the source: every pattern is wholesale-adapted from cianfhoghlaim
