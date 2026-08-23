/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { createFileRoute } from "@tanstack/react-router";
import * as React from "react";
export const Route = createFileRoute("/training")({ component: TrainingRoute });
function TrainingRoute() {
  const [modules, setModules] = React.useState<Array<{ id: string; title: string; progress: number }>>([]);
  React.useEffect(() => { fetch("/api/osint/met-training/modules").then(r => r.json()).then(d => setModules(d.modules || [])); }, []);
  return (
    <div className="max-w-4xl mx-auto p-8 flex flex-col gap-6">
      <h1 className="text-3xl font-bold text-blue-300">Training modules</h1>
      <div className="grid grid-cols-1 gap-4">
        {modules.map((m) => (
          <div key={m.id} className="bg-blue-950 border border-blue-900 rounded p-4">
            <h3 className="font-bold text-blue-300">{m.title}</h3>
            <div className="mt-3 h-2 bg-blue-900 rounded-full overflow-hidden">
              <div className="h-full bg-blue-500" style={{ width: `${m.progress}%` }} />
            </div>
            <p className="text-xs text-slate-400 mt-1">{m.progress}% complete</p>
          </div>
        ))}
      </div>
    </div>
  );
}
