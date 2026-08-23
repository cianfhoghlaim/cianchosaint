# ciafagent-self-host — multi-stage Docker image for self-hosted citizen
# =============================================================================
# Citizens run `docker compose up` on their own hardware (RPi5, NAS, etc.).
# The image bundles:
#   - bun + Node runtime
#   - The TanStack Start AG-UI chat window
#   - A minimal Hono API for the agent stream
#   - The 3 cianchosaint root agents (Python) for offline fallback
#   - A local SQLite cache
# =============================================================================

# Stage 1: build the web app
FROM oven/bun:1-alpine AS web-builder
WORKDIR /build
COPY cianchosaint/web/apps/ciafagent-self-host/ ./
RUN bun install --frozen-lockfile
RUN bun run build

# Stage 2: runtime
FROM oven/bun:1-alpine
WORKDIR /app

# Python + agents for the local fallback
RUN apk add --no-cache python3 py3-pip
COPY cianchosaint/agents/ /app/agents/
RUN pip3 install --no-cache-dir google-adk

# Copy the built web app
COPY --from=web-builder /build/dist /app/dist
COPY --from=web-builder /build/apps/web/package.json /app/apps/web/
COPY --from=web-builder /build/apps/web/app.config.ts /app/apps/web/
COPY --from=web-builder /build/apps/web/vite.config.ts /app/apps/web/

# Copy the embedded API
COPY --from=web-builder /build/apps/web/src/api /app/api/

EXPOSE 3086 8793

CMD ["bunx", "vite", "preview", "--host", "0.0.0.0", "--port", "3086"]
