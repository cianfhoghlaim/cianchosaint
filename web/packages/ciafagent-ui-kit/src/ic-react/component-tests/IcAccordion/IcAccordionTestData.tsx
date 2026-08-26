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
import React, { ReactElement } from "react";
import { IcAccordion, IcAccordionGroup, IcTypography } from "../../components";

const Icon = (): ReactElement => (
  <svg
    slot="icon"
    width="20"
    height="1em"
    viewBox="0 0 512 512"
    fill="currentColor"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path d="M362.7 19.3L314.3 67.7 444.3 197.7l48.4-48.4c25-25 25-65.5 0-90.5L453.3 19.3c-25-25-65.5-25-90.5 0zm-71 71L58.6 323.5c-10.4 10.4-18 23.3-22.2 37.4L1 481.2C-1.5 489.7 .8 498.8 7 505s15.3 8.5 23.7 6.1l120.3-35.4c14.1-4.2 27-11.8 37.4-22.2L421.7 220.3 291.7 90.3z" />
  </svg>
);

export const SimpleAccordion = (): ReactElement => (
  <IcAccordion heading="Accordion 1">Text</IcAccordion>
);

export const SimpleExpandedAccordion = (): ReactElement => (
  <IcAccordion expanded heading="Accordion 1">
    Text
  </IcAccordion>
);

export const AccordionsWithDisabled = (): ReactElement => (
  <>
    <IcAccordion heading="accordion1">Text 1</IcAccordion>
    <IcAccordion heading="accordion2" disabled>
      Text 2
    </IcAccordion>
    <IcAccordion heading="accordion3">Text 3</IcAccordion>
  </>
);

export const GroupWithOneExpanded = (): ReactElement => (
  <IcAccordionGroup label="Title">
    <TwoAccordionsWithOneExpanded />
  </IcAccordionGroup>
);

export const TwoAccordions = (): ReactElement => (
  <>
    <SimpleAccordion />
    <IcAccordion heading="Accordion 2">Text</IcAccordion>
  </>
);

export const TwoAccordionsWithOneExpanded = (): ReactElement => (
  <>
    <SimpleAccordion />
    <IcAccordion heading="Accordion 2" expanded>
      Text
    </IcAccordion>
  </>
);

export const SlottedHeadingAccordion = (): ReactElement => (
  <IcAccordionGroup>
    <h1 slot="label">Group title</h1>
    <IcAccordion>
      <h2 slot="heading">Heading</h2>
      <IcTypography variant="body">Text</IcTypography>
    </IcAccordion>
  </IcAccordionGroup>
);

export const WithIcon = (): ReactElement => {
  return (
    <IcAccordion heading="Accordion 1">
      <Icon />
      Text
    </IcAccordion>
  );
};

export const WithChildren = (): ReactElement => {
  return (
    <IcAccordion expanded heading="Accordion">
      <IcAccordion expanded heading="Child Accordion 1">
        Text
      </IcAccordion>
      <IcAccordion heading="Child Accordion 2">Text</IcAccordion>
      <IcAccordion heading="Child Accordion 3">Text</IcAccordion>
    </IcAccordion>
  );
};

export const DifferentSizes = (): ReactElement => {
  return (
    <>
      <IcAccordion heading="Small" size="small">
        Text
      </IcAccordion>
      <IcAccordion heading="Default">Text</IcAccordion>
      <IcAccordion heading="Large" size="large">
        Text
      </IcAccordion>
    </>
  );
};

export const DifferentSizesGroup = (): ReactElement => {
  return (
    <>
      <IcAccordionGroup size="small" label="Small">
        <TwoAccordions />
      </IcAccordionGroup>
      <IcAccordionGroup label="Default">
        <TwoAccordions />
      </IcAccordionGroup>
      <IcAccordionGroup size="large" label="Large">
        <TwoAccordions />
      </IcAccordionGroup>
    </>
  );
};

export const DarkTheme = (): ReactElement => {
  return (
    <div style={{ backgroundColor: "black" }}>
      <IcAccordion heading="Accordion 1" theme="dark">
        Text
      </IcAccordion>
    </div>
  );
};

export const DarkThemeGroup = (): ReactElement => {
  return (
    <div style={{ backgroundColor: "black" }}>
      <IcAccordionGroup theme="dark" label="Dark theme">
        <IcAccordion heading="Accordion 1" />
        <IcAccordion heading="Accordion 2" disabled />
        <IcAccordion heading="Accordion 3" message="Text" expanded />
      </IcAccordionGroup>
    </div>
  );
};

export const DarkThemeGroupSlottedContent = (): ReactElement => {
  return (
    <div style={{ backgroundColor: "black" }}>
      <IcAccordionGroup theme="dark">
        <IcTypography variant="h4" slot="label">
          Slotted group title
        </IcTypography>
        <IcAccordion>
          <Icon />
          <IcTypography variant="subtitle-large" slot="heading">
            Slotted heading
          </IcTypography>
        </IcAccordion>
        <IcAccordion disabled>
          <Icon />
          <IcTypography variant="subtitle-large" slot="heading">
            Slotted heading
          </IcTypography>
        </IcAccordion>
        <IcAccordion expanded>
          <IcTypography variant="subtitle-large" slot="heading">
            Slotted heading
          </IcTypography>
          <IcTypography variant="body">Text</IcTypography>
        </IcAccordion>
      </IcAccordionGroup>
    </div>
  );
};
