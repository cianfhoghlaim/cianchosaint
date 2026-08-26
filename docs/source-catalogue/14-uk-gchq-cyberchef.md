# 14 — UK GCHQ CyberChef (the Cyber Swiss Army Knife)

> Per the
> [`openspec/changes/cianchosaint-hmgcc-gchq-tooling-v1/`](../../openspec/changes/cianchosaint-hmgcc-gchq-tooling-v1/specs/cianchosaint-hmgcc-gchq-tooling/spec.md)
> spec (CyberChef track).

## Overview

[GCHQ CyberChef](https://github.com/gchq/CyberChef) is GCHQ's "Cyber
Swiss Army Knife" — a web app for cyber operations with **300+
operations** (encoding, encryption, hashing, IPv6 extraction,
certificate parsing, JSON/XML/CSV transforms, etc.). The cianchosaint
platform wholesale-copies the upstream catalog (`hmgcc/CyberChef/`,
**Apache 2.0**) + exposes a bounded subset of operations through a
FunctionTool that the AG-UI chat window can invoke.

CyberChef provides a **parallel GUI-based data analysis interface**
alongside the chat-based analysis the other `ciafagent-*` apps offer.
The analyst authors a recipe (or uses `ExtractCyberChefRecipe` to
generate one from a natural-language request) + the platform invokes
the upstream CyberChef HTTP API + returns the transformed result to
the chat.

## The wholesale source

| Field | Value |
|---|---|
| **Upstream** | `hmgcc/CyberChef/` (wholesale-copied) |
| **Upstream licence** | Apache 2.0 |
| **Version pinned** | Per `hmgcc/CyberChef/CHANGELOG.md` (auto-upstream pinning intentionally lags) |
| **Our subset** | ~28 operations (see `CYBERCHEF_OPERATIONS` in `CyberChefRecipePipeline`) |

## Sources

### CyberChef (the GCHQ cyber-tool wholesale copy)

- **URL**: https://github.com/gchq/CyberChef
- **Wholesale source**: `hmgcc/CyberChef/` (Apache 2.0)
- **DLT source**: `dlt_sources/cianchosaint/uk/cyberchef/recipe_extraction.py`
- **BAML extraction**: `baml_src/cianchosaint/processing/cyberchef_recipe_extraction.baml`
- **FunctionTool**: `agents/cianchosaint/tools/cyberchef_execute.py`
- **Web app**: `web/apps/ciafagent-cyberchef/`
- **OSINT allowlist**: yes
- **Coverage**: The bounded ~28 CyberChef operations exposed by the cianchosaint FunctionTool (encoding, encryption, hashing, IPv6 extraction, certificate parsing, JSON/XML/CSV transforms)
- **Update cadence**: weekly (mirrors upstream CyberChef releases)
- **Notes**: Apache 2.0 wholesale — we honour the upstream licence + provide attribution in every source file

## Workflow

1. **Analyst asks the ciafagent-cyberchef AG-UI chat**: "decode this base64 string + extract the IPv6 address + compute the SHA-256 hash"
2. **`ExtractCyberChefRecipe`** (BAML) generates a structured `CyberChefRecipe` (recipe_name + ordered operation list)
3. **`cyberchef_execute`** (FunctionTool) invokes the upstream CyberChef HTTP API with the recipe + input
4. **The transformed result** is returned to the chat (with full provenance: input digest, output digest, recipe ID)
5. **The execution row** is appended to the `cyberchef_executions` DLT resource (append-only)

## Gaps

- Upstream CyberChef has 300+ operations; the cianchosaint FunctionTool wraps ~28 (the most-used). The `ExtractCyberChefRecipe` BAML function will refuse operations outside the bounded subset (matches `CYBERCHEF_OPERATIONS`).
- The `CyberChef-Server` companion container is NOT yet bundled in the self-hosted Docker stack. Follow-up `cianchosaint-cyberchef-server-v1` change would close this gap (one container, ~200 MB).
- Auto-pinning of the CyberChef upstream version intentionally lags (we don't ship upstream releases the moment they're tagged — we vet them first).

## References

- The canonical openspec spec:
  [`openspec/changes/cianchosaint-hmgcc-gchq-tooling-v1/specs/cianchosaint-hmgcc-gchq-tooling/spec.md`](../../openspec/changes/cianchosaint-hmgcc-gchq-tooling-v1/specs/cianchosaint-hmgcc-gchq-tooling/spec.md)
- The wholesale Apache 2.0 source: [`hmgcc/CyberChef/`](../../hmgcc/CyberChef/)
- The upstream repo: https://github.com/gchq/CyberChef
- The OSINT allowlist:
  [`dlt_sources/cianchosaint/common/osint_allowlist.yaml`](../../dlt_sources/cianchosaint/common/osint_allowlist.yaml)
- The 4-tier provider chain:
  [`baml_src/_shared/provider_router.py`](../../baml_src/_shared/provider_router.py)
