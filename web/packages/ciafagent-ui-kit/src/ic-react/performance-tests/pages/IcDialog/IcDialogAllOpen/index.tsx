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
// IcDialogAllOpenPage displays multiple dialogs that are all open on page render for the purpose of performance testing of the IcDialog component.
import React from "react";
import { IcDialog, IcTypography, IcTheme } from "../../../../components";

type PageProps = {
  theme: "light" | "dark";
};

const IcDialogAllOpenPage: React.FC<PageProps> = ({ theme }) => {
  const dialogs = Array.from({ length: 20 }, (_, index) => (
    <IcDialog
      key={index}
      open={true}
      label={`Default dialog ${index + 1}`}
      heading={`This is default dialog ${index + 1}`}
    >
      <IcTypography>
        This is default dialog {index + 1}. It is used to display information to
        the user.
      </IcTypography>
    </IcDialog>
  ));

  return (
    <IcTheme id="theme-wrapper" theme={theme}>
      <IcTypography
        variant="subtitle-small"
        style={{ padding: "var(--ic-space-md)" }}
      >
        <h1>Dialog All Open Page</h1>
      </IcTypography>
      {dialogs}
    </IcTheme>
  );
};

export default IcDialogAllOpenPage;
