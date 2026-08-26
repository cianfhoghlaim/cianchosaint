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
import { fixture } from "@open-wc/testing-helpers";
import { axe } from "jest-axe";
import { checkShadowElementRendersCorrectly } from "../../../../utils/testa11y.helpers";

beforeEach(() => {
  // IntersectionObserver isn't available in test environment
  const mockResizeObserver = jest.fn();
  mockResizeObserver.mockReturnValue({
    observe: jest.fn().mockReturnValue(null),
    unobserve: jest.fn().mockReturnValue(null),
    disconnect: jest.fn().mockReturnValue(null),
  });
  window.ResizeObserver = mockResizeObserver;
  const matchMedia = jest.fn().mockReturnValue(true);
  window.matchMedia = matchMedia;
});

describe("ic-horizontal-scroll", () => {
  it("passes accessibility", async () => {
    const div = document.createElement("div");
    div.setAttribute("style", "width: 320px;");
    const el = await fixture(
      `
      <ic-horizontal-scroll>
        <ul>
          <ic-navigation-item label="Test nav item 1"></ic-navigation-item>
          <ic-navigation-item label="Test nav item 2"></ic-navigation-item>
          <ic-navigation-item label="Test nav item 3"></ic-navigation-item>
          <ic-navigation-item label="Test nav item 4"></ic-navigation-item>
          <ic-navigation-item label="Test nav item 5"></ic-navigation-item>
          <ic-navigation-item label="Test nav item 6"></ic-navigation-item>
        </ul>
      </ic-horizontal-scroll>
    `,
      { parentNode: div }
    );
    checkShadowElementRendersCorrectly(el);
    expect(await axe(el)).toHaveNoViolations();
  });
});
