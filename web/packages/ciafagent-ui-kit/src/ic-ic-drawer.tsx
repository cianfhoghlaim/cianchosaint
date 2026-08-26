/**
 * CIANCHOSAINT — ciafagent-ic-drawer integration wrapper.
 *
 * Wraps the upstream IC UI Kit `ic-dialog` Stencil web component as a
 * ciafagent-level "drawer" surface. The upstream IC Kit does not ship a
 * dedicated `ic-drawer`; per its styleguide, `ic-dialog` with a
 * `slide-in-from-<direction>` variant is the canonical drawer pattern.
 * The wrapper provides the ciafagent-level API that the 8 web apps
 * depend on (open + close + slide direction + slot content).
 *
 * Used by:
 *   - the per-source policy drawer (click a row → open the drawer with
 *     the per-source policy context)
 *   - the BAML extraction form drawer (trigger from chat → fill NER
 *     fields without leaving the AG-UI window)
 *   - the milestone-gate status drawer (open the run history)
 *
 * Per the openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md Requirement:
 * The 10 CIANCHOSAINT IC component integration wrappers.
 *
 * The wholesale-copied web component lives at
 * web/packages/ciafagent-ui-kit/src/ic-web-components/ic-dialog/
 * (per the bootstrap-v2 wholesale-copy pattern).
 *
 * Licence:
 *   - Upstream: MIT + OGL-3.0 (mi6/ic-ui-kit, preserved wholesale)
 *   - Wrapper: BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md)
 */

import * as React from "react";

const DIALOG_TAG = "ic-dialog" as const;

export type CianchosaintDrawerDirection = "left" | "right" | "top" | "bottom";

export interface CianchosaintDrawerProps {
  /** Whether the drawer is currently open. */
  open: boolean;
  /** Fired when the analyst closes the drawer (via Esc / backdrop click / close button). */
  on_close: () => void;
  /** The slide direction. */
  direction?: CianchosaintDrawerDirection;
  /** The drawer title (rendered in the slide-in header). */
  title: string;
  /** Optional subtitle / supporting text. */
  subtitle?: string;
  /** The drawer body content. */
  children?: React.ReactNode;
  /** Optional footer content (e.g. action buttons). */
  footer?: React.ReactNode;
  /** The drawer width (CSS value, default "420px"). */
  width?: string;
  /** Whether clicking the backdrop closes the drawer (default true). */
  close_on_backdrop?: boolean;
  /** Stable id for the drawer (used for aria + analytics). */
  drawer_id?: string;
}

const DEFAULT_WIDTH = "420px";
const DEFAULT_DIRECTION: CianchosaintDrawerDirection = "right";

export const CianchosaintDrawer: React.FC<CianchosaintDrawerProps> = ({
  open,
  on_close,
  direction = DEFAULT_DIRECTION,
  title,
  subtitle,
  children,
  footer,
  width = DEFAULT_WIDTH,
  close_on_backdrop = true,
  drawer_id,
}) => {
  React.useEffect(() => {
    if (
      typeof window !== "undefined" &&
      typeof customElements !== "undefined" &&
      !customElements.get(DIALOG_TAG)
    ) {
      import("../ic-web-components/ic-dialog/ic-dialog");
    }
  }, []);

  const handle_close = React.useCallback(() => {
    on_close();
  }, [on_close]);

  return React.createElement(
    DIALOG_TAG,
    {
      "data-cianchosaint-wrapper": "ic-drawer",
      "data-cianchosaint-direction": direction,
      "data-cianchosaint-drawer-id": drawer_id,
      "data-cianchosaint-open": open ? "true" : "false",
      "slide-direction": direction,
      width,
      label: title,
      "supporting-label": subtitle,
      "close-on-backdrop-click": close_on_backdrop ? "true" : "false",
      onIcDialogClose: handle_close,
      role: "dialog",
      "aria-modal": "true",
      "aria-hidden": open ? "false" : "true",
    },
    children,
    footer,
  );
};

export default CianchosaintDrawer;
