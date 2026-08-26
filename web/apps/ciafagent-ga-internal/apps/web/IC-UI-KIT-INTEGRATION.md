/**
 * CIANCHOSAINT — ciafagent-ui-kit (HMGCC IC Design System) integration note
 *   for ciafagent-ga-internal.
 *
 * Per openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md.
 *
 * This app uses the internal analyst audience — the OSINT ceiling
 * disclaimer is permanent (cannot be dismissed) per the BUSL-1.1 v2
 * licence posture.
 *
 * Example chat route integration:
 *
 *   ```tsx
 *   import {
 *     CianchosaintClassificationBanner,
 *     CianchosaintFooter,
 *     CianchosaintPrivacyDisclaimer,
 *   } from "@cianchosaint/ciafagent-ui-kit";
 *
 *   function ChatRoute() {
 *     return (
 *       <>
 *         <CianchosaintClassificationBanner
 *           classification="official-sensitive"
 *           show_jurisdiction_badge={true}
 *           jurisdiction="ga"
 *         />
 *         <CianchosaintPrivacyDisclaimer
 *           audience="internal-analyst"
 *           jurisdiction="ga"
 *         />
 *         <ChatWindow rootAgent="ga_root_agent" jurisdiction="ga" audience="internal" />
 *         <CianchosaintFooter
 *           classification_caption="OFFICIAL-SENSITIVE — internal analyst surface"
 *           build_sha="cianchosaint-ga-internal"
 *         />
 *       </>
 *     );
 *   }
 *   ```
 *
 * Licence: BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md).
 */

export const CIANCHOSAINT_GA_INTERNAL_IC_KIT_INTEGRATION_NOTE = "2026-08-26" as const;
