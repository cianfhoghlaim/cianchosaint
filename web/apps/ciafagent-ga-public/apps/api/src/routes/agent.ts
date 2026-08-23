/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// apps/api/src/routes/agent.ts — AG-UI event source for the GA root agent
// Streams from the ga_root_agent (Google ADK) via the ciafagent-api gateway.

import { Hono } from "hono";
import { stream } from "hono/streaming";
import { spawn } from "node:child_process";

export const agentRoute = new Hono();

const ROOT_AGENTS = ["ga_root_agent", "met_root_agent", "psni_root_agent"] as const;
type RootAgent = (typeof ROOT_AGENTS)[number];

// AG-UI event types per the ciafagent task spec
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
  const body = await c.req.json<{ input: string; providerTier?: 1 | 2 | 3 | 4 }>();

  c.header("Content-Type", "text/event-stream");
  c.header("Cache-Control", "no-cache");
  c.header("Connection", "keep-alive");

  return stream(c, async (s) => {
    // Spawn the Python ADK agent via subprocess. The path is the
    // canonical location per the cianchosaint-per-constituency-agents-v1 spec.
    //
    // Note: this is a Node.js bridge to a Python module. The relative
    // path `../../agents/cianchosaint/<root>_root_agent` is resolved
    // against the apps/api/ workspace; in production the monorepo root
    // is mounted and the absolute path is preferred.
    const agentPath = `../../../agents/cianchosaint/${root}`;

    await s.writeSSE({
      event: "text-delta",
      data: JSON.stringify({ type: "text-delta", content: `Streaming from ${root}…\n` }),
    });

    await new Promise<void>((resolve) => {
      const proc = spawn("python", ["-c", `
import sys
sys.path.insert(0, '${agentPath}/..')
from cianchosaint.${root} import ${root}
result = ${root}.handle("""${body.input.replace(/"/g, '\\"')}""")
print(result)
`], { cwd: process.cwd() });

      proc.stdout.on("data", async (chunk) => {
        const text = chunk.toString("utf8");
        await s.writeSSE({
          event: "text-delta",
          data: JSON.stringify({ type: "text-delta", content: text }),
        });
      });
      proc.stderr.on("data", async (chunk) => {
        await s.writeSSE({
          event: "error",
          data: JSON.stringify({ type: "error", error: chunk.toString("utf8") }),
        });
      });
      proc.on("close", () => resolve());
    });

    await s.writeSSE({
      event: "done",
      data: JSON.stringify({ type: "done" }),
    });
  });
});

agentRoute.get("/event-types", (c) => c.json({ eventTypes: SUPPORTED_EVENT_TYPES }));
