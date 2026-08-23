/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { createFileRoute, Link } from "@tanstack/react-router";
export const Route = createFileRoute("/")({ component: () => (
  <div className="max-w-4xl mx-auto p-8 flex flex-col gap-6">
    <h1 className="text-4xl font-bold text-emerald-400">PSNI</h1>
    <p className="text-slate-300 text-lg">Non-emergency citizen portal. For emergencies, dial <strong className="text-red-400">999</strong> immediately.</p>
    <div className="grid grid-cols-2 gap-4">
      {[{ slug: "chat", icon: "💬", title: "Chat", desc: "psni_root_agent", route: "/chat" as const }, { slug: "form", icon: "📝", title: "Form fill", desc: "Non-emergency forms", route: "/form-fill" as const }, { slug: "stat", icon: "📖", title: "Statute", desc: "NI legislation search", route: "/statute-search" as const }, { slug: "about", icon: "ℹ️", title: "About", desc: "Privacy", route: "/about" as const }].map((s) => (
        <Link key={s.slug} to={s.route} className="bg-slate-800 border border-emerald-900 rounded-xl p-6 hover:border-emerald-700"><h3 className="font-bold text-xl text-emerald-300 mb-2">{s.icon} {s.title}</h3><p className="text-slate-400 text-sm">{s.desc}</p></Link>
      ))}
    </div>
  </div>
) });
