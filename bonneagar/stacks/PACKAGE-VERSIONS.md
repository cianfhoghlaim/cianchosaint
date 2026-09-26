# PACKAGE-VERSIONS.md — the canonical version pinning table

> **Purpose:** Single source of truth for every opensource package used across cianchosaint + cianfhoghlaim. Pairs with [`scripts/audit/audit_package_versions.py`](../scripts/audit/audit_package_versions.py) (the runtime audit script that detects drift).
>
> **Owner:** per the openspec/changes/2026-09-26-package-version-drift-audit-v1/specs/package-version-drift/spec.md, this is the canonical registry that every Stage 2-7 bump change updates.
>
> **Last refreshed:** 2026-09-26 (Stage 1 audit baseline)
>
> **Sister doc:** [`docs/VERSION-DRIFT-POLICY.md`](../../docs/VERSION-DRIFT-POLICY.md) (NEW 2026-09-26)

---

## Version policy (canonical)

| Package family | Pin policy | Rationale |
|---|---|---|
| **IaC stack Docker images** | `==X.Y.Z` (exact) | Reproducible deploys; any drift = explicit openspec change |
| **Python BIEP data platform deps** | `>=X.Y,<X+1.0` (caret) | Minor compat; bugfixes auto-flow |
| **Dev tooling** (mise `[tools]`) | `latest` | Toolchain drift is OK; lock only when build flakes |
| **Bun / npm / pnpm workspace** | `>=X.Y.0` (caret) | Per the canonical `package.json#engines` |

Per the LiteLLM release-support policy (2026-06-29): "LiteLLM will only actively support the four most recent stable minor lines" — applies to ALL packages on the LiteLLM rolling-window rule.

---

## IaC stack Docker images (15 stacks × 2 repos)

