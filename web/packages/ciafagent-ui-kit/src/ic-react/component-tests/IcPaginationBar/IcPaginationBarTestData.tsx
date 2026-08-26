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
import React, { useState } from "react";
import { IcPaginationBar, IcButton } from "../../components";

export const PaginationBarItemsPerPage = (props) => (
  <IcPaginationBar
    totalItems={100}
    showItemsPerPageControl
    itemsPerPageOptions={[
      { value: "10", label: "10" },
      { value: "20", label: "20" },
    ]}
    {...props}
  />
);

export const PaginationBarItemsPerPageWithButtons = (props) => {
  const [totalItems, setTotalItems] = useState(100);
  const handleSetTotalItems = (value: number) => {
    setTotalItems(value);
  };
  return (
    <>
      <IcPaginationBar
        totalItems={totalItems}
        showItemsPerPageControl
        itemsPerPageOptions={[
          { value: "10", label: "10" },
          { value: "20", label: "20" },
        ]}
        {...props}
      />
      <IcButton className="set-5" onClick={() => handleSetTotalItems(5)}>
        Set to 5
      </IcButton>
      <IcButton className="set-30" onClick={() => handleSetTotalItems(30)}>
        Set to 30
      </IcButton>
    </>
  );
};
