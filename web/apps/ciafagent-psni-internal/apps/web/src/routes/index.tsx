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
    <h1 className="text-3xl font-bold text-emerald-300">PSNI Internal Dashboard</h1>
    <p className="text-slate-400 text-sm">Welcome. NI Policing Board integration + internal circulars + training modules.</p>
    <div className="grid grid-cols-2 gap-4">
      {[{ slug: "chat", icon: "💬", title: "Chat", desc: "Investigative queries", route: "/chat" as const }, { slug: "pb", icon: "🏛️", title: "Policing Board", desc: "NI oversight body", route: "/policing-board" as const }, { slug: "circ", icon: "📋", title: "Circulars", desc: "Internal PSNI circulars", route: "/circulars" as const }, { slug: "train", icon: "📚", title: "Training", desc: "Officer training", route: "/training" as const }].map((s) => (
        <Link key={s.slug} to={s.route} className="bg-emerald-950 border border-emerald-900 rounded-xl p-6 hover:border-emerald-700"><h3 className="font-bold text-xl text-emerald-300 mb-2">{s.icon} {s.title}</h3><p className="text-slate-400 text-sm">{s.desc}</p></Link>
      ))}
    </div>
  </div>
) });
