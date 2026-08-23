# Cross-Repo Sync: cianchosaint-baml-schemas-v1

This change is **single-repo** — it touches cianchosaint only and
**does NOT modify Cianfhoghlaim**. The wholesale-copied 4-tier BAML
client chain at `baml_src/clients.baml` is reused as-is.

| Repo | Committed? | Branch | Notes |
|:--|:--|:--|:--|
| `cianchosaint` | YES | `main` | The 8 NEW BAML files + the canonical spec + the spec delta |
| `cianfhoghlaim` | NO | — | No changes |
| `leabharlann` | NO | — | No changes (the leabharlann source PDFs are read-only context) |

## Order of operations

1. Commit + push cianchosaint (this repo)
2. No follow-up commit on Cianfhoghlaim
3. No follow-up commit on leabharlann

## Hard rule reminder

Per the cianchosaint `AGENTS.md` cross-repo protocol, agents MUST NOT
write into the `leabharlann/` worktree from this repo — `leabharlann/`
is a separate repo with its own git history.
