/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// Internal apps do NOT render the public-facing PrivacyDisclaimer.
// They render an InternalAccessNotice instead.

import * as React from "react";

export function PrivacyDisclaimer(_props: { jurisdiction: "ga" | "met" | "psni" }) {
  // Internal app — no public disclaimer needed.
  // The InternalAccessNotice is rendered separately in the main layout.
  return null;
}
