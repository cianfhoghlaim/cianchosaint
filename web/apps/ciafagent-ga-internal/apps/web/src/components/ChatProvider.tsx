/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import * as React from "react";
import { CopilotKit } from "@copilotkit/react-core/v2";

interface ChatProviderProps {
  rootAgent: "ga_root_agent" | "met_root_agent" | "psni_root_agent";
  children: React.ReactNode;
}

export function ChatProvider({ rootAgent, children }: ChatProviderProps) {
  return (
    <CopilotKit
      runtimeUrl={typeof process !== "undefined" ? process.env.COPILOTKIT_RUNTIME_URL || "/api/copilotkit" : "/api/copilotkit"}
      agent={rootAgent}
    >
      {children}
    </CopilotKit>
  );
}
