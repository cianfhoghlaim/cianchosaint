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
import { Footer } from "../../../ic-footer/ic-footer";
import { FooterLinkGroup } from "../../ic-footer-link-group";
import { FooterLink } from "../../../ic-footer-link/ic-footer-link";

describe("ic-footer-link-group", () => {
  it("should render", async () => {
    const page = await newSpecPage({
      components: [FooterLinkGroup],
      html: `<ic-footer-link-group label="Link group"></ic-footer-link-group>`,
    });

    expect(page.root).toMatchSnapshot("footer-link-group");
  });

  it("should render with links", async () => {
    const page = await newSpecPage({
      components: [FooterLinkGroup, FooterLink],
      html: `<ic-footer-link-group label="Link group"><ic-footer-link href="/">Link</ic-footer-link></ic-footer-link-group>`,
    });

    expect(page.root).toMatchSnapshot("footer-link-group-with-links");
  });

  it("should render within footer", async () => {
    const page = await newSpecPage({
      components: [Footer, FooterLinkGroup, FooterLink],
      html: `<ic-footer><ic-footer-link-group label="Link group"><ic-footer-link href="/">Link</ic-footer-link></ic-footer-link-group><ic-footer>`,
    });

    expect(page.root).toMatchSnapshot("footer-link-group-in-footer");
  });

  it("should expand and collapse", async () => {
    const page = await newSpecPage({
      components: [Footer, FooterLinkGroup, FooterLink],
      html: `<ic-footer-link-group label="Link group"><ic-footer-link href="/">Link</ic-footer-link></ic-footer-link-group>`,
    });

    expect(page.rootInstance.expanded).toBe(false);

    const event = new KeyboardEvent("keydown", { key: "Enter" });

    await page.rootInstance.handleKeydown(event);

    expect(page.rootInstance.expanded).toBe(true);

    await page.rootInstance.handleKeydown(event);

    expect(page.rootInstance.expanded).toBe(false);
  });

  it("should check and set small state", async () => {
    const page = await newSpecPage({
      components: [Footer, FooterLinkGroup, FooterLink],
      html: `<ic-footer-link-group label="Link group"><ic-footer-link href="/">Link</ic-footer-link></ic-footer-link-group>`,
    });

    await page.rootInstance.footerResizeHandler();

    expect(page.rootInstance.small).toBe(false);
  });

  it("should update theme", async () => {
    const page = await newSpecPage({
      components: [Footer, FooterLinkGroup, FooterLink],
      html: `<ic-footer-link-group label="Link group"><ic-footer-link href="/">Link</ic-footer-link></ic-footer-link-group>`,
    });

    await page.rootInstance.footerBrandChangeHandler({
      detail: { mode: "dark" },
    });

    expect(page.rootInstance.dropdownIconStyle).toBe("dark");
  });

  it("should render small", async () => {
    const page = await newSpecPage({
      components: [Footer, FooterLinkGroup, FooterLink],
      html: `<ic-footer breakpoint="extra large"><ic-footer-link-group small=true label="Link group"><ic-footer-link href="/">Link</ic-footer-link></ic-footer-link-group></ic-footer>`,
    });

    expect(page.root).not.toBeNull;

    expect(page.root).toMatchSnapshot("footer-link-group-small");
  });
});
