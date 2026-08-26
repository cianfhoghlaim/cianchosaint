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
// IcRadioMultiplePage displays multiple radio groups for the purpose of performance testing of the IcRadio component.
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

const handleRadioGroupChange = (index: number) => (ev: any) => {
  console.log(`Group ${index}:`, ev.detail.value);
};
const handleRadioOptionCheck = (index: number) => (ev: any) => {
  console.log(`Group ${index}: Radio option selected: `, ev.detail.value);
};

const RadioGroup = ({ index }: { index: number }) => (
  <IcRadioGroup
    name={`radio-group-${index}`}
    label={`Add a free purchase with any hot drink (Group ${index})`}
    helperText={`Helper text for group ${index}`}
    required
    onIcChange={handleRadioGroupChange(index)}
  >
    <IcRadioOption
      value="crisps"
      label={`Crisps (Group ${index})`}
      onIcCheck={handleRadioOptionCheck(index)}
    />
    <IcRadioOption
      value="cookie"
      label={`Deluxe chocolate chip cookie (Group ${index})`}
      onIcCheck={handleRadioOptionCheck(index)}
    />
    <IcRadioOption
      value="fruit"
      label={`Banana (Group ${index})`}
      onIcCheck={handleRadioOptionCheck(index)}
    />
    <IcRadioOption
      value="No item"
      label={`No thanks, just my coffee (Group ${index})`}
      selected
      onIcCheck={handleRadioOptionCheck(index)}
    />
  </IcRadioGroup>
);

const IcRadioMultiplePage: React.FC<PageProps> = ({ theme }) => (
  <IcTheme id="theme-wrapper" theme={theme}>
    <IcTypography
      variant="subtitle-small"
      style={{ padding: "var(--ic-space-md)" }}
    >
      <h1>Radio Multiple Page</h1>
    </IcTypography>
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        gap: "1rem",
        margin: "1rem",
        width: "fit-content",
        padding: "10px",
      }}
    >
      {Array.from({ length: 20 }, (_, i) => (
        <RadioGroup key={i} index={i + 1} />
      ))}
    </div>
  </IcTheme>
);

export default IcRadioMultiplePage;
