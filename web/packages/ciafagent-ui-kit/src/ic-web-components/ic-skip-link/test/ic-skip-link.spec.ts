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
import { Link } from "../../ic-link/ic-link";
import { SkipLink } from "../ic-skip-link";

describe("ic-skip-link component", () => {
  it("should render a skip link by default with the correct text", async () => {
    const page = await newSpecPage({
      components: [SkipLink, Link],
      html: `<ic-skip-link target="page-content"></ic-skip-link>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render a skip link with a custom label", async () => {
    const page = await newSpecPage({
      components: [SkipLink, Link],
      html: `<ic-skip-link target="page-content" label="Custom skip label"></ic-skip-link>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render a skip link without a background when `transparentBackground` is true", async () => {
    const page = await newSpecPage({
      components: [SkipLink, Link],
      html: `<ic-skip-link target="page-content" transparent-background="true"></ic-skip-link>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should pass down the theme and monochrome prop to the ic-link component", async () => {
    const page = await newSpecPage({
      components: [SkipLink, Link],
      html: `<ic-skip-link target="page-content" theme="dark" monochrome="true"></ic-skip-link>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with the `inline` prop", async () => {
    const page = await newSpecPage({
      components: [SkipLink, Link],
      html: `<ic-skip-link target="page-content" inline="true"></ic-skip-link>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should focus the link element when setFocus is called", async () => {
    const page = await newSpecPage({
      components: [SkipLink, Link],
      html: `<ic-skip-link target="page-content"></ic-skip-link>`,
    });

    const focusEvent = jest.spyOn(Link.prototype, "setFocus");

    page.rootInstance.setFocus();
    await page.waitForChanges();

    expect(focusEvent).toHaveBeenCalledTimes(1);
  });
});
