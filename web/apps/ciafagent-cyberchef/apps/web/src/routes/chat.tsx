/**
 * CIANCHOSAINT new-build: ciafagent-cyberchef chat route.
 *
 * Wholesale pattern: mirrors ciafagent-psni-internal/apps/web/src/routes/chat.tsx.
 *
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { createFileRoute } from "@tanstack/react-router";

export { ChatWindow } from "../components/ChatWindow";

export const Route = createFileRoute("/chat")({
  component: () => (
    <ChatWindow
      rootAgent="cyberchef_root_agent"
      jurisdiction="uk"
      audience="internal"
    />
  ),
});
