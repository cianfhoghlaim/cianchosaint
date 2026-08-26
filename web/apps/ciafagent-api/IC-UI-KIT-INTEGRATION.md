/**
 * CIANCHOSAINT — ciafagent-ui-kit (HMGCC IC Design System) integration note
 *   for ciafagent-api.
 *
 * Per openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md.
 *
 * The ciafagent-api gateway uses the @cianchosaint/ciafagent-ui-kit for
 * the OpenAPI/Swagger UI surface + the embedded AG-UI streaming UI.
 *
 * Example API gateway middleware:
 *
 *   ```ts
 *   import {
 *     CianchosaintClassificationBanner,
 *     CianchosaintFooter,
 *     CianchosaintPrivacyDisclaimer,
 *   } from "@cianchosaint/ciafagent-ui-kit";
 *
 *   // In the hono route that serves the AG-UI chat HTML page:
 *   app.get("/api/chat", (c) => {
 *     return c.html(`<!DOCTYPE html>
 *       <html>
 *         <body>
 *           ${CianchosaintClassificationBanner.toString({ classification: "official" })}
 *           ${CianchosaintPrivacyDisclaimer.toString({ audience: "internal-analyst", jurisdiction: "api" })}
 *           <div id="root"></div>
 *           ${CianchosaintFooter.toString({ build_sha: "cianchosaint-api" })}
 *         </body>
 *       </html>`);
 *   });
 *   ```
 *
 * Licence: BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md).
 */

export const CIANCHOSAINT_API_IC_KIT_INTEGRATION_NOTE = "2026-08-26" as const;
