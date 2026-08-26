/**
 * CIANCHOSAINT — ciafagent-ic-tab-group integration wrapper.
 *
 * Wraps the upstream IC UI Kit `ic-tab-group` + `ic-tab` +
 * `ic-tab-panel` Stencil web components for the 8 ciafagent-* web apps.
 *
 * Used by:
 *   - the SourcePolicyCard tabbed view (overview / BAML / milestone)
 *   - the per-source AG-UI chat window (conversation / form / statute)
 *   - the BIEP intelligence-oversight dashboard (MI5 / MI6 / GCHQ / IPCO / IPT / ISC)
 *
 * Per the openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md Requirement:
 * The 10 CIANCHOSAINT IC component integration wrappers.
 *
 * The wholesale-copied web components live at
 * web/packages/ciafagent-ui-kit/src/ic-web-components/ic-tab-group/,
 * ic-tab/, ic-tab-panel/ (per the bootstrap-v2 wholesale-copy pattern).
 *
 * Licence:
 *   - Upstream: MIT + OGL-3.0 (mi6/ic-ui-kit, preserved wholesale)
 *   - Wrapper: BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md)
 */

import * as React from "react";

const TAB_GROUP_TAG = "ic-tab-group" as const;
const TAB_TAG = "ic-tab" as const;
const TAB_PANEL_TAG = "ic-tab-panel" as const;

export interface CianchosaintTab {
  /** Stable tab id (e.g. "overview", "baml-function"). */
  id: string;
  /** The display label. */
  label: string;
  /** Whether the tab is disabled. */
  disabled?: boolean;
  /** The panel content. */
  panel: React.ReactNode;
  /** Optional badge content (e.g. "TRL 7"). */
  badge?: string;
}

export interface CianchosaintTabGroupProps {
  /** The ordered list of tabs. */
  tabs: CianchosaintTab[];
  /** The currently-active tab id (controlled mode). */
  active_tab_id?: string;
  /** Fired when the analyst selects a different tab. */
  on_tab_change?: (new_tab_id: string, previous_tab_id: string | null) => void;
  /** The visual appearance (default / bordered). */
  appearance?: "default" | "bordered";
  /** Accessible label for the entire tab group. */
  "aria-label"?: string;
}

export const CianchosaintTabGroup: React.FC<CianchosaintTabGroupProps> = ({
  tabs,
  active_tab_id,
  on_tab_change,
  appearance = "default",
  "aria-label": aria_label = "Tab group",
}) => {
  const [internal_active_id, set_internal_active_id] = React.useState<string | null>(
    tabs[0]?.id ?? null,
  );

  React.useEffect(() => {
    if (
      typeof window !== "undefined" &&
      typeof customElements !== "undefined" &&
      !customElements.get(TAB_GROUP_TAG)
    ) {
      import("../ic-web-components/ic-tab-group/ic-tab-group");
      import("../ic-web-components/ic-tab/ic-tab");
      import("../ic-web-components/ic-tab-panel/ic-tab-panel");
    }
  }, []);

  const current_active_id = active_tab_id ?? internal_active_id;

  const handle_tab_select = React.useCallback(
    (new_tab_id: string) => {
      const previous_tab_id = current_active_id;
      set_internal_active_id(new_tab_id);
      on_tab_change?.(new_tab_id, previous_tab_id);
    },
    [current_active_id, on_tab_change],
  );

  const tab_group = React.createElement(
    TAB_GROUP_TAG,
    {
      "data-cianchosaint-wrapper": "ic-tab-group",
      "data-cianchosaint-appearance": appearance,
      "aria-label": aria_label,
    },
    tabs.flatMap((tab) => {
      const tab_el = React.createElement(TAB_TAG, {
        key: `tab:${tab.id}`,
        "data-cianchosaint-tab-id": tab.id,
        tabId: tab.id,
        disabled: tab.disabled ? "true" : "false",
        selected: tab.id === current_active_id ? "true" : "false",
        badge: tab.badge,
        onClick: () => handle_tab_select(tab.id),
      }, tab.label);
      const panel_el = React.createElement(
        TAB_PANEL_TAG,
        {
          key: `panel:${tab.id}`,
          "data-cianchosaint-panel-id": tab.id,
          tabId: tab.id,
          "aria-hidden": tab.id === current_active_id ? "false" : "true",
        },
        tab.panel,
      );
      return tab.id === current_active_id ? [tab_el, panel_el] : [tab_el, panel_el];
    }),
  );

  return tab_group;
};

export default CianchosaintTabGroup;
