/**
 * CIANCHOSAINT new-build: ciafagent-cyberchef recipe index route.
 *
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/recipes")({
  component: () => (
    <div className="max-w-4xl mx-auto p-8 text-slate-200">
      <h1 className="text-2xl font-bold text-cyan-300 mb-4">CyberChef Recipes</h1>
      <p className="text-slate-400 text-sm">
        The recipe index is populated by the
        <code> cyberchef_recipes </code>
        DLT resource (see
        <code> dlt_sources/cianchosaint/uk/cyberchef/recipe_extraction.py </code>).
      </p>
    </div>
  ),
});
