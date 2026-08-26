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
import { newSpecPage } from "@stencil/core/testing";
import { AccordionGroup } from "../../ic-accordion-group";
import { Accordion } from "../../../ic-accordion/ic-accordion";

const event = { detail: { id: "ic-accordion-0" } };

beforeAll(() => {
  jest.spyOn(console, "warn").mockImplementation(jest.fn());
});

describe("ic-accordion-group snapshots", () => {
  it("should match default snapshot", async () => {
    const page = await newSpecPage({
      components: [AccordionGroup],
      html: `<ic-accordion-group label="Test heading"></ic-accordion-group>`,
    });
    expect(page.root).toMatchSnapshot("renders as default");
  });

  it("should match dark snapshot", async () => {
    const page = await newSpecPage({
      components: [AccordionGroup],
      html: `<ic-accordion-group theme="dark" label="Test heading"></ic-accordion-group>`,
    });
    expect(page.root).toMatchSnapshot("renders as dark");
  });
});

describe("ic-accordion-group functions unit test", () => {
  it("should check setExpandedToAreAllAccordionsOpen when single expansion is false", async () => {
    const page = await newSpecPage({
      components: [AccordionGroup, Accordion],
      html: `
    <ic-accordion-group label="Test heading">
      <ic-accordion>
        <ic-typography variant="body" >
          This is an example of the main body text.
        </ic-typography>
      </ic-accordion>
      <ic-accordion expanded>
      <ic-typography variant="body" >
        This is an example of the main body text.
      </ic-typography>
    </ic-accordion>
    </ic-accordion-group>`,
    });
    const spySetExpandedToAreAllAccordionsOpen = jest.spyOn(
      page.rootInstance,
      "setExpandedToAreAllAccordionsOpen"
    );
    expect(page.rootInstance.singleExpansion).toBe(false);
    await page.rootInstance.handleAccordionClicked(event);
    expect(spySetExpandedToAreAllAccordionsOpen).toBeCalled();
  });

  it("should check handleExpanded", async () => {
    const page = await newSpecPage({
      components: [AccordionGroup],
      html: `<ic-accordion-group label="Test heading" expanded></ic-accordion-group>`,
    });
    expect(page.rootInstance.expanded).toBe(true);
    await page.rootInstance.handleExpanded();
    await page.waitForChanges;
    expect(page.rootInstance.expanded).toBe(false);
  });
});

describe("ic-accordion-group component", () => {
  it("should test the handleExpanded function", async () => {
    const page = await newSpecPage({
      components: [AccordionGroup, Accordion],
      html: `
      <ic-accordion-group expanded="true" label="Test heading">
        <ic-accordion heading="Accordion 1">
          <ic-typography variant="body">
            This is an example of the main body text.
          </ic-typography>
        </ic-accordion>
      </ic-accordion-group>`,
    });
    expect(page.rootInstance.expanded).toBe(true);
    await page.rootInstance.handleExpanded();
    await page.waitForChanges();
    expect(page.rootInstance.expanded).toBe(false);
  });

  it("should test singleExpansion function", async () => {
    const page = await newSpecPage({
      components: [AccordionGroup, Accordion],
      html: `
      <ic-accordion-group label="Test heading" single-expansion="true">
        <ic-accordion heading="Accordion 1">
          <ic-typography variant="body">
            This is an example of the main body text.
          </ic-typography>
        </ic-accordion>
        <ic-accordion heading="Accordion 2" expanded>
          <ic-typography variant="body">
            This is an example of the main body text.
          </ic-typography>
        </ic-accordion>
      </ic-accordion-group>`,
    });

    const accordions = document.querySelectorAll("ic-accordion");
    const accordion1 = accordions[0];
    const accordion2 = accordions[1];
    const accordionButton = accordion1.shadowRoot?.querySelector(
      ".section-button"
    ) as HTMLButtonElement;
    await page.waitForChanges();
    expect(accordion1.expanded).toBe(false);
    expect(accordion2.expanded).toBe(true);
    accordionButton.click();
    await page.waitForChanges();
    expect(accordion1.expanded).toBe(true);
    expect(accordion2.expanded).toBe(false);
  });

  it("should check the areAllAccordionsOpen function", async () => {
    const page = await newSpecPage({
      components: [AccordionGroup, Accordion],
      html: `
      <ic-accordion-group label="Test heading">
        <ic-accordion heading="Accordion 1">
          <ic-typography variant="body">
            This is an example of the main body text.
          </ic-typography>
        </ic-accordion>
      </ic-accordion-group>`,
    });
    // uses handleExpanded to open accordion, making areAllAccordionsOpen = true
    await page.rootInstance.handleExpanded();
    await page.waitForChanges;
    expect(page.rootInstance.expanded).toBe(true);
    expect(page.rootInstance.areAllAccordionsOpen).toBe(true);

    // uses handleExpanded to close accordion, making areAllAccordionsOpen = false
    await page.rootInstance.handleExpanded();
    await page.waitForChanges;
    expect(page.rootInstance.expanded).toBe(false);
    expect(page.rootInstance.areAllAccordionsOpen).toBe(false);
  });

  it("should test the accessibleButtonLabel slot", async () => {
    const page = await newSpecPage({
      components: [AccordionGroup],
      html: `
      <ic-accordion-group label="Test heading">
        <span slot="accessibleButtonLabel">Custom accessible label</span>
        <ic-accordion heading="Accordion 1">
          <ic-typography variant="body">
            This is an example of the main body text.
          </ic-typography>
        </ic-accordion>
      </ic-accordion-group>`,
    });

    expect(page.root).toMatchSnapshot(
      "renders with accessibleButtonLabel slot"
    );
  });
});
