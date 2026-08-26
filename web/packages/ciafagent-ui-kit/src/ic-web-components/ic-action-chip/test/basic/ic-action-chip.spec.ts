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
import { ActionChip } from "../../ic-action-chip";
import * as helpers from "../../../../utils/helpers";

describe("ic-action-chip component", () => {
  it("should render filled by default", async () => {
    const page = await newSpecPage({
      components: [ActionChip],
      html: `<ic-action-chip label="Medium"></ic-action-chip>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render outlined when supplying the `variant` prop", async () => {
    const page = await newSpecPage({
      components: [ActionChip],
      html: `<ic-action-chip label="Medium" variant="outlined"></ic-action-chip>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with a solid background when outlined but `transparent-background` is `false`", async () => {
    const page = await newSpecPage({
      components: [ActionChip],
      html: `<ic-action-chip label="Medium" variant="outlined" transparent-background="false"></ic-action-chip>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should ignore `transparent-background` when the variant is `filled`", async () => {
    const page = await newSpecPage({
      components: [ActionChip],
      html: `<ic-action-chip label="Medium" transparent-background="false"></ic-action-chip>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render disabled", async () => {
    const page = await newSpecPage({
      components: [ActionChip],
      html: `<ic-action-chip label="Medium" disabled="true"></ic-action-chip>`,
    });

    expect(page.root).toMatchSnapshot();

    page.root?.setAttribute("disabled", "false");

    await page.waitForChanges();
    expect(page.root).toMatchSnapshot("disabled-removed");
  });

  it("should render small", async () => {
    const page = await newSpecPage({
      components: [ActionChip],
      html: `<ic-action-chip label="Small" size="small"></ic-action-chip>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render large", async () => {
    const page = await newSpecPage({
      components: [ActionChip],
      html: `<ic-action-chip label="Large" size="large"></ic-action-chip>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with an icon", async () => {
    const page = await newSpecPage({
      components: [ActionChip],
      html: `<ic-action-chip label="Medium">
  <svg
    slot="icon"
    width="20"
    height="20"
    viewBox="0 0 20 20"
    fill="currentColor"
    xmlns="http://www.w3.org/2000/svg"
    aria-label="account"
  >
    <path
      d="M10 0C4.48 0 0 4.48 0 10C0 15.52 4.48 20 10 20C15.52 20 20 15.52 20 10C20 4.48 15.52 0 10 0ZM10 3C11.66 3 13 4.34 13 6C13 7.66 11.66 9 10 9C8.34 9 7 7.66 7 6C7 4.34 8.34 3 10 3ZM10 17.2C7.5 17.2 5.29 15.92 4 13.98C4.03 11.99 8 10.9 10 10.9C11.99 10.9 15.97 11.99 16 13.98C14.71 15.92 12.5 17.2 10 17.2Z"
    />
  </svg>
</ic-action-chip>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with a badge", async () => {
    const page = await newSpecPage({
      components: [ActionChip],
      html: `<ic-action-chip label="Medium">
  <ic-badge label="1" slot="badge" variant="success"></ic-badge>
</ic-action-chip>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should apply the `theme` and `monochrome` props correctly", async () => {
    const page = await newSpecPage({
      components: [ActionChip],
      html: `<ic-action-chip label="Medium" theme="dark" monochrome="true"></ic-action-chip>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should call 'setFocus' when chip is focused", async () => {
    const page = await newSpecPage({
      components: [ActionChip],
      html: `<ic-action-chip label="Medium"></ic-action-chip>`,
    });

    //Can't expect anything in this test - this is to increase code coverage only
    await page.rootInstance.setFocus().toHaveBeenCalled;
  });

  it("render with correct `type` when prop defined", async () => {
    const page = await newSpecPage({
      components: [ActionChip],
      html: `<ic-action-chip label="Medium" type="submit"></ic-action-chip>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should test button as submit button on form", async () => {
    const page = await newSpecPage({
      components: [ActionChip],
      html: `<form id="new-form"><form><ic-action-chip id="form-submit-chip" label="Medium" type="submit" form="new-form"></ic-action-chip>`,
    });

    document.getElementById("form-submit-chip")?.click();

    expect(page.root).toMatchSnapshot();
  });

  it("should stop immediate propagation of a click event when disabled", async () => {
    const page = await newSpecPage({
      components: [ActionChip],
      html: `<ic-action-chip id="clickable-disabled" label="Medium" disabled="true" onclick="alert('test')"></ic-action-chip>`,
    });

    jest.spyOn(window, "alert").mockImplementation();

    document.getElementById("clickable-disabled")?.click();

    await page.waitForChanges();

    expect(window.alert).not.toHaveBeenCalled();
  });

  it('should render with "a" tag when href is passed', async () => {
    const page = await newSpecPage({
      components: [ActionChip],
      html: `<ic-action-chip label="Medium" href="#"></ic-action-chip>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it('should render with defined "a" tag props', async () => {
    const page = await newSpecPage({
      components: [ActionChip],
      html: `<ic-action-chip label="Medium" href="#" download="true" rel="nofollow" target="_blank"></ic-action-chip>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should apply the correct class when in an AG Grid", async () => {
    Object.defineProperty(helpers, "isElInAGGrid", {
      value: jest.fn().mockReturnValue(true),
    });

    const page = await newSpecPage({
      components: [ActionChip],
      html: `<ic-action-chip label="Medium"></ic-action-chip>`,
    });

    await page.waitForChanges();
    expect(
      page.root?.shadowRoot
        ?.querySelector("ic-typography")
        ?.classList.contains("in-ag-grid")
    ).toBe(true);
  });
});