| Stack | Pinned (cianchosaint) | Pinned (cianfhoghlaim) | Latest | Drift | Stage |
|---|---|---|---|---|---|
| **infisical** | `v0.165.15` | `v0.165.15` | `v0.165.15` (latest weekly) | **aligned** (Stage 2c complete) | 2c ✅ |
| **pangolin** | `ee-1.23.0` | `ee-1.23.0` | `1.23.0` (Sep 16, 2026) | **aligned** (Stage 2a complete) | 2a ✅ |
| **gerbil** | `1.5.1` | `1.5.1` | `1.5.1` (Aug 31, 2026) | **aligned** (Stage 2a complete) | 2a ✅ |
| **newt** | `latest` (legacy) | `1.16.x` (legacy) | `1.16.x` | aligned; legacy container kept for backward compat | 2a ✅ |
| **pangolin-cli** | `latest` (v1.23+ canonical) | `latest` (v1.23+ canonical) | `latest` | aligned; new-site pattern | 2a ✅ |
| **litellm** | `v1.102.0` | `v1.102.0` | `v1.102.0` (Sep 19, 2026) | **aligned** (Stage 2b.1 complete) | 2b ✅ |
| **langfuse** | `4.7.0` | `4.7.0` | `4.x` (latest patch) | **aligned** (Stage 2b.1 complete) | 2b ✅ |
| **langfuse-worker** | `4.7.0` | `4.7.0` | `4.x` (latest patch) | **aligned** (Stage 2b.1 complete) | 2b ✅ |
| **komodo** | `komodo-core:2 + komodo-periphery:2-dev + ferretdb:2` | `komodo-core:2 + komodo-periphery:2-dev + ferretdb:2` | `v2.3.3` (latest; we're on the v2 track) | **aligned** (Stage 2b.2 complete) | 2b ✅ |
| **openchamber** | `1.22.2` | `1.22.2` | `1.22.2` (Sep 5, 2026) | **aligned** (image-only; Stage 2b.3 complete) | 2b ✅ |
| **crawl4ai** | `v0.9.4` | `v0.9.4` | `v0.9.4` (Sep 23, 2026) | **aligned** (Stage 2c complete) | 2c ✅ |
| **garage** | `v2.4.1` | `v2.4.1` | `v2.4.1` (Sep 8, 2026) | **aligned** (Stage 2c complete) | 2c ✅ |
| **stagehand** | `local` | `n/a` | n/a | local-only | skip |
| **locket** | `local` | `n/a` | n/a | local-only | skip |
| **openclaw** | `local` | `local` | n/a | local-only | skip |
| **bailo** | n/a | n/a | n/a | skip | n/a |

**Known canonical clashes** (per Firecrawl research 2026-09-26):
- **Pangolin 1.23.0 renamed Newt → "Pangolin Site"** — see `openspec/changes/2026-09-26-pangolin-newt-v1.23-upgrade-v1/`
- **LiteLLM only actively supports 4 most recent minor lines** — see Stage 2b
- **Pangolin v1.23+ requires clients post-2026-08-19** — see Stage 2a

---

## Python BIEP data platform deps

| Package | Pinned (cianchosaint) | Pinned (cianfhoghlaim) | Latest | Drift | Stage |
|---|---|---|---|---|---|
| **dagster** | `>=1.13,<2.0` | `>=1.13,<2.0` | `1.13.24` (Sep 2026) | **aligned** (Stage 3 complete) | 3 ✅ |
| **dagster-dlt** | `>=0.29,<1.0` | `>=0.29,<1.0` | `0.29.24` (Sep 2026) | **aligned** (Stage 3 complete) | 3 ✅ |
| **dagster-dbt** | `>=0.29,<1.0` | `>=0.29,<1.0` | `0.29.24` (Sep 2026) | **aligned** (Stage 3 complete) | 3 ✅ |
| **cocoindex** | `>=1.0.20,<2.0` | `>=1.0.20,<2.0` | `1.0.24` (Sep 19, 2026) | **aligned** (Stage 3 complete) | 3 ✅ |
| **baml-py** | `>=0.223,<1.0` | `>=0.223,<1.0` | `0.226.2` (Sep 2026) | **aligned** (Stage 3 complete) | 3 ✅ |
| **dlt** | `>=1.30,<2.0` | `>=1.30,<2.0` | `1.30.0` (Sep 2026) | **aligned** (Stage 3 complete) | 3 ✅ |
| **duckdb** | `>=1.5.5,<1.6.0` | `>=1.5.5,<1.6.0` | `1.5.5` LTS | **aligned** (Stage 3 complete) | 3 ✅ |
| **motherduck** | `>=0.10,<1.0` | `>=0.10,<1.0` | (latest 0.x) | **aligned** (Stage 3 complete) | 3 ✅ |
| **lancedb** | `>=0.39,<1.0` | `>=0.39,<1.0` | `0.39.0` (Aug 31, 2026) | **aligned** (Stage 3 complete) | 3 ✅ |
| **google-adk** | unpinned | `>=2.9.0,<3` | `2.10.0` (Sep 10, 2026) | **aligned** (Stage 3 complete) | 3 ✅ |
| **langfuse-py** | `>=4.7.0,<5.0` | `>=4.15.1 (via logfire)` | `4.15.6` | **aligned** (Stage 2b.1 complete) | 3 ✅ |
| **litellm-py** | unpinned | `>=1.97.0` | `1.102.1` (Sep 19, 2026) | cianfhoghlaim behind 5 minor | 3 |
| **firecrawl-py** | unpinned | `>=4.28.2` | `4.44.0` | behind 16 minor | skip |
| **marimo** | unpinned | `>=0.23.10` | `0.25.0` (Sep 11, 2026) | unverified (unpinned) | skip |
| **openai** | unpinned | `>=2.32.0` | `3.19.2` | behind major (2.x → 3.x) | skip |
| **anthropic** | unpinned | `>=0.106.0` | `1.8.0` | behind major | skip |
| **groq** | unpinned | `>=1.4.0` | `1.7.0` | unverified (unpinned) | skip |
| **google-genai** | unpinned | `>=1.73.1` | `2.25.0` | behind major | skip |
| **pydantic** | `>=2.10.0` | `>=2 (via pydantic-settings)` | `2.13.5` | aligned (minor) | skip |
| **structlog** | `>=25.0.0` | `>=25` | `26.1.0` | behind major | skip |
| **logfire** | unpinned | `>=4.15.1` | `5.1.1` | behind major | skip |
| **fastapi** | unpinned | `>=0.115.0,<0.140` | `0.141.1` | unverified (unpinned) | skip |
| **agno** | unpinned | `>=2.6.11` | `3.0.11` | behind major | skip |
| **ibis-framework** | unpinned | `>=10` | `12.0.0` | unverified (unpinned) | skip |
| **pyiceberg** | unpinned | `>=0.10` | `0.12.0` | unverified (unpinned) | skip |
| **pymupdf** | unpinned | `>=1.24` | `1.28.2` | behind 4 minor | skip |
| **tenacity** | unpinned | `>=9,<10` | `9.1.4` | unverified (unpinned) | skip |
| **httpx** | unpinned | `>=0.27,<1.0` | `0.28.1` | behind major (0.x → 1.x?) | skip |
| **beautifulsoup4** | unpinned | `>=4.12` | `4.15.0` | unverified (unpinned) | skip |
| **pyyaml** | `>=6.0.0` | unpinned | `6.0.3` | aligned | skip |

---

## TypeScript / Bun workspace deps (cianfhoghlaim)

| Package | Pinned | Latest | Drift | Stage |
|---|---|---|---|---|
| **bun** | `1.4.0` (in `package.json#engines.bun`) | `1.4.0` | aligned | 7 (monitoring) |
| **turbo** | (per `package.json`) | needs-research | unverified | 7 |
| **komodo_client** | (per `package.json`) | needs-research | unverified | 7 |
| **opencode** | `latest` | needs-research | unverified | 7 |

---

## The 79 skills (each maps to a package)

Per the `.agents/skills/` directory inventory (79 directories as of 2026-09-26), each skill's `SKILL.md` has a version header (per `.agents/skills/_template/SKILL.md`). The Stage 6 change refreshes all 79 headers + adds the "Version policy" section to each.

Sample current header pattern:
```
**Version:** 1.97.0 | **Last Updated:** 2026-08-21
```

**Refresh cadence (per Stage 7 monitoring):** weekly GH workflow run + on-demand bump.

---

## What gets bumped when (the saga timeline)

| Stage | Bumps | Openspec change(s) | Status |
|---|---|---|---|
| **2a** | **pangolin + gerbil + newt + pangolin-cli (new)** | **`2026-09-26-pangolin-newt-v1.23-upgrade-v1/`** | **✅ SHIPPED 2026-09-26** |
| 2b | litellm + langfuse + komodo + openchamber image | 3 changes | pending |
| 2c | crawl4ai + garage + infisical | `2026-09-26-loc-data-storage-stack-upgrade-v1/` |
| 3 | dagster + dagster-dlt + dagster-dbt + cocoindex + baml-py + dlt + duckdb + motherduck + lancedb + google-adk + langfuse-py + litellm-py | `2026-09-26-biep-data-platform-deps-bump-v1/` |
| 4 | openchamber full refactor (1.0 → 1.22) | `2026-09-26-openchamber-v1.22-major-upgrade-v1/` |
| 5 | lancedb Lance v1 → Lance v2 in-place migration | `2026-09-26-lancedb-v0.39-lance-v2-upgrade-v1/` |
| 6 | refresh all 79 skill version headers | `2026-09-26-skill-version-header-refresh-v1/` |
| 7 | add the GH workflow + Dagster sensor + `mise run devops:version-drift` + `docs/VERSION-DRIFT-POLICY.md` | `2026-09-26-version-drift-monitoring-v1/` |

---

## How to use this file

1. **For a new package addition:** add a row + run `scripts/audit/audit_package_versions.py --strict` to verify the policy.
2. **For a version bump:** update the row, then update the corresponding openspec change, then re-run the audit.
3. **For drift detection:** run `python3 scripts/audit/audit_package_versions.py` — the script reads this file's sibling `audit_package_versions.py`.

---

## Cross-references

- [`scripts/audit/audit_package_versions.py`](../scripts/audit/audit_package_versions.py) — the runtime audit script
- [`docs/VERSION-DRIFT-POLICY.md`](../../docs/VERSION-DRIFT-POLICY.md) — the canonical policy doc (NEW 2026-09-26)
- [`.agents/skills/package-version-drift/SKILL.md`](../../.agents/skills/package-version-drift/SKILL.md) — the canonical skill
- [`openspec/changes/2026-09-26-package-version-drift-audit-v1/specs/package-version-drift/spec.md`](../../openspec/changes/2026-09-26-package-version-drift-audit-v1/specs/package-version-drift/spec.md) — the canonical spec
