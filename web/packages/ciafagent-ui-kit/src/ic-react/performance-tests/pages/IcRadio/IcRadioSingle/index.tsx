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
// IcRadioSinglePage displays a single radio group with multiple options for the purpose of performance testing of the IcRadio component.
import React from "react";
import {
  IcRadioGroup,
  IcRadioOption,
  IcTheme,
  IcTypography,
} from "../../../../components";

type PageProps = {
  theme: "light" | "dark";
};

const IcRadioSinglePage: React.FC<PageProps> = ({ theme }) => {
  const handleRadioGroupChange = (ev: any) => {
    console.log(ev.detail.value);
  };
  const handleRadioOptionCheck = (ev: any) => {
    console.log("Radio option selected: ", ev.detail.value);
  };

  return (
    <IcTheme id="theme-wrapper" theme={theme}>
      <div style={{ padding: "var(--ic-space-md)" }}>
        <IcTypography variant="subtitle-small">
          <h1>Radio Page</h1>
        </IcTypography>
        <IcRadioGroup
          name="radio-group-1"
          label="Add a free purchase with any hot drink"
          helperText="Helper text"
          required
          onIcChange={handleRadioGroupChange}
        >
          <IcRadioOption
            value="crisps"
            label="Crisps"
            onIcCheck={handleRadioOptionCheck}
          />
          <IcRadioOption
            value="cookie"
            label="Deluxe chocolate chip cookie (sold out)"
            disabled
          />
          <IcRadioOption
            value="fruit"
            label="Banana"
            onIcCheck={handleRadioOptionCheck}
          />
          <IcRadioOption
            value="No item"
            label="No thanks, just my coffee"
            selected
            onIcCheck={handleRadioOptionCheck}
          />
        </IcRadioGroup>
      </div>
    </IcTheme>
  );
};

export default IcRadioSinglePage;
