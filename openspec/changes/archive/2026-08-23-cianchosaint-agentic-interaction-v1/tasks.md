# Tasks: cianchosaint-agentic-interaction-v1

## 0. Pre-flight

- [ ] Verify `cianchosaint-repo-foundation-v1` has archived (it's still pending; this task is for sequencing the next change after the foundation lands)
- [ ] Verify openspec CLI: `openspec --version` (expected 1.4.1)
- [ ] Verify the 4-tier `ModelProviderRouter` contract is documented (per the foundation change)
- [ ] Verify the existing Cianfhoghlaim legal pipelines still exist (per the cross-repo mirror pattern)

## 1. New specs (canonical + AGENTS.md)

- [ ] Write `openspec/specs/cianchosaint-agentic-interaction/spec.md` (6 Requirements, ~7 Scenarios) — DONE
- [ ] Write `openspec/specs/cianchosaint-agentic-interaction/AGENTS.md` (≤30 lines per the repo-hygiene convention) — DONE
- [ ] Write `openspec/specs/cianchosaint-self-hosted-citizen/spec.md` (4 Requirements, 4 Scenarios) — DONE
- [ ] Write `openspec/specs/cianchosaint-self-hosted-citizen/AGENTS.md` (≤30 lines) — DONE
- [ ] Write `openspec/specs/cianchosaint-per-constituency-agents/spec.md` (6 Requirements, 7 Scenarios) — DONE
- [ ] Write `openspec/specs/cianchosaint-per-constituency-agents/AGENTS.md` (≤30 lines) — DONE

## 2. OpenSpec change artifacts

- [ ] Write `openspec/changes/cianchosaint-agentic-interaction-v1/proposal.md` (this file's purpose) — DONE
- [ ] Write `openspec/changes/cianchosaint-agentic-interaction-v1/tasks.md` (this file) — DONE
- [ ] Write `openspec/changes/cianchosaint-agentic-interaction-v1/cross-repo-sync.md` — DONE
- [ ] Write `openspec/changes/cianchosaint-agentic-interaction-v1/specs/cianchosaint-agentic-interaction/spec.md` (the ADDED Requirements delta) — TODO
- [ ] Write `openspec/changes/cianchosaint-agentic-interaction-v1/specs/cianchosaint-self-hosted-citizen/spec.md` (the ADDED Requirements delta) — TODO
- [ ] Write `openspec/changes/cianchosaint-agentic-interaction-v1/specs/cianchosaint-per-constituency-agents/spec.md` (the ADDED Requirements delta) — TODO

## 3. Validation gates

- [ ] Run `openspec validate cianchosaint-agentic-interaction-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-agentic-interaction --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-self-hosted-citizen --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-per-constituency-agents --strict` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL changes + ALL specs pass

## 4. Implementation (P1a — GA agentic interaction)

- [ ] Add `pyproject.toml` `[tool.uv.sources]` entry to mirror the Cianfhoghlaim legal pipelines
- [ ] Author `agents/cianchosaint/__init__.py` (the 24-agent fleet registry)
- [ ] Author `agents/cianchosaint/ga_root_agent.py` (Google ADK root for An Garda Síochána)
- [ ] Author `agents/cianchosaint/ga_specialists/` (5 specialist agents)
- [ ] Author `agents/cianchosaint/tools/garda_form_fill.py` (Google ADK FunctionTool)
- [ ] Author `agents/cianchosaint/tools/statute_lookup.py`
- [ ] Author `agents/cianchosaint/tools/foia_request.py`
- [ ] Author `web/apps/cianchosaint-ga-public/` (TanStack Start + Convex + AG-UI + CopilotKit)
- [ ] Author `web/apps/cianchosaint-ga-internal/` (Garda member interface)

## 5. Implementation (P1b — GA traffic violation form filler)

- [ ] Author `dlt_sources/cianchosaint/ireland/garda/traffic_violation_form.py`
- [ ] Author `baml_src/cianchosaint/processing/garda_traffic.baml`
- [ ] Wire `agents/cianchosaint/tools/garda_form_fill.py` to the new DLT + BAML

## 6. Implementation (P2a — MET agent)

- [ ] Author `agents/cianchosaint/met_root_agent.py`
- [ ] Author `agents/cianchosaint/met_specialists/` (5 specialists)
- [ ] Author `agents/cianchosaint/tools/met_form_fill.py`
- [ ] Author `dlt_sources/cianchosaint/uk/met_police/data_police_uk.py` + 4 sibling DLT sources
- [ ] Author `baml_src/cianchosaint/processing/met_police.baml`
- [ ] Author `web/apps/cianchosaint-met-public/` + `cianchosaint-met-internal/`

## 7. Implementation (P2b — PSNI agent)

- [ ] Author `agents/cianchosaint/psni_root_agent.py`
- [ ] Author `agents/cianchosaint/psni_specialists/` (5 specialists)
- [ ] Author `agents/cianchosaint/tools/psni_form_fill.py`
- [ ] Author `agents/cianchosaint/tools/cross_jurisdiction_query.py`
- [ ] Author `dlt_sources/cianchosaint/ni/psni/press_releases.py` + `justice_ni.py`
- [ ] Author `baml_src/cianchosaint/processing/psni.baml`
- [ ] Author `web/apps/cianchosaint-psni-public/` + `cianchosaint-psni-internal/`

## 8. Implementation (P3 — self-hosted citizen Docker image)

- [ ] Author `docker/cianchosaint-citizen/Dockerfile`
- [ ] Author `docker/cianchosaint-citizen/compose.yaml`
- [ ] Author `docker/cianchosaint-citizen/sidecar.yaml` (Locket)
- [ ] Author `docker/cianchosaint-citizen/secrets.env`
- [ ] Author `docker/cianchosaint-citizen/pangolin.yaml`
- [ ] Author `docker/cianchosaint-citizen/blueprint.yaml`
- [ ] Author `docker/cianchosaint-citizen/.env.example`
- [ ] Author `docker/cianchosaint-citizen/README.md`
- [ ] Author `web/apps/cianchosaint-self-host/`

## 9. CI gates + commit

- [ ] Run `mise run lint:license` and verify exit code 0
- [ ] Run `mise run lint:openspec` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify EVERYTHING passes
- [ ] Commit on `cianchosaint:main` with message:
      `feat(openspec): cianchosaint-agentic-interaction-v1 — agentic interaction layer (Google ADK + 4-tier chain + browser tools)`
- [ ] Push to `github.com/cianfhoghlaim/cianchosaint`
- [ ] Archive this openspec change once the foundation change has also been merged

## 10. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-provider-router-v1` — implements the 4-tier chain
- [ ] `browser-tool-router-v1` — implements the BrowserToolRouter
- [ ] `browser-tool-provider-chain-integration-v1` — wires the chain into browser tools
- [ ] `cianchosaint-baml-schemas-v1` — the per-constituency BAML extraction functions
- [ ] `cianchosaint-bipp-v1` — British Isles Policing Pipeline
- [ ] `cianchosaint-bidp-v1` — British Isles Defence Pipeline
- [ ] `cianchosaint-biip-v1` — British Isles Intelligence Oversight Pipeline
- [ ] `cianchosaint-citizen-use-grant-v1` — license amendment for citizen use
- [ ] `firecrawl-mcp-browser-tool-router-integration-v1` (cianfhoghlaim side) — refactor firecrawl_mcp client
- [ ] `unsloth-studio-pangolin-ingress-v1` (bonneagar side) — Pangolin ingress for Unsloth Studio

## Verification

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list --specs
# Expected: 4 specs (cianchosaint-pipeline + cianchosaint-agentic-interaction + cianchosaint-self-hosted-citizen + cianchosaint-per-constituency-agents)

openspec list
# Expected: 2 changes (cianchosaint-repo-foundation-v1 + cianchosaint-agentic-interaction-v1)

openspec validate --all --strict
# Expected: All pass
```
