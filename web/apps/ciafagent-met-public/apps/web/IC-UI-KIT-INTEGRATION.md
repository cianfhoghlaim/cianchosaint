/**
 * CIANCHOSAINT — ciafagent-ui-kit (HMGCC IC Design System) integration note
 *   for ciafagent-met-public.
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
 *           classification="official"
 *           show_jurisdiction_badge={true}
 *           jurisdiction="met"
 *         />
 *         <CianchosaintPrivacyDisclaimer
 *           audience="public-facing"
 *           jurisdiction="met"
 *         />
 *         <ChatWindow rootAgent="met_root_agent" jurisdiction="met" audience="public" />
 *         <CianchosaintFooter build_sha="cianchosaint-met-public" />
 *       </>
 *     );
 *   }
 *   ```
 *
 * Licence: BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md).
 */

export const CIANCHOSAINT_MET_PUBLIC_IC_KIT_INTEGRATION_NOTE = "2026-08-26" as const;
