/**
 * CIANCHOSAINT — ciafagent-ic-privacy-disclaimer integration wrapper.
 *
 * Wraps the upstream IC UI Kit privacy disclaimer banner (the standard
 * "OFFICIAL — public-facing content only" disclaimer that the IC Kit
 * ships inside `ic-top-navigation` + `ic-footer`) as a standalone React
 * component for the 8 ciafagent-* web apps.
 *
 * The disclaimer is REQUIRED on every British-Isles defence / policing
 * / intelligence-oversight analyst surface per the OSINT ceiling + the
 * BUSL-1.1 v2 licence posture (see
 * docs/HOW-BRITISH-ISLES-INTELLIGENCE-DEFENCE-POLICING-ENTITIES-USE-CIANCHOSAINT.md
 * §11).
 *
 * Per the openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md Requirement:
 * The 10 CIANCHOSAINT IC component integration wrappers (15 — including
 * the privacy disclaimer).
 *
 * Licence:
 *   - Upstream: MIT + OGL-3.0 (mi6/ic-ui-kit, preserved wholesale)
 *   - Wrapper: BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md)
 */

import * as React from "react";

export type CianchosaintPrivacyAudience =
  | "public-facing"
  | "internal-analyst"
  | "supervisory-body";

export interface CianchosaintPrivacyDisclaimerProps {
  /** Which audience the disclaimer is being shown to. */
  audience: CianchosaintPrivacyAudience;
  /** The per-persona jurisdiction (e.g. "ga", "met", "psni"). */
  jurisdiction: string;
  /** Optional override for the disclaimer body text. */
  body?: string;
  /** Whether the disclaimer is dismissible (defaults to true for public-facing, false for internal). */
  dismissible?: boolean;
  /** Fired when the analyst dismisses the disclaimer. */
  on_dismiss?: () => void;
}

const DEFAULT_BODY_BY_AUDIENCE: Record<CianchosaintPrivacyAudience, string> = {
  "public-facing":
    "This is a non-emergency service. For emergencies, dial 999 or 112. " +
    "Conversations are retained for 30 days for safety and audit purposes. " +
    "OSINT ceiling enforced — public-facing content only.",
  "internal-analyst":
    "Internal analyst surface. All activity is logged for the Security " +
    "Vetting + Audit per the BUSL-1.1 v2 licence posture. " +
    "OSINT ceiling enforced — public-facing content only.",
  "supervisory-body":
    "Supervisory body surface (e.g. CPCAB / IPCO / ISC). " +
    "Activity is logged for IAO review per the warrant-to-enforce clause. " +
    "OSINT ceiling enforced — public-facing content only.",
};

export const CianchosaintPrivacyDisclaimer: React.FC<CianchosaintPrivacyDisclaimerProps> = ({
  audience,
  jurisdiction,
  body,
  dismissible,
  on_dismiss,
}) => {
  const [dismissed, set_dismissed] = React.useState(false);
  const is_dismissible = dismissible ?? audience === "public-facing";

  React.useEffect(() => {
    if (typeof document !== "undefined") {
      import("../ic-web-components/global/icds.css").catch(() => {
        // CSS imports are best-effort — production builds use a bundler.
      });
    }
  }, []);

  const handle_dismiss = React.useCallback(() => {
    set_dismissed(true);
    on_dismiss?.();
  }, [on_dismiss]);

  if (dismissed) {
    return null;
  }

  const final_body = body ?? DEFAULT_BODY_BY_AUDIENCE[audience];

  return React.createElement(
    "div",
    {
      className: "cianchosaint-privacy-disclaimer",
      role: "status",
      "data-cianchosaint-wrapper": "ic-privacy-disclaimer",
      "data-cianchosaint-audience": audience,
      "data-cianchosaint-jurisdiction": jurisdiction,
    },
    React.createElement(
      "span",
      { className: "cianchosaint-privacy-disclaimer__title" },
      "Privacy & OSINT ceiling:",
    ),
    React.createElement(
      "span",
      { className: "cianchosaint-privacy-disclaimer__body" },
      final_body,
    ),
    is_dismissible
      ? React.createElement(
          "button",
          {
            type: "button",
            className: "cianchosaint-privacy-disclaimer__dismiss",
            onClick: handle_dismiss,
          },
          "Dismiss",
        )
      : null,
  );
};

export default CianchosaintPrivacyDisclaimer;
