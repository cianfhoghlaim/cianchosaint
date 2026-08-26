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
export const defaultStepper = `
    <ic-stepper>
        <ic-step heading="First"></ic-step>
        <ic-step
        heading="Second With a Very Long Title"
        subheading="Optional Subtitle"
        type="current"
        ></ic-step>
        <ic-step heading="Third" type="disabled"></ic-step>
        <ic-step
        heading="Fourth"
        subheading="Optional Subtitle"
        type="completed"
        ></ic-step>
    </ic-stepper>`;

export const customConnectorWidthStepper = `
    <ic-stepper aligned="left" connector-width="150">
        <ic-step heading="First"></ic-step>
        <ic-step
        heading="Second With a Very Long Title"
        subheading="Optional Subtitle"
        type="current"
        ></ic-step>
        <ic-step heading="Third" type="disabled"></ic-step>
        <ic-step
        heading="Fourth"
        subheading="Optional Subtitle"
        type="completed"
        ></ic-step>
    </ic-stepper>`;

export const invalidConnectorWidthStepper = `
    <ic-stepper aligned="left" connector-width="96">
        <ic-step heading="First"></ic-step>
        <ic-step
        heading="Second With a Very Long Title"
        subheading="Optional Subtitle"
        type="current"
        ></ic-step>
        <ic-step heading="Third" type="disabled"></ic-step>
        <ic-step
        heading="Fourth"
        subheading="Optional Subtitle"
        type="completed"
        ></ic-step>
    </ic-stepper>`;

export const compactStepper = `
    <ic-stepper variant="compact" id="custom-compact-stepper">
        <ic-step 
        heading="First"
        ></ic-step>
        <ic-step
          heading="Second With a Very Long Title"
          subheading="Optional subtitle that is long and should wrap"
          current
          type="current"
        ></ic-step>
        <ic-step
          heading="Third"
          type="disabled"
        ></ic-step>
        <ic-step
          heading="Fourth title that is long and should wrap"
          subheading="Optional Subtitle"
          type="completed"
        ></ic-step>
        <ic-step
          heading="Fifth and final step"
          subheading="Optional Subtitle"
          icon
          status="optional"
          type="completed"
        ></ic-step>
      </ic-stepper>`;
