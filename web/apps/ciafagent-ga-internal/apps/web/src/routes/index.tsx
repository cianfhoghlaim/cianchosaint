/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: () => (
    <div className="max-w-4xl mx-auto p-8 flex flex-col gap-6">
      <h1 className="text-3xl font-bold text-blue-300">Internal Dashboard</h1>
      <p className="text-slate-400 text-sm">
        Welcome Garda member. Use the navigation above to access the
        PULSE schema cross-reference, internal circulars, or training materials.
      </p>
      <div className="grid grid-cols-2 gap-4">
        {SERVICES.map((s) => (
          <Link key={s.slug} to={s.route} className="bg-slate-900 border border-blue-900 rounded-xl p-6 hover:border-blue-700">
            <h3 className="font-bold text-xl mb-2 text-blue-300">{s.icon} {s.title}</h3>
            <p className="text-slate-400 text-sm">{s.description}</p>
          </Link>
        ))}
      </div>
    </div>
  ),
});

const SERVICES = [
  { slug: "chat", icon: "💬", title: "Chat with ga_root_agent", description: "Investigative queries + statutory references.", route: "/chat" as const },
  { slug: "pulse", icon: "🔍", title: "PULSE schema lookup", description: "Cross-reference PULSE fields to your query.", route: "/pulse" as const },
  { slug: "circulars", icon: "📋", title: "Internal circulars", description: "Search GA circulars + Garda HQ directives.", route: "/circulars" as const },
  { slug: "training", icon: "📚", title: "Training modules", description: "E-learning modules + competency tracking.", route: "/training" as const },
];
