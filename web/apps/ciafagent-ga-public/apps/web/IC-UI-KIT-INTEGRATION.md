/**
 * CIANCHOSAINT — ciafagent-ui-kit (HMGCC IC Design System) integration note
 *   for ciafagent-ga-public.
 *
 * Per openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md Requirement: Update
 * every ciafagent-* web app to use the IC components from
 * @cianchosaint/ciafagent-ui-kit.
 *
 * This file documents the integration pattern. The wholesale-copied
 * upstream web components live at
 * web/packages/ciafagent-ui-kit/src/ic-web-components/
 * (322 .ts/.tsx files, 70 component directories) per the bootstrap-v2
 * wholesale-copy pattern.
 *
 * The 9 ciafagent-level integration wrappers are:
 *   1. CianchosaintClassificationBanner — use at the top of every page
 *   2. CianchosaintTopNavigation — use as the global nav
 *   3. CianchosaintSearchBar — use as the search entry point
 *   4. CianchosaintDataTable — for tabular analyst views
 *   5. CianchosaintTabGroup — for tabbed analyst views
 *   6. CianchosaintDrawer — for slide-in panels
 *   7. CianchosaintCardVertical — for one-source / one-result cards
 *   8. CianchosaintFooter — use at the bottom of every page
 *   9. CianchosaintPrivacyDisclaimer — stand-alone privacy banner
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
 *           jurisdiction="ga"
 *         />
 *         <CianchosaintPrivacyDisclaimer
 *           audience="public-facing"
 *           jurisdiction="ga"
 *         />
 *         <ChatWindow rootAgent="ga_root_agent" jurisdiction="ga" audience="public" />
 *         <CianchosaintFooter build_sha="cianchosaint-ga-public" />
 *       </>
 *     );
 *   }
 *   ```
 *
 * The @cianchosaint/ciafagent-ui-kit dependency is added to
 * ciafagent-ga-public/package.json (workspace:*). The bun workspace
 * resolution picks it up automatically — no further install is needed.
 *
 * Licence: BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md).
 */

// This is a documentation-only file. No runtime export.
export const CIANCHOSAINT_GA_PUBLIC_IC_KIT_INTEGRATION_NOTE = "2026-08-26" as const;
