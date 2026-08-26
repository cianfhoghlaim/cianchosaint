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
// IcDialogSinglePage displays a single dialog for the purpose of performance testing of the IcDialog component.
import React, { useState } from "react";
import {
  IcButton,
  IcDialog,
  IcTypography,
  IcTheme,
} from "../../../../components";

type PageProps = {
  theme: "light" | "dark";
};

const IcDialogSinglePage: React.FC<PageProps> = ({ theme }) => {
  const [openDialog, setOpenDialog] = useState<boolean>(true);
  const handleDialogOpen = () => {
    console.log("Dialog opened");
    setOpenDialog(true);
  };
  const handleDialogClose = () => {
    console.log("Dialog closed");
    setOpenDialog(false);
  };
  const handleDialogConfirmed = () => {
    console.log("Dialog confirmed");
    setOpenDialog(false);
  };

  return (
    <IcTheme id="theme-wrapper" theme={theme}>
      <div style={{ padding: "var(--ic-space-md)" }}>
        <IcTypography variant="subtitle-small">
          <h1>Dialog Page</h1>
        </IcTypography>
        <IcButton variant="primary" onClick={handleDialogOpen}>
          Launch auto opening dialog
        </IcButton>
        <IcDialog
          id="auto-opening-dialog"
          heading="This dialog opens automatically using the open prop"
          label="Auto opening dialog"
          open={openDialog}
          onIcDialogClosed={handleDialogClose}
          onIcDialogConfirmed={handleDialogConfirmed}
        >
          <IcTypography>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua.
          </IcTypography>
        </IcDialog>
      </div>
    </IcTheme>
  );
};

export default IcDialogSinglePage;
