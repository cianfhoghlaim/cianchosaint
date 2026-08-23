# Change: cianchosaint-repo-foundation-v1

## Why

Three problems converged on 2026-08-23:

1. **The British Isles public-sector defence / policing / intelligence-oversight ecosystem has no open-source data platform equivalent to cianfhoghlaim/cianfhoghlaim.** Every British Isles sub-nation (Republic of Ireland, the 4 UK nations, the 3 Crown Dependencies) currently operates its own bespoke OSINT tooling — or relies on proprietary AI vendors. There is no shared, auditable, sovereign-capability stack.

2. **LiteLLM, the existing LLM routing backbone, is frequently down in our environment** (verified across the 2026-07 / 2026-08 incident timeline). All LLMs in the proposed cianchosaint repo MUST route through a 4-tier fallback chain with Unsloth Studio as the primary provider, LiteLLM as fallback #1, MiniMax Token Plan as fallback #2, and Gemini API as the last-resort fallback. This pattern is more resilient and more sovereign than the existing LiteLLM-primary setup.

3. **The existing partial pipelines in cianfhoghlaim/cianfhoghlaim are mis-classified for defence / policing / intelligence-oversight use.** They live under `dlt_sources/official_media/` (which is a multi-purpose bucket) and `baml_src/processing/official_media.baml` (which is a multi-purpose schema). These need to be wholesale-migrated into a NEW repo `cianfhoghlaim/cianchosaint` under a tighter BUSL-1.1 licence that grants use only to British Isles public-sector bodies (broadly within each sub-nation) and explicitly bans foreign intelligence agencies.

The user explicitly requested (verified 2026-08-23): *"in a similar way to how we made a tangent to this repository recently for a specific hackathon branch off a new repository project called CIANCHOSAINT which is similar to the goals of CIANFHOGHLAIM ... but now for defence for all instead of the education systems for all sub nations of the British Isles for all intelligence agencies police forces army air forces everything like that all official documentations and things like criminal statistics from official sources ... we need a brand-new project starting from scratch ... this is for the Irish Gaelic for defence which is COSAINT and combined with CIAN my name again"*.

## What changes

- **New repo `github.com/cianfhoghlaim/cianchosaint`** — sibling to `cianfhoghlaim/cianfhoghlaim`. Cold-start skeleton (AGENTS.md + README.md + pyproject.toml + mise.toml + package.json + openspec/).
- **`LICENSE.md` — BUSL-1.1 v2 CIANCHOSAINT edition** with the Additional Use Grant covering every governmental body of Ireland, the UK, and the Crown Dependencies; the 3-step foreign-use gate (Explain → Do us a favour → Maybe); and the warrant-to-enforce clause granted to every licencee, triggered by either publicly observable evidence OR a credible written complaint.
- **`openspec/specs/cianchosaint-pipeline/spec.md` — the umbrella capability spec** describing the full end-state (foundation + 3 vertical sub-pipelines BIPP v1 / BIDP v1 / BIIP v1).
- **The wholesale-migration plan** (see `cross-repo-sync.md`) for 8 assets from cianfhoghlaim → cianchosaint: the HMGCC rolling-window stub, the 5 per-Crown-Dependency official-media stubs, the allowlist classifier, and the `official_media.baml` schema.
- **The 4-tier provider chain contract** (documented in this proposal and codified in a follow-up openspec change `cianchosaint-provider-router-v1`): Unsloth Studio → LiteLLM → MiniMax Token Plan → Gemini API, with a 30-second timeout per provider and a 3-strike circuit-breaker.
- **The OSINT source URL allowlist** at `dlt_sources/cianchosaint/common/osint_allowlist.yaml` (NEW), enforced by `mise run lint:license` (NEW) at CI time.
- **Per-spec `AGENTS.md` convention** (mirrors cianfhoghlaim's `repo-hygiene-agent-routing` spec).
- **Cross-repo openspec sync convention** with the `cross-repo-sync.md` file (the standard Cianfhoghlaim pattern, retained in cianchosaint).

## Impact

- Affected specs: **1 new spec** (`cianchosaint-pipeline`) + 1 modified Cianfhoghlaim spec (`official-media-pipeline`, which becomes the documented upstream of the wholesale-migrated assets).
- Affected code/config: cianchosaint repo skeleton (NEW); LICENSE.md (NEW); openspec/specs/cianchosaint-pipeline/spec.md (NEW); openspec/specs/cianchosaint-pipeline/AGENTS.md (NEW); openspec/AGENTS.md (NEW); AGENTS.md (NEW); README.md (NEW); cross-repo-sync.md (NEW).
- New openspec changes that BLOCK on this change:
  - `cianchosaint-provider-router-v1` — implements the 4-tier chain
  - `cianchosaint-baml-schemas-v1` — the 12 BAML extraction functions
  - `cianchosaint-bipp-v1` — British Isles Policing Pipeline
  - `cianchosaint-bidp-v1` — British Isles Defence Pipeline
  - `cianchosaint-biip-v1` — British Isles Intelligence Oversight Pipeline
  - `cianchosaint-per-persona-web-surfaces-v1` — the 7 persona apps
  - `cianchosaint-hmgcc-extension-v1` — extends the migrated rolling-window
  - `cianchosaint-licence-enforcement-v1` — operationalises the warrant-to-enforce clause
- No secret values are written to disk: all keys resolve via `infisical://dev-baile/cianchosaint/...` template refs hydrated by mise + Locket.
- The cianfhoghlaim repo is unaffected by this change beyond the wholesale-migration markers (added in a follow-up cianfhoghlaim openspec change `official-media-pipeline-migration-to-cianchosaint-v1` — also written in this PR).

## Out of scope

- The actual implementation of the 4-tier provider router (follow-up change `cianchosaint-provider-router-v1`).
- The 12 new BAML extraction functions (follow-up change `cianchosaint-baml-schemas-v1`).
- The ~60 DLT source extensions per sub-nation (covered by BIPP v1 / BIDP v1 / BIIP v1 follow-ups).
- The 7 per-persona web apps (follow-up change `cianchosaint-per-persona-web-surfaces-v1`).
- The Pangolin ingress for Unsloth Studio (separate IaC change in `bonneagar`).
- Retrofitting the 4-tier chain into Cianfhoghlaim (separate follow-up `litellm-to-unsloth-provider-chain-v1` per Q6 = a).

## Dependencies

`Blocked by: none.`
`Blocked by (soft): cianfhoghlaim/cianfhoghlaim@official-media-pipeline` (the existing partial pipeline that cianchosaint extends).
`Affected repos: cianchosaint, cianfhoghlaim.`

## Cross-repo sync

See [`cross-repo-sync.md`](./cross-repo-sync.md) for the commit plan + branch + push target for each repo + the order of operations (cianfhoghlaim first, then cianchosaint).
