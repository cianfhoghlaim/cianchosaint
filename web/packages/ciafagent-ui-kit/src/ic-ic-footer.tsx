/**
 * CIANCHOSAINT — ciafagent-ic-footer integration wrapper.
 *
 * Wraps the upstream IC UI Kit `ic-footer` Stencil web component for
 * the 8 ciafagent-* web apps. The footer is the standard GOV.UK-style
 * classified-information footer that includes:
 *   - the BUSL-1.1 v2 licence posture
 *   - the OSINT ceiling reminder
 *   - the licence-enforcement contact for foreign-use requests
 *   - the 3-step foreign-use gate link
 *   - the standard MI6 / GCHQ "© Crown Copyright" attribution
 *
 * Per the openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md Requirement:
 * The 10 CIANCHOSAINT IC component integration wrappers.
 *
 * The wholesale-copied web component lives at
 * web/packages/ciafagent-ui-kit/src/ic-web-components/ic-footer/
 * (per the bootstrap-v2 wholesale-copy pattern).
 *
 * Licence:
 *   - Upstream: MIT + OGL-3.0 (mi6/ic-ui-kit, preserved wholesale)
 *   - Wrapper: BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md)
 */

import * as React from "react";

const FOOTER_TAG = "ic-footer" as const;

const LICENCE_POSTURE = "BUSL-1.1 v2 (British-Isles-only)" as const;
const OSINT_CEILING_REMINDER = "OSINT ceiling: public-facing content only" as const;
const CROWN_COPYRIGHT = "© Crown Copyright 2026" as const;

export interface CianchosaintFooterProps {
  /** The classification banner caption (defaults to the standard). */
  classification_caption?: string;
  /** The deployed build SHA (shown in the footer for traceability). */
  build_sha?: string;
  /** Whether to show the "Warrant to enforce" link (defaults to true). */
  show_warrant_to_enforce?: boolean;
  /** Whether to show the "Privacy" link (defaults to true). */
  show_privacy?: boolean;
  /** Whether to show the "British-Isles-only" chip (defaults to true). */
  show_british_isles_only_chip?: boolean;
  /** Optional per-persona override for the "Contact" link. */
  contact_href?: string;
}

const DEFAULT_CLASSIFICATION_CAPTION = "OFFICIAL — public-facing content only";

export const CianchosaintFooter: React.FC<CianchosaintFooterProps> = ({
  classification_caption = DEFAULT_CLASSIFICATION_CAPTION,
  build_sha,
  show_warrant_to_enforce = true,
  show_privacy = true,
  show_british_isles_only_chip = true,
  contact_href = "https://cianchosaint.ie/contact",
}) => {
  React.useEffect(() => {
    if (
      typeof window !== "undefined" &&
      typeof customElements !== "undefined" &&
      !customElements.get(FOOTER_TAG)
    ) {
      import("../ic-web-components/ic-footer/ic-footer");
    }
  }, []);

  const licence_chip = show_british_isles_only_chip
    ? React.createElement(
        "ic-chip",
        {
          "data-cianchosaint-chip": "licence",
          label: LICENCE_POSTURE,
        },
      )
    : null;

  return React.createElement(
    FOOTER_TAG,
    {
      "data-cianchosaint-wrapper": "ic-footer",
      "data-cianchosaint-classification": classification_caption,
      "data-cianchosaint-build-sha": build_sha,
      classification: classification_caption,
    },
    React.createElement(
      "ic-footer-link-group",
      { slot: "links", "data-cianchosaint-slot": "links" },
      React.createElement(
        "ic-footer-link",
        { href: "/", "data-cianchosaint-link": "home" },
        "Home",
      ),
      React.createElement(
        "ic-footer-link",
        { href: "/privacy", "data-cianchosaint-link": "privacy" },
        show_privacy ? "Privacy" : "",
      ),
      show_warrant_to_enforce
        ? React.createElement(
            "ic-footer-link",
            { href: "/warrant-to-enforce", "data-cianchosaint-link": "warrant" },
            "Warrant to enforce",
          )
        : null,
      React.createElement(
        "ic-footer-link",
        { href: contact_href, "data-cianchosaint-link": "contact" },
        "Contact",
      ),
    ),
    React.createElement(
      "div",
      { slot: "caption", "data-cianchosaint-slot": "caption" },
      OSINT_CEILING_REMINDER,
      " · ",
      CROWN_COPYRIGHT,
      build_sha ? ` · build ${build_sha.slice(0, 7)}` : "",
    ),
    licence_chip,
  );
};

export default CianchosaintFooter;
