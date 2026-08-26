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
import { LayoutGridItem } from "../../ic-layout-grid-item";
import { newSpecPage } from "@stencil/core/testing";

describe("ic-layout-grid", () => {
  it("should render", async () => {
    const page = await newSpecPage({
      components: [LayoutGridItem],
      html: `<ic-layout-grid>
        <ic-layout-grid-item>
          <div>Test div 1</div>
        </ic-layout-grid-item>
      </ic-layout-grid>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with col start", async () => {
    const page = await newSpecPage({
      components: [LayoutGridItem],
      html: `<ic-layout-grid>
        <ic-layout-grid-item col-start="2">
          <div>Test div 1</div>
        </ic-layout-grid-item>
      </ic-layout-grid>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with row start", async () => {
    const page = await newSpecPage({
      components: [LayoutGridItem],
      html: `<ic-layout-grid>
        <ic-layout-grid-item row-start="2">
          <div>Test div 1</div>
        </ic-layout-grid-item>
      </ic-layout-grid>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with col span", async () => {
    const page = await newSpecPage({
      components: [LayoutGridItem],
      html: `<ic-layout-grid>
        <ic-layout-grid-item col-span="2">
          <div>Test div 1</div>
        </ic-layout-grid-item>
      </ic-layout-grid>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with row span", async () => {
    const page = await newSpecPage({
      components: [LayoutGridItem],
      html: `<ic-layout-grid>
        <ic-layout-grid-item row-span="2">
          <div>Test div 1</div>
        </ic-layout-grid-item>
      </ic-layout-grid>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with hide in mobile mode class", async () => {
    const page = await newSpecPage({
      components: [LayoutGridItem],
      html: `<ic-layout-grid>
        <ic-layout-grid-item hide-in-mobile-mode="true">
          <div>Test div 1</div>
        </ic-layout-grid-item>
      </ic-layout-grid>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should update --ic-grid-item-col-span when colSpan changes", async () => {
    const page = await newSpecPage({
      components: [LayoutGridItem],
      html: `<ic-layout-grid-item></ic-layout-grid-item>`,
    });
    page.rootInstance.colSpan = 5;
    await page.waitForChanges();
    expect(page.root!.style.getPropertyValue("--ic-grid-item-col-span")).toBe(
      "5"
    );
  });

  it("should update --ic-grid-item-col-start when colStart changes", async () => {
    const page = await newSpecPage({
      components: [LayoutGridItem],
      html: `<ic-layout-grid-item></ic-layout-grid-item>`,
    });
    page.rootInstance.colStart = 5;
    await page.waitForChanges();
    expect(page.root!.style.getPropertyValue("--ic-grid-item-col-start")).toBe(
      "5"
    );
  });

  it("should update --ic-grid-item-row-span when rowSpan changes", async () => {
    const page = await newSpecPage({
      components: [LayoutGridItem],
      html: `<ic-layout-grid-item></ic-layout-grid-item>`,
    });
    page.rootInstance.rowSpan = 5;
    await page.waitForChanges();
    expect(page.root!.style.getPropertyValue("--ic-grid-item-row-span")).toBe(
      "5"
    );
  });

  it("should update --ic-grid-item-row-start when rowStart changes", async () => {
    const page = await newSpecPage({
      components: [LayoutGridItem],
      html: `<ic-layout-grid-item></ic-layout-grid-item>`,
    });
    page.rootInstance.rowStart = 5;
    await page.waitForChanges();
    expect(page.root!.style.getPropertyValue("--ic-grid-item-row-start")).toBe(
      "5"
    );
  });
});
