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
// IcCheckboxSinglePage displays a single checkbox group for the purpose of performance testing of the IcCheckbox component.
import React from "react";
import {
  IcCheckbox,
  IcCheckboxGroup,
  IcTextField,
  IcTheme,
  IcTypography,
} from "../../../../components";

type PageProps = {
  theme: "light" | "dark";
};

const IcCheckboxSinglePage: React.FC<PageProps> = ({ theme }) => {
  const handleCheckboxGroupChange = (ev: any) => {
    console.log("onIcChange", ev.detail.value);
  };

  const handleCheckboxCheck = (ev: any) => {
    console.log("onIcCheck", ev);
  };

  return (
    <IcTheme id="theme-wrapper" theme={theme}>
      <div style={{ padding: "var(--ic-space-md)" }}>
        <IcTypography variant="subtitle-small">
          <h1>Checkbox Page</h1>
        </IcTypography>
        <IcCheckboxGroup
          label="Select your extras"
          name="default"
          onIcChange={handleCheckboxGroupChange}
        >
          <IcCheckbox
            value="extra"
            label="Extra shot (50p)"
            onIcCheck={handleCheckboxCheck}
          />
          <IcCheckbox value="Soya milk" label="Soya milk" checked />
          <IcCheckbox value="keep cup" label="Takeaway cup" disabled />
          <IcCheckbox value="other" label="Other">
            <IcTextField
              slot="additional-field"
              label="Please let us know..."
            />
          </IcCheckbox>
          <IcCheckbox
            additionalFieldDisplay="dynamic"
            value="other"
            label="Other"
          >
            <IcTextField
              slot="additional-field"
              label="Please let us know..."
            />
          </IcCheckbox>
        </IcCheckboxGroup>
      </div>
    </IcTheme>
  );
};

export default IcCheckboxSinglePage;
