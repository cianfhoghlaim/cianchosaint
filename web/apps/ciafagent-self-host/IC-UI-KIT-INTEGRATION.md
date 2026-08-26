/**
 * CIANCHOSAINT — ciafagent-ui-kit (HMGCC IC Design System) integration note
 *   for ciafagent-self-host.
 *
 * Per openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md.
 *
 * The self-host citizen footprint uses the public-facing audience and
 * the standard OFFICIAL classification banner. The footer should
 * include the "self-host" build_sha so analysts can verify which
 * container they are talking to.
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
 *           jurisdiction="self-host"
 *         />
 *         <CianchosaintPrivacyDisclaimer
 *           audience="public-facing"
 *           jurisdiction="self-host"
 *         />
 *         <ChatWindow rootAgent="self_host_root_agent" jurisdiction="self-host" audience="public" />
 *         <CianchosaintFooter
 *           build_sha="cianchosaint-self-host"
 *           contact_href="https://github.com/cianfhoghlaim/cianchosaint/issues"
 *         />
 *       </>
 *     );
 *   }
 *   ```
 *
 * Licence: BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md).
 */

export const CIANCHOSAINT_SELF_HOST_IC_KIT_INTEGRATION_NOTE = "2026-08-26" as const;
