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
// IcCheckboxBasicMultiplePage displays multiple basic checkbox groups for the purpose of performance testing of the IcCheckbox component.
import React from "react";
import {
  IcCheckbox,
  IcCheckboxGroup,
  IcTheme,
  IcTypography,
} from "../../../../components";

type PageProps = {
  theme: "light" | "dark";
};

const COLOURS = [
  { value: "black", label: "Black" },
  { value: "grey", label: "Grey" },
  { value: "blue", label: "Blue" },
  { value: "navy", label: "Navy" },
  { value: "purple", label: "Purple" },
  { value: "pink", label: "Pink" },
  { value: "orange", label: "Orange" },
  { value: "red", label: "Red" },
  { value: "green", label: "Green" },
  { value: "yellow", label: "Yellow" },
  { value: "cream", label: "Cream" },
  { value: "white", label: "White" },
  { value: "brown", label: "Brown" },
  { value: "silver", label: "Silver" },
  { value: "gold", label: "Gold" },
  { value: "multi", label: "Multi" },
];

const handleCheckboxGroupChange = (ev: any) => {
  console.log("onIcChange", ev.detail.value);
};
const handleCheckboxCheck = (ev: any) => {
  console.log("onIcCheck", ev);
};

const Checkbox = () => (
  <IcCheckboxGroup
    label="Select a colour or colours"
    name="default"
    onIcChange={handleCheckboxGroupChange}
  >
    {COLOURS.map((colour) => (
      <IcCheckbox
        key={colour.value}
        value={colour.value}
        label={colour.label}
        onIcCheck={handleCheckboxCheck}
      />
    ))}
  </IcCheckboxGroup>
);

const IcCheckboxBasicMultiplePage: React.FC<PageProps> = ({ theme }) => {
  const checkboxes = Array.from({ length: 10 }, (_, index) => (
    <Checkbox key={index} />
  ));

  return (
    <IcTheme id="theme-wrapper" theme={theme}>
      <IcTypography
        variant="subtitle-small"
        style={{ padding: "var(--ic-space-md)" }}
      >
        <h1>Checkbox Basic Multiple Page</h1>
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
        {checkboxes}
      </div>
    </IcTheme>
  );
};

export default IcCheckboxBasicMultiplePage;
