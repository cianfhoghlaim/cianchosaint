/**
 * CIANCHOSAINT — ciafagent-ic-classification-banner integration wrapper.
 *
 * Wraps the upstream IC UI Kit `ic-classification-banner` Stencil web
 * component for the 8 ciafagent-* web apps. The classification banner is
 * REQUIRED on every British-Isles defence / policing /
 * intelligence-oversight analyst surface per the OSINT ceiling + the
 * BUSL-1.1 v2 licence posture (every analyst session starts at
 * "OFFICIAL" by default; analysts must explicitly escalate the banner
 * before viewing any document classified RESTRICTED or above).
 *
 * Per the openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md Requirement:
 * The 10 CIANCHOSAINT IC component integration wrappers.
 *
 * The wholesale-copied web component lives at
 * web/packages/ciafagent-ui-kit/src/ic-web-components/ic-classification-banner/
 * (per the bootstrap-v2 wholesale-copy pattern). This wrapper is a thin
 * React façade that:
 *   1. Loads the upstream Stencil element lazily (avoids SSR drift).
 *   2. Pins the default classification to "OFFICIAL" (the cianchosaint
 *      OSINT ceiling default; analysts must opt-in to a higher
 *      classification per the warrant-to-enforce clause).
 *   3. Adds the cianchosaint jurisdiction-badge slot for the 8
 *      per-persona surfaces (ga / met / psni / etc.).
 *   4. Forwards all upstream events to the parent AG-UI chat window.
 *
 * Licence:
 *   - Upstream: MIT + OGL-3.0 (mi6/ic-ui-kit, preserved wholesale)
 *   - Wrapper: BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md)
 */

import * as React from "react";

const CLASSIFICATION_BANNER_TAG = "ic-classification-banner" as const;

export type CianchosaintClassificationLevel =
  | "official"
  | "official-sensitive"
  | "restricted"
  | "secret"
  | "top-secret";

export type CianchosaintJurisdiction =
  | "ga"
  | "met"
  | "psni"
  | "uk-mod"
  | "raf"
  | "rn"
  | "army"
  | "mi5"
  | "mi6"
  | "gchq"
  | "cjini"
  | "nca"
  | "home-office"
  | "moj";

export interface CianchosaintClassificationBannerProps
  extends Omit<React.HTMLAttributes<HTMLElement>, "children"> {
  /** British-Isles classification level. Defaults to "official". */
  classification?: CianchosaintClassificationLevel;
  /** Whether to show the cianchosaint jurisdiction badge in the banner. */
  show_jurisdiction_badge?: boolean;
  /** Jurisdiction tag (e.g. "ga", "met") — shown when show_jurisdiction_badge=true. */
  jurisdiction?: CianchosaintJurisdiction;
  /** Optional override for the banner caption (default: "OSINT ceiling: public-facing content only"). */
  caption?: string;
  /** Optional aria-label override (defaults to a stable, screen-reader-friendly label). */
  "aria-label"?: string;
}

const DEFAULT_CLASSIFICATION: CianchosaintClassificationLevel = "official";
const DEFAULT_CAPTION = "OSINT ceiling: public-facing content only";

/**
 * CianchosaintClassificationBanner — the React integration wrapper.
 *
 * Renders the upstream `ic-classification-banner` Stencil web component
 * (wholesale-copied at web/packages/ciafagent-ui-kit/src/ic-web-components/ic-classification-banner/ic-classification-banner.tsx)
 * with cianchosaint-specific defaults + the optional jurisdiction badge.
 */
export const CianchosaintClassificationBanner = React.forwardRef<
  HTMLElement,
  CianchosaintClassificationBannerProps
>(function CianchosaintClassificationBanner(
  {
    classification = DEFAULT_CLASSIFICATION,
    show_jurisdiction_badge = false,
    jurisdiction,
    caption = DEFAULT_CAPTION,
    ...rest
  },
  ref,
) {
  React.useEffect(() => {
    if (
      typeof window !== "undefined" &&
      typeof customElements !== "undefined" &&
      !customElements.get(CLASSIFICATION_BANNER_TAG)
    ) {
      import("../ic-web-components/ic-classification-banner/ic-classification-banner");
    }
  }, []);

  const props: Record<string, unknown> = {
    ...rest,
    ref: ref as unknown as React.Ref<HTMLDivElement>,
    "data-cianchosaint-wrapper": "ic-classification-banner",
    "data-cianchosaint-classification": classification,
    "data-cianchosaint-show-jurisdiction-badge": show_jurisdiction_badge,
    "data-cianchosaint-caption": caption,
  };

  if (show_jurisdiction_badge && jurisdiction) {
    props["data-cianchosaint-jurisdiction"] = jurisdiction;
  }

  return React.createElement(CLASSIFICATION_BANNER_TAG, props);
});

export default CianchosaintClassificationBanner;
