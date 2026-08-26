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
// IcSearchBarVariantsPage displays various configurations of the IcSearchBar component for performance testing purposes.
import React from "react";
import { IcSearchBar, IcTheme, IcTypography } from "../../../../components";

type PageProps = {
  theme: "light" | "dark";
};

const options = [
  { label: "Espresso", value: "espresso" },
  { label: "Double Espresso", value: "doubleespresso" },
  { label: "Flat White", value: "flatwhite" },
  { label: "Cappuccino", value: "cappuccino" },
  { label: "Americano", value: "americano" },
  { label: "Mocha", value: "mocha" },
];

const defaultSearchBarProps = {
  label: "What is your favourite coffee?",
  helperText: "Search for your favourite coffee",
  emptyOptionListText: "There's nothing here",
  options: options,
};

const defaultSearchBarEvents = {
  onIcChange: (ev: any) => console.log("Value changed: ", ev.detail.value),
  onIcClear: () => console.log("Value cleared"),
  onIcInput: (ev: any) => console.log("icInput: ", ev.detail.value),
  onIcOptionSelect: (ev: any) =>
    console.log("Option selected: ", ev.detail.value),
  onIcSearchBarBlur: () => console.log("Search bar blurred"),
  onIcSearchBarFocus: () => console.log("Search bar focused"),
  onIcSubmitSearch: () => console.log("Search submitted"),
  onIcMenuChange: (ev: any) => console.log("Menu opened/closed: ", ev.detail),
};

const IcSearchBarVariantsPage: React.FC<PageProps> = ({ theme }) => {
  return (
    <IcTheme id="theme-wrapper" theme={theme}>
      <IcTypography
        variant="subtitle-small"
        style={{ padding: "var(--ic-space-md)" }}
      >
        <h1>Search Bar Variants Page</h1>
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
        <IcSearchBar
          {...defaultSearchBarProps}
          charactersUntilSuggestion={3}
          assistiveHintText="You can use up and down arrows to navigate the options when they are available, and press enter to select an option."
          required
          {...defaultSearchBarEvents}
        />
        <IcSearchBar
          {...defaultSearchBarProps}
          placeholder="Small search bar"
          size="small"
          {...defaultSearchBarEvents}
        />
        <IcSearchBar
          {...defaultSearchBarProps}
          fullWidth
          {...defaultSearchBarEvents}
        />
        <IcSearchBar {...defaultSearchBarProps} disabled />
        <IcSearchBar {...defaultSearchBarProps} readonly={true} />
        <IcSearchBar
          {...defaultSearchBarProps}
          disableAutoFiltering={true}
          {...defaultSearchBarEvents}
        />
        <IcSearchBar
          {...defaultSearchBarProps}
          focusOnLoad={true}
          {...defaultSearchBarEvents}
        />
        <IcSearchBar
          {...defaultSearchBarProps}
          searchMode="query"
          {...defaultSearchBarEvents}
        />
      </div>
    </IcTheme>
  );
};

export default IcSearchBarVariantsPage;
