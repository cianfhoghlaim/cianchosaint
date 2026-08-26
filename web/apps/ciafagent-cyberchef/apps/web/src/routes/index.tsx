/**
 * CIANCHOSAINT new-build: ciafagent-cyberchef landing.
 *
 * Wholesale pattern: mirrors ciafagent-psni-internal/apps/web/src/routes/index.tsx.
 *
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: () => (
    <div className="max-w-4xl mx-auto p-8 flex flex-col gap-6">
      <h1 className="text-3xl font-bold text-cyan-300">
        CyberChef Internal Dashboard
      </h1>
      <p className="text-slate-400 text-sm">
        GUI-based data analysis powered by the GCHQ CyberChef (Apache
        2.0) wholesale source. The ~28 operations exposed here cover
        encoding, encryption, hashing, IPv6 extraction, certificate
        parsing, JSON/XML/CSV transforms.
      </p>
      <div className="grid grid-cols-2 gap-4">
        {[
          {
            slug: "chat",
            icon: "💬",
            title: "Chat",
            desc: "Author recipes via AG-UI",
            route: "/chat" as const,
          },
          {
            slug: "rec",
            icon: "📚",
            title: "Recipes",
            desc: "Recipe index (per the DLT source)",
            route: "/recipes" as const,
          },
          {
            slug: "cat",
            icon: "🧰",
            title: "Operation Catalog",
            desc: "The ~28 wrapped operations",
            route: "/operation-catalog" as const,
          },
          {
            slug: "exe",
            icon: "📜",
            title: "Executions",
            desc: "Append-only execution log",
            route: "/executions" as const,
          },
        ].map((s) => (
          <Link
            key={s.slug}
            to={s.route}
            className="bg-cyan-950 border border-cyan-900 rounded-xl p-6 hover:border-cyan-700"
          >
            <h3 className="font-bold text-xl text-cyan-300 mb-2">
              {s.icon} {s.title}
            </h3>
            <p className="text-slate-400 text-sm">{s.desc}</p>
          </Link>
        ))}
      </div>
    </div>
  ),
});
