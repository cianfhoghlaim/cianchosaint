/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// routes/chat.tsx — AG-UI chat window for ga_root_agent

import { createFileRoute } from "@tanstack/react-router";
import { ChatWindow } from "../components/ChatWindow";

export const Route = createFileRoute("/chat")({
  component: ChatComponent,
});

function ChatComponent() {
  return <ChatWindow rootAgent="ga_root_agent" jurisdiction="ga" audience="public" />;
}
