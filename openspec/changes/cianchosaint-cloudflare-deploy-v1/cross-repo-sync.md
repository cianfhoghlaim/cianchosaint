# Cross-Repo Sync: cianchosaint-cloudflare-deploy-v1

This change touches **ONLY the `cianchosaint` repo**. Cianfhoghlaim
(`/Users/cianmacandeisigh/dev/kings_college_galway/`) and leabharlann
(`/Users/cianmacandeisigh/dev/kings_college_galway/leabharlann/` — a
separate repo per the cianfhoghlaim AGENTS.md) remain **completely
unchanged**.

## Order of Operations

```
[1] cianfhoghlaim  → (no changes; the wholesale-copied Cloudflare
                       Workers pattern from Cianfhoghlaim remains the
                       upstream reference)
                            ↓
[2] cianchosaint   → openspec/changes/cianchosaint-cloudflare-deploy-v1/
                       (proposal + tasks + cross-repo-sync + 1 spec delta)
                       + 1 NEW canonical spec at openspec/specs/cianchosaint-cloudflare-deploy/
                       + 1 MODIFIED wrangler.toml at web/apps/ciafagent-api/wrangler.toml
                       Pushed to main.
                            ↓
[3] operator       → cd cianchosaint && openspec validate cianchosaint-cloudflare-deploy-v1 --strict
                       → openspec validate --all --strict (CI gate)
                       → All validations pass
                            ↓
[4] operator       → openspec archive cianchosaint-cloudflare-deploy-v1 --yes
                       → The 2 ADDED Requirements merge into the canonical
                         cianchosaint-cloudflare-deploy spec
```

## Repo 1: cianfhoghlaim (source — NO CHANGES)

The Cianfhoghlaim repo is **unchanged** by this change. Its existing
Cloudflare Workers deployment at `web/apps/ciafagent-api/wrangler.toml`
continues to serve Cianfhoghlaim's education use **directly and
unchanged**.

## Repo 2: cianchosaint (destination — all changes)

**Files to commit** (in the cianchosaint repo):

| Path | Action | Description |
|:--|:--|:--|
| `openspec/changes/cianchosaint-cloudflare-deploy-v1/proposal.md` | NEW | The proposal |
| `openspec/changes/cianchosaint-cloudflare-deploy-v1/tasks.md` | NEW | The tasks |
| `openspec/changes/cianchosaint-cloudflare-deploy-v1/cross-repo-sync.md` | NEW | This file |
| `openspec/changes/cianchosaint-cloudflare-deploy-v1/specs/cianchosaint-cloudflare-deploy/spec.md` | NEW | Spec delta (2 ADDED Requirements) |
| `openspec/specs/cianchosaint-cloudflare-deploy/spec.md` | NEW | Canonical END-STATE spec |
| `openspec/specs/cianchosaint-cloudflare-deploy/AGENTS.md` | NEW | Per-spec routing |
| `web/apps/ciafagent-api/wrangler.toml` | MODIFY | Extended to declare 8 web apps + 1 API gateway |

**Branch**: `main`

**Push target**: `github.com/cianfhoghlaim/cianchosaint`

**Commit message**: `feat(q3q4-track2): Cloudflare deploy for 8 web apps + Hono API gateway (Change 14)`

## Verification Commands

After this change lands:

```bash
# On cianchosaint
cd /Users/cianmacandeisigh/dev/cianchosaint
openspec list
# Expected: 7 pending changes (the existing baml-schemas + 6 new from this batch)

openspec validate --all --strict
# Expected: All pass

python3 -c "import tomllib; data = tomllib.loads(open('web/apps/ciafagent-api/wrangler.toml','rb').read()); print('routes:', len(data['env']['production']['routes']))"
# Expected: 9 (8 web apps + 1 API gateway)

# On cianfhoghlaim (unchanged)
cd /Users/cianmacandeisigh/dev/kings_college_galway
openspec list
# Expected: unchanged
```
