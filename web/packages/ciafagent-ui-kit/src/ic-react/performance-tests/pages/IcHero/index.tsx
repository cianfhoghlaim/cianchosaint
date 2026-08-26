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
// IcHeroPage displays a hero for the purpose of performance testing of the IcHero component.
import React from "react";
import {
  IcHero,
  IcButton,
  IcTextField,
  IcLink,
  IcCardVertical,
  IcSearchBar,
  IcTheme,
  IcTypography,
} from "../../../components";

type PageProps = {
  theme: "light" | "dark";
};

const IcHeroPage: React.FC<PageProps> = ({ theme }) => {
  return (
    <IcTheme id="theme-wrapper" theme={theme}>
      <IcTypography
        variant="subtitle-small"
        style={{ padding: "var(--ic-space-md)" }}
      >
        <h1>Hero Page</h1>
      </IcTypography>
      <IcHero
        heading="Hero heading"
        subheading="Hero description. This is a Hero component, it should be used as a page heading."
        secondaryHeading="Secondary Heading"
        secondarySubheading="This is a secondary description."
        aligned="center"
      >
        <div slot="interaction" style={{ display: "flex" }}>
          <IcTextField
            placeholder="Filter display"
            label="Filter display"
            hide-label
          />
          <IcButton
            variant="primary"
            style={{ marginLeft: "var(--ic-space-md)" }}
          >
            Filter
          </IcButton>
        </div>
        <IcButton variant="secondary" slot="interaction">
          See all
        </IcButton>
        <IcSearchBar slot="interaction" label="Label" hideLabel />
        <IcLink
          href="https://google.com"
          slot="interaction"
          style={{ marginTop: "var(--ic-space-sm)" }}
        >
          Help
        </IcLink>
        <IcCardVertical
          heading="Latest announcement"
          message="This is some example text that can be included in the card copy."
          slot="secondary"
        />
      </IcHero>
    </IcTheme>
  );
};

export default IcHeroPage;
