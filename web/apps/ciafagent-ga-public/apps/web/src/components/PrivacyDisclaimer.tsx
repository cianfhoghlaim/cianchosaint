/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// components/PrivacyDisclaimer.tsx — public-facing privacy disclaimer banner
// Rendered at the top of every public-facing chat window per the ciafagent task spec.

import * as React from "react";

interface PrivacyDisclaimerProps {
  jurisdiction: "ga" | "met" | "psni";
}

const DISCLAIMER_TEXT: Record<"ga" | "met" | "psni", { en: string; ga?: string }> = {
  ga: {
    en: "This is a non-emergency service. For emergencies, dial 999 or 112. Conversations are retained for 30 days for safety and audit purposes.",
    ga: "Seirbhís neamhéigeandála í seo. I gcás éigeandála, cuir glao ar 999 nó 112. Coimeádtar comhráite ar feadh 30 lá chun críocha sábháilteachta agus iniúchta.",
  },
  met: {
    en: "This is a non-emergency service. For emergencies, dial 999. Conversations are retained for 30 days for safety and audit purposes.",
  },
  psni: {
    en: "This is a non-emergency service. For emergencies, dial 999. Conversations are retained for 30 days for safety and audit purposes.",
  },
};

export function PrivacyDisclaimer({ jurisdiction }: PrivacyDisclaimerProps) {
  const [dismissed, setDismissed] = React.useState(false);
  if (dismissed) return null;
  const text = DISCLAIMER_TEXT[jurisdiction];
  return (
    <div className="bg-amber-950 border-b border-amber-800 px-4 py-2 flex items-center justify-between text-amber-100 text-xs">
      <div>
        <span className="font-semibold mr-2">⚠️ Privacy:</span>
        {text.en}
      </div>
      <button
        onClick={() => setDismissed(true)}
        className="text-amber-300 hover:text-amber-100 underline text-xs"
      >
        Dismiss
      </button>
    </div>
  );
}
