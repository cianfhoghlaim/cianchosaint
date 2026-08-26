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
import { DataRow } from "../../ic-data-row";

describe("ic-data-row", () => {
  it("should render", async () => {
    const page = await newSpecPage({
      components: [DataRow],
      html: `<ic-data-row label="label" value="value"></ic-data-row>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render slotted content in the label slot", async () => {
    const page = await newSpecPage({
      components: [DataRow],
      html: `<ic-data-row value="value"><ic-typography slot="label">Label</ic-typography></ic-data-row>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should not render label element if no label provided", async () => {
    const page = await newSpecPage({
      components: [DataRow],
      html: `<ic-data-row value="value"></ic-data-row>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render slotted content in the value slot", async () => {
    const page = await newSpecPage({
      components: [DataRow],
      html: `<ic-data-row label="label"><ic-status-tag variant="success" label="success" slot="value"></ic-status-tag></ic-data-row>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render slotted content in the end-component slot", async () => {
    const page = await newSpecPage({
      components: [DataRow],
      html: `<ic-data-row label="label" value="test value"><ic-status-tag variant="success" label="success" slot="end-component"></ic-status-tag></ic-data-row>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render the label variant of typography when list size is xs", async () => {
    const page = await newSpecPage({
      components: [DataRow],
      html: `<ic-data-row label="label"><ic-status-tag variant="success" label="success" slot="value"></ic-status-tag></ic-data-row>`,
    });

    page.rootInstance.listSize = "xs";
    await page.waitForChanges();

    expect(page.root).toMatchSnapshot();
  });

  it("should call runResizeObserver", async () => {
    const page = await newSpecPage({
      components: [DataRow],
      html: `<ic-data-row label="label" value="value"></ic-data-row>`,
    });

    await page.rootInstance.runResizeObserver();
    page.waitForChanges();

    const resize = new ResizeObserver(() => {
      page.rootInstance.checkLabelAbove();
    });

    expect(page.rootInstance.resizeObserver).toBe(resize);

    page.setContent("");
  });

  it("should change list size depending on screen size", async () => {
    const page = await newSpecPage({
      components: [DataRow],
      html: `<ic-data-row label="label" value="value"></ic-data-row>`,
    });

    Object.defineProperty(
      page.root?.shadowRoot?.querySelector(".data"),
      "clientWidth",
      {
        value: 200,
      }
    );

    page.waitForChanges();

    page.rootInstance.checkLabelAbove();

    expect(page.rootInstance.listSize).toBe("xs");
  });
});
