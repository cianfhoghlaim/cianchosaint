/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// hooks/useAGUIStream.ts — AG-UI event stream subscription hook

import * as React from "react";

interface UseAGUIStreamOptions {
  rootAgent: "ga_root_agent" | "met_root_agent" | "psni_root_agent";
  apiBase?: string;
}

interface AGUIEvent {
  type: "text-delta" | "tool-call" | "form-fill-request" | "form-fill-response" | "osint-evidence-citation" | "jurisdiction-disambiguation" | "done" | "error";
  content?: string;
  toolName?: string;
  toolArgs?: Record<string, unknown>;
  citations?: Array<{ source: string; url: string; page?: number }>;
  formFillRequest?: {
    formType: string;
    fields: Array<{ name: string; label: string; type: string; required: boolean }>;
  };
  jurisdictionDisambiguation?: { suggested: string; reason: string };
  error?: string;
}

export interface AGUIResponse {
  content: string;
  citations?: Array<{ source: string; url: string; page?: number }>;
  formFillRequest?: AGUIEvent["formFillRequest"];
  jurisdictionDisambiguation?: AGUIEvent["jurisdictionDisambiguation"];
}

const API_BASE = (() => {
  if (typeof process !== "undefined" && process.env?.VITE_AGUI_API_BASE) return process.env.VITE_AGUI_API_BASE;
  if (typeof import.meta !== "undefined") {
    return (import.meta as { env?: { VITE_AGUI_API_BASE?: string } }).env?.VITE_AGUI_API_BASE || "/api/agent";
  }
  return "/api/agent";
})();

export function useAGUIStream({ rootAgent, apiBase = API_BASE }: UseAGUIStreamOptions) {
  const [isStreaming, setIsStreaming] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const abortRef = React.useRef<AbortController | null>(null);

  const send = React.useCallback(
    async (input: string): Promise<AGUIResponse> => {
      setIsStreaming(true);
      setError(null);
      abortRef.current = new AbortController();
      try {
        const res = await fetch(`${apiBase}/${rootAgent}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ input }),
          signal: abortRef.current.signal,
        });
        if (!res.ok) throw new Error(`Agent ${rootAgent} returned ${res.status}`);
        const reader = res.body?.getReader();
        const decoder = new TextDecoder();
        let buffer = "";
        let content = "";
        let citations: AGUIResponse["citations"];
        let formFillRequest: AGUIResponse["formFillRequest"];
        let jurisdictionDisambiguation: AGUIResponse["jurisdictionDisambiguation"];
        if (reader) {
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split("\n");
            buffer = lines.pop() ?? "";
            for (const line of lines) {
              if (!line.startsWith("data:")) continue;
              try {
                const event: AGUIEvent = JSON.parse(line.slice(5).trim());
                if (event.type === "text-delta" && event.content) content += event.content;
                if (event.type === "osint-evidence-citation") citations = event.citations;
                if (event.type === "form-fill-request") formFillRequest = event.formFillRequest;
                if (event.type === "jurisdiction-disambiguation") jurisdictionDisambiguation = event.jurisdictionDisambiguation;
                if (event.type === "error") throw new Error(event.error);
              } catch (parseErr) {
                // skip malformed lines
              }
            }
          }
        }
        return { content, citations, formFillRequest, jurisdictionDisambiguation };
      } catch (err) {
        if ((err as Error).name === "AbortError") {
          return { content: "" };
        }
        setError((err as Error).message);
        throw err;
      } finally {
        setIsStreaming(false);
      }
    },
    [rootAgent, apiBase],
  );

  const cancel = React.useCallback(() => {
    abortRef.current?.abort();
  }, []);

  React.useEffect(() => () => abortRef.current?.abort(), []);

  return { send, cancel, isStreaming, error };
}
