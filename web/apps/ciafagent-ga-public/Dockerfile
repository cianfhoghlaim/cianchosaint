# ciafagent-ga-public — Docker image (Cloudflare Container / Bun dev)
# =============================================================================
# Build context: REPO ROOT (so we can reach sibling workspaces).
#
# Uses bun (the monorepo's package manager — apps use `workspace:*` protocol
# which npm rejects but bun supports natively).
# =============================================================================

FROM oven/bun:1-alpine

WORKDIR /app/cianchosaint/web/apps/ciafagent-ga-public

# -----------------------------------------------------------------------------
# 1. Install dependencies via bun
# -----------------------------------------------------------------------------
COPY cianchosaint/web/apps/ciafagent-ga-public/package.json cianchosaint/web/apps/ciafagent-ga-public/bun.lock* cianchosaint/web/apps/ciafagent-ga-public/turbo.json ./
COPY cianchosaint/web/apps/ciafagent-ga-public/apps/web/package.json apps/web/
COPY cianchosaint/web/apps/ciafagent-ga-public/apps/api/package.json apps/api/
COPY cianchosaint/web/apps/ciafagent-ga-public/packages/ packages/

RUN bun install

# -----------------------------------------------------------------------------
# 2. Copy source
# -----------------------------------------------------------------------------
WORKDIR /app
COPY cianchosaint/web/apps/ciafagent-ga-public/ /app/cianchosaint/web/apps/ciafagent-ga-public/

# -----------------------------------------------------------------------------
# 3. Expose + run
# -----------------------------------------------------------------------------
EXPOSE 3080 8787

WORKDIR /app/cianchosaint/web/apps/ciafagent-ga-public/apps/web
CMD ["bunx", "vite", "dev", "--host", "0.0.0.0", "--port", "3080"]
