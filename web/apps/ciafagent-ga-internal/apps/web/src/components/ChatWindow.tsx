/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import * as React from "react";
import { useAGUIStream } from "../hooks/useAGUIStream";

interface ChatWindowProps {
  rootAgent: "ga_root_agent" | "met_root_agent" | "psni_root_agent";
  jurisdiction: "ga" | "met" | "psni";
  audience: "public" | "internal";
}

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  citations?: Array<{ source: string; url: string; page?: number }>;
  pulseLookup?: { table: string; field: string; type: string; description: string };
  circularCitation?: { id: string; title: string; date: string };
  timestamp: number;
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
          pulseLookup: (event as Record<string, unknown>).pulseLookup as ChatMessage["pulseLookup"],
          circularCitation: (event as Record<string, unknown>).circularCitation as ChatMessage["circularCitation"],
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
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`max-w-2xl rounded-lg p-3 ${msg.role === "user" ? "bg-blue-700" : "bg-slate-900"}`}>
              <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
              {msg.pulseLookup && (
                <div className="mt-2 p-2 bg-slate-800 border border-slate-700 rounded text-xs">
                  <strong>PULSE field:</strong> <code>{msg.pulseLookup.table}.{msg.pulseLookup.field}</code> ({msg.pulseLookup.type})
                  <p className="text-slate-400 mt-1">{msg.pulseLookup.description}</p>
                </div>
              )}
              {msg.circularCitation && (
                <div className="mt-2 p-2 bg-blue-950 border border-blue-800 rounded text-xs">
                  <strong>Circular:</strong> {msg.circularCitation.title} · {msg.circularCitation.date}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="border-t border-slate-700 p-4 flex gap-2">
        <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Internal query…" className="flex-1 bg-slate-900 text-slate-100 rounded px-3 py-2 text-sm" disabled={isStreaming} />
        <button type="submit" disabled={isStreaming || !input.trim()} className="bg-blue-700 hover:bg-blue-600 disabled:bg-slate-700 text-white px-4 py-2 rounded text-sm">Send</button>
      </form>
      {error && <div className="text-red-400 text-xs p-2">{error}</div>}
    </div>
  );
}
