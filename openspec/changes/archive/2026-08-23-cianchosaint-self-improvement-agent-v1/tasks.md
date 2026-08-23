# Tasks: cianchosaint-self-improvement-agent-v1

## 1. Canonical spec scaffold

- [ ] 1.1 Create `openspec/specs/cianchosaint-self-improvement-agent/spec.md`
      (3 ADDED Requirements)
- [ ] 1.2 Create `openspec/specs/cianchosaint-self-improvement-agent/AGENTS.md`
      (≤30 lines)
- [ ] 1.3 Create
      `openspec/changes/cianchosaint-self-improvement-agent-v1/specs/cianchosaint-self-improvement-agent/spec.md`
      (the spec delta)

## 2. Implementation file

- [ ] 2.1 `agents/cianchosaint/self_improvement_agent.py` — the
      Google ADK root agent with 3 FunctionTools
      (`analyze_codebase`, `analyze_leabharlann`, `propose_feature`)

## 3. Conservative-posture enforcement

- [ ] 3.1 The agent's `instruction` explicitly forbids bypassing the
      OSINT allowlist
- [ ] 3.2 The agent's `instruction` explicitly references the
      BUSL-1.1 v2 licence posture
- [ ] 3.3 The agent is **on-demand only** — no daily sensor, no
      automated `mise run cianchosaint:self-improvement:run` (per
      Q14 = on-demand)

## 4. Validation

- [ ] 4.1 `openspec validate cianchosaint-self-improvement-agent-v1 --strict`
      passes
- [ ] 4.2 `openspec validate openspec/specs/cianchosaint-self-improvement-agent/ --strict`
      passes
- [ ] 4.3 Python syntax check:
      `/Users/cianmacandeisigh/.local/share/uv/python/cpython-3.13-macos-aarch64-none/bin/python3.13 -c "import ast; ast.parse(open('agents/cianchosaint/self_improvement_agent.py').read())"`

## 5. Commit + archive

- [ ] 5.1 `git add agents/cianchosaint/self_improvement_agent.py
      openspec/specs/cianchosaint-self-improvement-agent/
      openspec/changes/cianchosaint-self-improvement-agent-v1/` only
- [ ] 5.2 `git commit -m "feat(q3-track1): Google ADK self-improvement agent (Q14 = on-demand) (Change 8)"`
- [ ] 5.3 `git push origin main`
- [ ] 5.4 `openspec archive cianchosaint-self-improvement-agent-v1 --yes`
