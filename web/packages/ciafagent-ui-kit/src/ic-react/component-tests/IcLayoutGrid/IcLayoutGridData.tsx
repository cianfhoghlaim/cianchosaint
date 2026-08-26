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
import { IcLayoutGrid, IcLayoutGridItem } from "../../components";

export const DefaultLayoutGrid = (props: any) => {
  return (
    <IcLayoutGrid {...props} style={{ border: "1px solid black" }}>
      <div
        style={{ width: "50px", height: "50px", backgroundColor: "lightblue" }}
      >
        Grid item 1
      </div>
      <div
        style={{ width: "50px", height: "50px", backgroundColor: "lightblue" }}
      >
        Grid item 2
      </div>
      <div
        style={{ width: "50px", height: "50px", backgroundColor: "lightblue" }}
      >
        Grid item 3
      </div>
      <div
        style={{ width: "50px", height: "50px", backgroundColor: "lightblue" }}
      >
        Grid item 4
      </div>
    </IcLayoutGrid>
  );
};

export const LayoutGridWithLayoutGridItem = () => {
  return (
    <IcLayoutGrid style={{ border: "1px solid black" }} columns={4}>
      <IcLayoutGridItem colStart={2} colSpan={2} rowSpan={2}>
        <div
          style={{
            width: "50px",
            height: "50px",
            backgroundColor: "lightblue",
          }}
        >
          Grid item 1
        </div>
      </IcLayoutGridItem>
      <IcLayoutGridItem hideInMobileMode>
        <div
          style={{
            width: "50px",
            height: "50px",
            backgroundColor: "lightblue",
          }}
        >
          Grid item 2
        </div>
      </IcLayoutGridItem>
      <div
        style={{ width: "50px", height: "50px", backgroundColor: "lightblue" }}
      >
        Grid item 3
      </div>
      <div
        style={{ width: "50px", height: "50px", backgroundColor: "lightblue" }}
      >
        Grid item 4
      </div>
      <div
        style={{ width: "50px", height: "50px", backgroundColor: "lightblue" }}
      >
        Grid item 5
      </div>
    </IcLayoutGrid>
  );
};
