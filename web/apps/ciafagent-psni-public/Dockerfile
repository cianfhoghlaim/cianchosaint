FROM oven/bun:1-alpine
WORKDIR /app/cianchosaint/web/apps/ciafagent-psni-public
COPY cianchosaint/web/apps/ciafagent-psni-public/package.json cianchosaint/web/apps/ciafagent-psni-public/bun.lock* cianchosaint/web/apps/ciafagent-psni-public/turbo.json ./
COPY cianchosaint/web/apps/ciafagent-psni-public/apps/web/package.json apps/web/
COPY cianchosaint/web/apps/ciafagent-psni-public/apps/api/package.json apps/api/
COPY cianchosaint/web/apps/ciafagent-psni-public/packages/ packages/
RUN bun install
WORKDIR /app
COPY cianchosaint/web/apps/ciafagent-psni-public/ /app/cianchosaint/web/apps/ciafagent-psni-public/
EXPOSE 3084 8791
WORKDIR /app/cianchosaint/web/apps/ciafagent-psni-public/apps/web
CMD ["bunx", "vite", "dev", "--host", "0.0.0.0", "--port", "3084"]
