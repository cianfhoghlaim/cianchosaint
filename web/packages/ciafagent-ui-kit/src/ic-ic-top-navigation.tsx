/**
 * CIANCHOSAINT — ciafagent-ic-top-navigation integration wrapper.
 *
 * Wraps the upstream IC UI Kit `ic-top-navigation` Stencil web component
 * for the 8 ciafagent-* web apps. The top navigation is the GLOBAL nav
 * surface that hosts the per-persona menu (An Garda Síochána, MET, PSNI,
 * UK MoD, RAF, RN, Army, MI5, MI6, GCHQ), the search bar, and the
 * session badge.
 *
 * Per the openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md Requirement:
 * The 10 CIANCHOSAINT IC component integration wrappers.
 *
 * The wholesale-copied web component lives at
 * web/packages/ciafagent-ui-kit/src/ic-web-components/ic-top-navigation/
 * (per the bootstrap-v2 wholesale-copy pattern).
 *
 * Licence:
 *   - Upstream: MIT + OGL-3.0 (mi6/ic-ui-kit, preserved wholesale)
 *   - Wrapper: BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md)
 */

import * as React from "react";

const TOP_NAVIGATION_TAG = "ic-top-navigation" as const;

export interface CianchosaintTopNavigationProps {
  /** The app label (e.g. "An Garda Síochána", "Metropolitan Police", "PSNI"). */
  app_label: string;
  /** The per-persona route prefix (e.g. "ga-public", "met-internal"). */
  app_route_prefix: string;
  /** ISO 3166-2 jurisdiction code (e.g. "IE", "GB-ENG", "GB-NIR"). */
  jurisdiction_code: string;
  /** Whether to display the search bar in the top navigation. */
  show_search?: boolean;
  /** Whether to display the session badge in the top navigation. */
  show_session_badge?: boolean;
  /** Optional slot overrides for the cianchosaint navigation slots. */
  status_slot?: React.ReactNode;
  /** Optional short status string shown next to the app label. */
  status_text?: string;
  /** Optional icon name for the cianchosaint app (e.g. "shield", "scales"). */
  app_icon?: string;
}

export const CianchosaintTopNavigation: React.FC<CianchosaintTopNavigationProps> = ({
  app_label,
  app_route_prefix,
  jurisdiction_code,
  show_search = true,
  show_session_badge = true,
  status_slot,
  status_text,
  app_icon,
}) => {
  React.useEffect(() => {
    if (
      typeof window !== "undefined" &&
      typeof customElements !== "undefined" &&
      !customElements.get(TOP_NAVIGATION_TAG)
    ) {
      import("../ic-web-components/ic-top-navigation/ic-top-navigation");
    }
  }, []);

  return React.createElement(TOP_NAVIGATION_TAG, {
    "app-label": app_label,
    "app-route-prefix": app_route_prefix,
    "jurisdiction-code": jurisdiction_code,
    "show-search": show_search ? "true" : "false",
    "show-session-badge": show_session_badge ? "true" : "false",
    "status-text": status_text,
    "app-icon": app_icon,
    "data-cianchosaint-wrapper": "ic-top-navigation",
  }, status_slot);
};

export default CianchosaintTopNavigation;
