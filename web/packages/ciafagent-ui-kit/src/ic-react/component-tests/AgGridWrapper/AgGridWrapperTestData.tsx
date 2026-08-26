/**
 * CIANCHOSAINT wholesale-copy of mi6/ic-ui-kit.
 *
 * Original: mi6/ic-ui-kit (https://github.com/mi6/ic-ui-kit, MIT + OGL-3.0).
 * Wholesale-copied into cianchosaint: 2026-08-26 per
 * openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md.
 *
 * Upstream licences (preserved):
 *   - MIT (https://github.com/mi6/ic-ui-kit/blob/main/LICENSE)
 *   - Open Government Licence v3.0 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)
 *
 * Cianchosaint licence:
 *   - BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md) — British-Isles-only.
 *   - This file is part of the ciafagent UI kit that wraps the IC Design System
 *     for British-Isles defence / policing / intelligence-oversight analysts.
 *
 * Namespace: cianchosaint (every reference is renamed from the upstream
 * `ukic` / `@ukic` package scope to the `cianchosaint` workspace scope
 * during build via the cianchosaint @ukic/* package aliases).
 */
import React from "react";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css";
import "@ukic/web-components/dist/core/ag-theme-icds.css";
import { IcTheme } from "../../components";

const rowData = [
  { make: "Tesla", model: "Model Y", price: 64950, electric: true },
  { make: "Ford", model: "F-Series", price: 33850, electric: false },
  { make: "Toyota", model: "Corolla", price: 29600, electric: false },
];

const colDefs = [
  {
    headerName: "Car details",
    children: [
      { columnGroupShow: "closed", field: "price" },
      {
        columnGroupShow: "open",
        field: "make",
        filter: true,
        filterParams: {
          filterOptions: ["contains", "startsWith"],
        },
      },
      {
        columnGroupShow: "open",
        field: "model",
        editable: true,
        cellEditor: "agLargeTextCellEditor",
        cellEditorPopup: true,
      },
    ],
  },
  {
    headerName: "Car specs",
    headerTooltip: "Specs of the car",
    children: [{ field: "electric", pinned: "left" }],
  },
];

export const AGGridLight = () => {
  return (
    <>
      <div className="ag-theme-icds" style={{ height: 500 }}>
        <AgGridReact rowData={rowData} columnDefs={colDefs} pagination />
      </div>
    </>
  );
};

export const AGGridDark = () => {
  return (
    <IcTheme theme="dark">
      <div className="ag-theme-icds" style={{ height: 500 }}>
        <AgGridReact rowData={rowData} columnDefs={colDefs} pagination />
      </div>
    </IcTheme>
  );
};
