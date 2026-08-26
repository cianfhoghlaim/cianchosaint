/**
 * CIANCHOSAINT new-build: ciafagent-cyberchef OSINT route (mirrors the
 * per-source `SourcePolicyCard` upstream contract).
 *
 * Wholesale pattern: mirrors ciafagent-psni-internal/apps/api/src/routes/osint.ts.
 *
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { Hono } from "hono";

const osintRoute = new Hono();

osintRoute.get("/", (c) =>
  c.json({
    source_id: "gchq_cyberchef",
    body: "GCHQ (CyberChef wholesale — Apache 2.0)",
    category: "intelligence_agency",
    osint_ceiling: "Public-facing CyberChef UI + catalogue only",
    gaps: [
      "Classified CyberChef operations excluded by the OSINT ceiling",
      "Auto-upstream CyberChef version pinning intentionally lags the upstream release",
    ],
    baml_function: "ExtractCyberChefRecipe",
    milestone_gate: "cianchosaint:cyberchef:smoke",
  }),
);

export { osintRoute };
