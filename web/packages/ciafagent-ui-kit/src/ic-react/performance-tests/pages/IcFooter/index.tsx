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
// IcFooterPage displays a footer for the purpose of performance testing of the IcFooter component.
import React from "react";
import {
  IcFooter,
  IcFooterLink,
  IcClassificationBanner,
  IcTheme,
  IcTypography,
} from "../../../components";

type PageProps = {
  theme: "light" | "dark";
};

const IcFooterPage: React.FC<PageProps> = ({ theme }) => {
  return (
    <IcTheme id="theme-wrapper" theme={theme}>
      <IcTypography
        variant="subtitle-small"
        style={{ padding: "var(--ic-space-md)" }}
      >
        <h1>Footer Page</h1>
      </IcTypography>
      <>
        <IcClassificationBanner classification="official" />
        <IcFooter
          description="The ICDS is maintained by the Design Practice Team. If you've got a question or want to feedback, please get in touch."
          caption="All content is available under the Open Government Licence v3.0, except source code and code examples which are available under the MIT Licence."
          style={{ position: "fixed", bottom: "0", left: "0", right: "0" }}
        >
          <IcFooterLink slot="link" href="/">
            Get Started
          </IcFooterLink>
          <IcFooterLink slot="link" href="/">
            Accessibility
          </IcFooterLink>
          <IcFooterLink slot="link" href="/">
            Styles
          </IcFooterLink>
          <IcFooterLink slot="link" href="/">
            Components
          </IcFooterLink>
          <IcFooterLink slot="link" href="/">
            Patterns
          </IcFooterLink>
          <IcFooterLink slot="link" href="/">
            Design toolkit
          </IcFooterLink>
          <div
            slot="logo"
            role="list"
            style={{
              display: "flex",
              gap: "var(--ic-space-lg)",
            }}
          >
            <IcFooterLink href="/">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="48px"
                viewBox="0 0 24 24"
                width="48px"
                fill="#FFFFFF"
              >
                <title>Footer logo link 1</title>
                <path d="M0 0h24v24H0V0z" fill="none" />
                <path d="M19 5v14H5V5h14m0-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-4.86 8.86l-3 3.87L9 13.14 6 17h12l-3.86-5.14z" />
              </svg>
            </IcFooterLink>
            <IcFooterLink href="/">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="48px"
                viewBox="0 0 24 24"
                width="48px"
                fill="#FFFFFF"
              >
                <title>Footer logo link 2</title>
                <path d="M0 0h24v24H0V0z" fill="none" />
                <path d="M19 5v14H5V5h14m0-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-4.86 8.86l-3 3.87L9 13.14 6 17h12l-3.86-5.14z" />
              </svg>
            </IcFooterLink>
            <IcFooterLink href="/">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="48px"
                viewBox="0 0 24 24"
                width="48px"
                fill="#FFFFFF"
              >
                <title>Footer logo link 3</title>
                <path d="M0 0h24v24H0V0z" fill="none" />
                <path d="M19 5v14H5V5h14m0-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-4.86 8.86l-3 3.87L9 13.14 6 17h12l-3.86-5.14z" />
              </svg>
            </IcFooterLink>
          </div>
        </IcFooter>
      </>
    </IcTheme>
  );
};

export default IcFooterPage;
