FROM oven/bun:1-alpine
WORKDIR /app/cianchosaint/web/apps/ciafagent-cyberchef
COPY cianchosaint/web/apps/ciafagent-cyberchef/package.json cianchosaint/web/apps/ciafagent-cyberchef/bun.lock* cianchosaint/web/apps/ciafagent-cyberchef/turbo.json ./
COPY cianchosaint/web/apps/ciafagent-cyberchef/apps/web/package.json apps/web/
COPY cianchosaint/web/apps/ciafagent-cyberchef/apps/api/package.json apps/api/
COPY cianchosaint/web/apps/ciafagent-cyberchef/packages/ packages/
RUN bun install
WORKDIR /app
COPY cianchosaint/web/apps/ciafagent-cyberchef/ /app/cianchosaint/web/apps/ciafagent-cyberchef/
EXPOSE 3085 8792
WORKDIR /app/cianchosaint/web/apps/ciafagent-cyberchef/apps/web
CMD ["bunx", "vite", "dev", "--host", "0.0.0.0", "--port", "3085"]
