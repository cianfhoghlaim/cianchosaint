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
// IcAccordionMultiplePage displays multiple accordion groups for the purpose of performance testing of the IcAccordion component.
import React from "react";
import {
  IcAccordion,
  IcAccordionGroup,
  IcTypography,
  IcTheme,
} from "../../../../components";
import { SlottedSVG } from "../../../../react-component-lib/slottedSVG";

const ACCORDION_ICON = (
  <SlottedSVG
    slot="icon"
    width="20"
    height="1em"
    viewBox="0 0 512 512"
    fill="currentColor"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path d="M362.7 19.3L314.3 67.7 444.3 197.7l48.4-48.4c25-25 25-65.5 0-90.5L453.3 19.3c-25-25-65.5-25-90.5 0zm-71 71L58.6 323.5c-10.4 10.4-18 23.3-22.2 37.4L1 481.2C-1.5 489.7 .8 498.8 7 505s15.3 8.5 23.7 6.1l120.3-35.4c14.1-4.2 27-11.8 37.4-22.2L421.7 220.3 291.7 90.3z" />
  </SlottedSVG>
);

type PageProps = {
  theme: "light" | "dark";
};

const Accordion = () => (
  <IcAccordionGroup label="Title of the Accordion Group">
    <IcAccordion heading="Accordion 1">
      {ACCORDION_ICON}
      <IcTypography variant="body">
        This is an example of the main body text
      </IcTypography>
    </IcAccordion>
    <IcAccordion heading="Accordion 2">
      {ACCORDION_ICON}
      <IcTypography variant="body">
        This is an example of the main body text
      </IcTypography>
    </IcAccordion>
    <IcAccordion heading="Accordion 3">
      {ACCORDION_ICON}
      <IcTypography variant="body">
        This is an example of the main body text
      </IcTypography>
    </IcAccordion>
    <IcAccordion heading="Accordion 4">
      {ACCORDION_ICON}
      <IcTypography variant="body">
        This is an example of the main body text
      </IcTypography>
    </IcAccordion>
  </IcAccordionGroup>
);

const IcAccordionMultiplePage: React.FC<PageProps> = ({ theme }) => {
  return (
    <IcTheme id="theme-wrapper" theme={theme}>
      <div style={{ padding: "var(--ic-space-md)" }}>
        {Array.from({ length: 20 }).map((_, i) => (
          <Accordion key={i} />
        ))}
      </div>
    </IcTheme>
  );
};

export default IcAccordionMultiplePage;
