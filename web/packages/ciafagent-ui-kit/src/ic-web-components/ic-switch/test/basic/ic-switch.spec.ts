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
import { Switch } from "../../ic-switch";

describe("ic-switch component", () => {
  it("should render an aria-label", async () => {
    const page = await newSpecPage({
      components: [Switch],
      html: `<ic-switch label="Custom title"></ic-switch>`,
    });

    expect(page.root).toMatchSnapshot("renders-with-aria");
  });

  it("should render disabled", async () => {
    const page = await newSpecPage({
      components: [Switch],
      html: `<ic-switch label="Custom title" disabled=true></ic-switch>`,
    });

    expect(page.root).toMatchSnapshot("renders-disabled");

    page.root?.setAttribute("disabled", "false");

    await page.waitForChanges();
    expect(page.root).toMatchSnapshot("disabled-removed");
  });

  it("should render checked", async () => {
    const page = await newSpecPage({
      components: [Switch],
      html: `<ic-switch label="Custom title" checked=true></ic-switch>`,
    });

    expect(page.root).toMatchSnapshot("renders-checked");
  });

  it("should render small", async () => {
    const page = await newSpecPage({
      components: [Switch],
      html: `<ic-switch label="Custom title" checked=true size="small"></ic-switch>`,
    });

    expect(page.root).toMatchSnapshot("renders-small");
  });

  it("should focus", async () => {
    const page = await newSpecPage({
      components: [Switch],
      html: `<ic-switch label="Custom title" checked=true></ic-switch>`,
    });

    const callbackFn = jest.fn();
    page.doc.addEventListener("icFocus", callbackFn);
    const input = page.root?.shadowRoot?.querySelector("input");
    input?.focus();
    await page.waitForChanges();
    expect(callbackFn).toHaveBeenCalled();
  });

  it("should blur", async () => {
    const page = await newSpecPage({
      components: [Switch],
      html: `<ic-switch label="Custom title" checked=true></ic-switch>`,
    });

    const callbackFn = jest.fn();
    page.doc.addEventListener("icBlur", callbackFn);
    const input = page.root?.shadowRoot?.querySelector("input");
    input?.blur();
    await page.waitForChanges();
    expect(callbackFn).toHaveBeenCalled();
  });

  it("should toggle checkedState", async () => {
    const page = await newSpecPage({
      components: [Switch],
      html: `<ic-switch label="Custom title" checked=true></ic-switch>`,
    });

    expect(page.rootInstance.checkedState).toBe(true);
    page.rootInstance.handleChange();
    await page.waitForChanges();

    expect(page.rootInstance.checkedState).toBe(false);
  });

  it("should call 'setFocus' when switch is focused", async () => {
    const page = await newSpecPage({
      components: [Switch],
      html: `<ic-switch label="Custom title"></ic-switch>`,
    });

    //Can't expect anything in this test - this is to increase code coverage only
    await page.rootInstance.setFocus().toHaveBeenCalled;
  });

  it("should reset to initial state on form reset", async () => {
    const page = await newSpecPage({
      components: [Switch],
      html: `<form><ic-switch label="Custom title" checked=true></ic-switch><button id="resetButton" type="reset">Reset</button></form>`,
    });

    expect(page.rootInstance.checkedState).toBe(true);

    page.rootInstance.handleChange();
    await page.waitForChanges();

    expect(page.rootInstance.checkedState).toBe(false);

    await page.rootInstance.handleFormReset();
    await page.waitForChanges();

    expect(page.rootInstance.checkedState).toBe(true);

    //test disconnected callback
    page.setContent("");
  });
});
