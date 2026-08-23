/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// apps/web/src/app.tsx — root app for ciafagent-ga-public
// Renders the PrivacyDisclaimer at the top + mounts the CopilotKit provider.

import * as React from "react";
import { CopilotKit } from "@copilotkit/react-core/v2";
import { PrivacyDisclaimer } from "./components/PrivacyDisclaimer";

interface AppProps {
  children: React.ReactNode;
}

export function App({ children }: AppProps) {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit" agent="ga_root_agent">
      <div className="min-h-screen bg-slate-900 text-slate-100">
        <PrivacyDisclaimer jurisdiction="ga" />
        {children}
      </div>
    </CopilotKit>
  );
}
