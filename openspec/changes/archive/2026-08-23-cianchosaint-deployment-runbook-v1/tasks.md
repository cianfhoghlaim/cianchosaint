# Tasks: cianchosaint-deployment-runbook-v1

## 0. Pre-flight (preconditions)

- [ ] Verify the 13 stacks are present at `bonneagar/stacks/` — DONE
- [ ] Verify `mise run devops:validate-stacks` exits 0 — DONE
- [ ] Verify the 8 per-persona web apps are present at `web/apps/ciafagent-*/`
- [ ] Verify the 24 per-constituency agents are present at `agents/cianchosaint/`
- [ ] Verify the 4-tier `ModelProviderRouter` is at
      `baml_src/_shared/provider_router.py`
- [ ] Verify CCC indexing is set up at `.cocoindex_code/` (settings.yml + guides.yml)
- [ ] Verify the OSINT allowlist is at
      `dlt_sources/cianchosaint/common/osint_allowlist.yaml`

## 1. OpenSpec artifacts

- [ ] Author `openspec/changes/cianchosaint-deployment-runbook-v1/proposal.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-deployment-runbook-v1/tasks.md` — this file
- [ ] Author `openspec/changes/cianchosaint-deployment-runbook-v1/cross-repo-sync.md` — NONE-equivalent (record the "Cianfhoghlaim unchanged" stance)
- [ ] Author `openspec/changes/cianchosaint-deployment-runbook-v1/specs/cianchosaint-deployment/spec.md` (delta — 6 ADDED Requirements)
- [ ] Author `openspec/specs/cianchosaint-deployment/spec.md` (canonical END-STATE spec, 6 Requirements + Scenarios)
- [ ] Author `openspec/specs/cianchosaint-deployment/AGENTS.md` (≤30 lines per the repo-hygiene convention)

## 2. The deployment runbook

- [ ] Author `docs/DEPLOYMENT.md` with the 13 required sections:
      1. Overview (13 stacks + 8 apps + 24 agents + 4-tier router + CCC + allowlist)
      2. The 13 compose stacks (table: stack | port | purpose | env vars | dependencies)
      3. Stack ordering — the lifecycle (infisical → motherduck/lakehouse → litellm/unsloth-serve → langfuse → crawl4ai/stagehand → changedetection → komodo/pangolin/locket → openchamber)
      4. Per-stack deployment (env vars + commands + smoke test + rollback, for each of the 13)
      5. Cross-stack contracts (Locket sidecar, Komodo/Pangolin wiring, the 4-tier provider chain, the OSINT allowlist)
      6. The 8 per-persona web apps (table: app | URL | route | backing agent)
      7. The 24 per-constituency agents (table: agent | constituency | sub-domain | backing BAML)
      8. Deployment to `arm1-oci` (procedures + commands + env files)
      9. Deployment to `bunchloch` (MacBook M4 local-dev procedures)
      10. Self-host citizen deployment (`docker/ciafagent-self-host/` procedures)
      11. Smoke tests (per-stack smoke test command table)
      12. Health checks (`mise run cianchosaint:provider:health-check` + `cianchosaint:browser-tool:health-check` + `cianchosaint:osint:health-check`)
      13. Rollback plan (per-stack rollback procedures)

## 3. Validation gates

- [ ] Run `openspec validate cianchosaint-deployment-runbook-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-deployment --strict` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL changes + ALL specs pass
- [ ] Run `mise run lint:drift-docs` and verify the runbook's number claims match ground truth
- [ ] Verify all 13 internal links in `docs/DEPLOYMENT.md` resolve (no broken links)
- [ ] Verify all 8 ciafagent apps + 24 agents are enumerated correctly

## 4. CI gates + commit + push

- [ ] Commit on `cianchosaint:main` with message: `docs(openspec): cianchosaint-deployment-runbook-v1 — the canonical 13-stacks + 8-apps + 24-agents deployment runbook`
- [ ] Push to `github.com/cianfhoghlaim/cianchosaint`
- [ ] Archive `cianchosaint-deployment-runbook-v1` (no blockers)

## 5. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-pantheon-migration-v1` — if/when the 13-stack model
      needs to scale to 94 stacks
- [ ] `cianchosaint-citizen-use-grant-v1` — the licence amendment for
      citizen self-host (may revise §10 of the runbook)

## Verification

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint

openspec list --specs
# Expected: 9 specs (the 8 existing + cianchosaint-deployment)

openspec list
# Expected: at least 2 pending changes (cianchosaint-deployment-runbook-v1 + ...)

openspec validate --all --strict
# Expected: ALL pass

ls docs/DEPLOYMENT.md
# Expected: file exists (~3,000-5,000 words)

wc -l docs/DEPLOYMENT.md
# Expected: ≤ 500 lines (markdown is dense)

# Verify the runbook links resolve
grep -c 'href=' docs/DEPLOYMENT.md
# Expected: ≥ 30 links (the runbook links to many specs + stacks + agents)

# Verify the 13 stacks are documented
grep -c '^###.*[Ss]tack\|## .*litellm\|## .*langfuse\|## .*motherduck\|## .*lakehouse\|## .*unsloth\|## .*openchamber\|## .*crawl4ai\|## .*stagehand\|## .*changedetection\|## .*komodo\|## .*pangolin\|## .*infisical\|## .*locket' docs/DEPLOYMENT.md
# Expected: ≥ 13

# Verify the 8 apps + 24 agents are documented
grep -c 'ciafagent-' docs/DEPLOYMENT.md
# Expected: ≥ 8
grep -c '_(root\|specialists)_' docs/DEPLOYMENT.md
# Expected: ≥ 24
```
