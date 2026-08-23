FROM oven/bun:1-alpine
WORKDIR /app/cianchosaint/web/apps/ciafagent-met-public
COPY cianchosaint/web/apps/ciafagent-met-public/package.json cianchosaint/web/apps/ciafagent-met-public/bun.lock* cianchosaint/web/apps/ciafagent-met-public/turbo.json ./
COPY cianchosaint/web/apps/ciafagent-met-public/apps/web/package.json apps/web/
COPY cianchosaint/web/apps/ciafagent-met-public/apps/api/package.json apps/api/
COPY cianchosaint/web/apps/ciafagent-met-public/packages/ packages/
RUN bun install
WORKDIR /app
COPY cianchosaint/web/apps/ciafagent-met-public/ /app/cianchosaint/web/apps/ciafagent-met-public/
EXPOSE 3082 8789
WORKDIR /app/cianchosaint/web/apps/ciafagent-met-public/apps/web
CMD ["bunx", "vite", "dev", "--host", "0.0.0.0", "--port", "3082"]
