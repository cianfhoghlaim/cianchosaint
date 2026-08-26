/**
 * CIANCHOSAINT — ciafagent-ic-card-vertical integration wrapper.
 *
 * Wraps the upstream IC UI Kit `ic-card-vertical` Stencil web component
 * for the 8 ciafagent-* web apps. The vertical card is the canonical
 * "one source / one result row" surface used by:
 *   - the SourcePolicyCard gallery view
 *   - the BIEP / BIPP / BIDP source catalogue
 *   - the AG-UI chat window's per-source search results
 *   - the cianchosaint.com home page (24 political parties + 5 intel agencies)
 *
 * Per the openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md Requirement:
 * The 10 CIANCHOSAINT IC component integration wrappers.
 *
 * The wholesale-copied web component lives at
 * web/packages/ciafagent-ui-kit/src/ic-web-components/ic-card-vertical/
 * (per the bootstrap-v2 wholesale-copy pattern).
 *
 * Licence:
 *   - Upstream: MIT + OGL-3.0 (mi6/ic-ui-kit, preserved wholesale)
 *   - Wrapper: BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md)
 */

import * as React from "react";

const CARD_VERTICAL_TAG = "ic-card-vertical" as const;

export type CianchosaintCardVariant =
  | "default"
  | "osint-ceiling-banner"
  | "milestone-gate-badge"
  | "baml-function-preview"
  | "jurisdiction-badge";

export interface CianchosaintCardVerticalProps {
  /** The card heading (e.g. the body name: "An Garda Síochána"). */
  heading: string;
  /** Optional supporting text (e.g. "14 cohorts · OSINT ceiling enforced"). */
  subheading?: string;
  /** Optional ISO jurisdiction code (e.g. "IE", "GB-ENG") — shown as a chip. */
  jurisdiction_code?: string;
  /** Optional icon name (per the IC Kit's icon set). */
  icon?: string;
  /** The card body content (typically a list of action buttons). */
  children?: React.ReactNode;
  /** Optional badge text (e.g. "TRL 7" or "BIPP v1 m1"). */
  badge?: string;
  /** Whether the card displays the OSINT ceiling banner. */
  show_osint_banner?: boolean;
  /** Visual variant (changes the accent colour + the chip positions). */
  variant?: CianchosaintCardVariant;
  /** The card URL (if the card is a link). */
  href?: string;
  /** Fired when the analyst clicks the card. */
  on_click?: () => void;
  /** Whether the card is currently loading (shows a skeleton). */
  loading?: boolean;
  /** Stable id for the card (used for analytics + data-testid). */
  card_id?: string;
}

export const CianchosaintCardVertical: React.FC<CianchosaintCardVerticalProps> = ({
  heading,
  subheading,
  jurisdiction_code,
  icon,
  children,
  badge,
  show_osint_banner = false,
  variant = "default",
  href,
  on_click,
  loading = false,
  card_id,
}) => {
  React.useEffect(() => {
    if (
      typeof window !== "undefined" &&
      typeof customElements !== "undefined" &&
      !customElements.get(CARD_VERTICAL_TAG)
    ) {
      import("../ic-web-components/ic-card-vertical/ic-card-vertical");
    }
  }, []);

  if (loading) {
    return React.createElement("ic-skeleton", {
      "data-cianchosaint-wrapper": "ic-card-vertical",
      "data-cianchosaint-card-id": card_id,
      "data-cianchosaint-state": "loading",
    });
  }

  return React.createElement(
    CARD_VERTICAL_TAG,
    {
      "data-cianchosaint-wrapper": "ic-card-vertical",
      "data-cianchosaint-variant": variant,
      "data-cianchosaint-card-id": card_id,
      "data-cianchosaint-show-osint-banner": show_osint_banner ? "true" : "false",
      "data-cianchosaint-jurisdiction": jurisdiction_code,
      heading,
      subheading,
      icon,
      badge,
      href,
      "on-click": on_click ? () => on_click() : undefined,
    },
    children,
  );
};

export default CianchosaintCardVertical;
