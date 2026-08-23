/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// apps/api/src/routes/agent.ts — AG-UI event source for the 3 root agents
// Streams from the 24-agent Google ADK fleet via the cianchosaint Python bridge.
//
// The agent.ts route imports `from "../../agents/cianchosaint/<root>_root_agent"`.
// At runtime, the Python subprocess is invoked from the apps/api/ workspace;
// the relative path resolves to `../../agents/cianchosaint/<root>_root_agent.py`.
// In production, the monorepo root is mounted and the absolute path is preferred.

import { Hono } from "hono";
import { stream } from "hono/streaming";
import { spawn } from "node:child_process";
import path from "node:path";

export const agentRoute = new Hono();

const ROOT_AGENTS = ["ga_root_agent", "met_root_agent", "psni_root_agent"] as const;
type RootAgent = (typeof ROOT_AGENTS)[number];

const SUPPORTED_EVENT_TYPES = [
  "text-delta",
  "tool-call",
  "form-fill-request",
  "form-fill-response",
  "osint-evidence-citation",
  "jurisdiction-disambiguation",
  "done",
  "error",
] as const;

agentRoute.post("/:root", async (c) => {
  const root = c.req.param("root") as RootAgent;
  if (!ROOT_AGENTS.includes(root)) {
    return c.json({ error: `Unknown root agent: ${root}` }, 400);
  }
  const body = await c.req.json<{
    input: string;
    providerTier?: 1 | 2 | 3 | 4;
    audience?: "public" | "internal";
  }>();

  c.header("Content-Type", "text/event-stream");
  c.header("Cache-Control", "no-cache");
  c.header("Connection", "keep-alive");
  c.header("X-Accel-Buffering", "no");

  // Resolve the Python agent path
  const agentsRoot = path.resolve(process.cwd(), "../../agents");
  const agentImportPath = path.join(agentsRoot, "cianchosaint", root);

  return stream(c, async (s) => {
    await s.writeSSE({
      event: "text-delta",
      data: JSON.stringify({ type: "text-delta", content: `Streaming from ${root} via ciafagent-api gateway…\n` }),
    });

    const pythonCode = `
import sys
sys.path.insert(0, '${agentsRoot}')
from cianchosaint.${root} import ${root}
result = ${root}.handle("""${body.input.replace(/"/g, '\\"').replace(/\n/g, '\\n')}""")
print(result)
`;

    await new Promise<void>((resolve) => {
      const proc = spawn("python3", ["-c", pythonCode], {
        cwd: agentsRoot,
        env: { ...process.env, PYTHONPATH: agentsRoot },
      });

      proc.stdout.on("data", async (chunk) => {
        await s.writeSSE({
          event: "text-delta",
          data: JSON.stringify({ type: "text-delta", content: chunk.toString("utf8") }),
        });
      });
      proc.stderr.on("data", async (chunk) => {
        await s.writeSSE({
          event: "error",
          data: JSON.stringify({ type: "error", error: chunk.toString("utf8") }),
        });
      });
      proc.on("close", (code) => {
        if (code !== 0) {
          s.writeSSE({
            event: "error",
            data: JSON.stringify({ type: "error", error: `Agent exited with code ${code}` }),
          }).catch(() => {});
        }
        resolve();
      });
    });

    await s.writeSSE({ event: "done", data: JSON.stringify({ type: "done" }) });
  });
});

agentRoute.get("/event-types", (c) => c.json({ eventTypes: SUPPORTED_EVENT_TYPES }));

agentRoute.get("/", (c) => c.json({
  root_agents: ROOT_AGENTS,
  supported_events: SUPPORTED_EVENT_TYPES,
}));
