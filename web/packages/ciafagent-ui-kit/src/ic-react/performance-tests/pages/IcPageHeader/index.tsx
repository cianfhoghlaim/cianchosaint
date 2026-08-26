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
// IcPageHeaderPage displays a page header for the purpose of performance testing of the IcPageHeader component.
import React from "react";
import {
  IcPageHeader,
  IcStatusTag,
  IcBreadcrumbGroup,
  IcBreadcrumb,
  IcButton,
  IcTextField,
  IcNavigationItem,
  IcTheme,
  IcTypography,
} from "../../../components";
import { SlottedSVG } from "../../../react-component-lib/slottedSVG";

type PageProps = {
  theme: "light" | "dark";
};

const IcPageHeaderPage: React.FC<PageProps> = ({ theme }) => {
  return (
    <IcTheme id="theme-wrapper" theme={theme}>
      <IcTypography
        variant="subtitle-small"
        style={{ padding: "var(--ic-space-md)" }}
      >
        <h1>Page Header Page</h1>
      </IcTypography>
      <IcPageHeader
        heading="Page header"
        subheading="This is a simple page header component and this is the text. This page header is only sticky for viewport widths of 992px and above.."
        stickyDesktopOnly
        aligned="full-width"
      >
        <IcStatusTag slot="heading-adornment" label="Beta" />
        <IcBreadcrumbGroup slot="breadcrumbs">
          <IcBreadcrumb pageTitle="Breadcrumb 1" href="/breadcrumb-1" />
          <IcBreadcrumb
            current={true}
            pageTitle="Breadcrumb 2"
            href="/breadcrumb-2"
          />
        </IcBreadcrumbGroup>
        <IcButton slot="actions" variant="primary">
          Create coffee
          <SlottedSVG
            slot="left-icon"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z"
              fill="currentColor"
            />
          </SlottedSVG>
        </IcButton>
        <IcButton slot="actions" variant="secondary">
          Filter coffee
        </IcButton>
        <IcTextField
          slot="input"
          placeholder="Enter your input"
          label="Input"
          hideLabel
        />
        <IcNavigationItem slot="tabs" label="All recipes" href="/" selected />
        <IcNavigationItem slot="tabs" label="Favourites" href="/" />
      </IcPageHeader>
    </IcTheme>
  );
};

export default IcPageHeaderPage;
