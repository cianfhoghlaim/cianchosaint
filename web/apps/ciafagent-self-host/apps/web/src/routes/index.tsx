/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 *
 * IC UI Kit integration: per
 * openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md.
 */
import { createFileRoute, Link } from "@tanstack/react-router";
import {
  CianchosaintClassificationBanner,
  CianchosaintFooter,
  CianchosaintPrivacyDisclaimer,
} from "@cianchosaint/ciafagent-ui-kit";

export const Route = createFileRoute("/")({ component: () => (
  <>
    <CianchosaintClassificationBanner
      classification="official"
      show_jurisdiction_badge={true}
      jurisdiction="self-host"
    />
    <CianchosaintPrivacyDisclaimer
      audience="public-facing"
      jurisdiction="self-host"
    />
    <div className="max-w-4xl mx-auto p-8 flex flex-col gap-6">
      <h1 className="text-4xl font-bold text-emerald-400">ciafagent self-host</h1>
      <p className="text-slate-300 text-lg">Your local citizen portal. All data stays on your device.</p>
      <div className="bg-emerald-950 border border-emerald-900 rounded-lg p-4">
        <h2 className="font-bold text-emerald-300 mb-2">Offline mode active</h2>
        <p className="text-slate-400 text-sm">This portal runs locally. When offline, the embedded agents answer from the pre-baked SQLite cache.</p>
      </div>
      <Link to="/chat" className="bg-emerald-600 hover:bg-emerald-500 text-white px-6 py-3 rounded text-lg font-semibold inline-block w-fit">Start chatting →</Link>
    </div>
    <CianchosaintFooter build_sha="cianchosaint-self-host" />
  </>
) });
