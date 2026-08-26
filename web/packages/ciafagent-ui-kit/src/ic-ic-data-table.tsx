/**
 * CIANCHOSAINT — ciafagent-ic-data-table integration wrapper.
 *
 * Wraps the upstream IC UI Kit `ic-data-list` + `ic-data-row` Stencil
 * web components as a composable ciafagent "data table" surface. The
 * upstream IC Kit does NOT ship a dedicated `ic-data-table` (the
 * pattern recommends `ic-data-list` + `ic-data-row` for tabular data);
 * the wrapper provides the ciafagent-level API that the 8 web apps
 * depend on.
 *
 * Used by:
 *   - the BIIP intelligence-oversight dashboard (MI5 / MI6 / GCHQ rows)
 *   - the BIPP policing-force dashboard (43 UK forces + 14 GA cohorts + 3 CD)
 *   - the BIDP defence dashboard (32 UK MoD cohorts + 16 IDF cohorts)
 *   - the per-source policy index ("viewing N entries for jurisdiction X")
 *
 * Per the openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md Requirement:
 * The 10 CIANCHOSAINT IC component integration wrappers.
 *
 * The wholesale-copied web components live at
 * web/packages/ciafagent-ui-kit/src/ic-web-components/ic-data-list/ and
 * ic-data-row/ (per the bootstrap-v2 wholesale-copy pattern).
 *
 * Licence:
 *   - Upstream: MIT + OGL-3.0 (mi6/ic-ui-kit, preserved wholesale)
 *   - Wrapper: BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md)
 */

import * as React from "react";

const DATA_LIST_TAG = "ic-data-list" as const;
const DATA_ROW_TAG = "ic-data-row" as const;

export type CianchosaintDataTableDensity = "default" | "compact" | "comfortable";

export interface CianchosaintDataTableColumn<T> {
  /** Stable column key (e.g. "force_id", "trl_level"). */
  key: string;
  /** Human-readable column header. */
  label: string;
  /** Optional column width (CSS value, e.g. "240px" or "20%"). */
  width?: string;
  /** Optional cell-level accessor (for derived values). */
  accessor?: (row: T) => React.ReactNode;
  /** Whether the column is sortable. */
  sortable?: boolean;
}

export interface CianchosaintDataTableProps<T> {
  /** The column definitions. */
  columns: CianchosaintDataTableColumn<T>[];
  /** The row data. */
  rows: T[];
  /** The currently-focused row key (for accessibility). */
  focused_row_key?: string;
  /** The visual density. */
  density?: CianchosaintDataTableDensity;
  /** Whether to show the row count caption. */
  show_caption?: boolean;
  /** Optional row click handler. */
  on_row_click?: (row: T) => void;
  /** Whether the table is in loading state. */
  loading?: boolean;
  /** Accessible label for the table. */
  "aria-label"?: string;
  /** Empty-state message when rows is empty. */
  empty_message?: string;
}

export function CianchosaintDataTable<T extends Record<string, unknown>>({
  columns,
  rows,
  density = "default",
  show_caption = true,
  on_row_click,
  loading = false,
  "aria-label": aria_label = "Data table",
  empty_message = "No data",
  focused_row_key,
}: CianchosaintDataTableProps<T>): React.ReactElement {
  React.useEffect(() => {
    if (
      typeof window !== "undefined" &&
      typeof customElements !== "undefined" &&
      !customElements.get(DATA_LIST_TAG)
    ) {
      import("../ic-web-components/ic-data-list/ic-data-list");
      import("../ic-web-components/ic-data-row/ic-data-row");
    }
  }, []);

  const caption = show_caption
    ? `${rows.length} ${rows.length === 1 ? "entry" : "entries"}`
    : null;

  if (loading) {
    return React.createElement("ic-loading-indicator", {
      "data-cianchosaint-wrapper": "ic-data-table",
      "data-cianchosaint-state": "loading",
      label: "Loading data table...",
    });
  }

  if (rows.length === 0) {
    return React.createElement("ic-empty-state", {
      "data-cianchosaint-wrapper": "ic-data-table",
      "data-cianchosaint-state": "empty",
      "aria-label": aria_label,
      title: "No data",
      body: empty_message,
    });
  }

  const data_list = React.createElement(
    DATA_LIST_TAG,
    {
      "data-cianchosaint-density": density,
      "data-cianchosaint-wrapper": "ic-data-table",
      "aria-label": aria_label,
    },
    columns.flatMap((column) =>
      rows.map((row, row_idx) => {
        const cell_value = column.accessor
          ? column.accessor(row)
          : (row[column.key] as React.ReactNode);
        const row_key = `${column.key}:${row_idx}`;
        const is_focused = focused_row_key === row_key;
        return React.createElement(
          DATA_ROW_TAG,
          {
            key: row_key,
            "data-cianchosaint-column": column.key,
            "data-cianchosaint-row-idx": row_idx,
            "data-cianchosaint-focused": is_focused ? "true" : "false",
            label: column.label,
            value: typeof cell_value === "string" ? cell_value : undefined,
            onClick: on_row_click ? () => on_row_click(row) : undefined,
          },
          typeof cell_value !== "string" && cell_value !== undefined && cell_value !== null
            ? cell_value
            : undefined,
        );
      }),
    ),
  );

  return React.createElement(
    "div",
    {
      "data-cianchosaint-wrapper": "ic-data-table",
      "data-cianchosaint-density": density,
      role: "region",
      "aria-label": aria_label,
    },
    caption
      ? React.createElement(
          "p",
          { className: "cianchosaint-data-table-caption" },
          caption,
        )
      : null,
    data_list,
  );
}

export default CianchosaintDataTable;
