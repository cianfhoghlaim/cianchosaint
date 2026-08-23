/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// components/ChatWindow.tsx — AG-UI chat window
// Streams from ga_root_agent via the ciafagent-api gateway.

import * as React from "react";
import { useAGUIStream } from "../hooks/useAGUIStream";
import { PrivacyDisclaimer } from "./PrivacyDisclaimer";

interface ChatWindowProps {
  rootAgent: "ga_root_agent" | "met_root_agent" | "psni_root_agent";
  jurisdiction: "ga" | "met" | "psni";
  audience: "public" | "internal";
}

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  citations?: Array<{ source: string; url: string; page?: number }>;
  formFillRequest?: FormFillRequest;
  jurisdictionDisambiguation?: { suggested: string; reason: string };
  timestamp: number;
}

interface FormFillRequest {
  formType: "lost_property" | "minor_crime" | "victim_support";
  fields: Array<{ name: string; label: string; type: string; required: boolean }>;
}

export function ChatWindow({ rootAgent, jurisdiction, audience }: ChatWindowProps) {
  const [messages, setMessages] = React.useState<ChatMessage[]>([]);
  const [input, setInput] = React.useState("");
  const { send, isStreaming, error } = useAGUIStream({ rootAgent });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isStreaming) return;
    const userMsg: ChatMessage = { role: "user", content: input, timestamp: Date.now() };
    setMessages((m) => [...m, userMsg]);
    setInput("");

    try {
      const event = await send(input);
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          content: event.content,
          citations: event.citations,
          formFillRequest: event.formFillRequest,
          jurisdictionDisambiguation: event.jurisdictionDisambiguation,
          timestamp: Date.now(),
        },
      ]);
    } catch (err) {
      setMessages((m) => [
        ...m,
        { role: "assistant", content: `Error: ${(err as Error).message}`, timestamp: Date.now() },
      ]);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-3.5rem)]">
      <PrivacyDisclaimer jurisdiction={jurisdiction} />
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-slate-500 mt-8">
            Start typing to chat with the {rootAgent}.
          </div>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-2xl rounded-lg p-3 ${
                msg.role === "user"
                  ? "bg-emerald-700 text-white"
                  : "bg-slate-800 text-slate-100"
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
              {msg.citations && msg.citations.length > 0 && (
                <ul className="mt-2 text-xs text-slate-400 space-y-1">
                  {msg.citations.map((c, j) => (
                    <li key={j}>
                      <a href={c.url} target="_blank" rel="noreferrer" className="underline">
                        {c.source}{c.page ? ` · p. ${c.page}` : ""}
                      </a>
                    </li>
                  ))}
                </ul>
              )}
              {msg.jurisdictionDisambiguation && (
                <div className="mt-2 p-2 bg-amber-900 border border-amber-700 rounded text-xs">
                  <strong>Jurisdiction check:</strong> This query may be better handled by{" "}
                  <code>{msg.jurisdictionDisambiguation.suggested}</code>.{" "}
                  {msg.jurisdictionDisambiguation.reason}
                </div>
              )}
            </div>
          </div>
        ))}
        {isStreaming && <div className="text-slate-500 text-sm">Streaming…</div>}
        {error && <div className="text-red-400 text-sm">Error: {error}</div>}
      </div>
      <form onSubmit={handleSubmit} className="border-t border-slate-700 p-4 flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your question…"
          className="flex-1 bg-slate-800 text-slate-100 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
          disabled={isStreaming}
        />
        <button
          type="submit"
          disabled={isStreaming || !input.trim()}
          className="bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-700 text-white px-4 py-2 rounded text-sm"
        >
          Send
        </button>
      </form>
    </div>
  );
}
