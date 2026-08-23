FROM oven/bun:1-alpine
WORKDIR /app/cianchosaint/web/apps/ciafagent-psni-internal
COPY cianchosaint/web/apps/ciafagent-psni-internal/package.json cianchosaint/web/apps/ciafagent-psni-internal/bun.lock* cianchosaint/web/apps/ciafagent-psni-internal/turbo.json ./
COPY cianchosaint/web/apps/ciafagent-psni-internal/apps/web/package.json apps/web/
COPY cianchosaint/web/apps/ciafagent-psni-internal/apps/api/package.json apps/api/
COPY cianchosaint/web/apps/ciafagent-psni-internal/packages/ packages/
RUN bun install
WORKDIR /app
COPY cianchosaint/web/apps/ciafagent-psni-internal/ /app/cianchosaint/web/apps/ciafagent-psni-internal/
EXPOSE 3085 8792
WORKDIR /app/cianchosaint/web/apps/ciafagent-psni-internal/apps/web
CMD ["bunx", "vite", "dev", "--host", "0.0.0.0", "--port", "3085"]
