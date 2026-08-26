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
import { MenuItem } from "../../ic-menu-item";
import { Button } from "../../../ic-button/ic-button";

describe("menu item variants", () => {
  it("should render the default variant", async () => {
    const page = await newSpecPage({
      components: [MenuItem],
      html: `<ic-menu-item
            label="Default variant"
          />`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render the disabled variant", async () => {
    const page = await newSpecPage({
      components: [MenuItem],
      html: `<ic-menu-item
            label="Default variant"
            disabled
          />`,
    });

    expect(page.root).toMatchSnapshot();

    page.root?.setAttribute("disabled", "false");

    await page.waitForChanges();
    expect(page.root).toMatchSnapshot("disabled-removed");
  });

  it("should render a menu item with a description", async () => {
    const page = await newSpecPage({
      components: [MenuItem],
      html: `<ic-menu-item
            label="Default variant"
            description="This is the default variant of the menu item with a description"
          />`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with keyboard shortcut", async () => {
    const page = await newSpecPage({
      components: [MenuItem],
      html: `<ic-menu-item
              label="Toggle variant"
              keyboard-shortcut-label="Cmd+"
            />`,
    });
    expect(page.root).toMatchSnapshot();
  });

  it("should render the toggle variant", async () => {
    const page = await newSpecPage({
      components: [MenuItem, Button],
      html: `<ic-menu-item
            variant="toggle"
            label="Toggle variant"
            id="test-menu-item"
          />`,
    });

    expect(page.root).toMatchSnapshot();
    expect(page.rootInstance.variant).toMatch("toggle");
    expect(page.rootInstance.checked).toBeFalsy();

    const button = page.root?.shadowRoot
      ?.querySelector("li > ic-button")
      ?.shadowRoot?.querySelector("button");

    button?.click();
    await page.waitForChanges;
  });

  it("should render the destructive variant", async () => {
    const page = await newSpecPage({
      components: [MenuItem],
      html: `<ic-menu-item
            variant="destructive"
            label="Destructive variant"
          />`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render a menu item that triggers a popover menu instance", async () => {
    const page = await newSpecPage({
      components: [MenuItem],
      html: `<ic-menu-item
            variant="destructive"
            submenu-trigger-for="submenu-1"
            label="Destructive variant"
          />`,
    });

    expect(page.rootInstance.submenuTriggerFor).not.toBeUndefined();

    expect(page.rootInstance.variant).toMatch("default");
  });

  it('should emit the triggerPopoverMenuInstance event when the menu item has the prop: "submenu-trigger-for" and is clicked', async () => {
    const page = await newSpecPage({
      components: [MenuItem, Button],
      html: `<ic-menu-item
      id="test-menu-item"
            submenu-trigger-for="submenu-1"
            label="I emit an event"
          />`,
    });

    const eventSpy = jest.fn();
    page.win.addEventListener("triggerPopoverMenuInstance", eventSpy);
    expect(page.rootInstance.submenuTriggerFor).not.toBeUndefined();

    const element = await document.getElementById("test-menu-item");

    await element?.click();

    await page.waitForChanges();

    await page.rootInstance.handleClick;
  });

  it("should prevent default action on click if variant is 'toggle'", async () => {
    const page = await newSpecPage({
      components: [MenuItem],
      html: `<ic-menu-item
      id="test-menu-item"
            label="I emit an event"
            variant="toggle"
          />`,
    });

    const eventSpy = jest.fn();

    const mockEvent = {
      preventDefault: eventSpy,
    };

    await page.rootInstance.handleClick(mockEvent as unknown as MouseEvent);

    expect(eventSpy).toHaveBeenCalled();
  });
});
