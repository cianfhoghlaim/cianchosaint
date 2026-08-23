FROM oven/bun:1-alpine
WORKDIR /app/cianchosaint/web/apps/ciafagent-met-internal
COPY cianchosaint/web/apps/ciafagent-met-internal/package.json cianchosaint/web/apps/ciafagent-met-internal/bun.lock* cianchosaint/web/apps/ciafagent-met-internal/turbo.json ./
COPY cianchosaint/web/apps/ciafagent-met-internal/apps/web/package.json apps/web/
COPY cianchosaint/web/apps/ciafagent-met-internal/apps/api/package.json apps/api/
COPY cianchosaint/web/apps/ciafagent-met-internal/packages/ packages/
RUN bun install
WORKDIR /app
COPY cianchosaint/web/apps/ciafagent-met-internal/ /app/cianchosaint/web/apps/ciafagent-met-internal/
EXPOSE 3083 8790
WORKDIR /app/cianchosaint/web/apps/ciafagent-met-internal/apps/web
CMD ["bunx", "vite", "dev", "--host", "0.0.0.0", "--port", "3083"]
