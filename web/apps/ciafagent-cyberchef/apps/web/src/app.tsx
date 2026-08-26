/**
 * CIANCHOSAINT new-build: ciafagent-cyberchef web app root.
 *
 * Wholesale pattern: mirrors ciafagent-psni-internal/apps/web/src/app.tsx.
 *
 * Per the openspec/changes/cianchosaint-hmgcc-gchq-tooling-v1/
 * specs/cianchosaint-hmgcc-gchq-tooling/spec.md (CyberChef track).
 *
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import * as React from "react";
import { CopilotKit } from "@copilotkit/react-core/v2";

interface AppProps {
  children: React.ReactNode;
}

export function App({ children }: AppProps) {
  return (
    <CopilotKit
      runtimeUrl="/api/copilotkit"
      agent="cyberchef_root_agent"
    >
      <div className="min-h-screen bg-slate-950 text-slate-100">
        {children}
      </div>
    </CopilotKit>
  );
}
