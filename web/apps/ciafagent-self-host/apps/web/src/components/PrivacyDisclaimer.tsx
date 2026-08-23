/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import * as React from "react";
export function PrivacyDisclaimer(_: { jurisdiction: "ga" }) {
  const [dismissed, setDismissed] = React.useState(false);
  if (dismissed) return null;
  return (
    <div className="bg-amber-950 border-b border-amber-800 px-4 py-2 flex items-center justify-between text-amber-100 text-xs">
      <div><span className="font-semibold mr-2">⚠️:</span>Self-hosted instance — data stays on your device. For emergencies, dial 999 or 112.</div>
      <button onClick={() => setDismissed(true)} className="underline">Dismiss</button>
    </div>
  );
}
