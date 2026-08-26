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
import { FooterLink } from "../../ic-footer-link";

describe("ic-footer-link", () => {
  it("should render", async () => {
    const page = await newSpecPage({
      components: [FooterLink],
      html: `<ic-footer-link href="/">Link</ic-footer-link>`,
    });

    expect(page.root).toMatchSnapshot("footer-link");
  });

  it("should render small with grouped links", async () => {
    const page = await newSpecPage({
      components: [FooterLink],
      html: `<ic-footer-link href="/">Link</ic-footer-link>`,
    });

    page.rootInstance.footerConfig = { small: true, grouped: true };
    await page.waitForChanges();

    expect(page.root).toMatchSnapshot("small-footer-link-with-grouped-links");
  });

  it("should set foregroundColor on theme change", async () => {
    const page = await newSpecPage({
      components: [FooterLink],
      html: `<ic-footer-link label="button1" onclick="alert('test')">
      </ic-footer-link>`,
    });

    await page.rootInstance.footerBrandChangeHandler({
      detail: { mode: "light" },
    });
    await page.waitForChanges();

    expect(page.rootInstance.foregroundColor).toEqual("light");
  });

  it("should test footer resize handler", async () => {
    const page = await newSpecPage({
      components: [FooterLink],
      html: `<ic-footer-link label="button1" onclick="alert('test')">
      </ic-footer-link>`,
    });

    await page.rootInstance.footerResizeHandler();
    await page.waitForChanges();

    expect(page.rootInstance.footerConfig).toStrictEqual({
      grouped: false,
      small: false,
    });
  });
});
