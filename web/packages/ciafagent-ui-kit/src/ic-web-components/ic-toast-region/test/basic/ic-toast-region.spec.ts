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
import { Button } from "../../../ic-button/ic-button";
import { Toast } from "../../../ic-toast/ic-toast";
import { ToastRegion } from "../../ic-toast-region";

describe("ic-toast-region component", () => {
  it("should render", async () => {
    const page = await newSpecPage({
      components: [ToastRegion, Toast],
      html: `<ic-toast-region>
      <ic-toast heading="Heading"></ic-toast>
      </ic-toast-region>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should test showing and hiding toasts with openToast prop", async () => {
    const page = await newSpecPage({
      components: [ToastRegion, Toast],
      html: `<ic-toast-region>
      <ic-toast heading="Heading"></ic-toast>
      <ic-toast heading="Heading"></ic-toast>
      </ic-toast-region>`,
    });

    const toasts = document.querySelectorAll("ic-toast");

    page.rootInstance.openToast = toasts[0];

    await page.waitForChanges();

    expect(page.rootInstance.pendingVisibility.length).toBe(1);

    page.rootInstance.openToast = toasts[1];

    await page.waitForChanges();

    expect(page.rootInstance.pendingVisibility.length).toBe(2);

    await page.rootInstance.handleDismissedToast();
    expect(page.rootInstance.pendingVisibility.length).toBe(1);

    await page.rootInstance.handleDismissedToast();
    expect(page.rootInstance.pendingVisibility.length).toBe(0);

    await page.rootInstance.handleDismissedToast();
    expect(page.rootInstance.pendingVisibility.length).toBe(0);
  });

  it("should test previouslyFocused", async () => {
    const page = await newSpecPage({
      components: [ToastRegion, Toast, Button],
      html: `<ic-toast-region>
      <ic-button>Click Me</ic-button>
      <ic-toast heading="Heading"></ic-toast>
      </ic-toast-region>`,
    });

    const button = document.querySelector("ic-button");
    page.rootInstance.previouslyFocused = button;

    await page.rootInstance.handleDismissedToast();
    expect(page.rootInstance.pendingVisibility.length).toBe(0);
  });

  it("should test previously focused - standard element", async () => {
    const page = await newSpecPage({
      components: [ToastRegion, Toast],
      html: `<ic-toast-region>
      <button>Click Me</button>
      <ic-toast heading="Heading"></ic-toast>
      </ic-toast-region>`,
    });

    const button = document.querySelector("button");
    page.rootInstance.previouslyFocused = button;

    await page.rootInstance.handleDismissedToast();
    expect(page.rootInstance.pendingVisibility.length).toBe(0);
  });
});
