/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { Hono } from "hono";
import { stream } from "hono/streaming";
import { spawn } from "node:child_process";
export const agentRoute = new Hono();
const ROOT_AGENTS = ["ga_root_agent", "met_root_agent", "psni_root_agent"] as const;
agentRoute.post("/:root", async (c) => {
  const root = c.req.param("root");
  if (!ROOT_AGENTS.includes(root as (typeof ROOT_AGENTS)[number])) return c.json({ error: `Unknown: ${root}` }, 400);
  const body = await c.req.json<{ input: string }>();
  c.header("Content-Type", "text/event-stream");
  return stream(c, async (s) => {
    await s.writeSSE({ event: "text-delta", data: JSON.stringify({ type: "text-delta", content: `Streaming from ${root} (PSNI internal)…\n` }) });
    await new Promise<void>((resolve) => {
      const proc = spawn("python", ["-c", `import sys\nsys.path.insert(0, '../../../agents/cianchosaint/${root}/..')\nfrom cianchosaint.${root} import ${root}\nprint(${root}.handle("""${body.input.replace(/"/g, '\\"')}"""))`], { cwd: process.cwd() });
      proc.stdout.on("data", async (chunk) => { await s.writeSSE({ event: "text-delta", data: JSON.stringify({ type: "text-delta", content: chunk.toString("utf8") }) }); });
      proc.stderr.on("data", async (chunk) => { await s.writeSSE({ event: "error", data: JSON.stringify({ type: "error", error: chunk.toString("utf8") }) }); });
      proc.on("close", () => resolve());
    });
    await s.writeSSE({ event: "done", data: JSON.stringify({ type: "done" }) });
  });
});
