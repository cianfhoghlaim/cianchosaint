/**
 * CIANCHOSAINT — @cianchosaint/ciafagent-ui-kit
 *
 * The single canonical entry point for the 8 ciafagent-* web apps
 * (ciafagent-ga-public, ciafagent-ga-internal, ciafagent-met-public,
 * ciafagent-met-internal, ciafagent-psni-public, ciafagent-psni-internal,
 * ciafagent-api, ciafagent-self-host). Wholesale-copied from
 * mi6/ic-ui-kit (MIT + OGL-3.0) per the
 * openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md.
 *
 * The 9 CIANCHOSAINT IC component integration wrappers (the "façade"):
 *   1. CianchosaintClassificationBanner — the OFFICIAL-by-default banner
 *   2. CianchosaintTopNavigation — the global nav surface
 *   3. CianchosaintSearchBar — the AG-UI chat search entry point
 *   4. CianchosaintDataTable — wraps ic-data-list + ic-data-row
 *   5. CianchosaintTabGroup — wraps ic-tab-group + ic-tab + ic-tab-panel
 *   6. CianchosaintDrawer — wraps ic-dialog as a slide-in drawer
 *   7. CianchosaintCardVertical — the canonical card surface
 *   8. CianchosaintFooter — the GOV.UK-style classified footer
 *   9. CianchosaintPrivacyDisclaimer — the standalone disclaimer banner
 *
 * Plus the wholesale-copied upstream Stencil web components under
 * `ic-web-components/` (322 .ts/.tsx files, 70 component directories).
 *
 * Licence:
 *   - Upstream (preserved wholesale): MIT + OGL-3.0
 *   - Wrapper: BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md)
 */

export {
  CianchosaintClassificationBanner,
  type CianchosaintClassificationBannerProps,
  type CianchosaintClassificationLevel,
  type CianchosaintJurisdiction,
} from "./ic-ic-classification-banner";

export {
  CianchosaintTopNavigation,
  type CianchosaintTopNavigationProps,
} from "./ic-ic-top-navigation";

export {
  CianchosaintSearchBar,
  type CianchosaintSearchBarProps,
  type CianchosaintSearchScope,
} from "./ic-ic-search-bar";

export {
  CianchosaintDataTable,
  type CianchosaintDataTableProps,
  type CianchosaintDataTableColumn,
  type CianchosaintDataTableDensity,
} from "./ic-ic-data-table";

export {
  CianchosaintTabGroup,
  type CianchosaintTabGroupProps,
  type CianchosaintTab,
} from "./ic-ic-tab-group";

export {
  CianchosaintDrawer,
  type CianchosaintDrawerProps,
  type CianchosaintDrawerDirection,
} from "./ic-ic-drawer";

export {
  CianchosaintCardVertical,
  type CianchosaintCardVerticalProps,
  type CianchosaintCardVariant,
} from "./ic-ic-card-vertical";

export {
  CianchosaintFooter,
  type CianchosaintFooterProps,
} from "./ic-ic-footer";

export {
  CianchosaintPrivacyDisclaimer,
  type CianchosaintPrivacyDisclaimerProps,
  type CianchosaintPrivacyAudience,
} from "./ic-privacy-disclaimer";

/**
 * Re-export the wholesale-copied React component library from the upstream
 * @ukic/react package via the `ic-react` directory. These are the
 * auto-generated React proxies for the 70 Stencil web components.
 */
export * as IcReact from "./ic-react/components";
