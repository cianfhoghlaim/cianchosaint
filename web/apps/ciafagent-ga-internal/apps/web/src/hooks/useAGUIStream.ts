/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import * as React from "react";

interface UseAGUIStreamOptions {
  rootAgent: "ga_root_agent" | "met_root_agent" | "psni_root_agent";
}

interface AGUIEvent {
  type: "text-delta" | "pulse-schema-lookup" | "circular-citation" | "training-module-progress" | "done" | "error";
  content?: string;
  pulseLookup?: { table: string; field: string; type: string; description: string };
  circularCitation?: { id: string; title: string; date: string };
  trainingModule?: { id: string; progress: number };
  error?: string;
}

export interface AGUIResponse {
  content: string;
  citations?: Array<{ source: string; url: string; page?: number }>;
  pulseLookup?: AGUIEvent["pulseLookup"];
  circularCitation?: AGUIEvent["circularCitation"];
}

export function useAGUIStream({ rootAgent }: UseAGUIStreamOptions) {
  const [isStreaming, setIsStreaming] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const abortRef = React.useRef<AbortController | null>(null);

  const send = React.useCallback(
    async (input: string): Promise<AGUIResponse> => {
      setIsStreaming(true);
      setError(null);
      abortRef.current = new AbortController();
      try {
        const res = await fetch(`/api/agent/${rootAgent}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ input, audience: "internal" }),
          signal: abortRef.current.signal,
        });
        if (!res.ok) throw new Error(`Agent ${rootAgent} returned ${res.status}`);
        const reader = res.body?.getReader();
        const decoder = new TextDecoder();
        let buffer = "";
        let content = "";
        let pulseLookup: AGUIEvent["pulseLookup"];
        let circularCitation: AGUIEvent["circularCitation"];
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
                if (event.type === "pulse-schema-lookup") pulseLookup = event.pulseLookup;
                if (event.type === "circular-citation") circularCitation = event.circularCitation;
                if (event.type === "error") throw new Error(event.error);
              } catch { /* skip malformed */ }
            }
          }
        }
        return { content, pulseLookup, circularCitation };
      } catch (err) {
        if ((err as Error).name === "AbortError") return { content: "" };
        setError((err as Error).message);
        throw err;
      } finally {
        setIsStreaming(false);
      }
    },
    [rootAgent],
  );

  React.useEffect(() => () => abortRef.current?.abort(), []);

  return { send, isStreaming, error };
}
