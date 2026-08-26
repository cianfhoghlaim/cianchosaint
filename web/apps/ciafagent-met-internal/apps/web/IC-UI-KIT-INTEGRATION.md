/**
 * CIANCHOSAINT — ciafagent-ui-kit (HMGCC IC Design System) integration note
 *   for ciafagent-met-internal.
 *
 * Per openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md.
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
 *           jurisdiction="met"
 *         />
 *         <CianchosaintPrivacyDisclaimer
 *           audience="internal-analyst"
 *           jurisdiction="met"
 *         />
 *         <ChatWindow rootAgent="met_root_agent" jurisdiction="met" audience="internal" />
 *         <CianchosaintFooter
 *           classification_caption="OFFICIAL-SENSITIVE — internal analyst surface"
 *           build_sha="cianchosaint-met-internal"
 *         />
 *       </>
 *     );
 *   }
 *   ```
 *
 * Licence: BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md).
 */

export const CIANCHOSAINT_MET_INTERNAL_IC_KIT_INTEGRATION_NOTE = "2026-08-26" as const;
