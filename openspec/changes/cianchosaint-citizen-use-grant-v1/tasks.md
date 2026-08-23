# Tasks: cianchosaint-citizen-use-grant-v1

## 0. Pre-flight

- [x] Verify `cianchosaint-self-hosted-citizen` spec is archived
- [x] Verify `LICENSE.md` §Additional Use Grant exists
- [x] Verify the legal-text review notes (the grant preserves the
  prohibition on commercial monetisation + foreign use + public-facing
  deployment)

## 1. OpenSpec artifacts

- [ ] Author `openspec/changes/cianchosaint-citizen-use-grant-v1/proposal.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-citizen-use-grant-v1/tasks.md` (this file) — DONE
- [ ] Author `openspec/changes/cianchosaint-citizen-use-grant-v1/cross-repo-sync.md` — DONE
- [ ] Author `openspec/changes/cianchosaint-citizen-use-grant-v1/specs/cianchosaint-citizen-use-grant/spec.md` (the 2 ADDED Requirements delta) — DONE

## 2. Validation gates

- [ ] Run `openspec validate cianchosaint-citizen-use-grant-v1 --strict` and verify exit code 0
- [ ] Run `openspec validate cianchosaint-self-hosted-citizen --strict` and verify exit code 0
- [ ] Run `python3 -c "with open('LICENSE.md') as f: content = f.read(); assert 'NATURAL PERSON CITIZEN GRANT' in content; assert 'Additional Use Grant' in content; print('OK')"` and verify exit code 0
- [ ] Run `openspec validate --all --strict` and verify ALL pass

## 3. Implementation: 1 LICENSE.md amendment + 1 spec update

### Licence (1 file at repo root)
- [ ] `LICENSE.md` — extend with the "NATURAL PERSON CITIZEN GRANT"
  section (before the "**Change Date:**" section)

### Spec update (1 file at `openspec/specs/cianchosaint-self-hosted-citizen/`)
- [ ] `spec.md` — update the "Background" section to reference the
  citizen use grant amendment

## 4. Per-file pattern (LICENSE.md amendment)

Add to LICENSE.md before the "**Change Date:**" section:

```markdown
---

**NATURAL PERSON CITIZEN GRANT**

Natural persons of the British Isles who are not affiliated with
the bodies in (a), (b), or (c) above MAY use the Licensed Work for
non-commercial personal purposes, including self-hosted deployment,
subject to the prohibition on commercial monetisation in (1).

This grant covers:
  - Self-hosted deployment on a natural person's own machine
    (per the cianchosaint-self-hosted-citizen spec)
  - Personal OSINT investigation (subject to the OSINT allowlist
    ceiling)
  - Personal study, learning, and experimentation

This grant DOES NOT cover:
  - Public-facing deployment of any kind
  - Commercial monetisation of any kind
  - Use by any foreign entity (foreign intelligence agencies
    remain explicitly banned)
```

## 5. CI gates + commit + push

- [ ] Run `python3 -c "with open('LICENSE.md') as f: content = f.read(); assert 'NATURAL PERSON CITIZEN GRANT' in content; assert 'Additional Use Grant' in content; print('OK')"` and verify
- [ ] Run `openspec validate --all --strict` and verify ALL pass
- [ ] Commit on `cianchosaint:main` with message: `feat(q3q4-track2): Natural Person Citizen Grant + self-hosted spec update (Change 16)`
- [ ] Push to `github.com/cianfhoghlaim/cianchosaint`

## 6. Follow-up openspec changes (NOT in this change's scope)

- [ ] `cianchosaint-citizen-portal-credentials-v1` — provision the
  per-portal credentials for the citizen use case
- [ ] `cianchosaint-unsloth-studio-pangolin-ingress-v1` — expose
  Unsloth Studio at `unsloth.cianchosaint.ie:8889` (Change 17)
