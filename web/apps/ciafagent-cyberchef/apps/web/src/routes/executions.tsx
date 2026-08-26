/**
 * CIANCHOSAINT new-build: ciafagent-cyberchef executions route (the
 * append-only execution log; mirrors the
 * <code>cyberchef_executions</code> DLT resource).
 *
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/executions")({
  component: () => (
    <div className="max-w-4xl mx-auto p-8 text-slate-200">
      <h1 className="text-2xl font-bold text-cyan-300 mb-4">CyberChef Execution Log</h1>
      <p className="text-slate-400 text-sm">
        Append-only execution log. Each
        <code> cyberchef_execute </code>
        FunctionTool invocation writes a row with the recipe_id + input
        digest + output digest + analyst_user_id. Bounded by the OSINT
        ceiling + the licence posture (BUSL-1.1 v2, British-Isles-only).
      </p>
    </div>
  ),
});
