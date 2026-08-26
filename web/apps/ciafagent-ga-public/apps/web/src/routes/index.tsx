/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// routes/index.tsx — ciafagent-ga-public landing page

import { createFileRoute, Link } from "@tanstack/react-router";
import {
  CianchosaintClassificationBanner,
  CianchosaintFooter,
  CianchosaintPrivacyDisclaimer,
} from "@cianchosaint/ciafagent-ui-kit";

export const Route = createFileRoute("/")({
  component: LandingComponent,
});

function LandingComponent() {
  return (
    <>
      <CianchosaintClassificationBanner
        classification="official"
        show_jurisdiction_badge={true}
        jurisdiction="ga"
      />
      <CianchosaintPrivacyDisclaimer
        audience="public-facing"
        jurisdiction="ga"
      />
      <div className="max-w-4xl mx-auto flex flex-col gap-8 p-8">
        <div className="flex flex-col gap-2">
          <h1 className="text-4xl font-bold text-emerald-400">
            An Garda Síochána
          </h1>
          <p className="text-slate-300 text-lg">
            Your gateway to non-emergency Garda services. For emergencies, call{" "}
            <strong className="text-red-400">999</strong> or <strong className="text-red-400">112</strong>{" "}
            immediately.
          </p>
          <p className="text-slate-500 text-sm font-mono">
            ga-public.cianchosaint.ie · powered by the ga_root_agent (Google ADK) + 5 GA specialists
          </p>
        </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {SERVICES.map((s) => (
          <Link
            key={s.slug}
            to={s.route}
            className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-xl relative overflow-hidden group hover:border-emerald-700"
          >
            <h3 className="font-bold text-xl mb-2 flex items-center gap-2">
              <span>{s.icon}</span> {s.title}
            </h3>
            <p className="text-slate-400 text-sm mb-2">{s.title_ga}</p>
            <p className="text-slate-500 text-sm">{s.description}</p>
            <span className="inline-block text-sm mt-4 text-emerald-400 group-hover:underline">
              Open →
            </span>
          </Link>
        ))}
      </div>
      <div className="mt-4 p-4 bg-red-950 border border-red-800 rounded-lg">
        <h2 className="font-bold text-red-300 mb-2">Emergency?</h2>
        <p className="text-red-200 text-sm">
          If a crime is in progress or there is an immediate threat to life,
          call <strong>999</strong> or <strong>112</strong> immediately. This
          portal is for non-emergency queries only.
        </p>
      </div>
      </div>
      <CianchosaintFooter build_sha="cianchosaint-ga-public" />
    </>
  );
}

const SERVICES = [
  {
    slug: "chat",
    icon: "💬",
    title: "Chat with a Garda AI",
    title_ga: "Labhair le Garda AI",
    description: "Ask questions about non-emergency Garda services in EN or GA.",
    route: "/chat" as const,
  },
  {
    slug: "form-fill",
    icon: "📝",
    title: "Form filling",
    title_ga: "Foirm líonadh",
    description: "Lost property, minor crime reports, victim support forms.",
    route: "/form-fill" as const,
  },
  {
    slug: "statute",
    icon: "📖",
    title: "Statute search",
    title_ga: "Cuardach reachtaíochta",
    description: "Search irishstatutebook.ie for Acts and SIs.",
    route: "/statute-search" as const,
  },
  {
    slug: "about",
    icon: "ℹ️",
    title: "About this portal",
    title_ga: "Maidir leis an tairseach seo",
    description: "Privacy, data retention, and section disclosures.",
    route: "/about" as const,
  },
];
