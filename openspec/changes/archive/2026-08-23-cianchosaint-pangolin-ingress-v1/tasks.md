# Tasks: cianchosaint-pangolin-ingress-v1

## 0. Pre-flight

- [x] Verify `cianchosaint-per-persona-app-bundles-v1` is archived
- [x] Verify the 8 per-persona apps + the Hono API gateway exist
  on disk
- [x] Verify `bonneagar/pangolin/` directory exists
- [x] Verify the wholesale-copied Pangolin pattern from Cianfhoghlaim
  has the 6-label private resource convention

## 1. OpenSpec artifacts

- [ ] Author `openspec/changes/cianchosaint-pangolin-ingress-v1/proposal.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-pangolin-ingress-v1/tasks.md` (this file) — DONE
- [ ] Author `openspec/changes/cianchosaint-pangolin-ingress-v1/cross-repo-sync.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-pangolin-ingress-v1/specs/cianchosaint-pangolin-ingress/spec.md` (the 2 ADDED Requirements delta) — DONE
- [ ] Author `openspec/specs/cianchosaint-pangolin-ingress/spec.md` (canonical END-STATE spec) — DONE
- [ ] Author `openspec/specs/cianchosaint-pangolin-ingress/AGENTS.md` (per-spec routing) — DONE

## 2. Validation gates

- [ ] Run `openspec validate cianchosaint-pangolin-ingress-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-pangolin-ingress --strict` and verify exit code 0
- [ ] Run `python3.13 -c "import yaml; yaml.safe_load(open('bonneagar/pangolin/cianchosaint_resources.yaml').read())"` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL pass

## 3. Implementation: 1 YAML resource file

### Pangolin resources (1 file at `bonneagar/pangolin/`)
- [ ] `cianchosaint_resources.yaml` — the canonical Pangolin resource
  definitions for the 9 services (8 web apps + 1 API gateway)

## 4. Per-file pattern

```yaml
version: 1
resources:
  - name: ga.cianchosaint.ie
    type: web
    target: ciafagent-ga-public:7777
    visibility: public
    auth: pocketid
    labels: {constituency: ga, app: ciafagent-ga-public, persona: public}

  - name: api.cianchosaint.ie
    type: api
    target: ciafagent-api:8787
    visibility: private
    auth: pocketid
    labels: {app: ciafagent-api, role: hono-api-gateway}
```

## 5. CI gates + commit + push

- [ ] Run `python3.13 -c "import yaml; yaml.safe_load(open('bonneagar/pangolin/cianchosaint_resources.yaml').read())"` and verify
- [ ] Run `openspec validate --all --strict` and verify ALL pass
- [ ] Commit on `cianchosaint:main` with message: `feat(q3q4-track2): Pangolin ingress for 8 web apps + Hono API gateway (Change 13)`
- [ ] Push to `github.com/cianfhoghlaim/cianchosaint`

## 6. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-pangolin-apply-resources-v1` — wire
  `mise run pangolin:resources:apply` into the CI pipeline
