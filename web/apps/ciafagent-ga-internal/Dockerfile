FROM oven/bun:1-alpine
WORKDIR /app/cianchosaint/web/apps/ciafagent-ga-internal
COPY cianchosaint/web/apps/ciafagent-ga-internal/package.json cianchosaint/web/apps/ciafagent-ga-internal/bun.lock* cianchosaint/web/apps/ciafagent-ga-internal/turbo.json ./
COPY cianchosaint/web/apps/ciafagent-ga-internal/apps/web/package.json apps/web/
COPY cianchosaint/web/apps/ciafagent-ga-internal/apps/api/package.json apps/api/
COPY cianchosaint/web/apps/ciafagent-ga-internal/packages/ packages/
RUN bun install
WORKDIR /app
COPY cianchosaint/web/apps/ciafagent-ga-internal/ /app/cianchosaint/web/apps/ciafagent-ga-internal/
EXPOSE 3081 8788
WORKDIR /app/cianchosaint/web/apps/ciafagent-ga-internal/apps/web
CMD ["bunx", "vite", "dev", "--host", "0.0.0.0", "--port", "3081"]
