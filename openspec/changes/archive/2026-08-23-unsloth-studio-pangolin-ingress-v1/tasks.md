# Tasks: unsloth-studio-pangolin-ingress-v1

## 0. Pre-flight

- [x] Verify `cianchosaint-pangolin-ingress-v1` is archived
- [x] Verify `bonneagar/stacks/unsloth-serve/` exists (the wholesale-
  copied Unsloth Studio container stack)
- [x] Verify `bonneagar/pangolin/` exists
- [x] Verify the wholesale-copied Pocket ID + Member role pattern

## 1. OpenSpec artifacts

- [ ] Author `openspec/changes/unsloth-studio-pangolin-ingress-v1/proposal.md` — DONE
- [ ] Author `openspec/changes/unsloth-studio-pangolin-ingress-v1/tasks.md` (this file) — DONE
- [ ] Author `openspec/changes/unsloth-studio-pangolin-ingress-v1/cross-repo-sync.md` — DONE
- [ ] Author `openspec/changes/unsloth-studio-pangolin-ingress-v1/specs/unsloth-studio-pangolin-ingress/spec.md` (the 2 ADDED Requirements delta) — DONE
- [ ] Author `openspec/specs/unsloth-studio-pangolin-ingress/spec.md` (canonical END-STATE spec) — DONE
- [ ] Author `openspec/specs/unsloth-studio-pangolin-ingress/AGENTS.md` (per-spec routing) — DONE

## 2. Validation gates

- [ ] Run `openspec validate unsloth-studio-pangolin-ingress-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate unsloth-studio-pangolin-ingress --strict` and verify exit code 0
- [ ] Run `python3 -c "import yaml; yaml.safe_load(open('bonneagar/pangolin/unsloth_studio_resource.yaml').read())"` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL pass

## 3. Implementation: 1 YAML resource file

### Pangolin resources (1 file at `bonneagar/pangolin/`)
- [ ] `unsloth_studio_resource.yaml` — the canonical Pangolin resource
  definition for the Unsloth Studio local API at `unsloth-serve:8889`

## 4. Per-file pattern

```yaml
version: 1
resources:
  - name: unsloth.cianchosaint.ie
    type: api
    target: unsloth-serve:8889
    visibility: private
    auth: pocketid
    role: member
    labels: {app: unsloth-studio, role: model-server, jurisdiction: ireland, environment: prod, constituency: ops}
```

## 5. CI gates + commit + push

- [ ] Run `python3 -c "import yaml; yaml.safe_load(open('bonneagar/pangolin/unsloth_studio_resource.yaml').read())"` and verify
- [ ] Run `openspec validate --all --strict` and verify ALL pass
- [ ] Commit on `cianchosaint:main` with message: `feat(q3q4-track2): Unsloth Studio Pangolin ingress (Change 17)`
- [ ] Push to `github.com/cianfhoghlaim/cianchosaint`

## 6. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-unsloth-studio-public-docs-v1` — expose public
  API documentation at `docs.unsloth.cianchosaint.ie`
