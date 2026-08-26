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
// IcPopoverMenuMultiplePage displays multiple popover menus for the purpose of performance testing of the IcPopoverMenu component.
import React, { useState } from "react";
import {
  IcButton,
  IcMenuGroup,
  IcMenuItem,
  IcPopoverMenu,
  IcTheme,
  IcTypography,
} from "../../../../components";

type PageProps = {
  theme: "light" | "dark";
};

const NUM_POPOVERS = 15;

const IcPopoverMenuMultiplePage: React.FC<PageProps> = ({ theme }) => {
  const [popoverOpen, setPopoverOpen] = useState<boolean[]>([
    true,
    ...Array(NUM_POPOVERS - 1).fill(false),
  ]);

  const handlePopoverToggled = (idx: number) => {
    setPopoverOpen((prev) => prev.map((open, i) => (i === idx ? !open : open)));
  };

  const handlePopoverClosed = (idx: number) => {
    setPopoverOpen((prev) => prev.map((open, i) => (i === idx ? false : open)));
  };

  return (
    <IcTheme id="theme-wrapper" theme={theme}>
      <IcTypography
        variant="subtitle-small"
        style={{ padding: "var(--ic-space-md)" }}
      >
        <h1>Popover Menu Multiple Page</h1>
      </IcTypography>
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "1rem",
          margin: "1rem",
          width: "fit-content",
          padding: "10px",
          marginTop: "540px",
        }}
      >
        {Array.from({ length: NUM_POPOVERS }).map((_, idx) => (
          <div key={idx}>
            <IcButton
              title={`Show/hide popover ${idx + 1}`}
              id={`button-${idx}`}
              onClick={() => handlePopoverToggled(idx)}
              aria-expanded={popoverOpen[idx]}
            >
              Show/hide popover {idx + 1}
            </IcButton>
            <IcPopoverMenu
              anchor={`button-${idx}`}
              aria-label={`popover-${idx}`}
              open={popoverOpen[idx]}
              onIcPopoverClosed={(event) => {
                handlePopoverClosed(idx);
                console.log("Popover menu closed: ", event);
              }}
            >
              <IcMenuGroup label="Edit options">
                <IcMenuItem label="Copy" disabled />
                <IcMenuItem label="Paste" keyboardShortcutLabel="Cmd + V" />
              </IcMenuGroup>
              <IcMenuGroup>
                <IcMenuItem label="Format" />
                <IcMenuItem label="Help" />
              </IcMenuGroup>
            </IcPopoverMenu>
          </div>
        ))}
      </div>
    </IcTheme>
  );
};

export default IcPopoverMenuMultiplePage;
