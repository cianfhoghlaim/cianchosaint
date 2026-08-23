FROM oven/bun:1-alpine
WORKDIR /app/cianchosaint/web/apps/ciafagent-api
COPY cianchosaint/web/apps/ciafagent-api/package.json cianchosaint/web/apps/ciafagent-api/bun.lock* cianchosaint/web/apps/ciafagent-api/turbo.json ./
COPY cianchosaint/web/apps/ciafagent-api/apps/api/package.json apps/api/
COPY cianchosaint/web/apps/ciafagent-api/packages/ packages/
RUN bun install
WORKDIR /app
COPY cianchosaint/web/apps/ciafagent-api/ /app/cianchosaint/web/apps/ciafagent-api/
COPY cianchosaint/agents/ /app/cianchosaint/agents/
RUN apk add --no-cache python3 py3-pip && pip3 install --no-cache-dir google-adk
EXPOSE 8794
WORKDIR /app/cianchosaint/web/apps/ciafagent-api/apps/api
CMD ["bun", "run", "start"]
