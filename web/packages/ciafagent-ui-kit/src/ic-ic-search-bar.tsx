/**
 * CIANCHOSAINT — ciafagent-ic-search-bar integration wrapper.
 *
 * Wraps the upstream IC UI Kit `ic-search-bar` Stencil web component for
 * the 8 ciafagent-* web apps. The search bar is the entry point for the
 * AG-UI chat window + the per-source policy index; queries go through
 * the 4-tier provider chain (Unsloth Studio → LiteLLM → MiniMax → Gemini).
 *
 * Per the openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md Requirement:
 * The 10 CIANCHOSAINT IC component integration wrappers.
 *
 * The wholesale-copied web component lives at
 * web/packages/ciafagent-ui-kit/src/ic-web-components/ic-search-bar/
 * (per the bootstrap-v2 wholesale-copy pattern).
 *
 * Licence:
 *   - Upstream: MIT + OGL-3.0 (mi6/ic-ui-kit, preserved wholesale)
 *   - Wrapper: BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md)
 */

import * as React from "react";

const SEARCH_BAR_TAG = "ic-search-bar" as const;

export type CianchosaintSearchScope =
  | "ag-ui-chat"
  | "osint-allowlist"
  | "per-source-policy-index"
  | "uk-statute-book"
  | "ireland-statute-book"
  | "cases-and-tribunals"
  | "political-party-pipeline";

export interface CianchosaintSearchBarProps {
  /** The search scope — narrows the dataset the search bar queries. */
  scope: CianchosaintSearchScope;
  /** The placeholder text (e.g. "Search the OSINT allowlist..."). */
  placeholder?: string;
  /** The minimum query length (default 3). */
  min_query_length?: number;
  /** Debounce time in milliseconds (default 250). */
  debounce_ms?: number;
  /** The currently-active query. */
  value?: string;
  /** Fired when the analyst submits a query. */
  on_submit?: (query: string, scope: CianchosaintSearchScope) => void;
  /** Fired when the analyst clears the search bar. */
  on_clear?: () => void;
  /** Disabled state. */
  disabled?: boolean;
}

export const CianchosaintSearchBar: React.FC<CianchosaintSearchBarProps> = ({
  scope,
  placeholder = "Search...",
  min_query_length = 3,
  debounce_ms = 250,
  value,
  on_submit,
  on_clear,
  disabled = false,
}) => {
  React.useEffect(() => {
    if (
      typeof window !== "undefined" &&
      typeof customElements !== "undefined" &&
      !customElements.get(SEARCH_BAR_TAG)
    ) {
      import("../ic-web-components/ic-search-bar/ic-search-bar");
    }
  }, []);

  const handle_submit = React.useCallback(
    (event: Event) => {
      const target = event.target as HTMLElement & { value?: string };
      if (typeof target.value === "string" && on_submit) {
        on_submit(target.value, scope);
      }
    },
    [on_submit, scope],
  );

  const handle_clear = React.useCallback(() => {
    on_clear?.();
  }, [on_clear]);

  return React.createElement(SEARCH_BAR_TAG, {
    "data-cianchosaint-wrapper": "ic-search-bar",
    "data-cianchosaint-scope": scope,
    "placeholder": placeholder,
    "min-query-length": min_query_length,
    "debounce-ms": debounce_ms,
    "value": value,
    "disabled": disabled ? "true" : "false",
    onIcSubmit: handle_submit,
    onIcClear: handle_clear,
  });
};

export default CianchosaintSearchBar;
