/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// components/ChatProvider.tsx — CopilotKit provider wrapper for the GA root agent

import * as React from "react";
import { CopilotKit } from "@copilotkit/react-core/v2";

interface ChatProviderProps {
  rootAgent: "ga_root_agent" | "met_root_agent" | "psni_root_agent";
  children: React.ReactNode;
}

const RUNTIME_URL = (() => {
  if (typeof process !== "undefined" && process.env?.COPILOTKIT_RUNTIME_URL) {
    return process.env.COPILOTKIT_RUNTIME_URL;
  }
  if (typeof import.meta !== "undefined") {
    const env = (import.meta as { env?: { VITE_COPILOTKIT_RUNTIME_URL?: string } }).env;
    return env?.VITE_COPILOTKIT_RUNTIME_URL || "/api/copilotkit";
  }
  return "/api/copilotkit";
})();

export function ChatProvider({ rootAgent, children }: ChatProviderProps) {
  return (
    <CopilotKit runtimeUrl={RUNTIME_URL} agent={rootAgent}>
      {children}
    </CopilotKit>
  );
}
