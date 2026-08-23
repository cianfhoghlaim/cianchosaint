# OpenSpec — Agent Routing

> **OpenSpec workflow** for the `cianchosaint` repo. Mirrors the Cianfhoghlaim `openspec/` convention. Every non-trivial change lives in `openspec/changes/<id>/` as a 3-artifact bundle (`proposal.md` + `tasks.md` + spec deltas) before any code is written.

## Priority quick reference

### Priority commands

```bash
openspec list --specs                   # list all capability specs
openspec list                           # list all pending changes
openspec view                           # interactive dashboard
openspec show <change-id|spec-id>       # formatted view
openspec status <change-id>             # artifact completion check
openspec validate <change-id> --strict  # MUST pass before commit
openspec validate --all --strict       # validate every change + every spec
openspec archive <change-id> --yes      # after deploy
```

### Priority mise tasks

```bash
mise run openspec:validate-all          # CI gate — every change + every spec (strict)
mise run openspec:validate <id>        # validate one change (--strict)
mise run openspec:archive <id>          # archive a deployed change
mise run openspec:view                  # interactive dashboard
```

### Priority specs

| Spec | One-liner |
|:--|:--|
| [`cianchosaint-pipeline`](./specs/cianchosaint-pipeline/spec.md) | The umbrella — British Isles defence / policing / intelligence-oversight pipeline |

## The 6-file change bundle

Every openspec change MUST contain:

```
openspec/changes/<change-id>/
├── proposal.md              # why + what + impact + dependencies
├── tasks.md                 # the ordered checklist
├── cross-repo-sync.md       # ONLY if change touches >1 repo
└── specs/
    └── <spec-name>/
        └── spec.md          # ADDED/MODIFIED/REMOVED Requirements + Scenarios
```

For the canonical capability spec, the per-spec directory contains:

```
openspec/specs/<spec-name>/
├── spec.md                  # the END STATE (what the system looks like post-archive)
└── AGENTS.md                # per the repo-hygiene-agent-routing convention
```

## Spec delta format

```markdown
## ADDED Requirements
### Requirement: New Feature Name
The system SHALL provide...

#### Scenario: Success case
- **WHEN** user performs action
- **THEN** expected result
- **AND** additional expectation

## MODIFIED Requirements
### Requirement: Existing Feature Name
[Complete modified requirement with all scenarios]

## REMOVED Requirements
### Requirement: Old Feature Name
**Reason**: [Why removing]
**Migration**: [How to handle]
```

**Hard rules** (enforced by `openspec validate --strict`):

1. SHALL/MUST in every Requirement body.
2. Every Requirement MUST have ≥1 Scenario with WHEN/THEN/AND.
3. ADDED / MODIFIED / REMOVED markers are required (the deltas vs the canonical spec).
4. Never edit `openspec/specs/<spec>/spec.md` directly — only the deltas under `openspec/changes/<id>/specs/`.

## Cross-repo convention

For changes touching >1 repo (cianchosaint + cianfhoghlaim + leabharlann), include `cross-repo-sync.md` listing:

1. The commit plan for each repo
2. The branch name + remote URL for each push target
3. The order of operations

Standard order: **cianfhoghlaim first, then cianchosaint** (Cianfhoghlaim prepares the wholesale-migration markers; Cianchosaint imports them; both branches pushed; openspec archive runs after both deploy).

## Dependencies field convention

Every `proposal.md` SHALL include a `## Dependencies` section:

```markdown
## Dependencies

`Blocked by: <change-id>` (topo ordering)
`Blocked by (soft): <change-id>` (extends but doesn't block)
`Affected repos: cianchosaint, cianfhoghlaim, leabharlann`
```

The change CANNOT archive until blockers archive.

## Skill pointers

- `.agents/skills/openspec/SKILL.md` — the canonical OpenSpec skill (mirrors Cianfhoghlaim's)
- `.opencode/agents/proposal-author.md` — the openspec-aware subagent
- `AGENTS.md` — the cianchosaint root agent routing

## DO NOT

- Skip `openspec validate --strict` — CI gate, blocks merge
- Hand-edit `openspec/specs/<spec>/spec.md` directly — only deltas under `openspec/changes/<id>/specs/`
- Use "should" or "may" in Requirement bodies — SHALL/MUST only
- Leave Scenarios empty — minimum WHEN X THEN Y AND Z triple
- Archive before CI gates pass + deployments verified
